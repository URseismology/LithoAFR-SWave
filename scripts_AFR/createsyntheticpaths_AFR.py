
import math
import optparse
import random
import sys

import tomodata


def vrot(v, theta):
    #c -s
    #s  c

    x, y = v
    rad = theta * math.pi/180.0
    
    xp = math.cos(rad)*x - math.sin(rad)*y
    yp = math.sin(rad)*x + math.cos(rad)*y

    return (xp, yp)

def bezier(p0, p1, p2, t):
    omt = 1.0 - t
    return omt*omt*p0 + 2.0*omt*t*p1 + t*t*p2

def generate_path(lon1, lat1, r1, lon2, lat2, r2, delta, v):

    clon = (lon1 + lon2)/2.0
    clat = (lat1 + lat2)/2.0

    dlon = (lon2 - lon1)
    dlat = (lat2 - lat1)

    n = int(math.ceil(math.sqrt(dlon*dlon + dlat*dlat)/delta))
    # Ensure we have at least a few points
    if n < 5: 
        n = 5
        
    if (v == 0.0):
        #
        # Straight line
        #

        p = map(lambda i: (lon1 + dlon*float(i)/float(n - 1),
                           lat1 + dlat*float(i)/float(n - 1),
                           r1 + (r2 - r1)*float(i)/float(n - 1)), range(n))

    else:

        if (v < 0.0):
            v = -v
            nlon, nlat = vrot((dlon, dlat), -90.0)
        else:
            nlon, nlat = vrot((dlon, dlat), 90.0)

        nlen = math.sqrt(nlon*nlon + nlat*nlat)

        plon = clon + v*nlon/nlen
        plat = clat + v*nlat/nlen

        p = map(lambda i: (bezier(lon1, plon, lon2, float(i)/float(n - 1)),
                           bezier(lat1, plat, lat2, float(i)/float(n - 1)),
                           r1 + (r2 - r1)*float(i)/float(n - 1)), range(n))
        
    return p
        
