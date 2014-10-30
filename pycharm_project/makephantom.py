__author__ = 'Edward'

import math
import Point
from geo import rcc2d, rpp2d, box2d, raw2d
from visualizer import pygamevisualizer
import geo.region
import auxutil

def makephantom():

    regions = []
    phantom = rcc2d.Rcc2d(16.0)

    width = 32.0
    height = 32.0
    xdivs = 31
    ydivs = 31
    bot = -16.0
    left = -16.0

    dx = width / xdivs
    dy = height / ydivs

    for i in range(xdivs):
        for j in range(ydivs):
            r = rpp2d.Rpp2d([left + i * dx, bot + j * dy], [dx, dy], False)
            #neary, nearx = None, None

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
                corespondingregion = geo.region.Region(phantom)
                corespondingregion += r
                corespondingregion.doeval = True
                corespondingregion.matid = 'E'

                #evalpt = (0, 0, 0)
                if r.cx**2 + r.cy**2 <= phantom.r**2:
                    #print(str(r.cx**2) + " + " + str(r.cy) + " < " + str())
                    evalpt = (r.cx, r.cy, .5)
                else:
                    if r.cx > 0 and r.cy > 0:
                        evalpt = (r.left+.0001, r.bottom+.0001, .5)
                    elif r.cy < 0 < r.cx:
                        evalpt = (r.left+.0001, r.top-.0001, .5)
                    elif r.cx < 0 < r.cy:
                        evalpt = (r.right-.0001, r.bottom+.0001, .5)
                    else:
                        evalpt = (r.right-.0001, r.top-.0001, .5)
                corespondingregion.evalpoints.append((evalpt[0], evalpt[1], evalpt[2]))
                regions.append(corespondingregion)
    return regions


def makeslice():

    srcpts = 16
    beamangle = math.radians(55)

    regions = []

    # Add the collimators and their air centers
    if srcpts < 4:
        colwidth = 10.0
    else:
        colwidth = 50 * math.tan(math.pi / srcpts)
    holewidth = 4 * math.tan(beamangle / 2)
    if holewidth > colwidth:
        print("WARNING: Collimator hole exceeds collimator size!")

    # Define the collimator regions
    upcol = box2d.Box2d((50, holewidth), (3, 0), (0, (colwidth-holewidth)), False)
    upcolreg = geo.region.Region(upcol)
    upcolreg.matid = "F"
    upcolreg.drawevals = True
    upcolreg.evalpoints.append((51.5, (colwidth + holewidth)/2))

    downcol = box2d.Box2d((50, -holewidth), (3, 0), (0, -(colwidth-holewidth)), False)
    downcolreg = geo.region.Region(downcol)
    downcolreg.matid = "F"
    downcolreg.drawevals = True
    downcolreg.evalpoints.append((51.5, -(colwidth + holewidth)/2))

    # Define the flat filter region
    flatfilter = box2d.Box2d((49.55, 0), (.1, 0), (0, 10), True)
    filterreg = geo.region.Region(flatfilter)
    filterreg.matid = "H"
    filterreg.drawevals = True
    filterreg.evalpoints.append((49.55, 0))

    # Define the bowtie region
    basebox = box2d.Box2d((44.5, 0), (1, 0), (0, 10))
    topbox = box2d.Box2d((47, 3.725), (4, 0), (0, 2.55))
    botbox = box2d.Box2d((47, -3.725), (4, 0), (0, 2.55))
    bowtie1 = auxutil.bowtie_triangle((45, 2.45), (45, 0), (45.5, .919))
    bowtie2 = auxutil.bowtie_triangle((45, 2.45), (45.5, .919), (46, 1.302))
    bowtie3 = auxutil.bowtie_triangle((45, 2.45), (46, 1.302), (47, 1.808))
    bowtie4 = auxutil.bowtie_triangle((45, 2.45), (47, 1.808), (48, 2.162))
    bowtie5 = auxutil.bowtie_triangle((45, 2.45), (48, 2.162), (49, 2.45))
    bowtie6 = auxutil.fliptie(bowtie1)
    bowtie7 = auxutil.fliptie(bowtie2)
    bowtie8 = auxutil.fliptie(bowtie3)
    bowtie9 = auxutil.fliptie(bowtie4)
    bowtie10 = auxutil.fliptie(bowtie5)
    bowtieregion = geo.region.Region(basebox) | topbox | botbox | bowtie1 | bowtie2 | bowtie3 | bowtie4 | bowtie5 | bowtie6 | bowtie7 | bowtie8 | bowtie9 | bowtie10
    bowtieregion.matid = "H"
    bowtieregion.drawevals = True
    bowtieregion.evalpoints.extend([(46.5, 3.8), (46.5, -3.8), (44.5, 0)])

    theta = 2 * math.pi / srcpts

    phantom = rcc2d.Rcc2d(16.0)
    uppervoid = box2d.Box2d((0, 0), (200, 0), (0, 100), provide_center=False)
    lowervoid = box2d.Box2d((0, 0), (100, 0), (0, 200), provide_center=False)
    uppervoid.rotate_about_2d(theta/2)
    lowervoid.rotate_about_2d(-theta/2 - math.pi/2)
    uppervoid.translate([uppervoid.vec1[0] * -.5, uppervoid.vec1[1] * -.5])
    lowervoid.translate([lowervoid.vec2[0] * -.5, lowervoid.vec2[1] * -.5])
    air = rcc2d.Rcc2d(74.0)
    airregion = geo.region.Region(air) - phantom - uppervoid - lowervoid - upcolreg - downcolreg - filterreg - bowtieregion
    airregion.matid = "G"
    airregion.drawevals = True
    airregion.evalpoints.extend([(30, 0, 0)])

    regions.extend([upcolreg, downcolreg, filterreg, bowtieregion, airregion])

    return regions

