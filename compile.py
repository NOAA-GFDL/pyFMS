import os
import subprocess

#path to the installed yaml library
yaml = "/opt/libyaml/0.2.5/GNU/14.2.0/"

#path to the installed netcdf library
netcdf = "/opt/netcdf/4.9.3/GNU/14.2.0/"

#Fortran compiler
FC = "mpif90"

#C compiler
CC  ="mpicc"

#default Fortran compiler flags
FMS_FCFLAGS = f"-I{yaml}/include -I{netcdf}/include -fPIC"

#default C compiler flags
FMS_CFLAGS = f"-I{yaml}/include -I{netcdf}/include -fPIC"

#library flags
FMS_LDFLAGS = f"-L{yaml}/lib -L{netcdf}/lib -lnetcdf"

cFMS_FCFLAGS = "-fPIC"
cFMS_CFLAGS = "-fPIC"
cFMS_LDFLAGS = ""

#current directory
currdir = os.path.dirname(__file__)

#absolute path to cFMS submodule
cFMS = f"{currdir}/cFMS"

#absolute path to FMS submodule
FMS = f"{cFMS}/FMS"

#absolue path to install libraries
cFMS_install = f"{currdir}/pyfms/lib/cFMS"
FMS_install = f"{currdir}/pyfms/lib/FMS"


def compile_FMS():

    """
    Install FMS to FMS_install
    """
    
    currdir = os.path.dirname(__file__)
    os.chdir(FMS)

    subprocess.run(["autoreconf", "-iv"])
    subprocess.run(["./configure",
                    "--enable-portable-kinds",
                    "--with-yaml",
                    f"FC={FC}",
                    f"CC={CC}",
                    f"FCFLAGS={FMS_FCFLAGS}",
                    f"CFLAGS={FMS_CFLAGS}",
                    f"LDFLAGS={FMS_LDFLAGS}",
                    f"--prefix={FMS_install}",                    
    ])
    subprocess.run(["make", "install"])

    os.chdir(currdir)


def compile_cFMS():

    """
    Install cFMS to cFMS_install
    """
    currdir = os.path.dirname(__file__)    
    os.chdir(cFMS)

    subprocess.run(["autoreconf", "-iv"])
    subprocess.run(["./configure",
                    f"--with-fms={FMS_install}",
                    f"FC={FC}",
                    f"CC={CC}",
                    f"FCFLAGS={cFMS_FCFLAGS}",
                    f"CFLAGS={cFMS_CFLAGS}",
                    F"LDFLAGS={cFMS_LDFLAGS}",
                    f"--prefix={cFMS_install}"
    ])
    subprocess.run(["make", "install"])

    os.chdir(currdir)


#compile
compile_FMS()
compile_cFMS()
