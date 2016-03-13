#!/usr/bin/python

import os
import sys
import subprocess
import time
import shutil

class Devilry_Sort:
    def __init__(self,
                 rootDir,
                 execute=True,
                 delete=False,
                 log=False,
                 rename=True,
                 unzip="false",
                 verbose=False):
        """
Initializes the class

Parameters
----------
self : this
    This class
rootDir : String
    A string describing the path to root directory
execute : boolean
    Execute means the primary function will be executed (default=True)
delete : boolean
    If true it will delete all older deliveries (default=False)
log : boolean
    If log is true a seperate log-file for what was done is created (default False)
rename : boolean
    If renaming is false, the user-id directories will not be renamed to
        contain only user-id (default=True)
unzip : boolean
    If true program is to unzip a .zip file containing the deliveries before execute (default=False)
verbose : boolean
    Be loud about what to do
        """
        self.rootDir = rootDir
        self.execute = execute
        self.delete = delete
        self.log = log
        self.rename = rename
        self.unzip = unzip
        self.verbose = verbose

        self.my_out = sys.stdout
        self.my_err = sys.stderr
        if log:
            self.log_file = open(format("%s/log.txt" % rootDir), 'w')
            self.log_file.close()
            self.log_file = open(format("%s/log.txt" % rootDir), 'a')
            self.write_to_log("Log created")
            self.my_out = self.log_file
            self.my_err = self.log_file
        elif not verbose:
            self.null_out = open(os.devnull, 'w')
            self.my_out = self.null_out
            self.my_err = subprocess.STDOUT

    def dive_delete(self, root_depth):
        """

        """
        for dirpath, subdirList, fileList in os.walk(rootDir, topdown=False):
            depthList = dirpath.split("/")
            depth = len(depthList) - root_depth
            if depth == 1:
                for subdir in subdirList:
                    path = format("%s/%s" % (dirpath, subdir)).replace(" ", "\ ")
                    command = ["rm", "-r", path]
                    if self.verbose:
                        print "Recursive removing '%s'" % path
                    elif self.log:
                        self.write_to_log(format("Recursive removing '%s'" % path))
                    subprocess.call(command, stdout = self.my_out, stderr = self.my_err)

    def dive_delete_dir(self, root_depth):
        for dirpath, subdirList, fileList in os.walk(rootDir, topdown = False):
            depth = len(dirpath.split("/")) - root_depth
            created = False
            for subdir in subdirList:
                folder = format("%s/%s" % (dirpath, subdir))
                command = ['rm', '-d', folder]
                try:
                    if self.verbose:
                        print "Trying to remove empty folder: %s" % folder
                    elif self.log:
                        self.write_to_log(format("Trying to remove empty folder: %s" % folder))
                    subprocess.check_call(command, stdout = self.my_out, stderr = self.my_err)
                except subprocess.CalledProcessError:
                    if depth == 1:
                        self.move(dirpath, subdir)

    def dive_move(self, root_depth):
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
                if self.verbose:
                    print "Moving all files in '%s' to '%s'" % (from_path, to_path)
                elif self.log:
                    self.write_to_log(format(
                        "Moving all files in '%s' to '%s'" % (from_path, to_path)))
                for work_file in fileList:
                    file_path = format("%s%s" % (from_path, work_file))
                    new_file_path = format("%s/%s" % (to_path, work_file))
                    if self.verbose:
                        print "Moved '%s' to '%s'" % (file_path, new_file_path)
                    elif self.log:
                        self.write_to_log(format("Moved '%s' to '%s'" % (file_path, new_file_path)))
                    shutil.move(file_path, new_file_path)

    def move(self, root_path, folder):
        from_path = format("%s/%s" % (root_path, folder))
        to_path = format("%s/older" % root_path)
        command = ['mv', from_path, to_path]
        if self.verbose:
            print "Moving older files '%s' into '%s'" % (from_path, to_path)
        elif self.log:
            self.write_to_log(format("Moving older files '%s' into '%s'" % (from_path, to_path)))
        subprocess.call(command, stdout = self.my_out, stderr = self.my_err)

    def run(self):
        root_depth = len(self.rootDir.split("/"))
        if self.unzip != "false":
            self.ececute = self.unzip_execute(root_depth)
        if self.rename:
            self.user_rename()
        if self.execute:
            self.dive_move(root_depth)
            self.dive_delete_dir(root_depth)
        if self.delete:
            self.dive_delete(root_depth)
        if self.log:
            self.log_file.close()
        elif not verbose:
            self.null_out.close()

    def unzip_execute(self, root_depth):
        zipfile = self.unzip
        if self.unzip == "true":
            zipfile = self.find_zip_file(root_depth)
        # Return if _one_ zip file only not found.
        if self.execute:
            self.unzip_file(zipfile)
            self.unzip_clean(root_depth, zipfile[:-4])
        return execute

    def find_zip_file(self, root_depth):
        files = ""
        zipfiles = []
        for dirpath, subdirs, filenames in os.walk(self.rootDir):
            depth = len(dirpath.split("/")) - root_depth
            if depth == 0:
                if self.verbose:
                    print "Looking for zip files."
                files = filenames;
                for afile in files:
                    if afile[-4:] == ".zip":
                        if self.verbose:
                            print "Found zip-file: %s" % afile
                        elif self.log:
                            self.write_to_log(format("Found zip-file: %s" % afile))
                        zipfiles.append(afile)
                if len(zipfiles) > 1:
                    print "Please have only the zipfile from Devilry in folder"
                    self.execute = False
                elif len(zipfiles) == 0:
                    print "No zipfiles were found in '%s/'" % rootDir
                    self.execute = False
                break # out from os.walk() as only files from root needed
        if len(zipfiles) > 0:
            return zipfiles[0]
        return ""

    def unzip_file(self, zipfile):
        # Unzip command
        from_path = format("%s" % (zipfile))
        to_path = self.rootDir
        command = ['unzip',
                   from_path,
                   "-d",
                   to_path]
        if self.verbose:
            print "Unzipping file: %s" % from_path
        elif self.log:
            self.write_to_log(format("Unzipping file '%s'" % (from_path)))
        subprocess.call(command, stdout = self.my_out, stderr = self.my_err)


    def unzip_clean(self, root_depth, unzippedfolder):
        for dirpath, subdirs, filenames in os.walk(self.rootDir):
            if (dirpath[-1] == '/'):
                depth = len(dirpath[:-1].split("/")) - root_depth
            else:
                depth = len(dirpath.split("/")) - root_depth
            if depth == 1:
                if self.verbose:
                    print "Going through folders within '%s'" % dirpath
                elif self.log:
                    self.write_to_log(format("Going through folders within '%s'" % (dirpath)))
                # Move all back down to root
                for subdir in subdirs:
                    from_path = format("%s/%s" % (dirpath, subdir))
                    to_path = '/'.join(dirpath.split("/")[:-1])
                    if self.verbose:
                        print "Moving '%s' down to '%s'" % (from_path, to_path)
                    elif self.log:
                        self.write_to_log(format("Moving '%s' down to '%s'" % (from_path, to_path)))
                    shutil.move(from_path, to_path)
                break # out from sub-folder created after zip. only these files needed moving
        # Remove the now empty folder
        from_path = format("%s/%s" % (self.rootDir, unzippedfolder))
        command = ["rm", "-d", from_path]
        if self.verbose:
            print "Removing empty folder: %s" % from_path
        elif self.log:
            self.write_to_log(format("Removing empty folder: %s" % (from_path)))
        subprocess.call(command, stdout = self.my_out, stderr = self.my_err)

    def user_rename(self):
        for dirpath, subdirList, fileList in os.walk(rootDir):
            for subdir in subdirList:
                filepath = format(''"%s/%s"'' % (dirpath, subdir))
                new_filepath = format("%s/%s" % (dirpath, subdir[0:subdir.find(' (')]))
                if self.verbose:
                    print "Renaming '%s' to '%s'" % (filepath, new_filepath)
                elif self.log:
                    self.write_to_log(format("Renaming '%s' to '%s'" % (filepath, new_filepath)))
                os.rename(filepath, new_filepath)
            break

    def write_to_log(self, text):
        self.log_file.write(
            format("%s-%s: %s\n" %
                   (time.strftime("%H:%M"),
                    time.strftime("%d/%m/%Y"),
                    text)))

