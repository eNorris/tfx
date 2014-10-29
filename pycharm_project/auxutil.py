__author__ = 'Edward'

from geo import rpp2d, raw2d
import geo.region
import geocheck
import math

from geo.region import Region
import geo.meshbnds
import geo.rcc2d


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


def automesh2(region, n=(10, 10), d=None):
    regions = []

    if not isinstance(region, geo.region.Region):
        raise TypeError("Type " + region.__class__.__name__ + " cannot be used, must be a geo.region.Region")

    # Get the bounds on the region
    #tmp_var = region.get_bounds()
    left, right, bottom, top, minz, maxz = region.get_bounds()  # TODO - Write the get_bounds() function

    # Calculate N and D based on the user input
    if d is None:
        nx = n[0]
        ny = n[1]
        dx = (right-left) / nx
        dy = (top-bottom) / ny
    else:
        dx = d[0]
        dy = d[1]
        nx = math.ceil((right-left)/dx)
        ny = math.ceil((top-bottom)/dy)



    for i in range(nx):
        for j in range(ny):

            # Build the ghost tree structure to represent the geometry
            # This can't be moved outside the loop because the ghost_tree is mutated by the acceptance building
            ghost_tree = region.ghostcopy()

            # Build the mesh element
            e = rpp2d.Rpp2d((left + i * dx, bottom + j * dy), (dx, dy), False)

            recursively_build_acceptance_tree(e, ghost_tree)

            accept = recursively_eval_tree(ghost_tree)
            #accept = acceptance(e, region)

            if accept == 1:
                regions.append(Region(e))
            elif accept == 0:
                regions.append(region + e)

    return regions


def recursively_build_acceptance_tree(e, ghosttree):
    if ghosttree.type == Region.BASE:
        ghosttree.left = acceptance(e, ghosttree.left)
    else:
        recursively_build_acceptance_tree(e, ghosttree.left)
        recursively_build_acceptance_tree(e, ghosttree.right)

def recursively_eval_tree(tree):
    if tree.type == Region.BASE:
        return tree.left
    if tree.type == Region.UNION:
        return max(tree.left, tree.right)
    elif tree.type == Region.SUBTRACT:
        return min(tree.left, -tree.right)
    elif tree.type == Region.INTERSECT:
        return min(tree.left, tree.right)
    else:
        print("ERROR: Unknown region type")

def acceptance(e, b):
    if b.__class__ == geo.rcc2d.Rcc2d:
        return acceptance_rcc2d(e, b)
    else:
        return acceptance_poly2d_body(e, b)

def acceptance_poly2d_body(element, body):
    """
    Returns:
     1 if the element is completely in the region,
    -1 if the element is completel outside the region, and
     0 if the element is partially in the region
    """
    completeaccept = True

    print("auxutil.accept_body: checking...")

    ecorners = element.get_corners()

    for c in ecorners:
        if not c in body:
            completeaccept = False
            break

    if completeaccept:
        return 1

    bcorners = body.get_corners()

    count = 0
    for i in range(-1, len(ecorners)-2):
        for j in range(-1, len(bcorners)-2):
            if intersects(ecorners[i], ecorners[i+1], bcorners[i], bcorners[i+1]):
                print("TRUE!")
                count += 1
                if count >= 2:
                    return 0

    #b = geo.meshbnds.Boundary(element.left, element.right, element.bottom, element.top)

    return -1

def acceptance_poly2d_region(element, region):
    """
    Returns:
     1 if the element is completely in the region,
    -1 if the element is completel outside the region, and
     0 if the element is partially in the region
    """
    completeaccept = True

    for c in element.get_corners():
        for b in region.get_all_bodies():
            if not c in b:
                completeaccept = False
                break
        if not completeaccept:
            break

    if completeaccept:
        return 1

    b = geo.meshbnds.Boundary(element.left, element.right, element.bottom, element.top)

    return -1

def acceptance_rcc2d(elem, bdy):
    """
    Returns:
     1 if the element is completely in the region,
    -1 if the element is completel outside the region, and
     0 if the element is partially in the region
    """
    xmin_dist = min(abs(elem.left - bdy.cx), abs(elem.right - bdy.cx))
    xmax_dist = max(abs(elem.left - bdy.cx), abs(elem.right - bdy.cx))

    ymin_dist = min(abs(elem.top - bdy.cy), abs(elem.bottom - bdy.cy))
    ymax_dist = max(abs(elem.top - bdy.cy), abs(elem.bottom - bdy.cy))

    if xmin_dist**2 + ymin_dist**2 >= bdy.r**2:
        return -1
    if xmax_dist**2 + ymax_dist**2 <= bdy.r**2:
        return 1
    return 0


def intersects(line1start, line1end, line2start, line2end):

    x1, y1 = line1start
    x2, y2 = line1end
    x3, y3 = line2start
    x4, y4 = line2end

    dx1 = x2-x1
    dx3 = x4-x3
    dy1 = y2-y1
    dy3 = y4-y3

    # The two equations are <dx1, dy1> t1 + <x1, y1>
    #                   and <dx3, dy3> t3 + <x3, y3>
    # Which yields
    # dx1 t1 + x1 = dx3 t3 + x3
    # dy1 t1 + y1 = dy3 t3 + y3
    #
    # Solving simultaneously for t1:

    denom = dx3*(dx1*dy3 - dy1)
    if denom < 1e-10:
        return False

    t1 = ((x3-x1)*dy3 + (y1-y3)*dx3) / denom

    if not 0 <= t1 <= 1:
        return False

    # Can't be a vertical line by the time we get here
    if dx3 < 1e-10:
        return False
    t3 = (dx1*t1 + x1 - x3)/dx3

    return 0 <= t3 <= 1