def makeslice2():

    srcpts = 16
    beamangle = math.radians(55)

    regions = []

    # Add the collimators and their air centers
    if srcpts < 4:
        colwidth = 10.0
    else:
        colwidth = 50 * math.tan(math.pi / srcpts)
    holewidth = 4 * math.tan(beamangle / 2)
    if holewidth > colwidth:
        print("WARNING: Collimator hole exceeds collimator size!")

    # Define the collimator regions
    upcol = box2d.Box2d((50, holewidth), (3, 0), (0, (colwidth-holewidth)), False)
    upcolreg = geo.region.Region(upcol)
    upcolreg.matid = "F"
    upcolreg.drawevals = True
    upcolreg.evalpoints.append((51.5, (colwidth + holewidth)/2))

    downcol = box2d.Box2d((50, -holewidth), (3, 0), (0, -(colwidth-holewidth)), False)
    downcolreg = geo.region.Region(downcol)
    downcolreg.matid = "F"
    downcolreg.drawevals = True
    downcolreg.evalpoints.append((51.5, -(colwidth + holewidth)/2))

    # Define the flat filter region
    flatfilter = box2d.Box2d((49.55, 0), (.1, 0), (0, 10), True)
    filterreg = geo.region.Region(flatfilter)
    filterreg.matid = "H"
    filterreg.drawevals = True
    filterreg.evalpoints.append((49.55, 0))

    # Define the bowtie region
    basebox = box2d.Box2d((44.5, 0), (1, 0), (0, 10))
    topbox = box2d.Box2d((47, 3.725), (4, 0), (0, 2.55))
    botbox = box2d.Box2d((47, -3.725), (4, 0), (0, 2.55))
    bowtie1 = auxutil.bowtie_triangle((45, 2.45), (45, 0), (45.5, .919))
    bowtie2 = auxutil.bowtie_triangle((45, 2.45), (45.5, .919), (46, 1.302))
    bowtie3 = auxutil.bowtie_triangle((45, 2.45), (46, 1.302), (47, 1.808))
    bowtie4 = auxutil.bowtie_triangle((45, 2.45), (47, 1.808), (48, 2.162))
    bowtie5 = auxutil.bowtie_triangle((45, 2.45), (48, 2.162), (49, 2.45))
    bowtie6 = auxutil.fliptie(bowtie1)
    bowtie7 = auxutil.fliptie(bowtie2)
    bowtie8 = auxutil.fliptie(bowtie3)
    bowtie9 = auxutil.fliptie(bowtie4)
    bowtie10 = auxutil.fliptie(bowtie5)
    bowtieregion = geo.region.Region(basebox) | topbox | botbox | bowtie1 | bowtie2 | bowtie3 | bowtie4 | bowtie5 | bowtie6 | bowtie7 | bowtie8 | bowtie9 | bowtie10
    bowtieregion.matid = "H"
    bowtieregion.drawevals = True
    bowtieregion.evalpoints.extend([(46.5, 3.8), (46.5, -3.8), (44.5, 0)])

    theta = 2 * math.pi / srcpts

    phantom = rcc2d.Rcc2d(16.0)
    #uppervoid = box2d.Box2d((0, 0), (200, 0), (0, 100), provide_center=False)
    #lowervoid = box2d.Box2d((0, 0), (100, 0), (0, 200), provide_center=False)
    #uppervoid.rotate_about_2d(theta/2)
    #lowervoid.rotate_about_2d(-theta/2 - math.pi/2)
    #uppervoid.translate([uppervoid.vec1[0] * -.5, uppervoid.vec1[1] * -.5])
    #lowervoid.translate([lowervoid.vec2[0] * -.5, lowervoid.vec2[1] * -.5])
    #air = rcc2d.Rcc2d(74.0)

    # TODO - finish this
    for r in [upcolreg, downcolreg, filterreg, bowtieregion]:
        r.rotate_about_2d(90, is_radians=False)

    air = auxutil.sliceregion(74, 360/16, is_radians=False)
    airregion = air - phantom - upcolreg - downcolreg - filterreg - bowtieregion
    airregion.matid = "G"
    airregion.drawevals = True
    airregion.evalpoints.extend([(30, 0, 0)])
    airregions = auxutil.automesh2(airregion, (10, 10))

    regions.extend([upcolreg, downcolreg, filterreg, bowtieregion])
    regions.extend(airregions)

    return regions


