#!/bin/bash

outdir="outputs"
rm -rf ${outdir}
mkdir ${outdir}

############
# GEOMETRY #
############

# INPUTS
geo_json="./obstacle_geo/sample_io/geom.json"
geo_case="bl" # or channel

# OUTPUTS
geo_out="${outdir}/obstacle.geo"
mesh_info_json="${outdir}/mesh_info.json"
bc_json="${outdir}/bc.json"

# Create obstacle geometry
python3 obstacle_geo/obstacle_tools.py \
    ${geo_json} \
    ${geo_case} \
    ${geo_out} \
    ${mesh_info_json} \
    ${bc_json}


########
# MESH #
########

# INPUTS
mesh_geo=${geo_out}
# Spatial Dimensions
ndim="3" 
# Mesh Polynomial Order
order="2" # from 1 to 5
# Exported Mesh Format
# Options: auto msh1 msh2 msh22 msh3 msh4 msh40 msh41 msh
#          unv wrl mail stl p3d mesh bdf cgns med diff
#          ir3 inp ply2 celum su2 x3d dat neu m key
mformat="msh2" 

# OUTPUTS
mesh_out="${outdir}/obstacle.msh"

sudo docker run -i -v `pwd`:`pwd` -w `pwd` avidalto/nek5000:v25 /bin/bash \
    gmsh_gen/main.sh \
    python3 gmsh_gen/create.py ${mesh_geo} ${ndim} ${order} ${mformat} ${mesh_out}


######################
# CONVERT TO NEK5000 #
######################

# INPUTS
mesh_msh=${mesh_out}
obstacle_bc="gmsh2nek/sample_io/obstacle.bc"
ndim="3" # 2 or 3
mformat="1" # 1 = ASCII file and 2 = binary file
# Mesh tolerance for genmap
meshtol="0.2"

# OUTPUTS
obstacle_re2="${outdir}/obstacle.re2"
obstacle_ma2="${outdir}/obstacle.ma2"

sudo docker run -i -v `pwd`:`pwd` -w `pwd` avidalto/nek5000:v25 /bin/bash \
    gmsh2nek/main.sh \
    python3 gmsh2nek/gmsh2nek.py ${mesh_msh} ${obstacle_re2} ${obstacle_ma2} ${ndim} ${mformat} ${meshtol} ${obstacle_bc}



