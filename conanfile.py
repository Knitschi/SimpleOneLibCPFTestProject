from conans import ConanFile

class SimpleOneLibCPFTestProject(ConanFile):
    
    name = "MyLib"
    url = "https://github.com/Knitschi/SimpleOneLibCPFTestProject"
    license = "MIT"
    description = "A package that is created by the SimpleOneLibCPFTestProject repository."

    # Dependencies
    python_requires = "CPFConanfile/0.0.1@knitschi/development",
    python_requires_extend = "CPFConanfile.CPFBaseConanfile",

    build_requires = "doxygen/1.8.17",

    cpf_conanfile_module = None

    def init(self):

        self.cpf_conanfile_module = self.python_requires["CPFConanfile"].module

        self.cpf_conanfile_module.init_impl(
            self,
            self.cpf_conanfile_module.CPFBaseConanfile,
            "https://github.com/Knitschi/SimpleOneLibCPFTestProject.git",
            path_CPFCMake='Sources/external/CPFCMake',
            path_CPFBuildscripts='Sources/external/CPFBuildscripts',
            path_CIBuildConfigurations = 'Sources/CIBuildConfigurations'
            )
