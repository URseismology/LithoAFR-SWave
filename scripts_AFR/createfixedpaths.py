
import sys

import numpy
import optparse

if __name__ == '__main__':

    sources = [(0.0, 0.5),
               (-0.5, 0.5),
               (-0.5, 0.0),
               (-0.5, -0.5)]
    receivers = [(0.0, -0.5),
                 (0.5, -0.5),
                 (0.5, 0.0),
                 (0.5, 0.5)]
    samples = [5, 10, 15, 20]

    fixed_r = 1000.0

    # Lengths should be 1, sqrt(2), 1, sqrt(2) (times radius)

    parser = optparse.OptionParser()

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

    sf = open(options.sourcefile, 'w')
    sf.write('%d\n' % len(sources))
    for (slon, slat) in sources:
        sf.write('%f %f\n' % (slon, slat))
    sf.close()

    rf = open(options.receiverfile, 'w')
    rf.write('%d\n' % len(receivers))
    for (rlon, rlat) in receivers:
        rf.write('%f %f\n' % (rlon, rlat))
    rf.close()

    pf = open(options.pathfile, 'w')
    pf.write('%d\n' % (len(sources) * len(receivers)))
    for s, n in zip(sources, samples):
        for r in receivers:

            lons = numpy.linspace(s[0], r[0], n)
            lats = numpy.linspace(s[1], r[1], n)
            
            pf.write('%d\n' % n)
            pf.write('\n'.join(map(lambda lon, lat: '%f %f %f' % (lon, lat, fixed_r), lons, lats)))
            pf.write('\n')

    
    pf.close()

    
