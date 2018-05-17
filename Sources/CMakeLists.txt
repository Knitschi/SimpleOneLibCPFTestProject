# Root CMakeLists file for the "CMakeProjectFramework"
cmake_minimum_required (VERSION 3.8.0) 

include("CPFCMake/Functions/cpfInit.cmake")
include("${CMAKE_TOOLCHAIN_FILE}")					# make sure the compiler is set before the project call


##################################### CREATE PROJECT ########################################
project(SimpleOneLibCPFTestProject)
cpfInit()

####################################### ADD Packages #############################################

set( externalPackages
	cotire
	CPFCMake
	CPFBuildscripts
)

set( globalFiles
	documentation/ProjectDoc.dox
)

cpfAddPackages( "${externalPackages}" "${globalFiles}")
