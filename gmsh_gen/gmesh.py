import os
import shutil
import subprocess

class GmshMesh:
    def __init__(self, geo):
        if hasattr(geo, 'path'):
            geo = geo.path
        self.geo = geo
        self.msh = None
        self.mformats = [
            'auto', 'msh1', 'msh2', 'msh22', 'msh3', 'msh4', 'msh40', 'msh41', 'msh', 'unv', 'vtk', 'wrl', 'mail', 'stl',
            'p3d', 'mesh', 'bdf', 'cgns', 'med', 'diff', 'ir3', 'inp', 'ply2', 'celum', 'su2', 'x3d', 'dat', 'neu', 'm', 'key'
        ]

    def gmsh(self, msh, ndim = 3, order = 2, mformat = 'msh2'):
        ndim = int(ndim)
        order = int(order)

        if shutil.which('gmsh') is None:
            raise RuntimeError('Command gmsh not found in PATH:\n{}'.format(os.environ['PATH']))

        if not os.path.isfile(self.geo):
            raise FileNotFoundError('Mesh definition file not found in path {}'.format(self.geo))

        if mformat not in self.mformats:
             raise RuntimeError('Invalid mesh format \'mformat\' = {}. Valid values are:\n{}'.format(mformat, ' ,'.join(self.mformats)))

        if ndim not in [1, 2, 3]:
            raise RuntimeError('Invalid number of spatial dimensions \'ndim\' = {}. Valid values are 1, 2 or 3'.format(str(ndim)))

        if order not in [1, 2, 3, 4, 5]:
            raise RuntimeError('Invalid mesh order \'order\' = {}. Valid values are 1, 2, 3, 4 or 5'.format(str(order)))

        # Make sure directory for gmsh exists
        if os.path.dirname(msh):
            os.makedirs(os.path.dirname(msh), exist_ok = True)

        # Mesh
        cmd = ['gmsh', self.geo, '-' + str(ndim), '-order', str(order), '-format', mformat, '-o', msh]
        print(' '.join([str(i) for i in cmd]))
        subprocess.call(cmd)

        if not os.path.isfile(msh):
            raise FileNotFoundError('Mesh file not found in path {}'.format(msh))
        else:
            self.msh = msh
