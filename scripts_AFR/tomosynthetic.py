import math

def uniform3km(lon, lat, rad):
    #
    # Uniform 3km/s tomography
    #
    return 3.0

def circularfast4km(lon, lat, rad):
    #
    # Circular fast region roughly centred on australia
    #
    clon = 140.0
    clat = -35.0

    dlon = lon - clon
    dlat = lat - clat

    if (dlon*dlon + dlat*dlat) < 25.0:
        return 4.0
    else:
        return 3.0
        
        
def circularfast4km_AFR(lon, lat, rad):
    #
    # Circular fast region roughly centred on Africa (inside congo)
    # radius of circular region is ~ 20 degrees
    #
    clon = 16.0
    clat = 0.0

    dlon = lon - clon
    dlat = lat - clat

    if (dlon*dlon + dlat*dlat) < 400.0:
        return 4.0
    else:
        return 3.0
        

def checkerboard1(lon, lat, rad):
    #
    # Checkerboard pattern every degree
    #
    ilon = int(lon) % 2
    ilat = int(lat) % 2
    return 2.75 + 0.5*float(ilon^ilat)
   
def checkerboard2(lon, lat, rad):
    #
    # Checkerboard pattern every 2 degrees
    #
    ilon = int(lon/2.0) % 2
    ilat = int(lat/2.0) % 2
    return 2.75 + 0.5*float(ilon^ilat)

def checkerboard5(lon, lat, rad):
    #
    # Checkerboard pattern every 5 degrees
    #
    ilon = int(lon/5.0) % 2
    ilat = int(lat/5.0) % 2
    return 2.75 + 0.5*float(ilon^ilat)

def gaussian5(lon, lat, rad):
    global mg
    #
    # 2D Gaussian with std. deviation of 5 centred at 0,0
    #
    g = math.exp(-0.5*(lon*lon + lat*lat)/25.0)/2.0
    return 2.75 + g

def gaussian1x5(lon, lat, rad):
    global mg
    #
    # 2D Gaussian with std. deviation of 1 in x and 5 in y centred at 0,0
    #
    g = math.exp(-0.5*(lon*lon + lat*lat/25.0))/2.0
    return 2.75 + g

def gaussian2x4(lon, lat, rad):
    global mg
    #
    # 2D Gaussian with std. deviation of 1 in x and 5 in y centred at 0,0
    #
    g = math.exp(-0.5*(lon*lon/4.0 + lat*lat/16.0))/2.0
    return 2.75 + g

fmap = { 'uniform3km': uniform3km,
         'circularfast4km': circularfast4km,
         'circularfast4km_AFR':circularfast4km_AFR,
         'checkerboard1': checkerboard1,
         'checkerboard2': checkerboard2,
         'checkerboard5': checkerboard5,
         'gaussian5': gaussian5,
         'gaussian1x5': gaussian1x5,
         'gaussian2x4': gaussian2x4,
         '' : None}

DEFAULT_MODEL='uniform3km'
