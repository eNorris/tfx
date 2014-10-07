__author__ = 'Edward'

# Import necessary modules
from visualizer import pygamevisualizer
import partswriter
import makephantom
import geocheck

# Create the regions
phantomregions = makephantom.makephantom()
sliceregions = makephantom.makeslice()

# Create sets of all the bodies
phantombodies = set()
for r in phantomregions:
    phantombodies.update(r.get_all_bodies())

slicebodies = set()
for r in sliceregions:
    slicebodies.update(r.get_all_bodies())

# Write the file
writer = partswriter.PartsWriter("./phantom.parts", {'E': "PHANTOM", 'F': "COLLIMATOR", 'G': "AIR", 'H': "ALUM"},
                                 override_existing=True)
writer.write("phantom_part", phantombodies, phantomregions, comment="The phantom istelf meshed into squares")
writer.write("slice_part", slicebodies, sliceregions, comment="A 1/16 slice")
writer.close()

# Create the visualiser
vis = pygamevisualizer.Visualizer()
#vis.register(phantombodies)
for p in slicebodies:
    p.visualizer = vis
    vis.drawables.add(p)
vis.register(sliceregions)

import math
theta = 2 * math.pi / 16
for i in range(1, 16):
    for r in sliceregions:
        rr = r.get_rotated_about_2d(theta * i)
        slicebodies.update(rr.get_all_bodies())
vis.register(slicebodies)

geocheck.circlecheck(phantomregions, 16, (0, 0), 100, vis)
#geocheck.check(phantomregions, 500, vis)

vis.launch()


