#!/bin/bash

set -xe

pyfms_dir=$PWD/pyfms
cfms_dir=$PWD/cFMS
install_fms=$cfms_dir/FMS/LIBFMS

export FC=mpif90
export CC=mpicc

cd $cfms_dir/FMS
autoreconf -iv
export FCFLAGS="$FCFLAGS `nf-config --fflags` -fPIC"
export CFLAGS="$CFLAGS `nc-config --cflags` -fPIC"
./configure --enable-portable-kinds --with-yaml --prefix=$install_fms
make install

cd ..

export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:$install_fms/lib"
export FCFLAGS="$FCFLAGS -I$install_fms/include"
export CFLAGS="$CFLAGS -I$install_fms/include"
export LDFLAGS="$LDFLAGS -lFMS -L$install_fms/lib"

autoreconf -iv
./configure --with-fms=$install_fms --prefix=$pyfms_dir/cLIBFMS
make install
