cmake_minimum_required(VERSION 3.18)

project(pyfms LANGUAGES C Fortran)

include(FetchContent)

set(CMAKE_POSITION_INDEPENDENT_CODE ON)

FetchContent_Declare(
    cFMS
    GIT_REPOSITORY https://github.com/fmalatino/cFMS.git
    GIT_TAG cmake
)
FetchContent_MakeAvailable(cFMS)

install(TARGETS cFMS DESTINATION ${SKBUILD_PLATLIB_DIR})