def makeoutter():
    regions = []
    bounds = rpp2d.Rpp2d(dims=(150, 150))
    inner = rcc2d.Rcc2d(74.0)
    r = geo.region.Region(bounds) - inner
    r.matid = "G"
    regions.append(r)
    return regions

def makeallgeo():
    # Problem constants
    srcpts = 16
    beamangle = math.radians(55)

    bodies = []
    regions = []
    vis = pygamevisualizer.Visualizer()

    phantom = rcc2d.Rcc2d(16.0)
    air = rpp2d.Rpp2d((0, 0), (150, 150))
    airregion = geo.region.Region(air) - phantom
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
            r = rpp2d.Rpp2d([left + i * dx, bot + j * dy], [dx, dy], False)
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
                corespondingregion = geo.region.Region(phantom)
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

    #upcollimator = box2d.Box2d((50, holewidth), (3, 0), (0, (colwidth-holewidth)), False)
    #downcollimator = box2d.Box2d((50, -holewidth), (3, 0), (0, -(colwidth-holewidth)), False)
    #upbow = raw2d.Raw2d((44, 5), (5, 0), (0, -5))
    #downbow = raw2d.Raw2d((44, -5), (5, 0), (0, 5))

    # Define the collimator regions
    upcol = box2d.Box2d((50, holewidth), (3, 0), (0, (colwidth-holewidth)), False)
    upcolreg = geo.region.Region(upcol)
    upcolreg.matid = "F"
    upcolreg.drawevals = True
    upcolreg.evalpoints.append((51.5, (colwidth + holewidth)/2))

    downcol = box2d.Box2d((50, -holewidth), (3, 0), (0, -(colwidth-holewidth)), False)
    downcolreg = geo.region.Region(downcol)
    downcolreg.matid = "F"
    downcolreg.drawevals = True
    downcolreg.evalpoints.append((-51.5, (colwidth + holewidth)/2))

    # Define the flat filter region
    flatfilter = box2d.Box2d((49.55, 0), (.1, 0), (0, 10), True)
    filterreg = geo.region.Region(flatfilter)
    filterreg.matid = "H"
    filterreg.drawevals = True
    filterreg.evalpoints.append((49.55, 0))

    # Define the bowtie region
    basebox = box2d.Box2d((44.5, 0), (1, 0), (0, 10))
    topbox = box2d.Box2d((47, 3.725), (4, 0), (0, 2.55))
    botbox = box2d.Box2d((47, -3.725), (4, 0), (0, 2.55))
    bowtie1 = auxutil.bowtie_triangle((45, 2.45), (45, 0), (45.5, .919))
    bowtie2 = auxutil.bowtie_triangle((45, 2.45), (45.5, .919), (46, 1.302))
    bowtie3 = auxutil.bowtie_triangle((45, 2.45), (46, 1.302), (47, 1.808))
    bowtie4 = auxutil.bowtie_triangle((45, 2.45), (47, 1.808), (48, 2.162))
    bowtie5 = auxutil.bowtie_triangle((45, 2.45), (48, 2.162), (49, 2.45))
    bowtie6 = auxutil.fliptie(bowtie1)
    bowtie7 = auxutil.fliptie(bowtie2)
    bowtie8 = auxutil.fliptie(bowtie3)
    bowtie9 = auxutil.fliptie(bowtie4)
    bowtie10 = auxutil.fliptie(bowtie5)
    bowtieregion = geo.region.Region(basebox) | topbox | botbox | bowtie1 | bowtie2 | bowtie3 | bowtie4 | bowtie5 | bowtie6 | bowtie7 | bowtie8 | bowtie9 | bowtie10
    bowtieregion.matid = "H"
    bowtieregion.drawevals = True
    bowtieregion.evalpoints.extend([(46.5, 3.8), (46.5, -3.8), (44.5, 0)])

    for i in range(srcpts):
        # Calculate the angle
        theta = i * 2 * math.pi / srcpts

        # Add a new eval point in the air region
        newevalpt = Point.Point2d((30 * math.cos(theta), 30 * math.sin(theta)))
        newevalpt.dodraw = True
        newevalpt.color = (255, 0, 255)
        newevalpt.radius = 3
        vis.registerthis(newevalpt)
        airregion.evalpoints.append((newevalpt[0], newevalpt[1], 0.5))

        newupcolreg = upcolreg.get_rotated_about_2d(theta, (0, 0), True)
        newdowncolreg = downcolreg.get_rotated_about_2d(theta, (0, 0), True)
        newfilterreg = filterreg.get_rotated_about_2d(theta, (0, 0), True)
        newbowtiereg = bowtieregion.get_rotated_about_2d(theta, (0, 0), True)

        for region in [newupcolreg, newdowncolreg, newfilterreg, newbowtiereg]:
            for b in region.get_all_bodies():
                vis.register(b)
                bodies.append(b)
                airregion -= b

        for region in [newupcolreg, newdowncolreg, newfilterreg, newbowtiereg]:
            regions.append(region)
            vis.register(region)
    return regions