# Root CMakeLists file for the "CMakeProjectFramework"
cmake_minimum_required (VERSION 3.8.0) 

include("CPFCMake/Functions/cpfAddPackages.cmake")
# make sure the compiler is set before the project call
include("${CMAKE_TOOLCHAIN_FILE}")

project(SimpleOneLibCPFTestProject)

cpfAddPackages()

