import subprocess
from typing import List

from setuptools import find_namespace_packages, setup
from setuptools.command.install import install


class CustomInstall(install):
    def run(self):
        # subprocess.run(["./compile_c_libs.sh"], capture_output=True, text=True)
        with open("install.log", "w") as f:
            subprocess.run(["./compile_c_libs.sh"], stdout=f)
        install.run(self)

def local_pkg(name: str, relative_path: str) -> str:
    """Returns an absolute path to a local package."""
    path = f"{name} @ file://{Path(os.path.abspath(__file__)).parent / relative_path}"
    return path


test_requirements = ["pytest", "pytest-subtests", "coverage"]
develop_requirements = test_requirements + ["pre-commit"]

extras_requires = {
    "test": test_requirements,
    "develop": develop_requirements,
}

requirements: List[str] = [
    "dacite",
    "h5netcdf",
    "numpy",
    "pyyaml",
    "xarray",
    "mpi4py==3.1.5",
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
    cmdclass={"install": CustomInstall},
    include_package_data=True,
    url="https://github.com/fmalatino/pyFMS.git",
    version="2024.12.0",
    zip_safe=False,
)
