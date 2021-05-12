import sys

import optparse

def write_namelist(filename, **kwargs):

    f = open(filename, 'w')

    f.write('&tomosettings \n')
    f.write('  sources_file = \'sources.dat\',\n')
    f.write('  receivers_file = \'receivers.dat\',\n')
    f.write('  observed_times_file = \'observations.dat\',\n')
    f.write('  paths_file = \'paths.dat\',\n')

    for k, v in kwargs.items():
        f.write('  %s = %s,\n' % (k, v))

    f.write('/\n')
    f.close()

if __name__ == '__main__':

    parser = optparse.OptionParser()
    parser.add_option('-n', '--namelist', dest='namelist', default = None, help='Namelist file to write')

    variables = ['burnin', 
                 'total',
                 'thin',
                 'minpartitions',
                 'maxpartitions',
                 'initpartitions',
                 'pd',
                 'vs_min',
                 'vs_max',
                 'vs_std_value',
                 'vs_std_bd',
                 'sigma_min',
                 'sigma_max',
                 'sigma_std',
                 'sigma_fixed',
                 'show_progress',
                 'seed_base',
                 'seed_mult',
                 'xsamples',
                 'ysamples',
                 'zsamples']
                 
    for v in variables:
        parser.add_option('--%s' % v,
                          dest = v,
                          default = None,
                          help = v)

    options, args = parser.parse_args()

    if options.namelist == None:
        print 'A namelist file must be specified.'
        sys.exit(-1)
        
    kw = {}
    for v in variables:
        if options.__dict__[v] != None:
            kw[v] = options.__dict__[v]
        
    write_namelist(options.namelist, **kw)
