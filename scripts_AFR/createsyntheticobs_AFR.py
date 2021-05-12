
import math
import sys
import optparse
import random

import tomodata
import tomosynthetic

def sphtocart(lon, lat, r):
    lon = lon * math.pi/180.0
    lat = lat * math.pi/180.0

    x = r * math.cos(lon) * math.cos(lat)
    y = r * math.sin(lon) * math.cos(lat)
    z = r * math.sin(lat)

    return (x, y, z)
    
def veclen(x, y, z):
    return math.sqrt(x*x + y*y + z*z)

def cartesian_dist(lon1, lat1, r1, lon2, lat2, r2):

    x1, y1, z1 = sphtocart(lon1, lat1, r1)
    x2, y2, z2 = sphtocart(lon2, lat2, r2)

    return veclen(x2 - x1, y2 - y1, z2 - z1)
    
def trace_path(path, velocity_fn):

    dist = [0.0] * len(path)
    
    # First pass, compute distances
    for i in range(1, len(path)):
        
        lon1, lat1, r1 = path[i - 1]
        lon2, lat2, r2 = path[i]

        d = cartesian_dist(lon1, lat1, r1, lon2, lat2, r2)

        dist[i - 1] = dist[i - 1] + d/2.0
        dist[i] = d/2.0
    
    # 2nd pass, integrate travel time
    t = 0.0
    total_dist = 0.0
    mean_v = 0.0
    for i in range(len(path)):

        lon, lat, r = path[i]
        v = velocity_fn(lon, lat, r)
        
        total_dist = total_dist + dist[i]
        mean_v = mean_v + v
        t = t + dist[i]/v

    mean_v = mean_v/float(len(path))
    print '      ', t, total_dist, total_dist/t, mean_v, total_dist/mean_v
    return t

