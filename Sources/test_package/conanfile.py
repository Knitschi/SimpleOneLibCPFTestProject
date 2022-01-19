import os
import glob
import shutil

from conans import ConanFile, tools, CMake
from conan.tools.layout import cmake_layout
from conan.tools.cmake import CMakeDeps
from conan.tools.cmake import CMakeToolchain



class HelloTestConan(ConanFile):

    python_requires = "CPFConanfile/0.0.1@knitschi/development",
    python_requires_extend = "CPFConanfile.CPFBaseConanfile",

    def configure(self):
        self.options["MyLib"].shared = self.options.shared

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
            lib_path = self.deps_cpp_info["MyLib"].rootpath
            for file in glob.glob(r'*.dll', root_dir=lib_path):
                abs_file_path = lib_path + "/" +  file
                shutil.copy(abs_file_path, dest_dir)

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
        print(cmake_generate_command)

        # CMake build
        self.run(cmake_generate_command)

        self.run(self._vcvars_command() + "cmake --build . --config {0}".format(self.settings.build_type))

    def layout(self):
        cmake_layout(self)

    def test(self):
        if not tools.cross_building(self):
            cmd = os.path.join(self.get_runtime_output_directory(), "example")
            self.run(cmd, env="conanrun")



