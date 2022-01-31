include(cpfPackageProject)

cpfPackageProject(
    BRIEF_DESCRIPTION "A C++ library used for testing the CPF and some documentation."
    LONG_DESCRIPTION "Put a long description in here ..."
    OWNER Knitschi
    TARGET_NAMESPACE mylib
    COMPONENTS
        documentation
        MyLib
	PACKAGE_ARCHIVES
		PACKAGE_ARCHIVE_CONTENT_TYPE 	CT_DEVELOPER
		PACKAGE_ARCHIVE_FORMATS 		7Z
)
