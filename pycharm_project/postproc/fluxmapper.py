__author__ = 'Edward'

import os.path
import sys

class FluxMapper(object):

    def __init__(self, name="input", binary=False, rmapfile=None, listfile=None, mshfile=None):
        self.rmapfile = None
        self.listfile = None
        self.mshfile = None
        self.READLIMIT = 10E6

        if rmapfile is not None:
            self.rmapfile = open(rmapfile, 'r')
        else:
            self.rmapfile = open(name + ".rmap", 'r')

        if listfile is not None:
            self.listfile = open(listfile, 'r')
        else:
            self.listfile = open(name + ".l", 'r')

        if binary:
            if mshfile is not None:
                self.mshfile = open(mshfile, 'wb')
            else:
                self.mshfile = open(name + ".msh", 'w')

    # TODO This should return the results array not do the printing itself
    def parse(self):
        mapping = {}
        results = []

        for line in self.rmapfile.readline():
            tokens = line.split()  # Split on whitepsace
            name = tokens[0]
            pt = [float(x) for x in tokens[1:len(tokens)]]
            mapping.update({name: pt})

        if os.path.getsize(self.listfile.name) > self.READLIMIT:
            # Read line by line
            pass
        else:
            # Read all at once
            lines = self.listfile.readlines()
            i = 0
            linecount = len(lines)
            found = False
            while i < linecount:
                if lines[i].startswith("FLUX & DOSE RATES BY GROUP, BY REGION, BY VOLUME"):
                    found = True
                    i += 4  # Skip next 4 lines
                if found:

                    data = lines[i].split()
                    count = len(data)
                    name = data[0]
                    vol = data[count - 4]
                    flux = data[count - 3]
                    doserate = data[count-2]
                    h2o = data[count-1]

                    pt = mapping.pop(name, None)  # Return None on failure
                    if pt is None:
                        print("WARNING: Couldn't find part " + name + " in " + self.rmapfile.name)

                    self.mshfile.write(str(pt[0]) + "\t" + str(pt[1]) + "\t" + str(pt[2]) + "\t" +
                                       str(vol) + "\t" + str(flux) + "\t" + str(doserate) + "\t" + str(h2o) + "\t")

                i += 1

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Useage: python fluxmapper.py rmapfile lfile mshfile")
    elif len(sys.argv) == 4:
        # Arg 0 is the program name, fluxmapper.py
        f = FluxMapper(rmapfile=sys.argv[1], listfile=sys.argv[2], mshfile=sys.argv[3])
        f.parse()
    else:
        print("Not the correct number of args!")
        print("Useage: python fluxmapper.py rmapfile lfile mshfile")