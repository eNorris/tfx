__author__ = 'Edward'

import math

import Rcc2d
import Rpp2d
import Box2d
import Raw2d
import Visualizer
import Region
import partswriter

def makeparts():

    # Problem constants
    srcpts = 16
    beamangle = math.radians(55)

    bodies = []
    regions = []
    vis = Visualizer.Visualizer()

    phantom = Rcc2d.Rcc2d(16.0)
    air = Rpp2d.Rpp2d((0, 0), (150, 150))
    airregion = Region.RegionNode(air) - phantom
    airregion.matid = 'G'
    bodies.extend([phantom, air])
    regions.append(airregion)
    vis.register([phantom, air])

    # Mesh the phantom and add the regions
    width = 32
    height = 32
    xdivs = 32
    ydivs = 32
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
                bodies.append(r)
                corespondingregion = Region.RegionNode(phantom)
                corespondingregion += r
                corespondingregion.doeval = True
                corespondingregion.matid = 'E'
                corespondingregion.evalpoint = (r.cx, r.cy, .5)
                regions.append(corespondingregion)

    # Add the collimators and their air centers
    colwidth = 50 * math.tan(math.pi / srcpts)
    holewidth = 4 * math.tan(beamangle / 2)
    if holewidth > holewidth:
        print("WARNING: Collimator hole exceeds collimator size!")

    upcollimator = Box2d.Box2d((51.5, holewidth), (-1.5, 0), (0, (colwidth-holewidth)/2))
    upcollimator.color = (255, 0, 0)
    downcollimator = Box2d.Box2d((51.5, -holewidth), (-1.5, 0), (0, -(colwidth-holewidth)/2))
    downcollimator.color = (0, 255, 0)
    upbow = Raw2d.Raw2d((44, 0), (0, 5), (5, 5))
    downbow = Raw2d.Raw2d((44, 0), (0, -5), (5, -5))
    for i in range(srcpts):
        theta = i * 2 * math.pi / srcpts

        # Create the bodies
        newcolup = upcollimator.clone().rotate_about(theta)
        newcoldown = downcollimator.clone().rotate_about(theta)
        newup = upbow.clone().rotate_about(theta, (0, 0))
        newdown = downbow.clone().rotate_about(theta, (0, 0))

        # Create the regions
        colreg = Region.RegionNode(newcolup)
        colreg.matid = 'F'
        colhreg = Region.RegionNode(newcoldown)
        colhreg.matid = 'F'
        upreg = Region.RegionNode(newup)
        upreg.matid = 'H'
        downreg = Region.RegionNode(newdown)
        downreg.matid = 'H'

        for b in [newcolup, newcoldown, newup, newdown]:
            airregion -= b

        bodies.extend([newcolup, newcoldown, newup, newdown])
        regions.extend([colreg, colhreg, upreg, downreg])
        vis.register([newcolup, newcoldown, newup, newdown])

    writer = partswriter.PartsWriter("./phantom2.parts", {'E':"PHANTOM", 'F':"COLLIMATOR", 'G':"AIR", 'H':"ALUM"})
    writer.write("phantom_part", bodies, regions)

    for b in bodies:
        print(b)
    for r in regions:
        print(r)

    vis.launch()