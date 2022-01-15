# This package contains files that provide build-configurations for the CI-Build-Server.
include(cpfPackageProject)
include(cpfAddFilePackageComponent)

cpfPackageProject(
	TARGET_NAMESPACE CIConfig
	COMPONENTS SINGLE_COMPONENT
)

set(files
	cpfCIBuildConfigurations.json
)

cpfAddFilePackageComponent(
	SOURCES "${files}"
)

cpfFinalizePackageProject()