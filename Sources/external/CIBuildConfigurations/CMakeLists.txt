# This package contains files that provide build-configurations for the CI-Build-Server.
include(cpfPackageProject)
include(cpfAddFilePackageComponent)

cpfPackageProject(
	TARGET_NAMESPACE CIConfig
	COMPONENTS SINGLE_COMPONENT
)

set(files
	Clang-shared-debug.config.cmake
	Clang-static-release.config.cmake
	cpfCIBuildConfigurations.json
	Gcc-shared-debug.config.cmake
	README.rst
	VS2019-shared.config.cmake
	VS2019-shared-debug.config.cmake
	VS2019-static-release.config.cmake
)

cpfAddFilePackageComponent(
	SOURCES "${files}"
)

cpfFinalizePackageProject()