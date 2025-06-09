#!/bin/bash

set -ex
#set -o posix

#yaml includes
YAML_FLAGS="-I/opt/libyaml/0.2.5/GNU/14.2.0/include"

#yaml libraries
YAML_LDFLAGS="-L/opt/libyaml/0.2.5/GNU/14.2.0/lib"

#fortran netcdf includes
NF_FLAGS=$(nf-config --fflags)

#c netcdf includes
NC_FLAGS=$(nc-config --cflags)

#netcdf libraries
NC_LDFLAGS=$(nc-config --libs | nf-config --flibs) 

#fortran and c compiler
FC=mpif90
CC=mpicc

#fms fortran, c, library compiler flags
FMS_FCFLAGS="$NF_FLAGS -fPIC"
FMS_CFLAGS="$NC_FLAGS $YAML_FLAGS -fPIC"
FMS_LDFLAGS="$NC_LDFLAGS $YAML_LDFLAGS"

#cfms fortran, c, library compiler flags
#cfms does not need the netcdf flags. 
#these will be removed once cfms configure.ac is updated
cFMS_FCFLAGS="-fPIC $NF_FLAGS"
cFMS_CFLAGS="-fPIC $NC_FLAGS"
cFMS_LDFLAGS=""

curr_dir=$PWD

#fms installation path
fms_install=$curr_dir/pyfms/lib/FMS

#cfms installation path
cfms_install=$curr_dir/pyfms/lib/cFMS

#cfms to compile
cfms_dir=$curr_dir/cFMS

#fms to compile
fms_dir=$cfms_dir/FMS

#compile fms with autotools
cd $fms_dir
autoreconf -iv
./configure --enable-portable-kinds \
            --with-yaml \
            --prefix=$fms_install \
            FC=$FC \
            CC=$CC \
            FCFLAGS="$FMS_FCFLAGS" \
            CFLAGS="$FMS_CFLAGS" \
            LDFLAGS="$FMS_LDFLAGS"
make install

cd $currdir

#compile cFMS with autotools
cd $cfms_dir
autoreconf -iv
./configure --with-fms=$fms_install \
            --prefix=$cfms_install \
            FC=$FC \
            CC=$CC \
            FCFLAGS="$cFMS_FCFLAGS" \
            CFLAGS="$cFMS_CFLAGS" \
            LDFLAGS="$cFMS_LDFLAGS"
make install

cd $currdir
    
