import os
import sys
import subprocess
import time
import shutil

def create(root_path, log_file, log, verbose):
    path = format("%s/older" % root_path)
    command = ['mkdir', path]
    if verbose:
        print "Creating folder in '%s' for older files" % path
        subprocess(command)
    elif log:
        write_to_log(log_file, format("Creating folder in '%s' for older files" % path))
        subprocess.call(command, stdout=log_file, stderr = log_file)
    else:
        null_out = open(os.devnull, 'w')
        subprocess(command, stdout = null_out, stderr = subprocess.STDOUT )
        null_out.close()

def dive_delete(rootDir, root_depth, log, verbose):
    if log:
        log_file = open(format("%s/log.txt" % rootDir), 'a')
    for dirpath, subdirList, fileList in os.walk(rootDir, topdown=False):
        depthList = dirpath.split("/")
        depth = len(depthList) - root_depth
        if depth == 1:
            for subdir in subdirList:
                path = format("%s/%s" % (dirpath, subdir)).replace(" ", "\ ")
                command = ["rm", "-r", path]
                if verbose:
                    print "Recursive removing '%s'" % path
                    subprocess.call(command)
                elif log:
                 write_to_log(log_file,
                              format("Recursive removing '%s'" % path))
                if log:
                    subprocess.call(command, stdout=log_file, stderr = log_file)
                else:
                    null_out = open(os.devnull, 'w')
                    subprocess.call(command, stdout = null_out, stderr = subprocess.STDOUT)
                    null_out.close()
    if log:
        log_file.close()

def dive_delete_dir(rootDir, root_depth, log, verbose):
    if log:
        log_file = open(format("%s/log.txt" % rootDir), 'a')
    for dirpath, subdirList, fileList in os.walk(rootDir, topdown = False):
        depth = len(dirpath.split("/")) - root_depth
        created = False
        for subdir in subdirList:
            folder = format("%s/%s" % (dirpath, subdir))
            command = ['rm', '-d', folder]
            try:
                if verbose:
                    print "Trying to remove empty folder: %s" % folder
                    subprocess.check_callk(command, stdout=subprocess, stderr = subprocess.STDOUT)
                elif log:
                    write_to_log(log_file, format("Trying to remove empty folder: %s" % folder))
                    subprocess.check_call(command, stdout=log_file, stderr=log_file)
                else:
                    subprocess.check_call(command)
            except subprocess.CalledProcessError:
                if depth == 1:
                    if not created:
                        create(dirpath, log_file, log, verbose)
                        created = True
                    move(dirpath, subdir, log_file, log, verbose)

def dive_move(rootDir, root_depth, log, verbose):
    if log:
        log_file = open(format("%s/log.txt" % rootDir), 'a')
    for dirpath, subdirList, fileList in os.walk(rootDir, topdown=True):
        depthList = dirpath.split("/")
        depth = len(depthList) - root_depth
        # We only want last deadline and last delivery
        if depth == 1 or depth == 2:
            if (len(subdirList) > 1):
                last = sorted(subdirList)[-1]
                i = 0
                max = len(subdirList)
                while (i < max):
                    if (last != subdirList[i]):
                        del subdirList[i]
                        i-=1
                        max-=1
                    i+=1
            #subdirList = sorted(subdirList)[-1:]
        elif depth == 3:
            from_path = format("%s/" % dirpath)
            to_path = '/'.join(from_path.split("/")[:-3])
            if verbose:
                print "Moving all files in '%s' to '%s'" % (from_path, to_path)
            elif log:
                write_to_log(log_file,
                          format("Moving all files in '%s' to '%s'" % (from_path, to_path)))
            for work_file in fileList:
                file_path = format("%s%s" % (from_path, work_file))
                new_file_path = format("%s/%s" % (to_path, work_file))
                if verbose:
                    print "Moved '%s' to '%s'" % (file_path, new_file_path)
                shutil.move(file_path, new_file_path)
    if log:
        log_file.close()

def move(root_path, folder, log_file, log, verbose):
    from_path = format("%s/%s" % (root_path, folder))
    to_path = format("%s/older" % root_path)
    command = ['mv', from_path, to_path]
    if verbose:
        print "Moving older files '%s' into '%s'" % (from_path, to_path)
        subprocess.call(command)
    elif log:
        write_to_log(log_file, format("Moving older files '%s' into '%s'" % (from_path, to_path)))
        subprocess.call(command, stdout = log_file, stderr = log_file)
    else:
        null_out = open(os.devnull, 'w')
        subprocess.call(command, stdout = null_out, stderr = subprocess.STDOUT )
        null_out.close()

def run(rootDir,
        execute=True,
        delete=True,
        log=False,
        rename=True,
        unzip=False, 
        verbose=False):
    root_depth = len(rootDir.split("/"))
    if unzip:
        ececute = unzip_file(rootDir, root_depth, execute, log, verbose)
    if rename:
        user_rename(rootDir, log, verbose)
    if execute:
        dive_move(rootDir, root_depth, log, verbose)
        dive_delete_dir(rootDir, root_depth, log, verbose)
    if delete:
        dive_delete(rootDir, root_depth, log, verbose)

