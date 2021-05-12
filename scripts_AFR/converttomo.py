
import sys
from optparse import OptionParser

import tomodata


if __name__ == '__main__':

    parser = OptionParser()
    parser.add_option('-i', '--input', dest = 'infile', default=None, help='Input file to convert')
    parser.add_option('-o', '--output', dest = 'outfile', default=None, help='Output file to write')
    parser.add_option('-r', '--radius', dest = 'radius', default = tomodata.EARTH_RADIUS, help='Fixed radius to use')

    options, args = parser.parse_args()

    if options.infile == None:
        print('Input file required.')
        sys.exit(-1)

    if options.outfile == None:
        print('Output file required.')
        sys.exit(-1)

    paths = tomodata.load_raypath_original(options.infile, options.radius)

    print(len(paths))

    tomodata.save_raypath(options.outfile, paths)
