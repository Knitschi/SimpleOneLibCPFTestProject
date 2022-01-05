import platform
import os
from conans import ConanFile
#from conan.tools.cmake import CMake
#from conan.tools.cmake import CMakeToolchain
#from conan.tools.layout import cmake_layout
from conans.tools import os_info, SystemPackageTool
from conan.tools.cmake import CMakeToolchain
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
        "CPF_CONFIG": "ANY",
        "CPF_INHERITED_CONFIG": "ANY",
        "build_target": "ANY",
        "install_target": "ANY",
        "CMAKE_GENERATOR": "ANY",
        "CMAKE_MAKE_PROGRAM": "ANY"
    }

    default_options = {
        "shared": True,
        "CPF_CONFIG": "VS2019-shared-debug",
        "CPF_INHERITED_CONFIG": "PlatformIndependent",
        "build_target": "pipeline",
        "install_target": "install_MyLib",
        "CMAKE_MAKE_PROGRAM": ""
    }

    # Dependencies
    tool_requires = "cmake/3.20.4", "doxygen/1.8.17"

    generators = "cmake"
    #generators = "CMakeToolchain" "CMakeDeps" # according to mateusz the future default generators.

    def source(self):
        self.run("git clone --recursive https://github.com/Knitschi/SimpleOneLibCPFTestProject.git {0}".format(self.source_folder))
        self.run("cd {0} && git checkout {1}".format(self.source_folder, self.version))

    def generate(self):
        """
        We use conans imports step to do the CPF configure step because the CPF configure step requires
        the directories to the dependencies that are only available after dependencies have been installed.
        This also alows developers to run the conan import step instead of the CPF 0_CopyScripts
        and 1_Configure steps. After that they can rely on the normal CPF workflow and need no
        other conan commands.
        """
        python = python_command()

        # The cwd is the conan install directory in this method.
        cpf_root_dir = os.getcwd().replace("\\","/") + "/../.." # This is used when running conan install.
        if self.source_folder:  # This is used when running conan create.
            cpf_root_dir = self.source_folder.replace("\\","/")

        # Sadly the package folder is not available at this point, so we use an intermediate install prefix and copy the files
        # to the package folder in an extra step.
        install_prefix = cpf_root_dir + "/install"
        test_files_dir = cpf_root_dir + "/Tests/" + str(self.options.CPF_CONFIG)

        # Generate cmake toolchain file.
        tc = CMakeToolchain(self)
        tc.generate()
        toolchain_file = self.install_folder.replace("\\","/") + "/conan_toolchain.cmake"

        # Install Buildscripts
        self.run("{0} ./Sources/external/CPFBuildscripts/0_CopyScripts.py --CPFCMake_DIR Sources/external/CPFCMake --CIBuildConfigurations_DIR Sources/external/CIBuildConfigurations".format(python), cwd=cpf_root_dir)
        
        # Configure
        configure_command = "{0} 1_Configure.py {1} --inherits {2}".format(python, self.options.CPF_CONFIG, self.options.CPF_INHERITED_CONFIG) \
            + " -DCMAKE_INSTALL_PREFIX=\"{0}\"".format(install_prefix) \
            + " -DCPF_TEST_FILES_DIR=\"{0}\"".format(test_files_dir) \
            + " -DCMAKE_TOOLCHAIN_FILE=\"{0}\"".format(toolchain_file) \
            + " -DCMAKE_GENERATOR=\"{0}\"".format(self.options.CMAKE_GENERATOR) \
            + " -DCMAKE_MAKE_PROGRAM=\"{0}\"".format(self.options.CMAKE_MAKE_PROGRAM) 
            #+ " -D=\"{0}\"".format(toolchain_file) \


        self.run(configure_command, cwd=cpf_root_dir)

    def build(self):
        python = python_command()
        # Generate
        self.run("{0} 3_Generate.py {1} --clean".format(python, self.options.CPF_CONFIG))
        # Build
        self.run("{0} 4_Make.py {1} --target {2} --config {3}".format(
            python,
            self.options.CPF_CONFIG,
            self.options.build_target,
            self.settings.build_type
            ))
 
    def package(self):
        # Copy files into install tree.
        python = python_command()
        self.run("{0} 4_Make.py {1} --target {2} --config {3}".format(
            python,
            self.options.CPF_CONFIG,
            self.options.install_target,
            self.settings.build_type
            ))
        # Copy files to package directory
        self.copy("*", src="install")
 
 
    @property
    def _postfix(self):
        return self.options.debug_postfix if self.settings.build_type == "Debug" else ""
 
    def package_info(self):
        self.cpp_info.libdirs = ["lib"]
        self.cpp_info.bindirs = [""]
        self.cpp_info.includedirs = ["include"]

def python_command():
    if platform.system() == 'Windows':
        return 'python'
    else:
        return 'python3'


