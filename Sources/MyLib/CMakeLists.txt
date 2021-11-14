
include(cpfInitPackageProject)
include(cpfAddCppPackage)

cpfInitPackageProject(
	TARGET_NAMESPACE mylib
)

set( briefDescription "A C++ library used for testing the CPF" )
set( longDescription "Put a long description in here ..." )


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

set(PACKAGE_LINKED_LIBRARIES
)

set(PACKAGE_LINKED_TEST_LIBRARIES
)

set( archiveDevPackageOptions
	DISTRIBUTION_PACKAGE_CONTENT_TYPE 	CT_DEVELOPER
	DISTRIBUTION_PACKAGE_FORMATS 		7Z
)

############################################## Add Package #################################
cpfAddCppPackage( 
	OWNER					"Dummy Owner"
	TYPE					LIB
	BRIEF_DESCRIPTION		${briefDescription}
	LONG_DESCRIPTION		${longDescription}
	PUBLIC_HEADER			${PACKAGE_PUBLIC_HEADER}
	PRODUCTION_FILES		${PACKAGE_PRODUCTION_FILES}
	PUBLIC_FIXTURE_HEADER	${PACKAGE_PUBLIC_FIXTURE_HEADER}
	FIXTURE_FILES			${PACKAGE_FIXTURE_FILES}
	TEST_FILES				${PACKAGE_TEST_FILES}
	LINKED_LIBRARIES		${PACKAGE_LINKED_LIBRARIES}
	LINKED_TEST_LIBRARIES	${PACKAGE_LINKED_TEST_LIBRARIES}
	DISTRIBUTION_PACKAGES 	${archiveDevPackageOptions}
)
