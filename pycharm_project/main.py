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
import math

# The phantom itself is a 16 cm radius cylindrical phantom centered at (0, 0)
phantom = geo.region.Region(geo.rcc2d.Rcc2d(16))
phantom.matid = 'E'                                   # Set the material id to 'E' which is Phantom PMMA
phantomregions = auxutil.automesh(phantom, (16, 16))  # Mesh into 10x10 squares

# The slice is a 1/16 slice that contains a collimator, botwtie filter, and flat filter
# The air region is meshed into smaller RPP regions
sliceregions = makephantom.makeslice()

# Duplicate the slice region 16 times, once in each slice direction
#sliceregions_list = []
#for i in range(0,16):
#    sliceregions_list.append([x.get_rotated_about_2d(2*math.pi/16 * i) for x in sliceregions])

# The external region makes the whole thing fit in a -75, 75 x -75, 75 box
airinner = geo.rcc2d.Rcc2d(74)
airoutter = geo.rpp2d.Rpp2d(dims=(160, 160))
externregions = [geo.region.Region(airoutter) - airinner]
externregions[0].matid = 'G'  # Sets the material id to 'G' which is air


# Write the file
writer = partswriter.PartsWriter("./phantom.parts", {'E': "PHANTOM", 'F': "COLLIMATOR", 'G': "AIR", 'H': "ALUM"},
                                 override_existing=True)
writer.write("phantom_part", phantomregions, comment="The phantom istelf meshed into squares")
#writer.write("slice_part",   sliceregions,   comment="A 1/16 slice")

for i in range(0, 16):
    writer.write("slice_part" + str(i+1), sliceregions, comment="1/16 slice number " + str(i+1))
    auxutil.rotate_regions(sliceregions, 360/16, is_radians=False)
    #for r in sliceregions:
        #print("rotating a new region..." + str(r))
        #r.rotate_about_2d(360/16, aboutpt=(0, 0), is_radians=False)
        #print("finished with the region")

writer.write("extern_part",  externregions,  comment="Fills out to RPP boundary")
writer.close()

# Create the visualiser
#vis = pygamevisualizer.Visualizer()
#vis.register(sliceregions)
#vis.launch()


