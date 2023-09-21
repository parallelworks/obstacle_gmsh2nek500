import math
import sys, os
import json
import shutil
import numpy as np
from copy import deepcopy

def replace_in_file(fn, k, v, sep = '='):
    # Replaces everything after k+sep by v in each line of file fn
    # sep cannot be a space
    k=str(k)
    v=str(v)
    # Read in the file
    with open(fn, 'r') as f:
        filedata = f.read()

    # Replace the target string
    with open(fn, 'w') as f:
        for line in filedata.splitlines():
            clean_line=line.replace(' ','').split(')')[0].split('#')[0].split('!')[0].split(';')[0]
            if k+sep in clean_line:
                v_old=clean_line.split(k+sep)[1]
                f.write(line.split(k)[0] + k + line.split(k)[1].replace(v_old,v) + '\n')
            else:
                f.write(line+'\n')



def geom_expansion(d1 = None, df = None, r = None, Ne = None, tl = None):
    errmsg = 'Must specify (d1, df, r), (d1, r, Ne), (d1, Ne, tl) or (d1, df, tl)'
    if d1 is not None and r is not None:
        # d1, df, r --> Ne, tl
        if Ne is None:
            # Number of elements
            Ne = math.floor(math.log(df/d1)/math.log(r) + 1)
        # d1, r, Ne --> df, tl
        elif df is None:
            df = math.pow(r, Ne)
            # Element lengths
        else:
            sys.exit('ERROR:' + errmsg)
        els = [ d1 * math.pow(r,e) for e in range(Ne) ]
        df = els[Ne-1]
        # Total length
        tl = math.fsum(els)
    # d1, Ne, tl --> df, r
    elif d1 is not None and Ne is not None and tl is not None:
        # Coefficients of pol 0 = r^Ne + r^(Ne-1) + ... + r - tl/d1
        coeffs = np.ones(Ne)
        coeffs[Ne-1] = coeffs[Ne-1] - (tl / d1)
        rts = np.roots(coeffs)
        r = max(rts)
        df = d1 * math.pow(r, Ne-1)

    # d1, df, tl --> r, Ne
    elif d1 is not None and df is not None and tl is not None:
        # Increase Ne until d1_real < d1 and df_real < df
        Ne = 2
        if d1 + df > tl:
            print('d1: {}, df: {}, tl {}'.format(d1, df, tl))
            sys.exit('ERROR: d1 + df > tl!')
        while True:
            Ne_old = Ne
            r = math.exp(math.log(df/d1)/(Ne-1))
            tl_test = math.fsum([ d1 * math.pow(r,e) for e in range(Ne) ])
            if tl > tl_test:
                Ne = Ne + 1
            else:
                Ne = Ne - 1
            if Ne <= Ne_old:
                Ne = Ne_old
                r = math.exp(math.log(df/d1)/(Ne-1))
                d1 = tl / math.fsum([ math.pow(r,e) for e in range(Ne) ])
                df = d1 * math.pow(r, Ne-1)
                break
    else:
        sys.exit('ERROR: ' + errmsg)
    return {'d1': d1, 'df': df, 'r': r, 'Ne': Ne, 'tl': tl}


# Check if the mesh paramters are incompatible
def check_mesh_parameters(Lin, Lout, H, W05, Lx, Ly, Lz, dfx_in, dfx_out, dfy, dfz, mesh_name):
    error_msg=[]
    mesh_is_ok = True
    tol = 0.8
    def write_error_msg(L_outer, L_inner, df):
        fe = open('ERRORS.txt', 'a')
        fe.write('ERROR: Mesh {} must fulfill {} - {} > {}\n'.format(mesh_name, L_outer['name'], L_inner['name'], df['name']))
        fe.write('{} is too short! Increase {}, reduce {}, increase r or increase dmin.\n'.format(L_outer['name'], L_outer['name'], L_inner['name']))
        fe.write('{}: {}, {}: {}, {}: {}\n\n'.format(L_outer['name'], L_outer['value'], L_inner['name'], L_inner['value'], df['name'], df['value']))
        fe.close()

    if (Lin-Lx) < dfx_in*tol:
        mesh_is_ok = False
        L_outer = {'name':'Lin', 'value': Lin}
        L_inner = {'name':'Lx', 'value': Lx}
        df = {'name':'dfx', 'value': dfx_in}
        write_error_msg(L_outer, L_inner, df)
    if (Lout-Lx) < dfx_out*tol:
        mesh_is_ok = False
        L_outer = {'name':'Lout', 'value': Lout}
        L_inner = {'name':'Lx', 'value': Lx}
        df = {'name':'dfx', 'value': dfx_out}
        write_error_msg(L_outer, L_inner, df)
    if (H-Ly) < dfy*tol:
        mesh_is_ok = False
        L_outer = {'name':'H', 'value': H}
        L_inner = {'name':'Ly', 'value': Ly}
        df = {'name':'dfy', 'value': dfy}
        write_error_msg(L_outer, L_inner, df)
    if (W05-Lz) < dfz*tol:
        mesh_is_ok = False
        L_outer = {'name':'W/2', 'value': W05}
        L_inner = {'name':'Lz', 'value': Lz}
        df = {'name':'dfz', 'value': dfz}
        write_error_msg(L_outer, L_inner, df)
    return mesh_is_ok

