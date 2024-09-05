cmake_minimum_required(VERSION 3.10)
project(P1)

# Establecer la versión de C++ (puedes cambiar a 20 si prefieres)
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# Incluir la cabecera de Matplotlib C++
include_directories(include)

# Encontrar Python3 y sus componentes
find_package(Python3 COMPONENTS Interpreter Development NumPy REQUIRED)

# Añadir el ejecutable
add_executable(P1 src/main.cpp)

# Incluir los directorios de Python y NumPy
target_include_directories(P1 PRIVATE ${Python3_INCLUDE_DIRS} ${Python3_NumPy_INCLUDE_DIRS})

# Enlazar Python y las bibliotecas con el ejecutable
target_link_libraries(P1 PRIVATE ${Python3_LIBRARIES})
