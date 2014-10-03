__author__ = 'Edward'

import Rcc2d
import Rpp2d
import Box2d
import Raw2d
import Point
import Visualizer
import Region
import partswriter

import random
import time
import math


# Problem constants
srcpts = 16
beamangle = math.radians(55)

bodies = []
regions = []
vis = Visualizer.Visualizer()

phantom = Rcc2d.Rcc2d(16.0)
#phantomregion = Region.RegionNode(phantom)
#phantomregion.matid = 'E'
#halfwidth = math.sqrt(math.pi) * 16.0 / 2.0
#print("halfwidth = " + str(halfwidth))
#phantom = Rpp2d.Rpp2d((0, 0), (halfwidth, halfwidth))
air = Rpp2d.Rpp2d((0, 0), (150, 150))
airregion = Region.RegionNode(air) - phantom
# TODO Istead of having a doeval variable, just test length of evalpoints
airregion.doeval = True
airregion.matid = 'G'
bodies.extend([phantom, air])
regions.extend([airregion])
vis.register([phantom, air])

# Mesh the phantom and add the regions

width = 32
height = 32
xdivs = 31
ydivs = 31
bot = -16
left = -16

dx = width / xdivs
dy = height / ydivs


for i in range(xdivs):
    for j in range(ydivs):
        r = Rpp2d.Rpp2d([left + i * dx, bot + j * dy], [dx, dy], False)
        neary, nearx = None, None

        if r.top < phantom.cy:
            neary = r.top
        elif r.bottom > phantom.cy:
            neary = r.bottom
        else:
            neary = phantom.cy

        if r.right < phantom.cx:
            nearx = r.right
        elif r.left > phantom.cx:
            nearx = r.left
        else:
            nearx = phantom.cx

        if (neary - phantom.cy)**2 + (nearx - phantom.cx)**2 < phantom.r**2:
            vis.register(r)
            #r.fillcolor = (0, 255, 0, 1)
            bodies.append(r)
            corespondingregion = Region.RegionNode(phantom)
            corespondingregion += r
            corespondingregion.doeval = True
            corespondingregion.matid = 'E'

            evalpt = (0, 0, 0)
            if r.cx**2 + r.cy**2 <= phantom.r**2:
                #print(str(r.cx**2) + " + " + str(r.cy) + " < " + str())
                evalpt = (r.cx, r.cy, .5)
            else:
                if r.cx > 0 and r.cy > 0:
                    evalpt = (r.left+.0001, r.bottom+.0001, .5)
                elif r.cx > 0 and r.cy < 0:
                    evalpt = (r.left+.0001, r.top-.0001, .5)
                elif r.cx < 0 and r.cy > 0:
                    evalpt = (r.right-.0001, r.bottom+.0001, .5)
                else:
                    evalpt = (r.right-.0001, r.top-.0001, .5)
            evvispt = Point.Point2d((evalpt[0], evalpt[1]))
            evvispt.dodraw = True
            evvispt.color = (255, 0, 255)
            evvispt.radius = 3
            vis.registerthis(evvispt)
            corespondingregion.evalpoints.append((evalpt[0], evalpt[1], evalpt[2]))
            regions.append(corespondingregion)


# Add the collimators and their air centers
if srcpts < 4:
    colwidth = 10.0
else:
    colwidth = 50 * math.tan(math.pi / srcpts)
holewidth = 4 * math.tan(beamangle / 2)
if holewidth > colwidth:
    print("WARNING: Collimator hole exceeds collimator size!")

upcollimator = Box2d.Box2d((50, holewidth), (3, 0), (0, (colwidth-holewidth)), False)
downcollimator = Box2d.Box2d((50, -holewidth), (3, 0), (0, -(colwidth-holewidth)), False)
upbow = Raw2d.Raw2d((44, 5), (5, 0), (0, -5))
downbow = Raw2d.Raw2d((44, -5), (5, 0), (0, 5))