def create_obstacle_geo (gmsh_inputs, geo_f, case, copy_geo = None, position = None, h_mult_dict = None, Ne_y1 = None, Ne_y2 = None):

    if h_mult_dict is None:
        h_mult_dict = {
            "center": 1.0,
            "left": 1.0,
            "right": 1.0,
            "in": 1.0,
            "out": 1.0,
            "in_left": 1.0,
            "in_right": 1.0,
            "out_left": 1.0,
            "out_right": 1.0
        }

    if copy_geo is None:
        new_geo = geo_f
    else:
        new_geo = copy_geo

    h_ref = float(gmsh_inputs['geometry']['h'])
    h = h_ref * h_mult_dict["center"]
    wx = float(gmsh_inputs['geometry']['R_wx_h']) * h_ref
    wx05 = wx/2
    wz = float(gmsh_inputs['geometry']['R_wz_h']) * h_ref
    wz05 = wz/2
    H = float(gmsh_inputs['geometry']['R_H_h']) * h_ref
    W = float(gmsh_inputs['geometry']['R_W_h']) * h_ref
    W05 = W/2
    Lin = float(gmsh_inputs['geometry']['R_Lin_h']) * h_ref
    Lout = float(gmsh_inputs['geometry']['R_Lout_h']) * h_ref

    d1 = float(gmsh_inputs['mesh']['dmin'])
    dfx = float(gmsh_inputs['mesh']['dxmax'])
    dfy = float(gmsh_inputs['mesh']['dymax'])
    dfz = float(gmsh_inputs['mesh']['dzmax'])
    dfo = float(gmsh_inputs['mesh']['domax'])
    r_xz = float(gmsh_inputs['mesh']['r'])

    # Inner (near-obstacle) mesh values
    obs_xz_values = geom_expansion(d1 = d1, df = dfo , r = r_xz )
    print('Inner mesh values:')
    print(obs_xz_values)
    Ne_xz = obs_xz_values['Ne']
    Lx = obs_xz_values['tl']
    Lz = Lx # For 45 degree mesh
    Ly = h + Lx
    Ly_in = Lx + h_ref*(h_mult_dict["center"]+h_mult_dict["in"])/2
    Ly_out = Lx + h_ref*(h_mult_dict["center"]+h_mult_dict["out"])/2
    Ly_left = Lx + h_ref*(h_mult_dict["center"]+h_mult_dict["left"])/2
    Ly_right = Lx + h_ref*(h_mult_dict["center"]+h_mult_dict["right"])/2
    Ly_in_left = Lx + h_ref*(h_mult_dict["center"]+h_mult_dict["in_left"]+h_mult_dict["in"]+h_mult_dict["left"])/4
    Ly_in_right = Lx + h_ref*(h_mult_dict["center"]+h_mult_dict["in_right"]+h_mult_dict["in"]+h_mult_dict["right"])/4
    Ly_out_left = Lx + h_ref*(h_mult_dict["center"]+h_mult_dict["out_left"]+h_mult_dict["out"]+h_mult_dict["left"])/4
    Ly_out_right = Lx + h_ref*(h_mult_dict["center"]+h_mult_dict["out_right"]+h_mult_dict["out"]+h_mult_dict["right"])/4
    Ly_max = max(Ly, Ly_in, Ly_out, Ly_left, Ly_right, Ly_in_left, Ly_in_right, Ly_out_left, Ly_out_right)
    Ly_max = h_ref * max(h_mult_dict.values())

    if position == "inlet":
        dfx_in = dfx
        dfx_out = dfo
    elif position == "outlet":
        dfx_in = dfo
        dfx_out = dfx
    elif position == "core":
        dfx_in = dfo
        dfx_out = dfo
    else:
        dfx_in = dfx
        dfx_out = dfx

    mesh_is_ok = check_mesh_parameters(Lin, Lout, H, W05, Lx+wx05, Ly, Lz+wz05, dfx_in, dfx_out, dfy, dfz, new_geo)
    if not mesh_is_ok:
        sys.exit()

    Ne_wx = math.floor((2*Lx + wx) / (dfo/r_xz))
    Ne_wz = math.floor((2*Lz + wz) / (dfz/r_xz))

    Ne_x2_in = int(round((Lin - Lx - wx05) / dfx_in))
    Ne_x2_out = int(round((Lout - Lx - wx05) / dfx_out))

    print('Bottom Y-Outer (far-from-obstacle) mesh values')
    if Ne_y1 is None:
        obs_y1_values = geom_expansion(d1 = d1, df = dfy, tl = Ly_max)
        Ne_y1 = obs_y1_values['Ne']
    else:
        obs_y1_values = geom_expansion(d1 = d1,  Ne = Ne_y1, tl = Ly_max)

    r_y1 = obs_y1_values['r']
    print(obs_y1_values)

    if case == 'duct':
        print('Z-Outer (far from obstacle) mesh values')
        obs_z_values = geom_expansion(d1 = d1, df = dfz , tl = (W05-Lz-wz05) )
        print(obs_z_values)
        Ne_z2 = obs_z_values['Ne']
        r_z2 =  obs_z_values['r']
    else:
        # Uniform solution:
        Ne_z2 = int(round((W05-Lz-wz05) / dfz))
        r_z2 = 1.0

    if case == 'channel' or case == 'duct':
        print('Top Y-Outer (far-from-obstacle) mesh values')
        if Ne_y2 is None:
            obs_y2_values = geom_expansion(d1 = d1, df = dfy , tl = (H - Ly) )
            Ne_y2 = obs_y2_values['Ne']
        else:
            obs_y2_values = geom_expansion(d1 = d1, Ne = Ne_y2 , tl = (H - Ly) )
        print(obs_y2_values)
        r_y2 = obs_y2_values['r']
    else:
        # Uniform sol:
        if Ne_y2 is None:
            Ne_y2 = math.ceil((H - Ly) / dfy)
        r_y2 = 1

    # Total elemens
    # Columns:  (Ne_x2_in+Ne_x2_out)*(Ne_y1+Ne_y2)*2*Ne_z2
    # Central top part: Ne_wz*Ne_wx*Ne_y2
    # Sides: 2*Ne_wx*(Ne_y2+Ne_y1)*Ne_z2 + Ne_wz*(Ne_y2+Ne_y1)*(Ne_x2_in+Ne_x2_out)
    Ne_outer = (Ne_x2_in+Ne_x2_out)*(Ne_y1+Ne_y2)*2*Ne_z2 + 2*Ne_wx*(Ne_y2+Ne_y1)*Ne_z2 + Ne_wz*(Ne_y2+Ne_y1)*(Ne_x2_in+Ne_x2_out) + Ne_wz*Ne_wx*Ne_y2
    Ne_inner = 2*Ne_y1*Ne_xz*(Ne_wx+Ne_wz) + Ne_wx*Ne_wz*Ne_xz
    Ne_total = Ne_outer + Ne_inner

    # Added +1 to Ne_* to convert number of elements to numebr of nodes
    mesh = {
        "h": h,
        "wx": wx,
        "wz": wz,
        "H": H,
        "W": W,
        "Lin": Lin,
        "Lout": Lout,
        "Lx": Lx,
        "Lz": Lz,
        "Ly": Ly,
        "Ly_in": Ly_in,
        "Ly_out": Ly_out,
        "Ly_left": Ly_left,
        "Ly_right": Ly_right,
        "Ly_in_left": Ly_in_left,
        "Ly_in_right": Ly_in_right,
        "Ly_out_left": Ly_out_left,
        "Ly_out_right": Ly_out_right,
        "Ne_wx": Ne_wx+1,
        "b_wx": 4*r_xz,
        "Ne_wz": Ne_wz+1,
        "b_wz": 4*r_xz,
        "Ne_xz": Ne_xz+1,
        "r_xz": r_xz,
        "Ne_y1": Ne_y1+1,
        "r_y1": float(r_y1),
        "b_y1": 4*float(r_y1),
        "Ne_x2_in": Ne_x2_in+1,
        "Ne_x2_out": Ne_x2_out+1,
        "Ne_y2": Ne_y2+1,
        "r_y2": r_y2,
        "Ne_z2": Ne_z2+1,
        "r_z2": r_z2
    }
    print(mesh)
    if copy_geo is not None:
        shutil.copyfile(geo_f, new_geo)
    for key in mesh:
        value = str(mesh[key])
        replace_in_file(new_geo, key, value, sep = '=')
    return Ne_total

