import subprocess
from typing import List

from setuptools import find_namespace_packages, setup
from setuptools.command.build import build


class CustomBuild(build):
    def run(self):
        with open("install.log", "w") as f:
            subprocess.run(["./compile_c_libs.sh"], stdout=f, check=True)
        build.run(self)


test_requirements = ["pytest", "pytest-subtests", "coverage"]
develop_requirements = test_requirements + ["pre-commit"]

extras_requires = {
    "test": test_requirements,
    "develop": develop_requirements,
}

requirements = [
    "dacite",
    "h5netcdf",
    "numpy",
    "pyyaml",
    "mpi4py",
    "xarray",
    "netcdf4",
]

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
    cmdclass={"build": CustomBuild},
    include_package_data=True,
    url="https://github.com/fmalatino/pyFMS.git",
    version="2024.02.0",
    zip_safe=False,
)
