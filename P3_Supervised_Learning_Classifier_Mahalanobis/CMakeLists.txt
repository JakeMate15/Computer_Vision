cmake_minimum_required(VERSION 3.10)
project(P2)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED True)

include_directories(include)

find_package(Python3 COMPONENTS Interpreter Development NumPy REQUIRED)

add_executable(P1 src/main.cpp
        include/matrix.cpp
        include/matrix.h
        include/Clase.h)

target_include_directories(P1 PRIVATE ${Python3_INCLUDE_DIRS} ${Python3_NumPy_INCLUDE_DIRS})
target_link_libraries(P1 PRIVATE ${Python3_LIBRARIES})
