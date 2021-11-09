from conans import ConanFile
#from conan.tools.cmake import CMake
#from conan.tools.cmake import CMakeToolchain
#from conan.tools.layout import cmake_layout
from conans.tools import os_info, SystemPackageTool

class BuildCPFAssistantConan(ConanFile):
    name = "MyLib"
    version = "0.1.15"
    url = "blub"
    license = "MIT"
    description = "A collection of Knitschis toy projects."

    # Binary configuration
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "CPF_INHERITED_CONFIG": ["VS2019-shared-debug","VS2019-static-release", "MSVC2019", "Gcc", "Clang"],
        "CPF_CONFIG": "ANY"
    }

    default_options = {
        "shared": True,
        "CPF_INHERITED_CONFIG": "VS2019-shared-debug",
        "CPF_CONFIG": "VS2019-shared-debug"
    }

    # Dependencies
    build_requires = "cmake/3.20.4", "doxygen/1.8.17"

    generators = "cmake"

    def source(self):
        self.run("git clone https://github.com/Knitschi/SimpleOneLibCPFTestProject.git {0}".format(self.source_folder))
        self.run("cd {0} && git checkout {1}".format(self.source_folder, self.version))

    def build(self):
        self.run("python ./Sources/CPFBuildScripts/0_CopyScripts.py")
        self.run("python 1_Configure.py {0} --inherits {1}".format(self.options.CPF_CONFIG, self.options.CPF_INHERITED_CONFIG))
        self.run("python 3_Generate.py {0}".format(self.options.CPF_CONFIG))
        self.run("python 4_Make.py {0} --target MyLib --config {1}".format(self.options.CPF_CONFIG, self.settings.build_type))
 
    def package(self):
        self.run("python 4_Make.py {0} --target install_MyLib --config {1}".format(self.options.CPF_CONFIG, self.settings.build_type))
 
 
    def package_info(self):
        self.cpp_info.libs = ["libStlUtilities"]



