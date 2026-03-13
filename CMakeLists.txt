cmake_minimum_required(VERSION 3.18)

project(pyfms LANGUAGES C Fortran)

include(FetchContent)

set(CMAKE_POSITION_INDEPENDENT_CODE ON)

find_library(cFMS_LIBRARY NAMES "libcFMS.so" PATHS ${SKBUILD_PLATLIB_DIR})

if(NOT cFMS_LIBRARY)
    message(STATUS "Did not find cFMS, using FetchContent to build")
    FetchContent_Declare(
        cFMS_LIBRARY
        GIT_REPOSITORY https://github.com/fmalatino/cFMS.git
        GIT_TAG cmake
    )
    FetchContent_MakeAvailable(cFMS_LIBRARY)
else()
    message(STATUS "Found cFMS library, including it in install")
    add_library(cFMS_LIBRARY SHARED IMPORTED)
    message(STATUS "Added cFMS_LIBRARY as a target")
    set_property(TARGET cFMS_LIBRARY PROPERTY IMPORTED_LOCATION ${SKBUILD_PLATLIB_DIR})
endif()

install(TARGETS cFMS_LIBRARY LIBRARY DESTINATION ${SKBUILD_PLATLIB_DIR})