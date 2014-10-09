__author__ = 'Edward'

import time
import math
import random
import Point

def circlecheck(regions, r, center, n, vis):
    starttime = time.time()
    i = 0
    for pt in points_in_circle(n, r, center):
        i += 1
        nowtime = time.time()
        if nowtime - starttime > 1:
            starttime = nowtime
            print("{0:.2f}".format(100 * i / n) + "% complete")
        p = Point.Point2d(pt)
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
        if vis is not None:
            vis.registerthis(p)

def check(regions, checkval, visualizer=None):
    starttime = time.time()
    print("Checking geometry (" + str(checkval) + ") points: ")
    for i in range(checkval):
        nowtime = time.time()
        if nowtime - starttime > 1:
            starttime = nowtime
            print("{0:.2f}".format(100 * i / checkval) + "% complete")
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
        if visualizer is not None:
            visualizer.registerthis(p)

def points_in_circle(n=1, r=1.0, center=(0, 0)):
    count = 0
    while count < n:
        count += 1
        radius = random.random()
        theta = random.random() * 2 * math.pi
        yield r * math.sqrt(radius)*math.cos(theta) + center[0], r * math.sqrt(radius)*math.sin(theta) + center[1]

def points_in_rect(n=1, right=1, top=1, left=0, bottom=1):
    count = 0
    while count < n:
        count += 1
        yield rand_pt_in_rect(right, top, left, bottom)

def rand_pt_in_rect(right=1, top=1, left=0, bottom=1):
    x = random.random() * (right - left) + left
    y = random.random() * (top - bottom) + bottom
    return x, y