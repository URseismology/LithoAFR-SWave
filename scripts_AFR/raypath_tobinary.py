
import tomodata

if __name__ == '__main__':
    
    paths = tomodata.load_raypath('../data/raypath0.08.dat')
    tomodata.save_raypath_binary('../data/raypath0.08.bin', paths)


