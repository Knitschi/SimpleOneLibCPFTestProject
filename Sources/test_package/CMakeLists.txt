cmake_minimum_required(VERSION 3.15)
project(test_package CXX)

find_package(MyLib CONFIG REQUIRED)

add_executable(example src/example.cpp)
target_link_libraries(example mylib::MyLib)
