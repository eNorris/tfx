__author__ = 'Edward'

import math
from geo import rcc2d, box2d
import geo.region
import auxutil


def makeslice2d():
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
    upcolreg.evalpoints.append((51.5, (colwidth + holewidth)/2, 0.5))

    downcol = box2d.Box2d((50, -holewidth), (3, 0), (0, -(colwidth-holewidth)), False)
    downcolreg = geo.region.Region(downcol)
    downcolreg.matid = "F"
    downcolreg.drawevals = True
    downcolreg.evalpoints.append((51.5, -(colwidth + holewidth)/2, 0.5))

    # Define the flat filter region
    flatfilter = box2d.Box2d((49.55, 0), (.1, 0), (0, 10), True)
    filterreg = geo.region.Region(flatfilter)
    filterreg.matid = "H"
    filterreg.drawevals = True
    filterreg.evalpoints.append((49.55, 0, 0.5))

    # Define the bowtie region
    bowtiebox = box2d.Box2d((44.0, -5.0), (5.0, 0.0), (0.0, 10.0), False)
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

    bt1region = geo.region.Region(basebox)
    bt2region = geo.region.Region(topbox)
    bt3region = geo.region.Region(botbox)
    bt4region = geo.region.Region(bowtie5)
    bt5region = geo.region.Region(bowtie4) - bowtie5
    bt6region = geo.region.Region(bowtie3) - bowtie4 - bowtie5
    bt7region = geo.region.Region(bowtie2) - bowtie3 - bowtie4 - bowtie5
    bt8region = geo.region.Region(bowtie1) - bowtie2 - bowtie3 - bowtie4 - bowtie5
    bt9region = geo.region.Region(bowtie6) - bowtie7 - bowtie8 - bowtie9 - bowtie10
    bt10region = geo.region.Region(bowtie7) - bowtie8 - bowtie9 - bowtie10
    bt11region = geo.region.Region(bowtie8) - bowtie9 - bowtie10
    bt12region = geo.region.Region(bowtie9) - bowtie10
    bt13region = geo.region.Region(bowtie10)
    btgapregion = geo.region.Region(bowtiebox) - basebox - topbox - botbox - bowtie1 - bowtie2 - bowtie3 - bowtie4 - \
        bowtie5 - bowtie6 - bowtie7 - bowtie8 - bowtie9 - bowtie10

    for btr in [bt1region, bt2region, bt3region, bt4region, bt5region, bt6region, bt7region, bt8region, bt9region,
                bt10region, bt11region, bt12region, bt13region]:
        btr.matid = "H"
        btr.drawevals = True
        auxutil.add_scatter(btr)

    btgapregion.matid = "G"
    btgapregion.drawevals = True
    auxutil.add_scatter(btgapregion)

    bowtieregion = geo.region.Region(bowtiebox)
    bowtieregion.matid = "G"
    auxutil.add_scatter(bowtieregion)

    phantom = rcc2d.Rcc2d(16.0)

    # These have to be rotated together since they share bodies
    auxutil.rotate_regions([bt1region, bt2region, bt3region, bt4region, bt5region, bt6region, bt7region, bt8region,
                            bt9region, bt10region, bt11region, bt12region, bt13region, btgapregion], 90, is_radians=False)

    for r in [upcolreg, downcolreg, filterreg]:
        # This is okay since none of these regions mutually share bodies
        r.rotate_about_2d(90, is_radians=False)

    air = auxutil.sliceregion(74, 360/16, is_radians=False)
    airbound = rcc2d.Rcc2d(74)
    airregion = air + airbound - phantom - upcolreg - downcolreg - filterreg - bowtiebox
    airregion.matid = "G"
    airregion.drawevals = True
    airregion.evalpoints.extend([(0, 30, 0.5)])
    airregions = auxutil.automesh(airregion, (4, 8))

    #regions.extend([upcolreg, downcolreg, filterreg, bowtieregion])
    regions.extend([upcolreg, downcolreg, filterreg, bt1region, bt2region, bt3region, bt4region, bt5region, bt6region,
                    bt7region, bt8region, bt9region, bt10region, bt11region, bt12region, bt13region, btgapregion])
    # Change back to meshed version later!
    regions.extend(airregions)


    return regions


