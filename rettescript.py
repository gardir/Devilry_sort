import os.path
import sys
from subprocess import call
from subprocess import Popen, PIPE

def unzip(filename):
    print "---> Pakker ut alle filer..."

    if os.path.isdir(filename[0:-4]):
        print "---> Filene er alt pakket ut. Rydd opp og kjoer igjen.\n"
        print "----> Terminerer <----"
        quit()

    returnvalue = call(["unzip", "-qo", filename])

    if returnvalue == 0:
        for root, dirs, files in os.walk(filename[0:-4], topdown=True):
            newname = ""
            for c in root:
                if not c == " " and not c == "(" and not c == ")":
                    newname += c
            if newname != root:
                call(["mv", root, newname])
        print "---> OK!\n"
    else:
        print "---> Unzip feilet!\n"
        print "----> Terminerer <----"
        quit()


def javac(path):
    print "---> Kompilerer alle filer..."
    failed = []
    maxdir = 0
    for root, dirs, files in os.walk(path, topdown=True):
        for direct in dirs:
            if direct[-12:-4] == "delivery":
                maxdir = max(maxdir, int(direct[-3:]))
        if root[-12:] == "delivery-" + "00" + str(maxdir):
            maxdir = 0
            for file in files:
                if file.endswith(".java"):
                    proc = Popen('javac ' + root + "/" + "*.java", shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
                    out, err = proc.communicate()
                    if err != '' and not err.startswith("Note"):
                        start = 0
                        stop = 0
                        for i in range(len(root)):
                            if root[i] == "/" and start == 0:
                                start = i
                            if root[i:].startswith("groupid") and stop == 0:
                                stop = i

                        failed.append(root[start+1:stop])
                    break
    print "---> OK!\n"
    return failed


def print_failed(fails):
    print "---> Studenter/grupper med kompileringsfeil i siste innlevering:"
    for fail in fails:
        print fail
    print "\n---> LYKKE TIL MED RETTINGEN! <---\n"

if __name__ == "__main__":
    print "==== Automatisk rettescript for INF1000 ====\n"
    if len(sys.argv) < 2:
        print "Bruk: python rettescript.py <filnavn>\n"
        print "----> Terminerer <----"
        quit()

    filename = sys.argv[1]
    pathname = filename[0:-4]

    if not os.path.isfile(filename):
        print "Ugyldig filnavn\n"
        print "----> Terminerer <----"
        quit()

    unzip(filename)
    fails = javac(pathname)
    print_failed(fails)