if __name__ == '__main__':

    parser = optparse.OptionParser()

    parser.add_option('--minlon', dest='minlon', type='float', default = 120.0, help='Lower longitude bound')
    parser.add_option('--maxlon', dest='maxlon', type='float', default = 150.0, help='Upper longitude bound')
    parser.add_option('--minlat', dest='minlat', type='float', default = -45.0, help='Lower latitude bound')
    parser.add_option('--maxlat', dest='maxlat', type='float', default = 0.0, help='Upper latitude bound')

    parser.add_option('--minr', dest='minr', type='float', default = tomodata.EARTH_RADIUS, help='Min radius')
    parser.add_option('--maxr', dest='maxr', type='float', default = tomodata.EARTH_RADIUS, help='Max radius')

    parser.add_option('-n', '--msources', dest='sources', type='int', default = 100, help='No. of sources')
    parser.add_option('-m', '--nreceivers', dest='receivers', type='int', default = 100, help='No. of receivers')

    parser.add_option('-v', '--variance', dest='variance', type='float', default = 1.0, help='Variance of curves (0 = straight lines.')
    parser.add_option('-d', '--delta', dest='delta', type='float', default = 0.2, help='Path step size')
	
	#@Olugboji, use here to load ekstrom type observation file ...
    parser.add_option('-e', '--ekstrom-src', dest='src_rec_in', default = None, help='Input source file in Ekstrom format - all sources can be receivers')
    parser.add_option('-f', '--ekstrom-path', dest='path_in', default = None, help='Input path file in Ekstrom format')
    
    parser.add_option('-s', '--source-output', dest='sourcefile', default = None, help='Sources output file')
    parser.add_option('-r', '--receiver-output', dest='receiverfile', default = None, help='Receivers output file')
    parser.add_option('-p', '--path-output', dest='pathfile', default = None, help='Paths output file')

    options, args = parser.parse_args()

    if (options.sourcefile == None):
        print 'Required source file parameter missing'
        sys.exit(-1)

    if (options.receiverfile == None):
        print 'Required receiver file parameter missing'
        sys.exit(-1)

    if (options.pathfile == None):
        print 'Required path file parameter missing'
        sys.exit(-1)

    
    #@Olugboji -- tweak this code to load from tomodata -- add option to specify this load
    sources = tomodata.load_sources_EF(options.src_rec_in)
    receivers = tomodata.load_receivers_EF(options.src_rec_in)
    
    scode = tomodata.load_scode_EF(options.src_rec_in)
    rcode = tomodata.load_scode_EF(options.src_rec_in)
    
    # source reciever code inside path -- -use to resample upper triangle
    psrcode = tomodata.load_psrcode_EF(options.path_in)
    
    
    nsources = len(sources)
    nrecevs = len(receivers)
    
    sf = open(options.sourcefile, 'w')
    sf.write('%d\n' % nsources)

    rf = open(options.receiverfile, 'w')
    rf.write('%d\n' % nrecevs)

    pf = open(options.pathfile, 'w')
    pf.write('%d\n' % (nsources * nrecevs))

    sources_with_r = []
    recevs_with_r = []
    
    
    for (slat, slon) in sources:
    	sources_with_r.append((slon, slat, tomodata.EARTH_RADIUS))
    	sf.write('%f %f\n' % (slon, slat))
    	
    for (rlat, rlon) in receivers:
        recevs_with_r.append((rlon, rlat, tomodata.EARTH_RADIUS))
        rf.write('%f %f\n' % (rlon, rlat))
        
        
    
    #for s in range(options.sources):
    #    slon = random.uniform(options.minlon, options.maxlon)
    #    slat = random.uniform(options.minlat, options.maxlat)
    #    sr = random.uniform(options.minr, options.maxr)
    #    sources.append((slon, slat, sr))

    #   sf.write('%f %f\n' % (slon, slat))

    #receivers = []
    #for r in range(options.receivers):
    #    
    #    rlon = random.uniform(options.minlon, options.maxlon)
    #    rlat = random.uniform(options.minlat, options.maxlat)
    #    rr = random.uniform(options.minr, options.maxr)
    #    receivers.append((rlon, rlat, rr))
    #    rf.write('%f %f\n' % (rlon, rlat))
    
    #@Olugboji: demo a new way to build paths ...
    
    pi = 0;
    for s in range(nsources):
    	for r in range(nrecevs):
    	    (slon, slat, sr) = sources_with_r[s]
    	    (rlon, rlat, rr) = recevs_with_r[r]
    	    #print (slon, slat, rlon, rlat, pi)
    	    if r < s:
    	        p = generate_path(slon, slat, sr, rlon, rlat, rr, options.delta, 0)
    	        pf.write('%d\n' % len(p))
    	        print (2, len(p))
    	        for (lon, lat, r) in p:
    	            pf.write('%f %f %f\n' % (lon, lat, r))
    	    
    	    elif r == s:
    			p = generate_path(slon, slat, sr, rlon+0.2, rlat+0.2, rr, options.delta, 0)
    			pf.write('%d\n' % len(p))
    			print (1, len(p))
    			
    			for (lon, lat, r) in p:
    				pf.write('%f %f %f\n' % (lon, lat, r))	
            elif r > s: 
                s_code = scode[s]
                r_code = rcode[r]
                ps_code = psrcode[pi][0]
                pr_code = psrcode[pi][1]
                pi = pi+1
                #print (s_code, r_code, ps_code, pr_code, pi)	
                print (s, r, s_code, r_code, slon, slat, rlon, rlat)
                
                if slon == rlon and slat == rlat:
                	p = generate_path(slon, slat, sr, rlon+0.2, rlat+0.2, rr, options.delta, 0)
                else:
                	p = generate_path(slon, slat, sr, rlon, rlat, rr, options.delta, options.variance)
                	
                pf.write('%d\n' % len(p))
                
                for (lon, lat, r) in p:
                	pf.write('%f %f %f\n' % (lon, lat, r))
    		
    		
    				
    		
    			
    			
    		


    #for (slon, slat, sr) in sources_with_r:
    #    for (rlon, rlat, rr) in recevs_with_r:

    #        p = generate_path(slon, slat, sr, rlon, rlat, rr, options.delta, options.variance)

    #        pf.write('%d\n' % len(p))
    #        for (lon, lat, r) in p:
    #            pf.write('%f %f %f\n' % (lon, lat, r))

    sf.close()
    rf.close()
    pf.close()
            
            

            
