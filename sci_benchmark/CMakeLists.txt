cmake_minimum_required(VERSION 3.4...3.18)
project(cmake_example)

add_subdirectory(pybind11)
pybind11_add_module(pybind11_func src/pybind11_func.cpp)

# EXAMPLE_VERSION_INFO is defined by setup.py and passed into the C++ code as a
# define (VERSION_INFO) here.
target_compile_definitions(pybind11_func
                           PRIVATE VERSION_INFO=${EXAMPLE_VERSION_INFO})


install(
    TARGETS pybind11_func
    LIBRARY DESTINATION .
)

find_package(Python 3.8 COMPONENTS Interpreter Development.Module REQUIRED)

if (NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
  set(CMAKE_BUILD_TYPE Release CACHE STRING "Choose the type of build." FORCE)
  set_property(CACHE CMAKE_BUILD_TYPE PROPERTY STRINGS "Debug" "Release" "MinSizeRel" "RelWithDebInfo")
endif()

add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/nanobind)
# Detect the installed nanobind package and import it into CMake

nanobind_add_module(nanobind_func src/nanobind_func.cpp)
install(
    TARGETS nanobind_func 
    LIBRARY DESTINATION .
)
