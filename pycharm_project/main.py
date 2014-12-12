__author__ = 'Edward'

# Import necessary modules
from visualizer import pygamevisualizer
import partswriter
import makephantom
import geo.region
import geo.rcc2d
import geo.rpp2d
import geo.raw2d
import auxutil
import geocheck
import math

# The phantom itself is a 16 cm radius cylindrical phantom centered at (0, 0)
phantom = geo.region.Region(geo.rcc2d.Rcc2d(16))
phantom.matid = 'E'                                   # Set the material id to 'E' which is Phantom PMMA
phantomregions = auxutil.automesh(phantom, (31, 31))  # Mesh into 10x10 squares
phantomregions = auxutil.extend_2d_to_3d(phantomregions, 15.0)
#phantomregions = auxutil.layerize(phantomregions, 5)

# The slice is a 1/16 slice that contains a collimator, botwtie filter, and flat filter
# The air region is meshed into smaller RPP regions
sliceregions = makephantom.makeslice3d()
sliceregions = auxutil.extend_2d_to_3d(sliceregions, 15.0)
for r in sliceregions:
    for b in r.get_all_bodies():
        if b.comment == "Collimator hole":
            b.l = 5.0
            b.z = -0.14814/2

# The external region makes the whole thing fit in a -75, 75 x -75, 75 box
airinner = geo.rcc2d.Rcc2d(74)
airoutter = geo.rpp2d.Rpp2d(dims=(160, 160))
externregions = [geo.region.Region(airoutter) - airinner]
externregions[0].matid = 'G'  # Sets the material id to 'G' which is air
externregions = auxutil.extend_2d_to_3d(externregions, 15.0)

# Create the visualiser
vis = pygamevisualizer.Visualizer()
#vis.register(phantomregions)
geocheck.check_domain(sliceregions, 2000, (-80, -80, -7.5), (80, 80, 7.5), vis)
#geocheck.check(phantomregions, 500, vis)
#geocheck.volumecheck(phantomregions, 1000)
print("Phantom Bounds = " + str(geocheck.get_super_bounds(phantomregions)))
print("Slice Bounds = " + str(geocheck.get_super_bounds(sliceregions)))
print("Extern Bounds = " + str(geocheck.get_super_bounds(externregions)))
vis.launch()

# Write the file
writer = partswriter.PartsWriter("./phantom.parts", {'E': "PHANTOM", 'F': "COLLIMATOR", 'G': "AIR", 'H': "ALUM"},
                                 override_existing=True)
writer.write("phantom_part", phantomregions, gatregion="PHANTOM", comment="The phantom istelf meshed into squares")
#writer.write("slice_part",   sliceregions,   comment="A 1/16 slice")

for i in range(0, 16):
    writer.write("slice_part" + str(i+1), sliceregions, gatregion="SLICE" + str(i+1), comment="1/16 slice number " + str(i+1))
    auxutil.rotate_regions(sliceregions, 360/16, is_radians=False)

writer.write("extern_part",  externregions,  gatregion="BOUNDS", comment="Fills out to RPP boundary")
writer.close()

print("region count = " + str(16 * len(sliceregions) + 2))




