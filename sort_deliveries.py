import os
import sys

def dir_dive_print(ext_dir):
    rootDir = "."
    rootDir = format("%s/%s" % (rootDir, ext_dir))
    root_depth = len(rootDir.split("/"))
    for dirName, subdirList, fileList in os.walk(rootDir):
        depthList = dirName.split("/")
        depth = len(depthList) - root_depth
        if depth == 2:
            subdirList = sorted(subdirList)[-1:]
        elif depth == 3:
            command = format("mv \"%s/\"* \"%s/../../\"" % (dirName[2:], dirName[2:]))
            os.system(command)
    for dirName, subdirList, fileList in os.walk(rootDir, topdown=False):
        depthList = dirName.split("/")
        depth = len(depthList) - root_depth
        if depth == 0:
            for subdir in subdirList:
                filepath = format("\"%s/%s\"" % (dirName[2:], subdir))
                new_filepath = format("%s/%s" % (dirName[2:], subdir.split(" ")[0]))
                command = format("mv %s %s" % (filepath, new_filepath))
                os.system(command)
        elif depth == 1:
            for subdir in subdirList:
                command = format("rm -r \"%s/%s\"" % (dirName[2:], subdir))
                os.system(command)

if __name__=='__main__':
    usage = "Usage:\npython sort_deliveries.py [options] path"
    if len(sys.argv) < 1:
        print usage
    else:
        execute = True
        for arg in sys.argv:
            if arg == "-z":
                command = format("unzip %s/*.zip" % sys.argv[1])
                os.system(command)
            elif arg == "-h":
                print "%s\nOptions:\n-h -- shows this menu\n-z -- unzip" % usage
                execute = False
        if execute:
            dir_dive_print(sys.argv[-1])
