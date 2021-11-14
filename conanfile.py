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
        "CPF_INHERITED_CONFIG": ["VS2019-shared-debug","VS2019-static-release", "MSVC2019", "Gcc", "Clang"],
        "CPF_CONFIG": "ANY",
        "debug_postfix": "ANY",
        "CPF_DOXYGEN_DIR": "ANY"
    }

    default_options = {
        "shared": True,
        "CPF_INHERITED_CONFIG": "VS2019-shared-debug",
        "CPF_CONFIG": "VS2019-shared-debug",
        "debug_postfix": "-debug",
        "CPF_DOXYGEN_DIR": ""
    }

    # Dependencies
    build_requires = "cmake/3.20.4", "doxygen/1.8.17"

    generators = "cmake"
    #generators = "CMakeToolchain" "CMakeDeps" # according to mateusz the future default generators.

    def source(self):
        self.run("git clone --recursive https://github.com/Knitschi/SimpleOneLibCPFTestProject.git {0}".format(self.source_folder))
        #self.run("cd {0} && git checkout {1}".format(self.source_folder, self.version))

    def build(self):
        installPathPosixs = self.package_folder.replace("\\","/")

        self.run("python ./Sources/CPFBuildScripts/0_CopyScripts.py")
        self.run("python 1_Configure.py {0} --inherits {1} -DCMAKE_INSTALL_PREFIX=\"{2}\" -DCPF_DOXYGEN_DIR=\"{3}\"".format(
            self.options.CPF_CONFIG,
            self.options.CPF_INHERITED_CONFIG,
            installPathPosixs,
            self.deps_cpp_info["doxygen"].bindirs[0].replace("\\","/")
        ))
        self.run("python 3_Generate.py {0}".format(self.options.CPF_CONFIG))
        self.run("python 4_Make.py {0} --target MyLib --config {1}".format(self.options.CPF_CONFIG, self.settings.build_type))
 
    def package(self):
        self.run("python 4_Make.py {0} --target install_MyLib --config {1}".format(self.options.CPF_CONFIG, self.settings.build_type))
 
 
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