def print_usage():
    print "Usage: python sort_deliveries.py [options] path"
    print "Options: -b -h -l -d -v -D -z [zipfile]"
    print "%10s -- %-s" % ("-b", "bare move, no rename of user folder")
    print "%10s -- %-s" % ("-h", "shows this menu")
    print "%10s -- %-s" % ("-l", "creates a log file for what happens")
    print "%10s -- %-s" % ("-d", "delete the other files and folders")
    print "%10s -- %-s" % ("-v", "loud about what happens")
    print "%10s -- %-s" % ("-D", "DEBUG mode, program will not execute")
    print "%10s -- %-s" % ("-z", "unzips the .zip file in path first (if only 1 is present)")
    print "%10s -- %-s" % ("-z zipfile", "unzipz the specified zip file in path first")


if __name__=='__main__':
    """
    TO BE DONE
    # Argument Parser
    parser = argparse.ArgumentParser(description="Usage:\npython sort_deliveries.py [options] pathProgram preprocesses a latex-file ('infile') and produces a new latex-file ('outfile') with additional functionality")
    parser.add_argument("infile", help="Name of the latex-file you want preprocessed")
    parser.add_argument("-o", "--outfile", nargs=1, help="Name of the new file (cannot be equal to infile)")
    parser.add_argument("-f", "--fancy_verbatim", help="produces more fancy verbatim", action="store_true")
    parser.add_argument("-v", "--verbosity", help="increase output verbosity", action="store_true")
    args = parser.parse_args()
    verbose = args.verbosity
    fancy = args.fancy_verbatim

    if len(sys.argv) < 2 or sys.argv[-1][0] == '-':
        print_usage()
        sys.exit()
        # Quits
    """
    rootDir = "."
    execute = True
    delete = False
    rename = True
    log = False
    unzip = "false"
    verbose = False

    # Find correct path according to arguments
    argc = 1 # 0 would be programname
    argl = len(sys.argv)-1
    # .py  -> program not the only argument
    # '-'  -> last argument not an option
    # .zip -> last argument not the zip-file
    if argl < 1 or \
       sys.argv[argl].find(".py") >= 0 or \
       sys.argv[argl][0] == '-' or \
       sys.argv[argl].find(".zip") >= 0:
        print_usage()
        sys.exit()
    rootDir = format("%s/%s" % (rootDir, sys.argv[-1]))[2:]
    if (rootDir[-1] == "/"):
        rootDir = rootDir[:-1]

    # Handle arguments
    while argc < argl:
        arg = sys.argv[argc]
	options = list(arg)
        for letter in options[1]:
            if letter == 'z':
                unzip = "true"
                if argc+1 < argl and sys.argv[argc+1].find(".zip", len(sys.argv[argc+1])-4) != -1:
                    argc += 1
                    unzip = sys.argv[argc]
            elif letter == "h":
                print_usage()
                execute = False
                break
            elif letter == "l":
                log = True
            elif letter == "v":
                verbose = True
            elif letter == "d":
                delete = True
            elif letter == "b":
                rename = False
            elif letter == "D":
                execute = False
        argc += 1

    # Execute if executable
    if execute:
        sorter = Devilry_Sort(rootDir, execute, delete, log, rename, unzip, verbose)
        sorter.run()
