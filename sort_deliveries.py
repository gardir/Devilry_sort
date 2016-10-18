#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import time
import shutil
import glob
from rettescript import print_failed

class Devilry_Sort:
    def __init__(self,
                 rootDir,
                 execute=True,
                 delete=False,
                 log=False,
                 rename=True,
                 unzip="false",
                 javacFlag=False,
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
        self.javacFlag = javacFlag
        self.verbose = verbose

        self.failed_javac = []

        self.my_out = sys.stdout
        self.my_err = sys.stderr
        if log:
            log_filename = os.path.join(rootDir, "log.txt")
            self.log_file = open(log_filename, 'w')
            self.log_file.close()
            self.log_file = open(log_filename, 'a')
            self.write_to_log("Log created")
            self.my_out = self.log_file
            self.my_err = self.log_file
        elif not verbose:
            self.null_out = open(os.devnull, 'w')
            self.my_out = self.null_out
            self.my_err = subprocess.STDOUT

    def attempt_javac(self, path):
	"""
	Function inspired by rettescript.py written by Henrik Hillestad Løvold
	"""
        command = format("javac %s" % os.path.join(path, "*.java"))
        if self.verbose:
            print("%s:" % (command))

        elif self.log:
            self.write_to_log(format("%s:" % command))
        try:
            subprocess.check_call(command, shell=True, stdout=self.my_out, stderr=self.my_err)
            
        except subprocess.CalledProcessError:
            return 1

        # No problem
        return 0
            
    def dive_delete(self, root_depth):
        """

        """
        for dirpath, subdirList, fileList in os.walk(rootDir, topdown=False):
            depthList = dirpath.split(os.path.sep)
            depth = len(depthList) - root_depth
            if depth == 1:
                for subdir in subdirList:
                    path = os.path.join(dirpath, subdir).replace(" ", "\ ")
                    command = ["rm", "-r", path]
                    if self.verbose:
                        print("Recursive removing '%s'" % path)
                        
                    elif self.log:
                        self.write_to_log(format("Recursive removing '%s'" % path))
                        
                    #subprocess.call(command, stdout = self.my_out, stderr = self.my_err)
                    shutil.rmtree(path)

    def dive_delete_dir(self, root_depth):
        for dirpath, subdirList, fileList in os.walk(rootDir, topdown = False):
            depth = len(dirpath.split(os.path.sep)) - root_depth
            created = False
            for subdir in subdirList:
                folder = os.path.join(dirpath, subdir)
                command = ['rm', '-d', folder]
                try:
                    if self.verbose:
                        print("Trying to remove empty folder: %s" % folder)
                        
                    elif self.log:
                        self.write_to_log(format("Trying to remove empty folder: %s" % folder))
                        
                    #subprocess.check_call(command, stdout = self.my_out, stderr = self.my_err)
                    os.rmdir(folder)
                    
                #except subprocess.CalledProcessError:
                except OSError:
                    if self.verbose:
                        print("Removing empty folder failed: %s" % folder)
                        
                    elif self.log:
                        self.write_to_log(format("Removing empty folder failed: %s" % folder))
                        
                if depth == 1:
                    self.move(dirpath, subdir)
                    java_files_present = len(glob.glob(dirpath+os.path.sep+'*.java')) > 0
                    if java_files_present and self.attempt_javac(dirpath) != 0:
                        if self.verbose:
                            print("%s failed javac" % dirpath)
                            
                        elif self.log:
                            self.write_to_log(format("%s failed javac" % dirpath))
                            
                        self.failed_javac.append(dirpath)

    def dive_move(self, root_depth):
        for dirpath, subdirList, fileList in os.walk(rootDir, topdown=True):
            depthList = dirpath.split(os.path.sep)
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
                from_path = dirpath
                to_path = os.path.join(*from_path.split(os.path.sep)[:-2])
                if self.verbose:
                    print("Moving all files in '%s' to '%s'" % (from_path, to_path))
                    
                elif self.log:
                    self.write_to_log(format(
                        "Moving all files in '%s' to '%s'" % (from_path, to_path)))
                    
                for work_file in fileList:
                    file_path = os.path.join(from_path, work_file)
                    new_file_path = os.path.join(to_path, work_file)
                    if self.verbose:
                        print("Renaming '%s' to '%s'" % (file_path, new_file_path))
                        
                    elif self.log:
                        self.write_to_log(format("Moved '%s' to '%s'" % (file_path, new_file_path)))
                        
                    #shutil.move(file_path, new_file_path)
                    os.rename(file_path, new_file_path)

    def move(self, root_path, folder):
        from_path = os.path.join(root_path, folder)
        to_path = os.path.join(root_path, "older")
        command = ['mv', from_path, to_path]
        if self.verbose:
            print("Moving older files '%s' into '%s'" % (from_path, to_path))
            
        elif self.log:
            self.write_to_log(format("Moving older files '%s' into '%s'" % (from_path, to_path)))
            
        #subprocess.call(command, stdout = self.my_out, stderr = self.my_err)
        try:
            shutil.move(from_path, to_path)
            
        except IOError as e:
            if self.verbose:
                print("ERROR: Could not move '%s' to '%s'" % (from_path, to_path))
                print(e)
            elif self.log:
                self.write_to_log("ERROR: Could not move '%s' to '%s'\n%s" % (from_path, to_path, e))

    def run(self):
        root_depth = len(self.rootDir.split(os.path.sep))
        if self.unzip != "false":
            self.execute = self.unzip_execute(root_depth)
            
        if self.execute:
            if self.rename:
	        self.user_rename()
	        
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
            self.unzip_clean(root_depth, zipfile)
        return execute

    def find_zip_file(self, root_depth):
        files = ""
        zipfiles = []
        for dirpath, subdirs, filenames in os.walk(self.rootDir):
            depth = len(dirpath.split(os.path.sep)) - root_depth
            if depth == 0:
                if self.verbose:
                    print("Looking for zip files.")
                    
                files = filenames;
                for afile in files:
                    if afile[-4:] == ".zip":
                        if self.verbose:
                            print("Found zip-file: %s" % afile)
                            
                        elif self.log:
                            self.write_to_log(format("Found zip-file: %s" % afile))
                            
                        zipfiles.append(afile)
                        
                if len(zipfiles) > 1:
                    print("Please have only the zipfile from Devilry in folder")
                    self.execute = False
                    
                elif len(zipfiles) == 0:
                    print("No zipfiles were found in '%s%s'" % (rootDir, os.path.sep))
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
            print("Unzipping file: %s" % from_path)
            
        elif self.log:
            self.write_to_log(format("Unzipping file '%s'" % (from_path)))
            
        subprocess.call(command, stdout = self.my_out, stderr = self.my_err)

    def unzip_clean(self, root_depth, unzip_file):
        for dirpath, subdirs, filenames in os.walk(self.rootDir):
            # Finding current depth
            if (dirpath[-1] == os.path.sep):
                depth = len(dirpath[:-1].split(os.path.sep)) - root_depth
                
            else:
                depth = len(dirpath.split(os.path.sep)) - root_depth

            # After unzipping, depth 1 is inside unzipped folder (based on Devilry)
            if depth == 1:
                if self.verbose:
                    print("Going through folders within '%s'" % dirpath)
                    
                elif self.log:
                    self.write_to_log(format("Going through folders within '%s'" % (dirpath)))
                    
                # Move all users/groups one directory down/back
                for subdir in subdirs:
                    from_path = os.path.join(dirpath, subdir)
                    to_path = os.path.join(*dirpath.split(os.path.sep)[:-1])
                    if self.verbose:
                        print("Moving '%s' down to '%s'" % (from_path, to_path))
                        
                    elif self.log:
                        self.write_to_log(format("Moving '%s' down to '%s'" % (from_path, to_path)))
                        
                    shutil.move(from_path, to_path)
                    
                break # out from sub-folder created after zip. only these files needed moving
            
        # Remove the now empty folder
        unzipped_folder = unzip_file[unzip_file.rfind("/")+1:-4]
        from_path = os.path.join(self.rootDir, unzipped_folder)
        command = ["rm", "-d", from_path]
        
        if self.verbose:
            print("Removing empty folder: %s" % from_path)
            
        elif self.log:
            self.write_to_log(format("Removing empty folder: %s" % (from_path)))
            
        #subprocess.call(command, stdout = self.my_out, stderr = self.my_err)
        shutil.rmtree(from_path)

    def user_rename(self):
        for dirpath, subdirList, fileList in os.walk(rootDir):
            for subdir in subdirList:
                filepath = os.path.join(dirpath, subdir)
                new_filepath = os.path.join(dirpath, (subdir[0:subdir.find('(')]).replace(" ", ""))
                if self.verbose:
                    print("Renaming '%s' to '%s'" % (filepath, new_filepath))
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
    print("Usage: python sort_deliveries.py [options] path")
    print("Mandatory: path")
    print("%10s -- %-s" % ("path", "the mandatory argument which is the output folder to have all user directories within when script is done"))
    print("Options: -b -c -d -D -h -l -v -z [zipfile]")
    print("%10s -- %-s" % ("-b", "bare move, no rename of user folder"))
    print("%10s -- %-s" % ("-c", "runs javac on each user, and prints those that fail"))
    print("%10s -- %-s" % ("-d", "delete the other files and folders"))
    print("%10s -- %-s" % ("-D", "DEBUG mode, program will not execute"))
    print("%10s -- %-s" % ("-h", "shows this menu"))
    print("%10s -- %-s" % ("-l", "creates a log file for what happens"))
    print("%10s -- %-s" % ("-v", "loud about what happens"))
    print("%10s -- %-s" % ("-z", "unzips the .zip file in path first (if only 1 is present)"))
    print("%10s -- %-s" % ("-z zipfile", "unzipz the specified zip file in path first"))
    print("Example usages")
    print("python sort_deliveries -z ~/Downloads/deliveries.zip .")
    print("Above command will first unzip the 'deliveries.zip' into current folder, and then sort all files")
    print("--")
    print("python sort_deliveries -z ~/Downloads/deliveries.zip ~/assignments/assignment1")
    print("Above command will first unzip the 'deliveries.zip' into the folder at '$HOME/assignments/assignment1/' before sorting said directory")
    print("--")
    print("python sort_deliveries .")
    print("Above command will sort deliveries from current directory - it should contain ALL the users folders - so it is NOT enough to just unzip the zip file and then run the sort script on subdirectory. It should be run on directory.")
    print("Command executions example")
    print("unzip ~/Downloads/deliveries.zip ## This will create a folder with the same name as zip-file in current working directory")
    print("python sort_deliveries deliveries ## Assuming the name of folder is equal to the zip file, it should be included as 'path'")


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
    javacFlag = False

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
    rootDir = os.path.join(rootDir, sys.argv[-1])[2:]
    if (rootDir[-1] == os.path.sep):
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
            elif letter == "c":
                javacFlag = True
        argc += 1

    # Execute if executable
    if execute:
        sorter = Devilry_Sort(rootDir, execute, delete, log, rename, unzip, javacFlag, verbose)
        sorter.run()
        if javacFlag and len(sorter.failed_javac) > 0:
            print_failed(sorter.failed_javac)
        elif javacFlag:
            print("All students compiled")
