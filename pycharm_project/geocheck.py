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
    lasttime = starttime
    writefile = open("./geocheck.log", 'w')
    errcount = 0
    nowtime = 0
    print("Checking geometry (" + str(checkval) + ") points: ")
    for i in range(checkval):
        nowtime = time.time()
        if nowtime - lasttime > 1:
            lasttime = nowtime
            eta = (checkval - i) * (nowtime - starttime) / i
            print("{0:.2f}".format(100 * i / checkval) + "% complete - " + str(errcount) + " errors detected so far (" +
                  "{0:.4f}".format(errcount/i) + "% error rate) - ETA: " + "{0:.1f}".format(eta/60) + " min (" +
                  "{0:.1f}".format(eta) + " sec)")
        r = random.random()
        t = random.random() * 2*math.pi
        x = 16*math.sqrt(r) * math.cos(t)
        y = 16*math.sqrt(r) * math.sin(t)
        z = random.random() * 15 - 7.5
        p = Point.Point3d((x, y, z))
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
            writefile.write("WARNING: Error point: " + str(p) + "\n")
            writefile.write("Contained by " + str(counts) + " regions" + "\n")
            errcount += 1
            #print("WARNING: Error point: " + str(p))
            #print("Contained by " + str(counts) + " regions")
        else:
            writefile.write("okay: " + str(p) + "\n")
        if visualizer is not None:
            visualizer.registerthis(p)

    print("100.0% Complete - Total time to completion: " + "{0:.1f}".format((nowtime - starttime)/60) + " min (" +
                  "{0:.1f}".format(nowtime - starttime) + " sec)")

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

def volumecheck(regions, checkval):

    print("Checking volumes (" + str(checkval) + " points) for " + str(len(regions)) + " regions")
    writefile = open("./volumecheck.log", 'w')

    starttime = time.time()
    lasttime = starttime
    errcount = 0
    nowtime = 0
    totalpts = len(regions) * checkval

    for ri, r in enumerate(regions):
        xmin, xmax, ymin, ymax, zmin, zmax = r.get_bounds()
        dx, dy, dz = xmax - xmin, ymax - ymin, zmax - zmin
        boundvol = dx * dy * dz

        if boundvol < 1e-10:
            print("WARNING: Zero volume in " + str(r))
            continue

        count = 0
        for i in range(checkval):

            nowtime = time.time()
            if nowtime - lasttime > 1:
                lasttime = nowtime
                eta = (totalpts - (ri * checkval + i)) * (nowtime - starttime) / (ri * checkval + i)
                print("{0:.2f}".format(100 * (ri * checkval + i) / totalpts) + "% complete - ETA: " +
                      "{0:.1f}".format(eta/60) + " min (" +
                      "{0:.1f}".format(eta) + " sec)")

            x = random.random() * dx + xmin
            y = random.random() * dy + ymin
            z = random.random() * dz + zmin

            if (x, y, z) in r:
                count += 1

        if count == 0:
            print("WARNING: Zero volume in " + str(r))

        volume = count / checkval * boundvol
        writefile.write(str(volume) + " : " + str(r) + "\n")
    print("100.0% Complete - Total time to completion: " + "{0:.1f}".format((nowtime - starttime)/60) + " min (" +
                  "{0:.1f}".format(nowtime - starttime) + " sec)")
    print("Done with volume check")
    writefile.close()