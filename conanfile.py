from conans import ConanFile, CMake, tools
import os

class TlExpectedConan(ConanFile):
    name = "tl-expected"
    version = "1.0.0"
    license = "CC0-1.0"
    author = "Simon Brand <tartanllama@gmail.com>"
    homepage = "https://tl.tartanllama.xyz"
    url = "https://github.com/yipdw/conan-expected"
    description = "C++11/14/17 std::expected with functional-style extensions"
    no_copy_source = True
    options = {
        "enable_tests": [True, False]
    }
    default_options = {
        "enable_tests": False
    }

    def source(self):
        url = "https://github.com/TartanLlama/expected/archive/v{}.zip".format(self.version)
        sha256 = "c1733556cbd3b532a02b68e2fbc2091b5bc2cccc279e4f6c6bd83877aabd4b02"
        tools.get(url, sha256=sha256)

    @property
    def tl_expected_source_folder(self):
        return os.path.join(self.source_folder, "expected-{}".format(self.version))

    def configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["EXPECTED_ENABLE_TESTS"] = self.options.enable_tests
        cmake.configure(source_folder=self.tl_expected_source_folder)

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
