
include(cpfPackageProject)
include(cpfAddCppPackageComponent)

cpfPackageProject(
    TARGET_NAMESPACE mylib
    COMPONENTS SINGLE_COMPONENT
	BRIEF_DESCRIPTION "A C++ library used for testing the CPF"
	LONG_DESCRIPTION "Put a long description in here ..."
	OWNER "Dummy Owner"
	DISTRIBUTION_PACKAGES
		DISTRIBUTION_PACKAGE_CONTENT_TYPE 	CT_DEVELOPER
		DISTRIBUTION_PACKAGE_FORMATS 		7Z
)

set( PACKAGE_PUBLIC_HEADER
	function.h
)

set( PACKAGE_PRODUCTION_FILES
	function.cpp
)

set( PACKAGE_PUBLIC_FIXTURE_HEADER
	fixture.h
)

set( PACKAGE_FIXTURE_FILES
	fixture.cpp
)
	
set( PACKAGE_TEST_FILES
	test_main.cpp
)

############################################## Add Package #################################
cpfAddCppPackageComponent( 
	TYPE					LIB
	PUBLIC_HEADER			${PACKAGE_PUBLIC_HEADER}
	PRODUCTION_FILES		${PACKAGE_PRODUCTION_FILES}
	PUBLIC_FIXTURE_HEADER	${PACKAGE_PUBLIC_FIXTURE_HEADER}
	FIXTURE_FILES			${PACKAGE_FIXTURE_FILES}
	TEST_FILES				${PACKAGE_TEST_FILES}
)
