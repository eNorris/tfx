__author__ = 'Edward'

from geo import rpp2d, raw2d
import geo.region
import geocheck
import math


def bowtie_triangle(pt, a, b):
    """
    pt is the corner of the right triangle
    a and b are points on the hypotenuse
    """
    if abs(b[0] - a[0]) < 1e-10 or abs(b[1] - a[1]) < 1e-10:
        print("WARNING: Illegal bowtie part!")
        return None
    else:
        m = (b[1] - a[1]) / (b[0] - a[0])
        v1 = (0, m * (pt[0] - a[0]) + a[1] - pt[1])
        v2 = ((pt[1] - a[1])/m + a[0] - pt[0], 0)
        return raw2d.Raw2d(pt, v1, v2)


def fliptie(tie):
    return raw2d.Raw2d((tie.px, -tie.py), (tie.vec1[0], -tie.vec1[1]), (tie.vec2[0], -tie.vec2[1]))


def automesh(region, size):
    print("WARNING: automesh isn't very smart: \n" +
          "\tautomesh is not curvature safe!\n" +
          "\tautomesh does not do corner point checking!\n" +
          "\tautomesh does not do surface error detection!\n" +
          "\tautomesh does not do disjoint detection!\n" +
          "so make sure you double check the automeshed geometry and correct as necessary!")

    regions = []
    left = 0.234
    bottom = -15.0
    height = 30.0
    width = 75.0
    #xdivs = 10
    #ydivs = 10
    #dx = width/xdivs
    #dy = height/ydivs

    dx = size
    dy = size
    xdivs = math.ceil(width/dx)
    ydivs = math.ceil(height/dy)

    for i in range(xdivs):
        for j in range(ydivs):
            #if i % 100 == 0 or j % 100 == 0:
            #print("i = " + str(i) + ", j = " + str(j))
            testbox = rpp2d.Rpp2d((left + dx * i, bottom + dy * j), (dx, dy), False)
            corners = testbox.get_corners()
            accept = False
            for c in corners:
                if c in region:
                    accept = True
            if not accept:
                continue

            # TODO - simplify this
            newregion = None

            allcornersin = True
            for c in corners:
                if not c in region:
                    allcornersin = False
            if allcornersin:
                newregion = geo.region.Region(testbox)
            else:
                newregion = region + testbox

            newregion.doeval = True
            newregion.drawevals = True
            #evalpt = (0, 0, .5)

            if (testbox.cx, testbox.cy) in region:
                evalpt = (testbox.cx, testbox.cy, .5)
            else:
                acceptedpts = 0
                totalx, totaly = 0, 0
                tries = 0
                # Give up after 1000 attempts
                while acceptedpts < 10 and tries < 1000:
                    tries += 1
                    #print(str(acceptedpts) + " accepted => FIRE!")
                    pt = geocheck.rand_pt_in_rect(*testbox.get_edges())
                    if pt in region:
                        totalx += pt[0]
                        totaly += pt[1]
                        acceptedpts += 1
                evalpt = (totalx/10, totaly/10, .5)

            newregion.evalpoints.append(evalpt)
            regions.append(newregion)

    return regions