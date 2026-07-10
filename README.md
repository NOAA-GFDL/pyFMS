# pyFMS

The `pyFMS` package is a Python-C-Fortran interface (through the use of the `ctypes` package), for access to select methods from the [Flexible Modeling System](https://github.com/NOAA-GFDL/FMS.git) (`FMS`) developed by NOAA/GFDL.

## Quickstart - bare metal

### Build

The build backend of `pyFMS` is `scikit-build-core`, which allows for the compilation of extension modules for Python packages through CMake.

`pyFMS` requires:

- GCC > 9.2 (C and Fortran compiler)
- MPI
- Python 3.12
- CMake >= 3.18

To clone `pyFMS` from its GitHub repository:

```shell
git clone https://github.com/NOAA-GFDL/pyFMS.git
```

We recommend creating a Python `venv` or `conda` environment for your installation.

```shell
python -m venv <name_of_environment>
source .<name_of_environment>/bin/activate
```

Inside of your Python environment, to install `pyFMS` and its dependencies:

```shell
pip install .[install_options]
```

The available `install_options` are:

- `test`
- `dev` (which installs the `test` dependencies as well)
- `extras` (which installs the `dev` dependencies as well)

For developers we suggest installing with the editable flag `-e` and the verbose flag `-v`:

```shell
pip install -v -e .[dev]
```

use of the editable installation method will allow updates to the Python source code to be reflected in the installation without re-installing. Subsequent installs of `pyFMS` will recompile all extension modules, due to the methods of compilation used by `scikit-build-core`.

The `CMakeLists.txt` file will be accessed by the build backend during the installation to compile the necessary shared object file from the C-Fortran interface, `cFMS`, to be loaded by the `ctypes` package for use by `pyFMS`.

### Editing the extension modules of pyFMS

If you require a different version of `cFMS` and/or its dependency `FMS`, depending on the use case, two methods of use are available:

1. Edit the `CMakeLists.txt` file to point to the repository containing your custom `cFMS` and/or `FMS` to install it alongside `pyFMS` through the methods outlined above
2. Perform a separate compilation of `cFMS` and/or `FMS` outside of the provided build tools and point to the desired shared object file when running `pyfms.cfms.init(libpath=<path_to_shared_object_library>)`

## pyFMS as a dependency

This package can be treated like any Python package when used needed as a dependency; ensure it is defined as a dependency for your project, and import as usual.
Subsequent installs of the dependent package will not trigger a recompilation of the extension modules of pyFMS, unless directly called to due so by a reinstall of pyFMS, as the dependency manager of the build backend for the dependent project will see the requirements of pyFMS are satisfied. If an editable version of pyFMS is needed for the dependent package, please use the method of editable install detailed above.
