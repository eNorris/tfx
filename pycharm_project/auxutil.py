__author__ = 'Edward'

import Raw2d


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
        return Raw2d.Raw2d(pt, v1, v2)

def fliptie(tie):
    return Raw2d.Raw2d((tie.px, -tie.py), (tie.vec1[0], -tie.vec1[1]), (tie.vec2[0], -tie.vec2[1]))