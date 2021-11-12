import os

from conans import ConanFile, tools, CMake
#from conan.tools.cmake import CMake
from conan.tools.layout import cmake_layout
from conan.tools.cmake import CMakeDeps

class HelloTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    # VirtualBuildEnv and VirtualRunEnv can be avoided if "tools.env.virtualenv:auto_use" is defined
    # (it will be defined in Conan 2.0)
    #generators = "CMakeDeps", "CMakeToolchain", "VirtualBuildEnv", "VirtualRunEnv"
    generators = "cmake"
    apply_env = False

    def imports(self):
        self.copy("*.dll", "build/" + str(self.settings.build_type), "MyLib")

    def build(self):
        cmake = CMake(self)
        cmake.definitions["MyLib_DIR"] = self.deps_cpp_info["MyLib"].rootpath + "/MyLib/lib/cmake/MyLib"
        cmake.configure()
        cmake.build()

    def layout(self):
        cmake_layout(self)

    def test(self):
        if not tools.cross_building(self):
            cmd = os.path.join(self.cpp.build.bindirs[0], "example")
            self.run(cmd, env="conanrun")



