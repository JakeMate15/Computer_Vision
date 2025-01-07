cmake_minimum_required(VERSION 3.29)
project(P8_Chain)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED True)

set(OpenCV_DIR /home/erik/build)

find_package(OpenCV REQUIRED)

add_executable(P8_Chain main.cpp)

target_link_libraries(P8_Chain PRIVATE ${OpenCV_LIBS})