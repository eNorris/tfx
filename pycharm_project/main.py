__author__ = 'Edward'

# Import necessary modules
from visualizer import pygamevisualizer
import partswriter
import makephantom
import geo.region
import geo.rcc2d
import geo.rpp2d
import geo.raw2d
import geocheck
import auxutil

# Play around region

# boxy = geo.region.Region(geo.raw2d.Raw2d((0, 0), (10, 0), (0, 10))) - geo.rcc2d.Rcc2d(5)
# #boxy = geo.region.Region(geo.rcc2d.Rcc2d(10))
# boxies = auxutil.automesh2(boxy, (30, 30))
#
# print("accepted: " + str(len(boxies)))
#
# vis = pygamevisualizer.Visualizer()
# vis.register(boxies)
# #vis.register(boxy)
# vis.launch()
#
# exit()

# The phantom itself is a 16 cm radius cylindrical phantom centered at (0, 0)
phantom = geo.region.Region(geo.rcc2d.Rcc2d(16))
phantom.matid = 'E'  # Set the material id to 'E' which is Phantom PMMA
phantomregions = auxutil.automesh2(phantom, (10, 10))  # Mesh into 10x10 squares

# The slice is a 1/16 slice that contains a collimator, botwtie filter, and flat filter
# The air region is meshed into smaller RPP regions
sliceregions = makephantom.makeslice2()

# The external region makes the whole thing fit in a -75, 75 x -75, 75 box
airinner = geo.rcc2d.Rcc2d(74)
airoutter = geo.rpp2d.Rpp2d(dims=(150, 150))
externregions = [geo.region.Region(airoutter) - airinner]
externregions[0].matid = 'G'  # Sets the material id to 'G' which is air


# Create the regions
#phantomregions = makephantom.makephantom()
#sliceregions = makephantom.makeslice()
#externregions = makephantom.makeoutter()

# Create sets of all the bodies
#phantombodies = set()
#for r in phantomregions:
#    phantombodies.update(r.get_all_bodies())
#
#slicebodies = set()
#for r in sliceregions:
#    slicebodies.update(r.get_all_bodies())
#
#externbodies = set()
#for r in externregions:
#    externbodies.update(r.get_all_bodies())

# Write the file
writer = partswriter.PartsWriter("./phantom.parts", {'E': "PHANTOM", 'F': "COLLIMATOR", 'G': "AIR", 'H': "ALUM"},
                                 override_existing=True)
writer.write("phantom_part", phantomregions, comment="The phantom istelf meshed into squares")
writer.write("slice_part",   sliceregions,   comment="A 1/16 slice")
writer.write("extern_part",  externregions,  comment="Fills out to RPP boundary")
writer.close()

# Create the visualiser
vis = pygamevisualizer.Visualizer()
vis.register(sliceregions)

#b = geo.rpp2d.Rpp2d((10, 5), (4, 10))
#
#tomesh = sliceregions[4]
#sliceregions = sliceregions[:3]
#subs = auxutil.automesh(tomesh, 2.0)
#sliceregions.extend(subs)

#cylregion = geo.region.Region(geo.rcc2d.Rcc2d(10.0)) - geo.rcc2d.Rcc2d(8.0) | geo.rpp2d.Rpp2d((10, 5), (4, 10))
#meshed = auxutil.automesh(cylregion, 1.0)
#for r in sliceregions:
#    vis.register(r)
    #vis.register(r.get_all_bodies())

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