def unzip_file(rootDir, root_depth, execute, log=False, verbose=False):
    files = ""
    zipfiles = []
    my_out = sys.stdout
    my_err = subprocess.STDOUT
    if log:
        log_file = open(format("%s/log.txt" % rootDir), 'a')
        my_out = log_file
        my_err = log_file
    elif not verbose:
        my_out = open(os.devnull, 'w')
    for dirpath, subdirs, filenames in os.walk(rootDir):
        depth = len(dirpath.split("/")) - root_depth
        if depth == 0:
            if verbose:
                print "Looking for zip files."
            files = filenames;
            for afile in files:
                if afile[-4:] == ".zip":
                    if verbose:
                        print "Found zip-file: %s" % afile
                    zipfiles.append(afile)
            if len(zipfiles) > 1:
                print "Please have only the zipfile from Devilry in folder"
                execute = False
            elif len(zipfiles) == 0:
                print "No zipfiles were found in '%s/'" % rootDir
                execute = False

            # Unzip command
            from_path = format("%s/%s" % (rootDir, zipfiles[0]))
            to_path = rootDir
            command = ["unzip",
                       from_path, 
                       "-d",
                       to_path]
            if verbose:
                print "Unzipping file: %s" % from_path
            elif log:
                write_to_log(log_file,
                             format("Unzipping file '%s'" % (from_path)))
            subprocess.call(command, stdout = my_out, stderr = my_err)
            break
    for dirpath, subdirs, filenames in os.walk(rootDir):
        if (dirpath[-1] == '/'):
            depth = len(dirpath[:-1].split("/")) - root_depth
        else:
            depth = len(dirpath.split("/")) - root_depth
        if depth == 1:
            if verbose:
                print "Going through folders within '%s'" % dirpath
            elif log:
                write_to_log(log_file,
                             format("Going through folders within '%s'" % (dirpath)))
            # Move all back down to root
            for subdir in subdirs:
                from_path = format("%s/%s" % (dirpath, subdir))
                to_path = '/'.join(dirpath.split("/")[:-1])
                if verbose:
                    print "Moving '%s' down to '%s'" % (from_path, to_path)
                elif log:
                    write_to_log(log_file,
                                 format("Moving '%s' down to '%s'" % (from_path, to_path)))
                shutil.move(from_path, to_path)
            break
    # Remove the now empty folder
    from_path = format("%s/%s" % (rootDir, zipfiles[0][:-4]))
    command = ["rm", "-d", from_path]
    if verbose:
        print "Removing empty folder: %s" % from_path
    elif log:
        write_to_log(log_file,
                    format("Removing empty folder: %s" % (from_path)))
    subprocess.call(command, stdout = my_out, stderr = my_err)
    if not verbose:
        my_out.close()

    if log:
        log_file.close()
    return execute

def user_rename(rootDir, log, verbose):
    if log:
        log_file = open(format("%s/log.txt" % rootDir), 'a')
    for dirpath, subdirList, fileList in os.walk(rootDir):
        for subdir in subdirList:
            filepath = format(''"%s/%s"'' % (dirpath, subdir))
            new_filepath = format("%s/%s" % (dirpath, subdir.split(" ")[0]))
            if verbose:
                print "Renaming '%s' to '%s'" % (filepath, new_filepath)
            elif log:
                 write_to_log(log_file,
                              format("Renaming '%s' to '%s'" % (filepath, new_filepath)))
            os.rename(filepath, new_filepath)
        break
    if log:
        log_file.close()    
        
def write_to_log(log_file, text):
    log_file.write(
        format("%s-%s: %s\n" %
               (time.strftime("%H:%M"),
                time.strftime("%d/%m/%Y"),
                text)))

def print_usage():
    print "Usage:\npython sort_deliveries.py [options] path"
    print "Options: -bhlkvz || -b -h -l -k -v -z"
    print "%3s -- %-s" % ("-b", "bare move, no rename of user folder")
    print "%3s -- %-s" % ("-h", "shows this menu")
    print "%3s -- %-s" % ("-l", "creates a log file for what happens")
    print "%3s -- %-s" % ("-d", "delete the other files and folders")
    print "%3s -- %-s" % ("-v", "loud about what happens")
    print "%3s -- %-s" % ("-z", "unzips the .zip file in path first")

if __name__=='__main__':
    if len(sys.argv) < 2 or sys.argv[-1][0] == '-':
        print_usage()
        sys.exit()
        # Quits
    
    rootDir = "."
    rootDir = format("%s/%s" % (rootDir, sys.argv[-1]))[2:]
    if (rootDir[-1] == "/"):
        print "TRUE"
        rootDir = rootDir[:-1]
    execute = True
    delete = False
    rename = True
    log = False
    unzip = False
    verbose = False
    for arg in sys.argv[1:-1]:
        options = list(arg)
        for letter in options:
            if letter == 'z':
                unzip = True
            elif letter == "h":
                print_usage()
                execute = False
                break
            elif letter == "l":
                log = True
                log_file = open(format("%s/log.txt" % rootDir), 'w')
                write_to_log(log_file, "Log created")
                log_file.close()
            elif letter == "v":
                verbose = True
            elif letter == "d":
                delete = True
            elif letter == "b":
                rename = False
    if execute:
        run(rootDir, execute, delete, log, rename, unzip, verbose)
