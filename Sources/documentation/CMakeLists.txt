
include(cpfInitPackageProject)
include(cpfAddDoxygenPackage)

cpfInitPackageProject(docs)

get_property( doxygenFiles TARGET CPFDoxygenConfig PROPERTY CPF_DOXYGEN_CONFIG_FILES)

cpfAddDoxygenPackage(
    ${doxygenFiles}
)

