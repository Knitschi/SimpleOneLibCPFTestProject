import os

from conans import ConanFile, tools, CMake
from conan.tools.layout import cmake_layout
from conan.tools.cmake import CMakeDeps
from conan.tools.cmake import CMakeToolchain



class HelloTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared" : [True, False]
    }

    generators = "cmake"
    apply_env = False

    def imports(self):
        self.copy("*.dll", "build/" + str(self.settings.build_type), "MyLib")

    def generate(self):
        # Generate cmake toolchain file.
        tc = CMakeToolchain(self)
        tc.generate()

    def build(self):

        self.toolchain_file = self.install_folder.replace("\\","/") + "build/conan/conan_toolchain.cmake"

        # Run CMake
        cmake = CMake(self)
        cmake.definitions["MyLib_DIR"] = self.deps_cpp_info["MyLib"].rootpath + "/lib/cmake/MyLib"
        cmake.definitions["CMAKE_TOOLCHAIN_FILE"] = self.toolchain_file
        cmake.configure()
        cmake.build()

    def layout(self):
        cmake_layout(self)

    def test(self):
        if not tools.cross_building(self):
            cmd = os.path.join(self.cpp.build.bindirs[0], "example")
            self.run(cmd, env="conanrun")