# Define the collimator regions
upcol = Box2d.Box2d((50, holewidth), (3, 0), (0, (colwidth-holewidth)/2), False)
upcolreg = Region.RegionNode(upcol)
upcolreg.matid = "F"
upcolreg.evalpoints.append((51.5, (colwidth + holewidth)/4))
# Define the flat filter region

# Define the bowtie region


for i in range(srcpts):
    theta = i * 2 * math.pi / srcpts

    # Add a new eval point in the air region
    newevalpt = Point.Point2d((30 * math.cos(theta), 30 * math.sin(theta)))
    newevalpt.dodraw = True
    newevalpt.color = (255, 0, 255)
    newevalpt.radius = 3
    vis.registerthis(newevalpt)
    #corespondingregion.evalpoints.append((evalpt[0], evalpt[1], evalpt[2]))
    airregion.evalpoints.append((newevalpt[0], newevalpt[1], 0.5))

    # Create the bodies
    newcolup = upcollimator.clone().rotate_about_2d(theta)
    newcoldown = downcollimator.clone().rotate_about_2d(theta)
    newup = upbow.clone().rotate_about_2d(theta, (0, 0))
    newdown = downbow.clone().rotate_about_2d(theta, (0, 0))

    # Create the regions
    colreg = Region.RegionNode(newcolup)
    colreg.matid = 'F'
    colhreg = Region.RegionNode(newcoldown)
    colhreg.matid = 'F'
    upreg = Region.RegionNode(newup)
    upreg.matid = 'H'
    downreg = Region.RegionNode(newdown)
    downreg.matid = 'H'

    # Add eval points to the bowtie filter parts
    upeval = Point.Point2d(newup.centroid())
    downeval = Point.Point2d(newdown.centroid())
    upeval.dodraw = True
    upeval.color = (255, 0, 255)
    upeval.radius = 3
    downeval.dodraw = True
    downeval.color = (255, 0, 255)
    downeval.radius = 3
    vis.registerthis(upeval)
    vis.registerthis(downeval)
    upreg.evalpoints.append((upeval[0], upeval[1], 0.5))
    downreg.evalpoints.append((downeval[0], downeval[1], 0.5))
    upreg.doeval = True
    downreg.doeval = True

    for b in [newcolup, newcoldown, newup, newdown]:
        #for b in [newcolup, newcoldown]:
        airregion -= b

    bodies.extend([newcolup, newcoldown, newup, newdown])
    regions.extend([colreg, colhreg, upreg, downreg])
    vis.register([newcolup, newcoldown, newup, newdown])
    # bodies.extend([newcolup, newcoldown])
    # regions.extend([colreg, colhreg])
    # vis.register([newcolup, newcoldown])

writer = partswriter.PartsWriter("./phantom2.parts", {'E': "PHANTOM", 'F': "COLLIMATOR", 'G': "AIR", 'H': "ALUM"})
writer.write("phantom_part", bodies, regions)

for b in bodies:
    print(b)
for r in regions:
    print(r)

checkval = 0
starttime = time.time()
print("Checking geometry (" + str(checkval) + ") points: ")
for i in range(checkval):
    nowtime = time.time()
    if nowtime - starttime > 1:
        starttime = nowtime
        print("{0:.2f}".format(100 * i/checkval) + "% complete")
    p = Point.Point2d((random.random() * 150 - 75, random.random() * 150 - 75))
    p.dodraw = True
    p.color = (255, 0, 0)
    counts = 0
    for r in regions:
        if p in r:
            counts += 1
            if counts == 1:
                p.color = (0, 255, 0)
            else:
                p.color = (255, 0, 0)
    if counts != 1:
        print("WARNING: Error point: " + str(p))
    vis.registerthis(p)

vis.launch()

regions = regions[1:-1]

for r in regions:
    if len(r.evalpoints) != 0:
        for body in r.get_all_bodies():
            body.fillcolor = (0, 255, 0, 1)

vis.launch()