# Make a new_geo_name geo file by displacing an existing orig_geo_name geo file
# by a vector disp.
def copy(orig_geo_name, new_geo_name, disp, gr):
    # Inputs:
    # orig_geo_name: Path to the original geo file
    # new_geo_name: Path to the translated geo file
    # disp: Displacement vector
    # gr: geo range. gr=0 starts with Points(1), gr=1000 starts with Point(1001)
    orig_geof = open(orig_geo_name, 'r')
    orig_geo_content = orig_geof.readlines()
    orig_geof.close()
    new_geof = open(new_geo_name, 'w')

    def sign(num):
        if int(num) < 0:
            return -1
        else:
            return 1

    replace = False
    for l in orig_geo_content:
        # Replace lines after first Point definition.
        if l.startswith('Point('):
            replace = True
        if '//' in l:
            new_l =l
        elif replace:
            if '{' in l and '(' in l:
                bef_par = l.split('(')[0] + '('
                in_par = l.split('(')[1].split(')')[0]
                if ',' in in_par:
                    bef_par = bef_par + in_par.split(',')[0] + ', '
                    in_par = in_par.split(',')[1]
                aft_par_bef_bra = ')' + l.split(')')[1].split('{')[0] + '{'
                in_bra =  l.split('{')[1].split('}')[0]
                aft_par_aft_bra = '}' + l.split(')')[1].split('}')[1]
                new_in_par = str(int(in_par)+gr*sign(in_par))
                new_in_bra = []
                if 'Point' in l:
                    coord = 0
                    for index in in_bra.split(','):
                        new_in_bra.append(index + ' + '  + str(disp[coord]))
                        coord += 1
                else:
                    for index in in_bra.split(','):
                        new_in_bra.append(str(int(index)+gr*sign(index)))
                new_in_bra = ', '.join(new_in_bra)
                new_l = bef_par + new_in_par + aft_par_bef_bra + new_in_bra + aft_par_aft_bra
            elif '{' in l:
                bef_bra = l.split('{')[0] + '{'
                in_bra =  l.split('{')[1].split('}')[0]
                aft_bra = '}' + l.split('}')[1]
                new_in_bra = str(int(in_bra)+gr*sign(in_bra))
                new_l = bef_bra + new_in_bra + aft_bra
            else:
                new_l = l
        else:
            new_l = l
        new_geof.write(new_l)
    new_geof.close()


