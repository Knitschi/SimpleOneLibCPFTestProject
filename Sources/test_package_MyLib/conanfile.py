from conans import ConanFile

class MyLibTest(ConanFile):

    # Dependencies
    python_requires =  "CPFConanfile/0.0.20@knitschi/development", "CPFPackageTestConanfile/0.0.4@knitschi/development",
    python_requires_extend = "CPFConanfile.CPFBaseConanfile", "CPFPackageTestConanfile.CPFBasePackageTestConanfile", 

    cpf_conanfile_module = None

    def init(self):
        self.cpf_conanfile_module = self.python_requires["CPFPackageTestConanfile"].module
        self.cpf_conanfile_module.init_impl(
            self,
            self.cpf_conanfile_module.CPFBasePackageTestConanfile,
            "MyLib")



