# **`fms2py`**

## **Installation**
pyFMS requires a compiled `cFMS` library.  If `cFMS` is not installed on the user's
local system, the library can be installed by 

```
1.  git clone --recursive https://github.com/NOAA-GFDL/pyFMS.git
2.  cd pyFMS
3.  modify ./compile.py as instructed in Section compile.py
4.  python ./compile.py
``` 

The script `compile.py` will first compile the FMS library within the cFMS submodule
directory.  Then, `compile.py` will compile the cFMS library linking to the just
compiled FMS library.  By default, installations are located in `pyFMS/lib` directory.

Upon `import pyfms` in your program, pyFMS will automatically load the cFMS library
in `pyFMS/lib`.  If the cFMS library does not exist, or if you want to load your own
installation of cFMS, the following should be set before invoking any pyFMS methods:

```
import pyfms

pyfms.cfms.init(libpath=path_to_cfms/libcFMS.so)
```

## compile.py
In order to compile cFMS, users will need to specify the following:

1.  Fortran and C compilers, for example, as shown below:

```
FC = "mpif90"
CC = "mpicc"
```

2.  Path to the libyaml and netCDF installations, for example, as shown below:

```
yaml = "/opt/libyaml/0.2.5/GNU/14.2.0/"
netcdf = "/opt/netcdf/4.9.3/GNU/14.2.0/"
```