# Merge the expansion geo file (exp_geo_name) to the original geo file (orig_geo_file)
# Input: A dictionary for the expansion and original geometries with:
# input = {
#     "name": name,
#     "gr": 0,
#     "pts": [12, 13, 14, 15],
#     "hor_lines": [26, 28, 32],
#     "ver_lines": [212, 213, 214, 215],
#     "surf": [126, 128, 132]}

def merge(orig_input, exp_input):
    # The orig file is overwritten
    merged_name = orig_input["name"]
    class geo():
        def __init__(self, geo_input):
            content = self.read_file_to_list(geo_input["name"])
            ol_pts = self.expand_pts(geo_input["pts"], geo_input["gr"])
            ol_lines = self.expand_lines(geo_input["hor_lines"], geo_input["ver_lines"], geo_input["gr"])
            ol_surfaces = self.expand_surfaces(geo_input["surf"], geo_input["gr"])

        def read_file_to_list(self, fname):
            f = open(fname, 'r')
            self.content = f.readlines()
            f.close()

        def expand_pts(self, base, gr):
            base_gr = [xi+gr for xi in base]
            self.ol_pts = base_gr + [xi+50 for xi in base_gr] + [xi+100 for xi in base_gr]

        def expand_lines(self, hor, ver, gr):
            exp_hor = hor + [xi+50 for xi in hor] + [xi+100 for xi in hor]
            exp_ver = ver + [xi+50 for xi in ver]
            self.ol_lines = [xi+gr for xi in exp_hor + exp_ver]

        def expand_surfaces(self, base, gr):
            base_gr = [xi+gr for xi in base]
            self.ol_surfaces = base_gr + [xi + 50 for xi in base_gr]

    exp = geo(exp_input)
    orig = geo(orig_input)
    mapping_surf = dict(zip(exp.ol_surfaces, orig.ol_surfaces))
    mapping_pts = dict(zip(exp.ol_pts, orig.ol_pts))
    mapping_lines = dict(zip(exp.ol_lines, orig.ol_lines))

    merged_geo = open(merged_name, 'a')
    skip_words = ["Transfinite Surface", "Recombine Surface", "Transfinite Volume", "Recombine Volume", "Mesh", "SetOrder", "Physical"]
    for lc in exp.content:
        new_lc = lc
        if lc.startswith('//'):
            continue
        elif any(skip_word in lc for skip_word in skip_words):
            continue
        elif lc.startswith('Point('):
            in_par = int(lc.split('(')[1].split(')')[0])
            if in_par in exp.ol_pts:
                continue
        elif lc.startswith('Line('):
            in_par = int(lc.split('(')[1].split(')')[0])
            if in_par in exp.ol_lines:
                continue
            # If line has a deleted point (perpendicular to overlapped surface)
            bef_bra = lc.split('{')[0] + '{'
            in_bra =  lc.split('{')[1].split('}')[0]
            aft_bra = '}' + lc.split('}')[1]
            new_in_bra = []
            for pt in in_bra.split(','):
                if int(pt) in exp.ol_pts:
                    new_in_bra.append(str(mapping_pts[int(pt)]))
                else:
                    new_in_bra.append(str(pt))
            new_in_bra = ', '.join(new_in_bra)
            new_lc = bef_bra + new_in_bra + aft_bra
        elif lc.startswith('Transfinite') and '{' in lc:
            in_bra =  int(lc.split('{')[1].split('}')[0])
            if in_bra in exp.ol_lines:
                continue
        elif 'Surface(' in lc:
            in_par = int(lc.split('(')[1].split(')')[0])
            if in_par in exp.ol_surfaces:
                continue
        elif 'Line Loop(' in lc:
            in_par = int(lc.split('(')[1].split(')')[0])
            if in_par in exp.ol_surfaces:
                continue
            # If surface has an overlapped line
            bef_bra = lc.split('{')[0] + '{'
            in_bra =  lc.split('{')[1].split('}')[0]
            aft_bra = '}' + lc.split('}')[1]
            new_in_bra = []
            for line in in_bra.split(','):
                if '-' in line:
                    pre = '-'
                else:
                    pre = ''
                if int(line.replace('-','')) in exp.ol_lines:
                    new_in_bra.append(pre + str(mapping_lines[int(line.replace('-',''))]))
                else:
                    new_in_bra.append(str(line))
            new_in_bra = ', '.join(new_in_bra)
            new_lc = bef_bra + new_in_bra + aft_bra

        elif 'Surface Loop(' in lc:
            bef_bra = lc.split('{')[0] + '{'
            in_bra =  lc.split('{')[1].split('}')[0]
            aft_bra = '}' + lc.split('}')[1]
            new_in_bra = []
            for sf in in_bra.split(','):
                if int(sf) in exp.ol_surfaces:
                    new_in_bra.append(str(mapping_surf[int(sf)]))
                else:
                    new_in_bra.append(str(sf))
            new_in_bra = ', '.join(new_in_bra)
            new_lc = bef_bra + new_in_bra + aft_bra

        merged_geo.write(new_lc)
    merged_geo.close()

