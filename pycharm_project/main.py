__author__ = 'Edward'

import Rcc2d
import Rpp2d
import Visualizer
import Region
import makephantom

makephantom.makeparts()

exit()

roi = Rcc2d.Rcc2d(150, [300, 200])

width = 400
height = 400
xdivs = 32
ydivs = 32
bot = 0
left = 100

dx = width / xdivs
dy = height / ydivs

mesh = []

for i in range(xdivs):
    mesh.append([])
    for j in range(ydivs):
        r = Rpp2d.Rpp2d([left + i * dx, bot + j * dy], [dx, dy], False)
        neary, nearx = None, None

        if r.top < roi.cy:
            neary = r.top
        elif r.bottom > roi.cy:
            neary = r.bottom
        else:
            neary = roi.cy

        if r.right < roi.cx:
            nearx = r.right
        elif r.left > roi.cx:
            nearx = r.left
        else:
            nearx = roi.cx

        if (neary - roi.cy)**2 + (nearx - roi.cx)**2 < roi.r**2:
            mesh[i].append(r)

vis = Visualizer.Visualizer()

rr = Rcc2d.Rcc2d()
rrr = Rpp2d.Rpp2d()
reg = Region.RegionNode(rr)
reg -= rrr
print(reg)

regions = []
for m in mesh:
    regg = Region.RegionNode(roi)
    regg += m
    regions.append(regg)

vis.register(roi)
roi.draw2d()
vis.unregister(roi)

vis.register(mesh)
vis.launch()

# roi.draw2d()

#for l in mesh:
#    for elem in l:
#        elem.draw()



