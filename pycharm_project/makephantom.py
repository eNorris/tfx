__author__ = 'Edward'

import math
from geo import rcc2d, box2d
import geo.region
import auxutil


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
    #bowtieregion = geo.region.Region(basebox) | topbox | botbox | bowtie1 | bowtie2 | bowtie3 | bowtie4 | bowtie5 | bowtie6 | bowtie7 | bowtie8 | bowtie9 | bowtie10
    bowtieregion = geo.region.Region(basebox) | topbox
    bowtieregion.matid = "H"
    bowtieregion.drawevals = True
    bowtieregion.evalpoints.extend([(46.5, 3.8), (46.5, -3.8), (44.5, 0)])

    phantom = rcc2d.Rcc2d(16.0)

    for r in [upcolreg, downcolreg, filterreg, bowtieregion]:
        r.rotate_about_2d(90, is_radians=False)

    air = auxutil.sliceregion(74, 360/16, is_radians=False)
    airbound = rcc2d.Rcc2d(74)
    airregion = air + airbound - phantom - upcolreg - downcolreg - filterreg - bowtieregion
    airregion.matid = "G"
    airregion.drawevals = True
    airregion.evalpoints.extend([(30, 0, 0)])
    #airregions = auxutil.automesh(airregion, (10, 10))

    regions.extend([upcolreg, downcolreg, filterreg, bowtieregion])
    regions.extend([airregion])

    return regions

