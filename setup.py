from setuptools import find_namespace_packages, setup


test_requirements = [
    "pytest",
    "pytest-subtests",
    "coverage",
    "xarray",
    "netCDF4",
    "h5netcdf",
]
develop_requirements = test_requirements + ["pre-commit"]

extras_requires = {
    "test": test_requirements,
    "develop": develop_requirements,
}

requirements = ["dacite", "numpy", "pyyaml", "mpi4py"]

setup(
    author="NOAA/GFDL",
    python_requires=">=3.11",
    classifiers=[
        "Development Status :: 1 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
    ],
    install_requires=requirements,
    extras_require=extras_requires,
    name="pyfms",
    license="",
    packages=find_namespace_packages(include=["pyfms", "pyfms.*"]),
    include_package_data=True,
    url="https://github.com/NOAA-GFDL/pyFMS.git",
    version="2024.12.0",
    zip_safe=False,
)
