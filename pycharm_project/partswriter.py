__author__ = 'Edward'

import os.path
import util

class PartsWriter:

    def __init__(self, filename, materialmap, override_existing=False):
        self.filename = filename
        self.matmap = materialmap
        self.file = None
        self.rmap = None
        self.gatfile = None

        if not override_existing:
            if os.path.isfile(filename):
                print("WARNING: Failed to override an existing file! write() will do nothing!!!")
                return

        self.file = open(self.filename, 'w')
        self.gatfile = open(self.filename.split(".")[0] + 'GAT.inp', 'w')
        self.writeheaders()

        lastdotindex = self.filename.rsplit(".", 1)
        self.rmap = open(lastdotindex[0] + ".rmap", 'w')

    def generate_evals(self, regions):
        lines = ""
        for region in regions:
            for pt in region.evalpoints:
                lines += "  " + str(region.id) + ": " + str(pt[0]) + ", " + str(pt[1]) + ", " + str(pt[2]) + \
                         ", " + str(1/len(region.evalpoints)) + ": Eval point/\n"
        return lines

    def collapse_simplify(self, objects):
        index = 1

        try:
            sortedlist = sorted(objects, key=lambda o: o.id)
            for obj in sortedlist:
                obj.id = index
                index += 1
        except TypeError:
            pass

    def writeheaders(self):
        if self.file is None:
            return
        self.file.write("TFX_Parts\n")
        self.file.write("!- Parts file\n")
        self.file.write("!- Auto generated by partswriter.py in tfx project (https://github.com/eNorris/tfx/)\n")
        self.file.write("!-\n")

        self.gatfile.write("GAT\n")

    def write(self, partname, regions, comment=""):

        self.file.write(partname + ": " + comment + "\n")

        bodies = set()
        try:
            for r in regions:
                bodies.update(r.get_all_bodies())
        except TypeError:
            bodies.update(regions.get_all_bodies())

        bodies = sorted(bodies, key=lambda x: x.id)
        try:
            regions = sorted(regions, key=lambda x: x.id)
        except TypeError:
            pass

        self.collapse_simplify(bodies)
        self.collapse_simplify(regions)

        #evalregions = [x for x in regions if x.doeval]
        evalregions = [x for x in regions if True]
        evalpointcount = sum(len(x.evalpoints) for x in evalregions)
        thispartmats = sorted(list(set([k.matid for k in regions])))

        # Count the number of materials, regions, and eval points needed
        self.file.write("0, " + str(len(thispartmats)) + ", " + str(len(bodies)) + ", " + str(len(regions)) + ", " +
                   str(evalpointcount) + "/\n")
        self.file.write(", ".join([str(k) + "=" + str(self.matmap[k]) for k in thispartmats]) + "/\n")

        # Write the actual region parts
        for b in bodies:
            self.file.write(str(b) + "/\n")
        for r in regions:
            self.file.write(str(r) + "/\n")
            #self.gatfile.write("'" + partname + ":1." + str(r.id) + "', 2=" + str(util.calc_volume(r, 1000)) + "/\n")
        self.file.write(self.generate_evals(evalregions))

        print("PartsWriter: calculating volumes for GAT file:")
        regioncount = len(regions)
        regionsdone = 0
        for r in regions:
            regionsdone += 1
            if regionsdone % 10 == 0:
                print("Finished " + str(regionsdone) + "/" + str(len(regions)))
            self.gatfile.write("'" + partname + ":1." + str(r.id) + "', 2=" + str(util.calc_volume(r, 1000)) + "/\n")

        for r in evalregions:
            for pt in r.evalpoints:
                self.rmap.write(str(r.id) + "\t" + str(pt[0]) + "\t" + str(pt[1]) + "\t" + str(pt[2]) + "\n")

    def close(self):
        if self.file is not None:
            self.file.close()
        if self.rmap is not None:
            self.rmap.close()
        if self.gatfile is not None:
            self.gatfile.write("/")
            self.gatfile.close()