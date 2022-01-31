
include(cpfAddDoxygenPackageComponent)

set( sources
    ProjectDocumentation.dox
)

cpfAddDoxygenPackageComponent(
    SOURCES ${sources}
    DOXYGEN_CONFIG_FILE "${CMAKE_CURRENT_SOURCE_DIR}/DoxygenConfig.txt"
    DOXYGEN_LAYOUT_FILE "${CMAKE_CURRENT_SOURCE_DIR}/DoxygenLayout.xml"
    DOXYGEN_STYLESHEET_FILE "${CMAKE_CURRENT_SOURCE_DIR}/DoxygenStylesheet.css"
    DOXYGEN_BIN_DIR ${CPF_DOXYGEN_DIR}
)