if __name__ == '__main__':

    parser = optparse.OptionParser()

    parser.add_option('-p', '--paths', dest='path', default = None, help='Paths file to load')
    parser.add_option('-s', '--sources', dest='source', default = None, help='Source file to load')
    parser.add_option('-r', '--receivers', dest='receiver', default = None, help='Receiver file to load')
    parser.add_option('-v', '--valid', dest='valid', type='int', default = 100, help='No. of valid observations to create')
    parser.add_option('-n', '--noise', dest='noise', type='float', default = 1.0, help='Std. deviation of noise in observed time.')

    parser.add_option('-o', '--observations', dest='observed', default = None, help='Observations file to write')
    parser.add_option('--real', dest='real', default = None, help='Exact Observations file to write')

    parser.add_option('-t', '--tomography', dest='tomography', default = tomosynthetic.DEFAULT_MODEL, help='Tomography model to use')

    parser.add_option('-l', '--list-tomography', dest='listtomography', action='store_true', help='List available tomography models')

    parser.add_option('-d', '--data', dest='data', default = None, help = 'Write data to file.')

    parser.add_option('-f', '--ekstrom-path', dest='path_in', default = None, help='Input path file in Ekstrom format')
    parser.add_option('-y', '--min-ovlp-time', dest='time_yr', type='float',  default = None, help='minimum overlap time in year to allow valid measurement')
    
    parser.add_option('-a', '--min-path-dist', dest='minR', type='float', default = None, help='minimum distance between source and receiver in km')
    parser.add_option('-b', '--max-path-dist', dest='maxR', type='float',  default = None, help='maximum distance between source and receiver in km')

    parser.add_option('-N', '--enable-noise', dest='enablenoise', default = False, action='store_true', help='Add noise to observations.')

    options, args = parser.parse_args()

    if (options.listtomography):
        print 'Default model:\n    "%s"' % tomosynthetic.DEFAULT_MODEL
        print 'Available models:'
        for k in tomosynthetic.fmap.keys():
            if len(k):
                print '    "%s"' % k
        sys.exit(0)

    if (options.path == None):
        print 'Missing paths file option.'
        sys.exit(-1)

    if (options.source == None):
        print 'Missing source file option.'
        sys.exit(-1)

    if (options.receiver == None):
        print 'Missing receiver file option.'
        sys.exit(-1)

    if (options.observed == None):
        print 'Missing observed file option.'
        sys.exit(-1)

    if (not tomosynthetic.fmap.has_key(options.tomography)):
        print 'Invalid tomography model.'
        sys.exit(-1)

    sources = tomodata.load_sources(options.source)
    print '%d sources' % len(sources)
    receivers = tomodata.load_receivers(options.receiver)
    print '%d receivers' % len(receivers)

    paths = tomodata.load_raypath(options.path)
    print '%d paths' % len(paths)
    if (len(paths) != (len(sources) * len(receivers))): 
        print 'Inconsistent number of sources, receivers and paths.'
        sys.exit(-1)

    # source reciever code inside path -- -use to resample upper triangle
    psrcode = tomodata.load_psrcode_EF(options.path_in)
    ovlpTime = tomodata.load_pwinTime_EF(options.path_in)
    pathDist = tomodata.load_pathR_EF(options.path_in)
    
    # conversion factor for changing correlation window to years ... check with option
    convFac = 1.0 / (365.0*6.0)
    
    srmatrix = {}

    #choices = map(lambda i: (i / len(receivers), i % len(receivers)), range(len(sources) * len(receivers)))
    choices = [(s, r) for s in range(len(sources)) for r in range(len(receivers)) if r>s]
    
    # build valid choces based on scan of overlap time and distance restriction
    valids = []
    for ichoice in range( len(choices) ):
        ovlp_inyrs = ovlpTime[ichoice] * convFac
        isvalid = (ovlp_inyrs >= options.time_yr and pathDist[ichoice] >= options.minR and pathDist[ichoice] <= options.maxR)
        
        print 'choice %5d: ovlp_yrs: %f pathD:  %f valid: %s' % ((ichoice + 1), ovlp_inyrs, pathDist[ichoice], isvalid)
        
        if isvalid:
            valids.append(1)
        else:
            valids.append(0)
    
    valid = options.valid
    
    
    if valid > len(choices):
        print 'Warning: truncating valid to %s' % len(choices)
        valid = len(choices)

    print 'Noise enabled: ', options.enablenoise

    for i in range(len(choices)):
        #j = random.randint(0, len(choices) - 1)
        if valids[i] == 1:
            s, r = choices[i]
            #del choices[i]

            pi = s*len(receivers) + r
            print '%5d: Tracing path %d -> %d' % ((i + 1), s, r)
            if not srmatrix.has_key(s):
                srmatrix[s] = {}
            N = 0.0
            if options.enablenoise:
                N = random.normalvariate(0.0, options.noise)

            srmatrix[s][r] = (True, trace_path(paths[pi], tomosynthetic.fmap[options.tomography]), N, options.noise)
        
        else:
            #del choices[i]
            pass

    f = open(options.observed, 'w')
    for s in range(len(sources)):
        for r in range(len(receivers)):
            
            valid = False
            if srmatrix.has_key(s):
                if srmatrix[s].has_key(r):
                    (valid, t, N, n) = srmatrix[s][r]

            if valid:
                f.write('1 %f %f\n' % (t + N, n))
            else:
                f.write('0 0.0 0.0\n')

    f.close()

    if options.real:
        f = open(options.real, 'w')
        for s in range(len(sources)):
            for r in range(len(receivers)):
                
                valid = False
                if srmatrix.has_key(s):
                    if srmatrix[s].has_key(r):
                        (valid, t, N, n) = srmatrix[s][r]
                        
                if valid:
                    f.write('1 %f %f\n' % (t, n))
                else:
                    f.write('0 0.0 0.0\n')
                    
        f.close()

    if options.data:
        minlon, maxlon, minlat, maxlat = tomodata.minmax_raypath(paths)
        f = open(options.data, 'w')

        xsamples = 200
        ysamples = 200
        for ilat in range(ysamples):
            lat = float(ilat)/float(ysamples - 1) * (maxlat - minlat) + minlat
            for ilon in range(xsamples):
                lon = float(ilon)/float(xsamples - 1) * (maxlon - minlon) + minlon

                f.write('%f ' % tomosynthetic.fmap[options.tomography](lon, lat, tomodata.EARTH_RADIUS))

            f.write('\n')

        f.close()
        
            
    


        

    
