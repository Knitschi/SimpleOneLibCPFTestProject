
include(${CMAKE_CURRENT_LIST_DIR}/../CPFCMake/DefaultConfigurations/Linux.config.cmake)

set(CPF_CONFIG "Gcc" CACHE STRING "the config name" FORCE)

set( CMAKE_BUILD_TYPE "Debug" CACHE STRING "The compile configuration used by single configuration make tools." FORCE)
set( BUILD_SHARED_LIBS ON CACHE BOOL "Set this to ON to create all production target libraries as shared libries. The fixture libraries and libraries created for executables are always static libraries." FORCE)

# Locations
set( CPF_WEBPAGE_URL "" CACHE STRING "An url from which the distribution of the last build can be downloaded." FORCE)

