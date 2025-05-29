# **`fms2py`**

## **Installation**
pyFMS requires a compiled `cFMS` library and the pyFMS repository contains
cFMS as a submodule.  If `cFMS` is not installed on the user's
local system, the library can be installed by 

```
1.  git clone --recursive https://github.com/NOAA-GFDL/pyFMS.git
2.  cd pyFMS
3.  emacs ./compile.py (see Section compile.py)
4.  python ./compile.py
``` 

The script `compile.py` will first compile and install the FMS library (which is 
a submodule in cFMS) to `pyfms/lib/FMS`.   Then, compile.py will compile the cFMS library
linking to FMS in `pyfms/lib/FMS`.  cFMS will be installed to `pyfms/lib/cFMS`.

Upon `import pyfms`, pyFMS will automatically load the cFMS library
in `pyfms/lib/cFMS`.  If the cFMS library does not exist, or if users wish to load a 
diferent instance of cFMS, the following should be set in the program before invoking
any pyFMS methods:

```
import pyfms

pyfms.cfms.init(libpath=path_to_cfms/libcFMS.so)
```

## compile.py
To compile cFMS with the script `compile.py`, users will need to specify the following
fields:

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

