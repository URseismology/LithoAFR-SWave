
import cairo
import optparse
import sys
import tomodata

def rescale_extent(minv, maxv, ratio):
    cv = (maxv + minv)/2.0
    nv2 = (maxv - cv) * ratio
    
    return (cv, cv - nv2, cv + nv2)

def map_coord(v, cv, dv, size):
    return float(size)/2.0 + (v - cv)/dv

if __name__ == '__main__':

    parser = optparse.OptionParser()

    parser.add_option('-p', '--paths', dest='paths', default=None, help='Paths file to render')
    parser.add_option('-o', '--output', dest='output', default=None, help='PNG Output file to write')

    parser.add_option('-W', '--width', type='int', dest='width', default=1920, help='Image width')
    parser.add_option('-H', '--height', type='int', dest='height', default=1080, help='Image height')

    dminlon = 360.0
    dmaxlon = -360.0
    dminlat = 90.0
    dmaxlat = -90.0

    options, args = parser.parse_args()

    if (options.paths == None):
        print 'Paths file option missing.'
        sys.exit(-1)

    if (options.output == None):
        print 'Output file option missing.'
        sys.exit(-1)
    
    paths = tomodata.load_raypath(options.paths)

    for path in paths:
        for (x, y, r) in path:
            if (x < dminlon):
                dminlon = x
            if (x > dmaxlon):
                dmaxlon = x

            if (y < dminlat):
                dminlat = y
            if (y > dmaxlat):
                dmaxlat = y

    print dminlon, dmaxlon, dminlat, dmaxlat
    print dmaxlon - dminlon, dmaxlat - dminlat

    clon, minlon, maxlon = rescale_extent(dminlon, dmaxlon, 1.1)
    clat, minlat, maxlat = rescale_extent(dminlat, dmaxlat, 1.1)

    print minlon, maxlon, minlat, maxlat
    print maxlon - minlon, maxlat - minlat

    dlon = (maxlon - minlon)/float(options.width)
    dlat = (maxlat - minlat)/float(options.height)

    print dlon, dlat

    if (dlat >= dlon):
        dlon = dlat
        minlon = clon - dlon * float(options.width)/2.0
        maxlon = clon + dlon * float(options.width)/2.0
    else:
        dlat = dlon
        minlat = clat - dlat * float(options.height)/2.0
        maxlat = clat + dlat * float(options.height)/2.0

    print minlon, maxlon, minlat, maxlat


    # To flip y coordinate
    dlat = -dlat

    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, options.width, options.height)
    ctx = cairo.Context(surface)

    ctx.set_source_rgba(0.0, 0.0, 0.0, 1.0)
    ctx.set_line_width(1.0)

    ctx.move_to(map_coord(dminlon, clon, dlon, options.width), 
                map_coord(dminlat, clat, dlat, options.height))

    ctx.line_to(map_coord(dminlon, clon, dlon, options.width), 
                map_coord(dmaxlat, clat, dlat, options.height))
    ctx.line_to(map_coord(dmaxlon, clon, dlon, options.width), 
                map_coord(dmaxlat, clat, dlat, options.height))
    ctx.line_to(map_coord(dmaxlon, clon, dlon, options.width), 
                map_coord(dminlat, clat, dlat, options.height))
    ctx.line_to(map_coord(dminlon, clon, dlon, options.width), 
                map_coord(dminlat, clat, dlat, options.height))

    ctx.stroke()

    ctx.set_source_rgba(0.5, 0.5, 0.5, 0.75)
    ctx.set_line_width(0.5)

    for path in paths:
        x, y, r = path[0]

        ctx.set_source_rgba(0.0, 1.0, 0.0, 1.00)
        ctx.rectangle(map_coord(x, clon, dlon, options.width),
                      map_coord(y, clat, dlat, options.height),
                      5.0, 5.0)
        ctx.fill()

        ctx.set_source_rgba(0.5, 0.5, 0.5, 0.75)
        ctx.move_to(map_coord(x, clon, dlon, options.width),
                    map_coord(y, clat, dlat, options.height))
        for (x, y, r) in path[1:]:
            ctx.line_to(map_coord(x, clon, dlon, options.width),
                        map_coord(y, clat, dlat, options.height))

        ctx.stroke()

        x, y, r = path[len(path) - 1]

        ctx.set_source_rgba(1.0, 0.0, 0.0, 1.00)
        ctx.rectangle(map_coord(x, clon, dlon, options.width),
                      map_coord(y, clat, dlat, options.height),
                      5.0, 5.0)
        ctx.fill()


    surface.write_to_png(options.output)

