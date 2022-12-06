import os
import sys


def get_all_fullpath(rootpath, absolute=True):
    def get_fullpath(resultat, rootpath, file_or_dir):
        newpath = os.path.join(rootpath, file_or_dir)

        if os.path.isdir(newpath):
            for elt in os.listdir(newpath):
                get_fullpath(resultat, os.path.join(
                    rootpath, file_or_dir), elt)
        else:
            resultat.append(os.path.join(rootpath, file_or_dir))

    absolute_path = os.path.abspath(rootpath)
    if rootpath != "." \
            and rootpath[:len(os.sep)+1] != str("." + os.sep):
        rootpath = "." + os.path.join(os.sep, rootpath)

    resultat = []
    tmp = os.listdir(rootpath)
    for elt in tmp:
        get_fullpath(resultat, rootpath, elt)
    resultat = sorted(resultat)

    if (absolute):
        for index in range(len(resultat)):
            if (resultat[index][len(rootpath):len(rootpath)+1] == os.sep):
                resultat[index] = absolute_path + \
                    resultat[index][len(rootpath):]
            else:
                resultat[index] = absolute_path + \
                    os.sep + resultat[index][len(rootpath):]

    return resultat


def to_json(lines):
    mydico = {}

    def splitbysep(path):
        newpath = path.split(os.sep)
        resultat = []
        for i in range(len(newpath)):
            if i+1 == len(newpath):
                resultat.append((newpath[i], True))
            else:
                resultat.append((newpath[i], False))
        return resultat

    def reduce(mydico, pathinlist, depth=0):
        if pathinlist[0][1]:
            # fichier
            mydico[pathinlist[0][0]] = depth
        else:
            if not (pathinlist[0][0] in mydico.keys()):
                mydico[pathinlist[0][0]] = {}
            reduce(mydico[pathinlist[0][0]], pathinlist[1:], depth+1)

    for i in lines:
        newpath = splitbysep(i)
        reduce(mydico, newpath)
    return mydico


#json.dump(mydico, open("output.json", "w"), indent=4)
def printhelp():
    s = """
  Options are : 
  -h, -help         display this help msg
  -o, -out          output format. 'std' or 'json'.
  -f, -filename     output file name. return a file with name '*.txt' or '*.json'. default "output.{txt|json}"
  
  example: python filepath_recur.py targetfolder -o json -f output.json 
  """
    print(s)


if (len(sys.argv) == 1 or len(sys.argv) == 2):
    printhelp()
else:
    if (sys.argv[1] == "-h" or sys.argv[1] == "-help"):
        printhelp()
    else:
        if (os.path.exists(sys.argv[1])) and (os.path.isdir(sys.argv[1])):

            if (len(sys.argv) == 4):
                filename = -1
            else:
                if (len(sys.argv) > 5):
                    if (sys.argv[4] == "-f" or sys.argv[4] == "-filename"):
                        filename = sys.argv[5]
                    else:
                        printhelp()
                else:
                    filename = "output"

            if (sys.argv[2] == "-o" or sys.argv[2] == "-out"):
                # did here because we need it anyway for json
                tmp = get_all_fullpath(sys.argv[1])
                if (sys.argv[3] == "std"):
                    # std display
                    # display stdout or file
                    if (filename == -1):
                        for i in tmp:
                            print(i)
                    else:
                        if (filename[-4:] != ".txt"):
                            filename += ".txt"
                        with open(filename, "w") as f:
                            for i in tmp:
                                f.write(i + "\n")


                elif (sys.argv[3] == "json"):
                    # json display
                    import json
                    mydico = to_json(tmp)
                    # display stdout or file
                    if (filename == -1):
                        print(json.dumps(mydico, indent=4))
                    else:
                        if (filename[-5:] != ".json"):
                            filename += ".json"
                        json.dump(mydico, open(filename, "w"), indent=4)

                else:
                    printhelp()
            else:
                printhelp()
        else:
            print("folder doesn't exist")
