import json
import pexpect
import shutil
import os, glob

def create_bcfile(json_bc, bc, pertol = 1e-6):
    with open(json_bc, 'r') as jf:
        data = json.load(jf)

    surface_inputs = data['surfaces']
    nonperbc = []
    perbc = []
    for k,v in surface_inputs.items():
        if 'bc' not in v:
            continue
        if v['bc'] is not 'P':
            if type(v['sidesets']) is list:
                for sideset in v['sidesets']:
                    nonperbc.append(str(sideset) + ' ' + v['bc'])
            else:
                nonperbc.append(str(v['sidesets']) + ' ' + v['bc'])
        else:
            sidesets = ' '.join([str(sideset) for sideset in v['sidesets']])
            vector = ' '.join([str(comp) for comp in v['vector']])
            perbc.append(sidesets + ' ' + vector)
    # Write bc file
    f = open(bc, 'w')
    f.write(str(len(nonperbc)))
    for bc in nonperbc:
        f.write('\n' + bc)
    f.write('\n' + str(len(perbc)) + ' ' + str(pertol))
    for bc in perbc:
        f.write('\n' + bc)
    f.close()


def gmsh2re2(msh, re2, bc = None, ndim = 3, mformat = 1):
    if shutil.which('gmsh2nek') is None:
        raise RuntimeError('Command gmsh2nek not found in PATH:\n{}'.format(os.environ['PATH']))

    if not os.path.isfile(msh):
        raise FileNotFoundError('Mesh file not found in path {}'.format(msh))

    if bc is not None and not os.path.isfile(bc):
        raise FileNotFoundError('Boundary file not found in path {}'.format(bc))

    # Make sure directory for re2 exists
    if os.path.dirname(re2):
        os.makedirs(os.path.dirname(re2), exist_ok = True)

    # If .bc is provided copy to gmsh directory and change name to mfname.bc (./mfname.bc)
    if bc is not None:
        if not os.path.isfile(bc):
            raise FileNotFoundError('Boundary file not found in path {}'.format(bc))

        extension = os.path.basename(bc).split('.')[1]
        if extension == 'json':
            # Create the corresponding .bc file in the same directory
            create_bcfile(
                bc,
                bc.replace('.json', '.bc')
            )
            bc = bc.replace('.json', '.bc')

    # Copy bc file to msh directory
    msh_dir = os.path.dirname(msh)
    mfname=os.path.basename(msh).split('.')[0]
    shutil.copyfile(bc, os.path.join(msh_dir, mfname + '.bc'))

    # MSH filename cannot be too long (34 characters)
    msh_old = msh
    msh = os.path.join(
        os.path.dirname(msh), 'mesh.msh'
    )
    shutil.copyfile(msh_old, msh)

    # Change to msh directory before running exo2nek
    cwd = os.getcwd()
    if not os.path.dirname(msh) == "":
        os.chdir(os.path.dirname(msh))

    print(os.getcwd())
    # Run gmsh command
    print('gmsh2nek')
    child = pexpect.spawn('gmsh2nek')
    child.sendline(mfname)
    child.sendline(str(ndim))
    child.sendline(str(mformat))
    child.expect(pexpect.EOF)

    if re2.startswith('/'): # Absolut path
        shutil.move(mfname + ".re2", re2)
    else: # Relative path
        shutil.move(mfname + ".re2", cwd + '/' + re2)
    os.chdir(cwd)

def genmap(re2, ma2, meshtol = 0.2):
    cwd = os.getcwd()
    if shutil.which('genmap') is None:
        raise RuntimeError('Command genmap not found in PATH:\n{}'.format(os.environ['PATH']))

    # re2
    re2_dir = os.path.dirname(re2)
    mfname=os.path.basename(re2).split('.')[0]

    if re2_dir:
        os.chdir(re2_dir)

    print('Running genmap in {}'.format(os.getcwd()))
    child = pexpect.spawn('genmap', timeout=999999)
    print('genmap')
    child.expect('Input .rea / .re2 name:')
    print('Input .rea / .re2 name:')
    child.sendline(mfname)
    print(mfname)
    child.sendline(str(meshtol))
    print(meshtol)
    child.expect(pexpect.EOF)
    if not glob.glob('*.ma2') + glob.glob('*.map'):
        raise FileNotFoundError('Missing MAP and/or MA2 file in directory {}'.format(os.getcwd()))

    if ma2.startswith('/'): # Absolut path
        shutil.move(mfname + ".ma2", ma2)
    else: # Relative path
        shutil.move(mfname + ".ma2", cwd + '/' + ma2)

    os.chdir(cwd)

if __name__ == '__main__':
    import sys
    msh = sys.argv[1]
    re2 = sys.argv[2]
    ma2 = sys.argv[3]
    ndim = sys.argv[4]
    mformat = sys.argv[5]
    meshtol = sys.argv[6]
    bc = sys.argv[7]

    gmsh2re2(msh, re2, bc = bc, ndim = ndim, mformat = mformat)
    genmap(re2, ma2, meshtol = meshtol)