def create_matrix(base_geo_name, gmsh_inputs, merged_geo_name, case):

    def create_obstacle_height_connectivity(h_mult_array, n, I, J, case):
        j = (n-1) // I + 1
        i = n - (j-1)*I

        if i == 1:
            if case == "duct":
                i_left = 1
            else:
                i_left = I
        else:
            i_left = i - 1

        if i == I:
            if case == "duct":
                i_right = I
            else:
                i_right = 1
        else:
            i_right = i + 1

        if j == 1:
            if case == "duct" or case == "channel":
                j_in = J
            else:
                j_in = 1
        else:
            j_in = j - 1

        if j == J:
            if case == "duct" or case == "channel":
                j_out = 1
            else:
                j_out = J
        else:
            j_out = j + 1

        h_mult_n = {
            "center": h_mult_array[i-1][j-1],
            "left": h_mult_array[i_left-1][j-1],
            "right": h_mult_array[i_right-1][j-1],
            "in": h_mult_array[i-1][j_in-1],
            "out": h_mult_array[i-1][j_out-1],
            "in_left": h_mult_array[i_left-1][j_in-1],
            "in_right": h_mult_array[i_right-1][j_in-1],
            "out_left": h_mult_array[i_left-1][j_out-1],
            "out_right": h_mult_array[i_right-1][j_out-1]
        }
        return h_mult_n

    #base_geo_name = 'base_sphere.geo'
    #merged_geo_name = 'merged_sphere.geo'
    # Create a IxJ matrix of obstacles
    # Number of ostacles in the z direction: I
    # Number of obstacles in the x direction: J
    #gmsh_inputs = general.read_json(gmsh_input_f)
    I = int(gmsh_inputs['matrix']['I'])
    J = int(gmsh_inputs['matrix']['J'])
    N = I * J
    h = float(gmsh_inputs['geometry']['h'])
    L = float(gmsh_inputs['matrix']['R_L_h']) * (h/2)
    W = float(gmsh_inputs['geometry']['R_W_h']) * h
    Lin = float(gmsh_inputs['geometry']['R_Lin_h']) * h
    Lout = float(gmsh_inputs['geometry']['R_Lout_h']) * h
    #L = Lin + Lout
    # Create base geo files:
    # Inlet
    inlet_inputs = deepcopy(gmsh_inputs)
    h_mult_list = gmsh_inputs['matrix']['h_mult_list']  #[0.5, 0.75, 0.75, 1]
    h_mult_array = np.array(h_mult_list).reshape((J, I)).T

    # FIXME: Ne_y1 and Ne_y2 need to be calculated beforehand!
    H = float(gmsh_inputs['geometry']['R_H_h']) * h
    r_xz = float(gmsh_inputs['mesh']['r'])
    d1 = float(gmsh_inputs['mesh']['dmin'])
    dfo = float(gmsh_inputs['mesh']['domax'])
    dfy = float(gmsh_inputs['mesh']['dymax'])
    obs_xz_values = geom_expansion(d1 = d1, df = dfo , r = r_xz )
    Ne_xz = obs_xz_values['Ne']
    Lx = obs_xz_values['tl']
    Lz = Lx # For 45 degree mesh
    Ly_max = h*max(h_mult_list) + Lx
    Ly_min = h*min(h_mult_list) + Lx
    obs_y1_values = geom_expansion(d1 = d1, df = dfy, tl = Ly_max)
    Ne_y1 = obs_y1_values['Ne']


    if case == 'channel' or case == 'duct':
        obs_y2_values = geom_expansion(d1 = d1, df = dfy , tl = (H - Ly_min) )
        Ne_y2 = obs_y2_values['Ne']
    else:
        Ne_y2 = math.ceil((H - Ly_min) / dfy)

    for n in range(1,N+1):
        lelg = 0
        j = (n-1) // I + 1
        i = n - (j-1)*I
        n_inputs = deepcopy(gmsh_inputs)
        h_mult_dict_n = create_obstacle_height_connectivity(h_mult_array, n, I, J, case)
        copy_geo = "obstacle_{}.geo".format(str(n))

        if N == 1:
            pos = ""
        elif j == 1: # Inlet Line
            pos = "inlet"
            n_inputs['geometry']['R_Lout_h'] = L
        elif j == J: # Outlet Line
            pos = "outlet"
            n_inputs['geometry']['R_Lin_h'] = L
        else: # Core
            pos = "core"
            n_inputs['geometry']['R_Lin_h'] = L
            n_inputs['geometry']['R_Lout_h'] = L

        Ne_n = create_obstacle_geo(n_inputs, base_geo_name, case, copy_geo = copy_geo, position = pos,  h_mult_dict = h_mult_dict_n, Ne_y1 = Ne_y1, Ne_y2 = Ne_y2)
        lelg += Ne_n


    for n in range(1,N+1):
        j = (n-1) // I + 1
        i = n - (j-1)*I
        copy_geo = "obstacle_{}.geo".format(str(n))
        print(str(i) + ', ' + str(j) + ', ' + str(n))
        if n == 1:
            shutil.copyfile(copy_geo, merged_geo_name)
        else:
            exp_gr = (n-1)*1000
            copy_geo_name = str(exp_gr) + '.geo'

            # Create copy to merge:
            if j == 1: # Inlet line
                disp = [0, 0, (i-1)*W]
                copy(copy_geo, copy_geo_name, disp, exp_gr)
            elif j == J: # Outlet line
                disp = [(J-1)*2*L, 0, (i-1)*W]
                copy(copy_geo, copy_geo_name, disp, exp_gr)
            else:
                disp = [(j-1)*2*L, 0, (i-1)*W]
                copy(copy_geo, copy_geo_name, disp, exp_gr)

            # Merge:
            if j == 1:
                orig_gr = (n-1-1)*1000
                orig_pts = [12, 13, 14, 15]
                orig_hor_lines = [26, 28, 32]
                orig_ver_lines = [212, 213, 214, 215]
                orig_surf = [126, 128, 132]

                exp_pts = [9, 20, 19, 18]
                exp_hor_lines = [23, 27, 29]
                exp_ver_lines = [209, 220, 219, 218]
                exp_surf = [123, 127, 129]

            elif i == 1:
                orig_gr =  (n-I-1)*1000
                orig_pts = [18, 17, 16, 15]
                orig_hor_lines = [20, 21, 22]
                orig_ver_lines = [218, 217, 216, 215]
                orig_surf = [120, 121, 122]

                exp_pts = [9, 10, 11, 12]
                exp_hor_lines = [13, 14, 15]
                exp_ver_lines = [209, 210, 211, 212]
                exp_surf = [113, 114, 115]
            else:
                orig_gr_left = (n-1-1)*1000
                orig_gr_bottom = (n-I-1)*1000
                # Merge function only takes 1 gr
                orig_gr = orig_gr_bottom
                orig_gr_diff = orig_gr_left - orig_gr
                #          Bottom                                         Left
                orig_pts = [18, 17, 16, 15] + [xi+orig_gr_diff for xi in [13, 14, 15]]
                orig_hor_lines = [20, 21, 22] + [xi+orig_gr_diff for xi in [26, 28, 32]]
                orig_ver_lines = [218, 217, 216, 215] + [xi+orig_gr_diff for xi in [213, 214, 215]]
                orig_surf = [120, 121, 122] + [xi+orig_gr_diff for xi in [126, 128, 132]]

                exp_pts = [9, 10, 11, 12] + [20, 19, 18]
                exp_hor_lines = [13, 14, 15] + [23, 27, 29]
                exp_ver_lines = [209, 210, 211, 212] + [220, 219, 218]
                exp_surf = [113, 114, 115] + [123, 127, 129]

            orig_input = {
                "name": merged_geo_name,
                "gr": orig_gr,
                "pts": orig_pts,
                "hor_lines": orig_hor_lines,
                "ver_lines": orig_ver_lines,
                "surf": orig_surf
            }

            exp_input = {
                "name": copy_geo_name,
                "gr": exp_gr,
                "pts" : exp_pts,
                "hor_lines": exp_hor_lines,
                "ver_lines": exp_ver_lines,
                "surf": exp_surf
            }

            merge(orig_input, exp_input)
    merged_geo = open(merged_geo_name, 'a')

    # Clean merged_geo
    skip_words = ["Transfinite Surface", "Recombine Surface", "Transfinite Volume", "Recombine Volume", "Mesh", "SetOrder", "Physical"]
    merged_geof = open(merged_geo_name, 'r')
    merged_geo_content = merged_geof.readlines()
    merged_geof.close()
    merged_geof = open(merged_geo_name, 'w')
    for lm in merged_geo_content:
        if any(skip_word in lm for skip_word in skip_words):
            continue
        else:
            merged_geof.write(lm)

    merged_geof.write("Transfinite Surface \"*\";" + '\n')
    merged_geof.write("Recombine Surface \"*\";" + '\n')
    merged_geof.write("Transfinite Volume \"*\";" + '\n')
    merged_geof.write("Recombine Volume \"*\";" + '\n')
    merged_geof.write("Mesh 3;" + '\n')
    merged_geof.write("SetOrder 2;" + '\n')

    # Define BCs
    inlet = [113, 114, 115, 163, 164, 165]
    inlet_grs = [ (i-1)*1000 for i in range(1,I+1) ]
    inlet = ','.join([ str(xi+gr) for xi in inlet for gr in inlet_grs ])
    outlet = [120, 121, 122, 170, 171, 172]
    outlet_grs = [ (i-1)*1000 for i in range(N-I+1, N+1) ]
    outlet = ','.join([ str(xi+gr) for xi in outlet for gr in outlet_grs ])
    bottom = [2, 3, 4, 5, 12, 13, 14, 15, 16, 17, 18, 19]
    bottom = ','.join([ str(xi+gr) for xi in bottom for gr in range(0,I*J*1000,1000) ])
    top = [31, 32, 33, 34, 35, 36, 37, 38, 39]
    top = ','.join([ str(xi+gr) for xi in top for gr in range(0,I*J*1000,1000) ])
    left = [123, 127, 129, 173, 177, 179]
    left_grs =  [ (j-1)*I*1000 for j in range(1,J+1) ]
    left = ','.join([ str(xi+gr) for xi in left for gr in left_grs ])
    right = [126, 128, 132, 176, 178, 182]
    right_grs = [ (I+(j-1)*I-1)*1000 for j in range(1,J+1) ]
    right = ','.join([ str(xi+gr) for xi in right for gr in right_grs ])
    obstacle = [101, 102, 103, 104, 6]
    obstacle = ','.join([ str(xi+gr) for xi in obstacle for gr in range(0,I*J*1000,1000) ])
    fluid = [2, 3, 4, 5, 6, 12, 13, 14, 15, 16, 17, 18, 19, 11, 22, 23, 24, 25, 26, 27, 28, 29]
    fluid = ','.join([ str(xi+gr) for xi in fluid for gr in range(0,I*J*1000,1000) ])
    merged_geof.write("Physical Surface(\"inlet\", 1) = {" + inlet + "};\n")
    merged_geof.write("Physical Surface(\"outlet\", 2) = {" + outlet + "};\n")
    merged_geof.write("Physical Surface(\"bottom\", 3) = {" + bottom + "};\n")
    merged_geof.write("Physical Surface(\"top\", 4) = {" + top + "};\n")
    merged_geof.write("Physical Surface(\"left\", 5) = {" + left + "};\n")
    merged_geof.write("Physical Surface(\"right\", 6) = {" + right + "};\n")
    merged_geof.write("Physical Surface(\"obstacle\", 7) = {" + obstacle + "};\n")
    merged_geof.write("Physical Volume(\"fluid\", 8) = {" + fluid + "};\n")
    merged_geof.close()
    # Center matrix around 0:
    Lz05 = (I-1)*W/2
    disp =  [0, 0, -Lz05]
    copy(merged_geo_name, merged_geo_name, disp, 0)
    return lelg #lelg*N


