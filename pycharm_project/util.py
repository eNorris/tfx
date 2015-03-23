__author__ = 'Edward'

import math
import random

def get_rotated_about_2d(pt, theta, aboutpt=(0, 0), is_radians=True):

    if not is_radians:
        theta *= math.pi / 180

    result = [pt[0], pt[1]]

    posvec = [aboutpt[0] - result[0], aboutpt[1] - result[1]]
    dx = posvec[0] * math.cos(theta) - posvec[1] * math.sin(theta)
    dy = posvec[0] * math.sin(theta) + posvec[1] * math.cos(theta)
    result[0] += posvec[0] - dx
    result[1] += posvec[1] - dy

    # Append all other dimensions unmodified
    result.extend(pt[2:])

    return result


def calc_volume(region, points=1000):

    if points <= 0:
        print("WARNING: Illegal number of points (" + str(points) + ") must be > 0. Setting vol to 1.0")
        return 1.0

    xmin, xmax, ymin, ymax, zmin, zmax = region.get_bounds()
    boxvol = (xmax - xmin) * (ymax - ymin) * (zmax-zmin)
    if boxvol < 1e-10:
        print("WARNING: Very small bounding volume detected: " + str(region) + " vol = " + str(boxvol))

    hits = 0
    for i in range(points):
        x = (xmax - xmin) * random.random() + xmin
        y = (ymax - ymin) * random.random() + ymin
        z = (zmax - zmin) * random.random() + zmin
        if (x, y, z) in region:
            hits += 1

    if hits/points * boxvol < 1e-6:
        print("WARNING: Very small volume: " + str(region.comment) + " vol = " + str(hits/points * boxvol))
        return 1.0e-6

    return hits/points * boxvol

def stateq(x, y):
    if y != 0:
        return 1-(1e-8) <= x/y <= 1+(1e-8)
    else:
        return x == 0

def statgeq(x, y):
    return x >= y or stateq(x, y)

def statleq(x, y):
    return x <= y or stateq(x, y)