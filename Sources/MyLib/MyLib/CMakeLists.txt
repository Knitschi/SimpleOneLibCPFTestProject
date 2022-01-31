
include(cpfAddCppPackageComponent)


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
	BRIEF_DESCRIPTION		"A C++ library used for testing the CPF"
	TYPE					LIB
	PUBLIC_HEADER			${PACKAGE_PUBLIC_HEADER}
	PRODUCTION_FILES		${PACKAGE_PRODUCTION_FILES}
	PUBLIC_FIXTURE_HEADER	${PACKAGE_PUBLIC_FIXTURE_HEADER}
	FIXTURE_FILES			${PACKAGE_FIXTURE_FILES}
	TEST_FILES				${PACKAGE_TEST_FILES}
)