def create_json_bcs(gmsh_inputs, case, jsonbcpath):
    h = float(gmsh_inputs['geometry']['h'])
    I = int(gmsh_inputs['matrix']['I'])
    J = int(gmsh_inputs['matrix']['J'])
    Wtot = float(gmsh_inputs['geometry']['R_W_h'])*I*h
    Ltot = (float(gmsh_inputs['geometry']['R_Lin_h']) + float(gmsh_inputs['matrix']['R_L_h'])*(J-1) + float(gmsh_inputs['geometry']['R_Lout_h']))*h
    if case == "channel":
        bcs = {
            "surfaces": {
                "wall": {
                    "bc": "W",
                    "sidesets": [3, 4, 7]},
                "perx": {
                    "bc": "P",
                    "sidesets": [1, 2],
                    "vector": [Ltot, 0.0, 0.0]
                },
                "perz": {
                    "bc": "P",
                    "sidesets": [5, 6],
                    "vector": [0.0, 0.0, Wtot]
                }
            }
        }
    elif case == "bl":
        bcs = {
            "surfaces": {
                "wall": {
                    "bc": "W",
                    "sidesets": [3, 7]
                },
                "inlet": {
                    "bc": "v",
                    "sidesets": 1
                },
                "outlet": {
                    "bc": "O",
                    "sidesets": 2
                },
                "moving_wall": {
                    "bc": "v",
                    "sidesets": [4]
                },
                "perz": {
                    "bc": "P",
                    "sidesets": [5, 6],
                    "vector": [0.0, 0.0, Wtot]
                }
            }
        }
    with open(jsonbcpath, 'w') as fp:
        json.dump(bcs, fp)

if __name__ == '__main__':
    sdir = os.path.dirname(sys.argv[0])

    geo_json = sys.argv[1]
    case = sys.argv[2]
    geo_out = sys.argv[3]
    mesh_info = sys.argv[4]
    bc_json = sys.argv[5]
    base_geo = sdir + '/box.geo'


    with open(geo_json, 'r') as rj:
        geom_info = json.load(rj)

    lelg = create_matrix(base_geo, geom_info, geo_out, case)

    # To connect to Nek5000RunDir
    with open(mesh_info, 'w') as fp:
        json.dump({'SIZE': {'lelg': lelg}}, fp)

    create_json_bcs(geom_info, case, bc_json)