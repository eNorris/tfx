__author__ = 'Edward'

import math

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

def makeparts():

    # Problem constants
    srcpts = 16
    beamangle = math.radians(55)

    bodies = []
    regions = []
    vis = Visualizer.Visualizer()

    phantom = Rcc2d.Rcc2d(16.0)
    phantomregion = Region.RegionNode(phantom)
    phantomregion.matid = 'E'
    #halfwidth = math.sqrt(math.pi) * 16.0 / 2.0
    #print("halfwidth = " + str(halfwidth))
    #phantom = Rpp2d.Rpp2d((0, 0), (halfwidth, halfwidth))
    air = Rpp2d.Rpp2d((0, 0), (150, 150))
    airregion = Region.RegionNode(air) - phantom
    airregion.matid = 'G'
    bodies.extend([phantom, air])
    regions.extend([phantomregion, airregion])
    vis.register([phantom, air])

    # Mesh the phantom and add the regions

    width = 32
    height = 32
    xdivs = 8
    ydivs = 8
    bot = -16
    left = -16

    dx = width / xdivs
    dy = height / ydivs

    '''
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

                evalpt = (0, 0, 0)
                if r.cx**2 + r.cy*2 <= phantom.r**2:
                    evalpt = (r.cx, r.cy, .5)
                else:
                    if r.cx > 0 and r.cy > 0:
                        evalpt = (r.left, r.bottom, .5)
                    elif r.cx > 0 and r.cy < 0:
                        evalpt = (r.left, r.top, .5)
                    elif r.cx < 0 and r.cy > 0:
                        evalpt = (r.right, r.bottom, .5)
                    else:
                        evalpt = (r.right, r.top, .5)
                corespondingregion.evalpoint = (evalpt[0], evalpt[1], evalpt[2])
                regions.append(corespondingregion)
    '''

    # Add the collimators and their air centers
    if srcpts < 4:
        colwidth = 10.0
    else:
        colwidth = 50 * math.tan(math.pi / srcpts)
    holewidth = 4 * math.tan(beamangle / 2)
    if holewidth > colwidth:
        print("WARNING: Collimator hole exceeds collimator size!")

    upcollimator = Box2d.Box2d((50, holewidth), (3, 0), (0, (colwidth-holewidth)/2), False)
    #upcollimator.color = (255, 0, 0)
    downcollimator = Box2d.Box2d((50, -holewidth), (3, 0), (0, -(colwidth-holewidth)/2), False)
    #downcollimator.color = (0, 255, 0)
    upbow = Raw2d.Raw2d((44, 5), (5, 0), (0, -5))
    downbow = Raw2d.Raw2d((44, -5), (5, 0), (0, 5))
    #upbow.color = (0, 0, 100)
    #downbow.color = (0, 0, 100)
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
            #for b in [newcolup, newcoldown]:
            airregion -= b

        bodies.extend([newcolup, newcoldown, newup, newdown])
        regions.extend([colreg, colhreg, upreg, downreg])
        vis.register([newcolup, newcoldown, newup, newdown])
        # bodies.extend([newcolup, newcoldown])
        # regions.extend([colreg, colhreg])
        # vis.register([newcolup, newcoldown])

    writer = partswriter.PartsWriter("./phantom2.parts", {'E':"PHANTOM", 'F':"COLLIMATOR", 'G':"AIR", 'H':"ALUM"})
    writer.write("phantom_part", bodies, regions)

    for b in bodies:
        print(b)
    for r in regions:
        print(r)

    checkval = 5000
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