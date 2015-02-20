__author__ = 'Edward'

import sys
import matplotlib.pyplot as pyplot
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.tri
import matplotlib.mlab
import numpy
import math

class FluxPlotter(object):

    def __init__(self, mshfile=None, binary=False):
        self.mshfile = None
        self.binary = binary
        self.data = []

        if mshfile is None:
            return

        if binary:
            self.mshfile = open(mshfile, 'rb')
        else:
            self.mshfile = open(mshfile, 'r')

    def parse(self):
        if self.mshfile is None:
            print("Meshfile not defined, can't parse!")
            return

        for line in self.mshfile.readlines():
            tokens = line.split()
            if len(tokens) != 7:
                print("Illegal number of entries: " + str(len(tokens)))
                continue

            #x, y, z, vol, flux, dose, h20 = [float(p) for p in tokens]
            self.data.append([float(p) for p in tokens])

    def flattenflux_z(self, zmin, zmax):
        pts = []
        for d in self.data:
            if zmin <= d[2] <= zmax:
                pts.append([d[0], d[1], d[4]])
        return pts


    def log_flux_data(self):
        for i in range(len(self.data)):
            self.data[i][4] = math.log10(self.data[i][4])
            print(self.data[i][4])


    def reduce_range(self, pts, x, y, z, throw_out=False):
        if z is None:
            return [[p[0], p[1], p[2]] for p in pts if
                (x != None and x[0] <= p[0] <= x[1]) and
                (y != None and y[0] <= p[1] <= y[1])]
        else:
            if throw_out:
                # All outside z range are removed
                return [[p[0], p[1], p[2]] for p in pts if
                (x != None and x[0] <= p[0] <= x[1]) and
                (y != None and y[0] <= p[1] <= y[1]) and
                (z[0] <= p[2] <= z[1])]
            else:
                # All outside z range are set to z max
                return [[p[0], p[1], p[2] if z[0] <= p[2] <= z[1] else z[1]] for p in pts if
                (x != None and x[0] <= p[0] <= x[1]) and
                (y != None and y[0] <= p[1] <= y[1])]


    def reduce_cyl_range(self, pts, x, y, z, r, throw_out=False):
        if z is None:
            return [[p[0], p[1], p[2]] for p in pts if ((x - p[0])**2 + (y - p[1])**2 <= r**2)]
        else:
            if throw_out:
                return [[p[0], p[1], p[2]] for p in pts if
                ((x - p[0])**2 + (y - p[1])**2 <= r**2) and
                (z[0] <= p[2] <= z[1])]
            else:
                return [[p[0], p[1], p[2] if z[0] <= p[2] <=z[1] else z[1]] for p in pts if
                ((x - p[0])**2 + (y - p[1])**2 <= r**2)]

    def xxgrid(self, x, y, z, resX=100, resY=100):
        "Convert 3 column data to matplotlib grid"
        xi = numpy.linspace(min(x), max(x), resX)
        yi = numpy.linspace(min(y), max(y), resY)
        Z = matplotlib.mlab.griddata(x, y, z, xi, yi)
        X, Y = numpy.meshgrid(xi, yi)
        return X, Y, Z

    def plotflux_z_surf(self, zmin, zmax):
        pts = self.flattenflux_z(zmin, zmax)
        #pts = self.reduce_range(pts, x=(-30, 30), y=(-30, 30), z=(0, 1e11))
        pts = self.reduce_cyl_range(pts, x=0, y=0, z=None, r=45)
        xs = numpy.array([p[0] for p in pts])
        ys = numpy.array([p[1] for p in pts])
        fluxs = numpy.array([p[2] for p in pts])

        fig = pyplot.figure()
        ax = fig.add_subplot(111, projection='3d')

        # 3-D Surface plot
        triangles = matplotlib.tri.Triangulation(xs, ys)
        surf = ax.plot_trisurf(xs, ys, fluxs, triangles, cmap=pyplot.get_cmap("jet"), lw=0.2,
                alpha=0.5)

        fig.colorbar(surf)
        pyplot.show()

    def plotflux_z_contour(self, zmin, zmax):
        # x, y, z, vol, flux, dose, h2o -> x, y, flux
        pts = self.flattenflux_z(zmin, zmax)
        pts = self.reduce_cyl_range(pts, x=0, y=0, z=(0, 5e-10), r=60)

        #for i in range(len(pts)):
        #    pts[i][2] = math.log10(pts[i][2])

        xs = numpy.array([p[0] for p in pts])
        ys = numpy.array([p[1] for p in pts])
        fluxs = numpy.array([p[2] for p in pts])

        fig = pyplot.figure()
        X, Y, Z = self.xxgrid(xs, ys, fluxs)
        #surf = pyplot.contourf(X, Y, Z, 100, cmap="jet")
        surf = pyplot.contourf(X, Y, Z, 100, cmap="jet")

        pyplot.xlabel("x")
        pyplot.ylabel("y")
        pyplot.title("Photon Flux Per Source Particle (photon/cm$^2$s)")

        cbar = fig.colorbar(surf)
        cbar.ax.set_xlabel("$10^x$")
        pyplot.show()

    def plotflux_z_line(self, zmin, zmax):

        pts = self.flattenflux_z(zmin, zmax)
        pts = self.reduce_range(pts, x=(-.5, .5), y=(-.5, 30), z=(0, 1e11))
        xs = numpy.array([p[0] for p in pts])
        ys = numpy.array([p[1] for p in pts])
        fluxs = numpy.array([p[2] for p in pts])

        fig = pyplot.figure()
        surf = pyplot.plot(ys, fluxs)

        surf.ylabel("y")
        pyplot.xlabel("x")

        f = open("../data.txt", 'w')
        for y,z in zip(ys, fluxs):
            f.write(str(y) + "\t" + str(z) + "\n")

        pyplot.show()

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Usage: python fluxplotter mshfile")
    elif len(sys.argv) == 2:
        p = FluxPlotter(sys.argv[1])
        p.parse()
        #p.log_flux_data()
        p.plotflux_z_contour(-.5, .5)
    else:
        print("Too many args!")
        print("Usage: python fluxplotter mshfile")