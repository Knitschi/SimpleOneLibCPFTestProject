import platform
from conans import ConanFile
#from conan.tools.cmake import CMake
#from conan.tools.cmake import CMakeToolchain
#from conan.tools.layout import cmake_layout
from conans.tools import os_info, SystemPackageTool
from pathlib import PurePath, PurePosixPath

class BuildCPFAssistantConan(ConanFile):
    name = "MyLib"
    url = "https://github.com/Knitschi/SimpleOneLibCPFTestProject"
    license = "MIT"
    description = "A package that is created by the SimpleOneLibCPFTestProject repository."

    # Binary configuration
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "CPF_INHERITED_CONFIG": ["VS2019-shared-debug","VS2019-static-release", "MSVC2019", "Gcc-shared-debug", "Clang-static-release"],
        "CPF_CONFIG": "ANY",
        "debug_postfix": "ANY"
    }

    default_options = {
        "shared": True,
        "CPF_INHERITED_CONFIG": "VS2019-shared-debug",
        "CPF_CONFIG": "VS2019-shared-debug",
        "debug_postfix": "-debug"
    }

    # Dependencies
    tool_requires = "cmake/3.20.4", "doxygen/1.8.17"

    generators = "cmake"
    #generators = "CMakeToolchain" "CMakeDeps" # according to mateusz the future default generators.

    def source(self):
        self.run("git clone --recursive https://github.com/Knitschi/SimpleOneLibCPFTestProject.git {0}".format(self.source_folder))
        #self.run("cd {0} && git checkout {1}".format(self.source_folder, self.version))

    def build(self):
        installPathPosix = self.package_folder.replace("\\","/")
        python = python_command()

        self.run("{0} ./Sources/external/CPFBuildscripts/0_CopyScripts.py --CPFCMake_DIR Sources/external/CPFCMake --CIBuildConfigurations_DIR Sources/external/CIBuildConfigurations".format(python))
        self.run("{0} 1_Configure.py {1} --inherits {2} -DCMAKE_INSTALL_PREFIX=\"{3}\"".format(
            python,
            self.options.CPF_CONFIG,
            self.options.CPF_INHERITED_CONFIG,
            installPathPosix
        ))
        self.run("{0} 3_Generate.py {1} --clean".format(python, self.options.CPF_CONFIG))
        self.run("{0} 4_Make.py {1} --target MyLib --config {2}".format(python, self.options.CPF_CONFIG, self.settings.build_type))
 
    def package(self):
        python = python_command()
        self.run("{0} 4_Make.py {1} --target install_MyLib --config {2}".format(python, self.options.CPF_CONFIG, self.settings.build_type))
 
 
    @property
    def _postfix(self):
        return self.options.debug_postfix if self.settings.build_type == "Debug" else ""
 
    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", "MyLib")
        self.cpp_info.set_property("cmake_target_name", "MyLib")
        self.cpp_info.set_property("cmake_target_namespace", "mylib")
        self.cpp_info.libs = ["MyLib{}".format(self._postfix)]
        self.cpp_info.libdirs = ["MyLib/lib"]
        self.cpp_info.bindirs = ["MyLib"]
        self.cpp_info.includedirs = ["MyLib/include"]
        self.cpp_info.cmake_target_name = "MyLib"
        self.cpp_info.pkg_config_name = "MyLib"

        #self.cpp_info.components["MyLib"].names["cmake_find_package"] = "MyLib"
        #self.cpp_info.components["MyLib"].names["cmake_find_package_multi"] = "MyLib"
        #self.cpp_info.components["MyLib"].names["cmake_find_package"] = "MyLib"
        #self.cpp_info.components["MyLib"].set_property("cmake_target_name", "MyLib")
        #self.cpp_info.components["MyLib"].set_property("pkg_config_name", "MyLib")

        #self.cpp_info.components["MyLib"].libs = ["MyLib{}".format(self._postfix)]
        #self.cpp_info.components["MyLib"].libdirs = ["MyLib/lib"]
        #self.cpp_info.components["MyLib"].bindirs = ["MyLib"]
        #self.cpp_info.components["MyLib"].includedirs = ["MyLib/include"]
        
        #self.cpp_info.components["MyLib"].requires = [""]

def python_command():
    if platform.system() == 'Windows':
        return 'python'
    else:
        return 'python3'


