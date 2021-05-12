
import struct
import string

EARTH_RADIUS = 6371.0

def load_raypath_original(filename, default_radius = EARTH_RADIUS):

    f = open(filename, 'r')
    lines = f.readlines()
    f.close()

    paths = []
    path = []
    pi = 0
    for line in lines[1:]:
        if pi == 0:
            if len(path) > 0:
                paths.append(path)
                path = []

            pi = int(line)
        else:
            lat, lon = map(float, line.split())
            path.append((lon, lat, default_radius))
            pi = pi - 1
    
    if len(path) > 0:
        paths.append(path)

    return paths

def load_raypath(filename):

    f = open(filename, 'r')
    lines = f.readlines()
    f.close()

    paths = []
    path = []
    pi = 0
    for line in lines[1:]:
        if pi == 0:
            if len(path) > 0:
                paths.append(path)
                path = []

            pi = int(line)
        else:
            lon, lat, radius = map(float, line.split())
            path.append((lon, lat, radius))
            pi = pi - 1

    if len(path) > 0:
        paths.append(path)
    
    return paths

def minmax_raypath(paths):
    
    minlon = 360.0
    maxlon = -360.0
    minlat = 90.0
    maxlat = -90.0

    for path in paths:
        for lon, lat, radius in path:
            minlon = min([lon, minlon])
            maxlon = max([lon, maxlon])
            minlat = min([lat, minlat])
            maxlat = max([lat, maxlat])

    return (minlon, maxlon, minlat, maxlat)

def save_raypath(filename, paths):

    f = open(filename, 'w')
    
    f.write('%d\n' % len(paths))

    for path in paths:
        f.write('%d\n' % len(path))
        for (x, y, r) in path:
            f.write('%f %f %f\n' % (x, y, r))

    f.close()

def save_raypath_binary(filename, paths):

    f = open(filename, 'w')
    
    f.write(struct.pack('i', len(paths)))

    for path in paths:
        f.write(struct.pack('i', len(path)))
        for (x, y, r) in path:
            f.write(struct.pack('fff', x, y, r))

    f.close()
    
def load_receivers(filename):

    f = open(filename, 'r')
    lines = f.readlines()
    f.close()

    nreceivers = int(lines[0])
#    receivers = map(lambda (slat, slon): (float(slon), float(slat)), map(string.split, lines[1:]))
    receivers = map(lambda x: map(float, x.split()), lines[1:])

    return receivers

def load_sources(filename):

    f = open(filename, 'r')
    lines = f.readlines()
    f.close()

    nsources = int(lines[0])
#    sources = map(lambda (slat, slon): (float(slon), float(slat)), map(string.split, lines[1:]))
    sources = map(lambda x: map(float, x.split()), lines[1:])

    return sources


# read and return sources in ekstrom format - lat, lon
def load_sources_EF(filename):
    f = open(filename, 'r')
    lines = f.readlines()
    f.close()
    asplit = map(lambda x: x.split(), lines[1:])
    sources = map(lambda x: map(float, x[2:4]), asplit)
    return sources

# read and return receivers in ekstrom format	
def load_receivers_EF(filename):
    f = open(filename, 'r')
    lines = f.readlines()
    f.close()
    asplit = map(lambda x: x.split(), lines[1:])
    receivers = map(lambda x: map(float, x[2:4]), asplit)
    return receivers

# read and return sta code in ekstrom format
def load_scode_EF(filename):
    f = open(filename, 'r')
    lines = f.readlines()
    f.close()
    asplit = map(lambda x: x.split(), lines[1:])
    scode =  map(lambda x: x[1], asplit)
    return scode
    
    # read and return sta code in ekstrom format
def load_psrcode_EF(filename):
    f = open(filename, 'r')
    lines = f.readlines()
    f.close()
    asplit = map(lambda x: x.split(), lines[1:])
    psrcode = map(lambda x: x[0:2], asplit)
    return psrcode
    
# read and return overlap time between station i & j -- used to determine if path is valid
def load_pwinTime_EF(filename):
    f = open(filename, 'r')
    lines = f.readlines()
    f.close()
    asplit = map(lambda x: x.split(), lines[1:])
    
    wwT = map(lambda x: x[7], asplit)
    wT = map(float, wwT)
    
    return wT

# read and return distance between station i & j -- used to determine if path is valid
def load_pathR_EF(filename):
    f = open(filename, 'r')
    lines = f.readlines()
    f.close()
    asplit = map(lambda x: x.split(), lines[1:])
    
    ppathR = map(lambda x:  x[6], asplit)
    pathR = map(float, ppathR)
    
    return pathR
    
	
	#a = map(lambda x: ( map(lambda y: map(float,y[2:4]), x.split()), lines[1:]) 