from conans import ConanFile, CMake, tools
import os

class TlExpectedConan(ConanFile):
    name = "tl-expected"
    version = "1.0.1"
    license = "CC0-1.0"
    homepage = "https://tl.tartanllama.xyz"
    url = "https://github.com/yipdw/conan-tl-expected"
    description = "C++11/14/17 std::expected with functional-style extensions"
    options = {
        "enable_tests": [True, False]
    }
    default_options = {
        "enable_tests": False
    }

    def source(self):
        git = tools.Git(folder="tl-expected")
        git.clone("https://github.com/TartanLlama/expected")
        git.checkout("6fe2af5191214cce620899f7f06585c047b9f1fc")

    def configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["EXPECTED_ENABLE_TESTS"] = self.options.enable_tests
        cmake.configure(source_folder="tl-expected")

        return cmake

    def build(self):
        cmake = self.configure_cmake()
        cmake.build()

        if self.options.enable_tests:
            self.run(os.path.join(self.build_folder, "tests"))

    def package(self):
        cmake = self.configure_cmake()
        cmake.install()

    def package_id(self):
        self.info.header_only()
