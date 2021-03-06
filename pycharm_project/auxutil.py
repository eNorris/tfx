__author__ = 'Edward'

from geo import rpp2d, raw2d, box2d
import geo.region
import math

from geo.region import Region
import geo.meshbnds
import geo.rcc2d
import util

import random


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


def automesh(region, n=(10, 10), d=None):
    regions = []

    if not isinstance(region, geo.region.Region):
        raise TypeError("Type " + region.__class__.__name__ + " cannot be used, must be a geo.region.Region")

    # Get the bounds on the region
    #tmp_var = region.get_bounds()
    left, right, bottom, top, minz, maxz = region.get_bounds()

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
                newregion = transform_rpp_to_box(e)  #Region(e)
                newregion.matid = region.matid
                add_scatter(newregion)
                regions.append(newregion)
            elif accept == 0:
                #newregion = region + e
                newregion = region + transform_rpp_to_box(e)
                newregion.matid = region.matid
                add_scatter(newregion)
                regions.append(newregion)

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
        return max(recursively_eval_tree(tree.left), recursively_eval_tree(tree.right))
    elif tree.type == Region.SUBTRACT:
        return min(recursively_eval_tree(tree.left), -recursively_eval_tree(tree.right))
    elif tree.type == Region.INTERSECT:
        return min(recursively_eval_tree(tree.left), recursively_eval_tree(tree.right))
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

    ecorners = element.get_corners()

    # This assumes the body is CONVEX and not an arbitrary polygon
    for c in ecorners:
        if not c in body:
            completeaccept = False
            break

    if completeaccept:
        return 1

    bcorners = body.get_corners()

    if not isinstance(element, geo.rpp2d.Rpp2d):
        raise Exception("Sorry, auxutil.accept_poly2d_body only works with Rpp2d bodies right now. Bummer.")

    for i in range(-1, len(bcorners)-1):
        x = bcorners[i][0]
        y = bcorners[i][1]
        dx = bcorners[i+1][0] - x
        dy = bcorners[i+1][1] - y

        # line is defined by   <dx, dy> t + <x, y>
        # First handle the edge cases of an orthogonal edge
        if abs(dx) < 1e-10:
            if not element.left < x < element.right:
                continue
        if abs(dy) < 1e-10:
            if not element.bottom < y < element.top:
                continue
        else:
            print(str(abs(dy)) + " > 1e-10")

        print("Here dy = " + str(dy))

        tmin, tmax = 0, 1

        if abs(dx) >= 1e-10:
            if dx > 0:
                txmin, txmax = (element.left - x)/dx, (element.right - x)/dx
            else:
                txmax, txmin = (element.left - x)/dx, (element.right - x)/dx

            tmin = max(tmin, txmin)
            tmax = min(tmax, txmax)

        if dy == 0:
            print(abs(dy))
            print(dy)
            print(abs(dy) < 1e-10)

        if abs(dy) >= 1e-10:
            if dy > 0:
                tymin, tymax = (element.bottom - y)/dy, (element.top - y)/dy
            else:
                tymax, tymin = (element.bottom - y)/dy, (element.top - y)/dy

            tmin = max(tmin, tymin)
            tmax = min(tmax, tymax)

        # If true, some part of the line segment was inside the RPP
        if tmin < tmax:
            return 0

    # If no intersections were found, reject
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


def sliceregion(radius, theta, is_radians=True):

    if not is_radians:
        theta *= math.pi / 180

    tant = math.tan(theta)
    cost2 = math.cos(theta/2)
    sint2 = math.sin(theta/2)

    slicebody = geo.raw2d.Raw2d(refpoint=(-radius * sint2, radius * cost2),
                                v1=(radius * sint2, -radius * cost2),
                                v2=(radius * cost2 * tant, radius * sint2 * tant))

    return geo.region.Region(slicebody)

def transform_rpp_to_box(input):
    box = geo.region.Region(box2d.Box2d((input.left, input.bottom), (0, input.top-input.bottom), (input.right-input.left, 0), False))
    #box.evalpoints = input.evalpoints
    return box


def add_scatter(region):
    # TODO All primitives should have a centroid that is naively accepted if the arg is a BASE
    left, right, bottom, top, zmin, zmax = region.get_bounds()

    fires = 0
    TRIES = 10000
    accepts = []

    while fires < TRIES and len(accepts) < 1000:
        fires += 1
        x, y = left + random.random() * (right - left), bottom + random.random() * (top - bottom)
        if (x, y) in region:
            accepts.append([x, y])

    if len(accepts) == 0:
        raise Exception("auxutil::add_scatter(): Failed to find a single scatter point after " + str(TRIES) + " tries!")

    xbar = sum(pt[0] for pt in accepts) / len(accepts)
    ybar = sum(pt[1] for pt in accepts) / len(accepts)

    # Try to find the average center, but otherwise, for example, if there's a hole, just take one at random
    if (xbar, ybar) in region:
        region.evalpoints.append([xbar, ybar, 0.5])
    else:
        region.evalpoints.append([accepts[0][0], accepts[0][1], 0.5])


def rotate_regions(regionlist, theta, aboutpt=(0, 0), is_radians=True):
    bodies = set()
    for r in regionlist:
        bodies.update(r.get_all_bodies())
    for b in bodies:
        b.rotate_about_2d(theta, aboutpt, is_radians)

    for r in regionlist:
        r.evalpoints = [util.get_rotated_about_2d(x, theta, aboutpt, is_radians) for x in r.evalpoints]