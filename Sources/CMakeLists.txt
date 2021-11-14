# Root CMakeLists file for the SimpleOneLibCPFTestProject

include("CPFCMake/cpfInitCIProject.cmake")

cmake_minimum_required (VERSION ${CPF_MINIMUM_CMAKE_VERSION}) 

project(SimpleOneLibCPFTestProject)

cpfAddPackages(GLOBAL_FILES "${CPF_ROOT_DIR}/conanfile.py")

