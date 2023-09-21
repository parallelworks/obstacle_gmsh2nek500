import sys
from gmesh import GmshMesh

print(sys.argv)
mesh_geo = sys.argv[1]
ndim = int(sys.argv[2])
order =  int(sys.argv[3])
mformat = str(sys.argv[4])
mesh_msh = sys.argv[5]


mesh = GmshMesh(mesh_geo)
mesh.gmsh(mesh_msh, ndim = ndim, order = order, mformat = mformat)

