cmake_minimum_required(VERSION 3.29)
project(P7_KMeans)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED True)

set(OpenCV_DIR /home/erik/build)

find_package(OpenCV REQUIRED)

add_executable(P7_KMeans main.cpp)

find_package(Python3 COMPONENTS Interpreter Development NumPy REQUIRED)

target_include_directories(P7_KMeans PRIVATE ${Python3_INCLUDE_DIRS} ${Python3_NumPy_INCLUDE_DIRS})

target_link_libraries(P7_KMeans PRIVATE ${OpenCV_LIBS} ${Python3_LIBRARIES})