def makeslice3d():
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

    outcol = box2d.Box2d((50, 5), (10, 0), (0, -10), False, comment="Collimator outter bounds")
    incol = box2d.Box2d((50, 2.08227), (5, 0), (0, -4.16454), False, comment="Collimator hole")

    incolreg = geo.region.Region(incol)
    incolreg.matid = "G"
    incolreg.drawevals = True
    incolreg.evalpoints.append((53, 0, 0.5))

    outcolreg = geo.region.Region(outcol)-incol
    outcolreg.matid = "F"
    outcolreg.drawevals = True
    outcolreg.evalpoints.append((57, 0, 0.5))

    # Define the flat filter region
    flatfilter = box2d.Box2d((49.55, 0), (.1, 0), (0, 10), True, comment="Flat filter")
    filterreg = geo.region.Region(flatfilter)
    filterreg.matid = "H"
    filterreg.drawevals = True
    filterreg.evalpoints.append((49.55, 0, 0.5))

    # Define the bowtie region
    bowtiebox = box2d.Box2d((44.0, -5.0), (5.0, 0.0), (0.0, 10.0), False, comment="Bowtie bounding box")
    basebox = box2d.Box2d((44.5, 0), (1, 0), (0, 10), comment="Bowtie back piece")
    topbox = box2d.Box2d((47, 3.725), (4, 0), (0, 2.55), comment="Bowtie left part")
    botbox = box2d.Box2d((47, -3.725), (4, 0), (0, 2.55), comment="Bowtie right part")
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
#
    bt1region = geo.region.Region(basebox)
    bt2region = geo.region.Region(topbox)
    bt3region = geo.region.Region(botbox)
    bt4region = geo.region.Region(bowtie5)
    bt5region = geo.region.Region(bowtie4) - bowtie5
    bt6region = geo.region.Region(bowtie3) - bowtie4 - bowtie5
    bt7region = geo.region.Region(bowtie2) - bowtie3 - bowtie4 - bowtie5
    bt8region = geo.region.Region(bowtie1) - bowtie2 - bowtie3 - bowtie4 - bowtie5
    bt9region = geo.region.Region(bowtie6) - bowtie7 - bowtie8 - bowtie9 - bowtie10
    bt10region = geo.region.Region(bowtie7) - bowtie8 - bowtie9 - bowtie10
    bt11region = geo.region.Region(bowtie8) - bowtie9 - bowtie10
    bt12region = geo.region.Region(bowtie9) - bowtie10
    bt13region = geo.region.Region(bowtie10)
    btgapregion = geo.region.Region(bowtiebox) - basebox - topbox - botbox - bowtie1 - bowtie2 - bowtie3 - bowtie4 - \
        bowtie5 - bowtie6 - bowtie7 - bowtie8 - bowtie9 - bowtie10
#
    for btr in [bt1region, bt2region, bt3region, bt4region, bt5region, bt6region, bt7region, bt8region, bt9region,
                bt10region, bt11region, bt12region, bt13region]:
        btr.matid = "H"
        btr.drawevals = True
        auxutil.add_scatter(btr)

    btgapregion.matid = "G"
    btgapregion.drawevals = True
    auxutil.add_scatter(btgapregion)

    bowtieregion = geo.region.Region(bowtiebox)
    bowtieregion.matid = "G"
    auxutil.add_scatter(bowtieregion)

    phantom = rcc2d.Rcc2d(16.0)

    # These have to be rotated together since they share bodies
    auxutil.rotate_regions([bt1region, bt2region, bt3region, bt4region, bt5region, bt6region, bt7region, bt8region,
                            bt9region, bt10region, bt11region, bt12region, bt13region, btgapregion], 90, is_radians=False)

    auxutil.rotate_regions([outcolreg, incolreg, filterreg], 90, is_radians=False)
    #for r in [outcolreg, incolreg, filterreg]:
    #    # This is okay since none of these regions mutually share bodies
    #    r.rotate_about_2d(90, is_radians=False)

    air = auxutil.sliceregion(74, 360/16, is_radians=False)
    airbound = rcc2d.Rcc2d(74)
    airregion = air + airbound - phantom - outcol - filterreg - bowtiebox
    airregion.matid = "G"
    airregion.drawevals = True
    airregion.evalpoints.extend([(0, 30, 0.5)])
    airregions = auxutil.automesh(airregion, (4, 8))

    #regions.extend([upcolreg, downcolreg, filterreg, bowtieregion])
    regions.extend([incolreg, outcolreg, filterreg, bt1region, bt2region, bt3region, bt4region, bt5region, bt6region,
                    bt7region, bt8region, bt9region, bt10region, bt11region, bt12region, bt13region, btgapregion])
    # Change back to meshed version later!
    regions.extend(airregions)

    return regions
