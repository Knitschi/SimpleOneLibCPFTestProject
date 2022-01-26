import os
import glob
import shutil
import pathlib

from conans import ConanFile, tools, CMake
from conan.tools.layout import cmake_layout
from conan.tools.cmake import CMakeDeps
from conan.tools.cmake import CMakeToolchain



class HelloTestConan(ConanFile):

    python_requires = "CPFConanfile/0.0.8@knitschi/development",
    python_requires_extend = "CPFConanfile.CPFBaseConanfile",

    def configure(self):
        # Hand options 1 to 1 down to the tested package to avoid a rebuild.
        self.options["MyLib"].CPF_CONFIG = self.options.CPF_CONFIG
        self.options["MyLib"].shared = self.options.shared
        self.options["MyLib"].build_target = self.options.build_target
        self.options["MyLib"].install_target = self.options.install_target
        self.options["MyLib"].CMAKE_C_COMPILER = self.options.CMAKE_C_COMPILER
        self.options["MyLib"].CMAKE_CXX_COMPILER = self.options.CMAKE_CXX_COMPILER
        self.options["MyLib"].CMAKE_GENERATOR = self.options.CMAKE_GENERATOR
        self.options["MyLib"].CMAKE_MAKE_PROGRAM = self.options.CMAKE_MAKE_PROGRAM
        self.options["MyLib"].CMAKE_EXPORT_COMPILE_COMMANDS = self.options.CMAKE_EXPORT_COMPILE_COMMANDS
        self.options["MyLib"].CPF_ENABLE_ABI_API_COMPATIBILITY_REPORT_TARGETS = self.options.CPF_ENABLE_ABI_API_COMPATIBILITY_REPORT_TARGETS
        self.options["MyLib"].CPF_ENABLE_ABI_API_STABILITY_CHECK_TARGETS = self.options.CPF_ENABLE_ABI_API_STABILITY_CHECK_TARGETS
        self.options["MyLib"].CPF_ENABLE_ACYCLIC_TARGET = self.options.CPF_ENABLE_ACYCLIC_TARGET
        self.options["MyLib"].CPF_ENABLE_CLANG_FORMAT_TARGETS = self.options.CPF_ENABLE_CLANG_FORMAT_TARGETS
        self.options["MyLib"].CPF_ENABLE_CLANG_TIDY_TARGET = self.options.CPF_ENABLE_CLANG_TIDY_TARGET
        self.options["MyLib"].CPF_ENABLE_OPENCPPCOVERAGE_TARGET = self.options.CPF_ENABLE_OPENCPPCOVERAGE_TARGET
        self.options["MyLib"].CPF_ENABLE_PACKAGE_DOX_FILE_GENERATION = self.options.CPF_ENABLE_PACKAGE_DOX_FILE_GENERATION
        self.options["MyLib"].CPF_ENABLE_TEST_EXE_TARGETS = self.options.CPF_ENABLE_TEST_EXE_TARGETS
        self.options["MyLib"].CPF_ENABLE_RUN_TESTS_TARGET = self.options.CPF_ENABLE_RUN_TESTS_TARGET
        self.options["MyLib"].CPF_ENABLE_VALGRIND_TARGET = self.options.CPF_ENABLE_VALGRIND_TARGET
        self.options["MyLib"].CPF_CLANG_TIDY_EXE = self.options.CPF_CLANG_TIDY_EXE
        self.options["MyLib"].CPF_CLANG_FORMAT_EXE = self.options.CPF_CLANG_FORMAT_EXE
        self.options["MyLib"].CPF_WEBSERVER_BASE_DIR = self.options.CPF_WEBSERVER_BASE_DIR
        self.options["MyLib"].CPF_TEST_FILES_DIR = self.options.CPF_TEST_FILES_DIR
        self.options["MyLib"].CPF_VERBOSE = self.options.CPF_VERBOSE

    def get_runtime_output_directory(self):
        return self.build_folder.replace("\\","/") + "/" + str(self.settings.build_type)

    def generate(self):
        # Generate cmake toolchain file.
        tc = CMakeToolchain(self)
        if self.options.CMAKE_GENERATOR == "Ninja":
            # Removes the CMAKE_GENERATOR_PLATFORM and CMAKE_GENERATOR_TOOLSET definitions which cause a CMake error when used with ninja.
            tc.blocks.remove("generic_system")
        tc.generate()


    def build(self):
        # Copy depended on dlls to runtime output directory.
        # For unknown reasons the import() function was not called so we do it here.
        if self.options.shared and self.settings.os == "Windows":
            dest_dir = self.get_runtime_output_directory()
            pathlib.Path(dest_dir).mkdir(parents=True, exist_ok=True)
            lib_path = self.deps_cpp_info["MyLib"].rootpath
            for file in glob.glob(r'*.dll', root_dir=lib_path):
                abs_file_path = lib_path + "/" +  file
                abs_dest_file_path = dest_dir + "/" +  file
                shutil.copyfile(abs_file_path, abs_dest_file_path)

        self.toolchain_file = self.build_folder.replace("\\","/") + "/conan/conan_toolchain.cmake"

        # CMake generate
        cmake_generate_command = self._vcvars_command() + "cmake -S.. -B . -G \"{0}\"".format(self.options.CMAKE_GENERATOR)
        cmake_generate_command += " -DMyLib_DIR=\"{0}\"".format(self.deps_cpp_info["MyLib"].rootpath + "/lib/cmake/MyLib")
        cmake_generate_command += " -DCMAKE_TOOLCHAIN_FILE=\"{0}\"".format(self.toolchain_file)
        if self.options.CMAKE_MAKE_PROGRAM != "":   # Setting an empty value here causes cmake errors.
            cmake_generate_command += " -DCMAKE_MAKE_PROGRAM=\"{0}\"".format(self.options.CMAKE_MAKE_PROGRAM)
        cmake_generate_command += " -DCMAKE_RUNTIME_OUTPUT_DIRECTORY_{0}=\"{1}\"".format(
            str(self.settings.build_type).upper(),
            self.get_runtime_output_directory())
        cmake_generate_command += " -DCMAKE_RUNTIME_OUTPUT_DIRECTORY=\"{1}\"".format(
            str(self.settings.build_type).upper(),
            self.get_runtime_output_directory())
        print(cmake_generate_command)

        # CMake build
        self.run(cmake_generate_command)

        self.run(self._vcvars_command() + "cmake --build . --config {0} --clean-first".format(self.settings.build_type))

    def layout(self):
        cmake_layout(self)

    def test(self):
        if not tools.cross_building(self):
            cmd = os.path.join(self.get_runtime_output_directory(), "example")
            self.run("\"" + cmd + "\"", env="conanrun")



