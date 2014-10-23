__author__ = 'Edward'

# Import necessary modules
from visualizer import pygamevisualizer
import partswriter
import makephantom
import geo.region
import geo.rcc2d
import geo.rpp2d
import geocheck
import auxutil

# Play around region

boxy = geo.region.Region(geo.rcc2d.Rcc2d(10))
boxies = auxutil.automesh2(boxy, (10, 5))

vis = pygamevisualizer.Visualizer()
vis.register(boxies)
vis.register(boxy)
vis.launch()

exit()








# Create the regions
phantomregions = makephantom.makephantom()
sliceregions = makephantom.makeslice()
externregions = makephantom.makeoutter()

# Create sets of all the bodies
phantombodies = set()
for r in phantomregions:
    phantombodies.update(r.get_all_bodies())

slicebodies = set()
for r in sliceregions:
    slicebodies.update(r.get_all_bodies())

externbodies = set()
for r in externregions:
    externbodies.update(r.get_all_bodies())

# Write the file
writer = partswriter.PartsWriter("./phantom.parts", {'E': "PHANTOM", 'F': "COLLIMATOR", 'G': "AIR", 'H': "ALUM"},
                                 override_existing=True)
writer.write("phantom_part", phantombodies, phantomregions, comment="The phantom istelf meshed into squares")
writer.write("slice_part", slicebodies, sliceregions, comment="A 1/16 slice")
writer.write("extern_part", externbodies, externregions, comment="Fills out to RPP boundary")
writer.close()

# Create the visualiser
vis = pygamevisualizer.Visualizer()

b = geo.rpp2d.Rpp2d((10, 5), (4, 10))

tomesh = sliceregions[4]
sliceregions = sliceregions[:3]
subs = auxutil.automesh(tomesh, 2.0)
sliceregions.extend(subs)

#cylregion = geo.region.Region(geo.rcc2d.Rcc2d(10.0)) - geo.rcc2d.Rcc2d(8.0) | geo.rpp2d.Rpp2d((10, 5), (4, 10))
#meshed = auxutil.automesh(cylregion, 1.0)
for r in sliceregions:
    vis.register(r)
    vis.register(r.get_all_bodies())

vis.launch()





#vis.register(phantombodies)
# for p in slicebodies:
#     p.visualizer = vis
#     vis.drawables.add(p)
# vis.register(sliceregions)
# for r in phantomregions:
#     vis.register(r.get_all_bodies())
#     vis.register(r)

# import math
# theta = 2 * math.pi / 16
# for i in range(1, 16):
#     for r in sliceregions:
#         rr = r.get_rotated_about_2d(theta * i)
#         slicebodies.update(rr.get_all_bodies())
# vis.register(slicebodies)
#
# geocheck.circlecheck(phantomregions, 16, (0, 0), 100, vis)
# #geocheck.check(phantomregions, 500, vis)
#
# vis.launch()


