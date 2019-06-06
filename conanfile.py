from conans import ConanFile, CMake, tools

commit = "1fb4029"

class ExpectedConan(ConanFile):
    name = "expected"
    version = "0.4.0-pre.1+" + commit
    license = "CC0-1.0"
    author = "Simon Brand <tartanllama@gmail.com>"
    url = "https://github.com/TartanLlama/expected"
    description = "C++11/14/17 std::expected with functional-style extensions"
    generators = "cmake"

    def source(self):
        git = tools.Git(folder=".")
        git.clone("https://github.com/TartanLlama/expected", "master")
        git.checkout(commit)

        tools.replace_in_file('CMakeLists.txt', 'project(expected)',
        '''project(expected)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()
        ''')

    def configure_cmake(self):
        cmake = CMake(self)
        cmake.configure()
        return cmake

    def build(self):
        cmake = self.configure_cmake()
        cmake.build()
       
        if not tools.cross_building(self.settings):
            self.run('%s/bin/tests' % self.build_folder)

    def package(self):
        self.copy('*.hpp', dst='include/tl', src='tl')

    def package_id(self):
        self.info.header_only()
