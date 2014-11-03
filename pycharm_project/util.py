__author__ = 'Edward'

import math

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