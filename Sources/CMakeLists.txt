# Root CMakeLists file for the SimpleOneLibCPFTestProject

include("external/CPFCMake/cpfInitCIProject.cmake")

cmake_minimum_required (VERSION ${CPF_MINIMUM_CMAKE_VERSION}) 

# Set hardcoded options
set(CPF_ENABLE_PRECOMPILED_HEADER TRUE)

project(SimpleOneLibCPFTestProject)

devMessage("${CMAKE_MAKE_PROGRAM}")


cpfAddPackages(GLOBAL_FILES "${CPF_ROOT_DIR}/conanfile.py")

