cmake_minimum_required(VERSION 3.29)
project(P9_Ascendente)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED True)

set(OpenCV_DIR /home/erik/build)

find_package(OpenCV REQUIRED)

add_executable(P9_Ascendente main.cpp)

#find_package(P9_Ascendente COMPONENTS Interpreter Development NumPy REQUIRED)

#target_include_directories(P9_Ascendente PRIVATE ${Python3_INCLUDE_DIRS} ${Python3_NumPy_INCLUDE_DIRS})
#
target_link_libraries(P9_Ascendente PRIVATE ${OpenCV_LIBS})