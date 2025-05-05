#!/bin/bash

top_dir=$PWD
cfms_dir=$PWD/cFMS
install_fms=$cfms_dir/FMS/LIBFMS

export FC=mpif90
export CC=mpicc

cd $cfms_dir/FMS
autoreconf -iv
export FCFLAGS="$FCFLAGS -fPIC"
export CFLAGS="$CFLAGS -fPIC"
./configure --enable-portable-kinds --with-yaml --prefix=$install_fms
make install

cd ..

export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:$install_fms/lib"
export FCFLAGS="$FCFLAGS -I$install_fms/include"
export CFLAGS="$CFLAGS -I$install_fms/include"
export LDFLAGS="$LDFLAGS -lFMS -L$install_fms/lib"

autoreconf -iv
./configure --prefix=$top_dir/pyfms/cLIBFMS
make install
