
include(cpfInitPackageProject)
include(cpfAddDoxygenPackage)

cpfInitPackageProject()

set( sources
    ProjectDocumentation.dox
)

cpfAddDoxygenPackage(
    SOURCES ${sources}
    DOXYGEN_CONFIG_FILE "${CMAKE_CURRENT_SOURCE_DIR}/DoxygenConfig.txt"
    DOXYGEN_LAYOUT_FILE "${CMAKE_CURRENT_SOURCE_DIR}/DoxygenLayout.xml"
    DOXYGEN_STYLESHEET_FILE "${CMAKE_CURRENT_SOURCE_DIR}/DoxygenStylesheet.css"
)

