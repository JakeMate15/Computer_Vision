# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.29

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Disable VCS-based implicit rules.
% : %,v

# Disable VCS-based implicit rules.
% : RCS/%

# Disable VCS-based implicit rules.
% : RCS/%,v

# Disable VCS-based implicit rules.
% : SCCS/s.%

# Disable VCS-based implicit rules.
% : s.%

.SUFFIXES: .hpux_make_needs_suffix_list

# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

#Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /snap/clion/296/bin/cmake/linux/x64/bin/cmake

# The command to remove a file.
RM = /snap/clion/296/bin/cmake/linux/x64/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/erik/Documents/ESCOM/Computer_Vision/P7_KMeans

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/erik/Documents/ESCOM/Computer_Vision/P7_KMeans/cmake-build-debug

# Include any dependencies generated for this target.
include CMakeFiles/P7_KMeans.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include CMakeFiles/P7_KMeans.dir/compiler_depend.make

# Include the progress variables for this target.
include CMakeFiles/P7_KMeans.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/P7_KMeans.dir/flags.make

CMakeFiles/P7_KMeans.dir/main.cpp.o: CMakeFiles/P7_KMeans.dir/flags.make
CMakeFiles/P7_KMeans.dir/main.cpp.o: /home/erik/Documents/ESCOM/Computer_Vision/P7_KMeans/main.cpp
CMakeFiles/P7_KMeans.dir/main.cpp.o: CMakeFiles/P7_KMeans.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green --progress-dir=/home/erik/Documents/ESCOM/Computer_Vision/P7_KMeans/cmake-build-debug/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/P7_KMeans.dir/main.cpp.o"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT CMakeFiles/P7_KMeans.dir/main.cpp.o -MF CMakeFiles/P7_KMeans.dir/main.cpp.o.d -o CMakeFiles/P7_KMeans.dir/main.cpp.o -c /home/erik/Documents/ESCOM/Computer_Vision/P7_KMeans/main.cpp

CMakeFiles/P7_KMeans.dir/main.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Preprocessing CXX source to CMakeFiles/P7_KMeans.dir/main.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/erik/Documents/ESCOM/Computer_Vision/P7_KMeans/main.cpp > CMakeFiles/P7_KMeans.dir/main.cpp.i

CMakeFiles/P7_KMeans.dir/main.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Compiling CXX source to assembly CMakeFiles/P7_KMeans.dir/main.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/erik/Documents/ESCOM/Computer_Vision/P7_KMeans/main.cpp -o CMakeFiles/P7_KMeans.dir/main.cpp.s

# Object files for target P7_KMeans
P7_KMeans_OBJECTS = \
"CMakeFiles/P7_KMeans.dir/main.cpp.o"

# External object files for target P7_KMeans
P7_KMeans_EXTERNAL_OBJECTS =

P7_KMeans: CMakeFiles/P7_KMeans.dir/main.cpp.o
P7_KMeans: CMakeFiles/P7_KMeans.dir/build.make
P7_KMeans: /home/erik/build/lib/libopencv_gapi.so.4.10.0
P7_KMeans: /home/erik/build/lib/libopencv_highgui.so.4.10.0
P7_KMeans: /home/erik/build/lib/libopencv_ml.so.4.10.0
P7_KMeans: /home/erik/build/lib/libopencv_objdetect.so.4.10.0
P7_KMeans: /home/erik/build/lib/libopencv_photo.so.4.10.0
P7_KMeans: /home/erik/build/lib/libopencv_stitching.so.4.10.0
P7_KMeans: /home/erik/build/lib/libopencv_video.so.4.10.0
P7_KMeans: /home/erik/build/lib/libopencv_videoio.so.4.10.0
P7_KMeans: /usr/lib/x86_64-linux-gnu/libpython3.10.so
P7_KMeans: /home/erik/build/lib/libopencv_imgcodecs.so.4.10.0
P7_KMeans: /home/erik/build/lib/libopencv_dnn.so.4.10.0
P7_KMeans: /home/erik/build/lib/libopencv_calib3d.so.4.10.0
P7_KMeans: /home/erik/build/lib/libopencv_features2d.so.4.10.0
P7_KMeans: /home/erik/build/lib/libopencv_flann.so.4.10.0
P7_KMeans: /home/erik/build/lib/libopencv_imgproc.so.4.10.0
P7_KMeans: /home/erik/build/lib/libopencv_core.so.4.10.0
P7_KMeans: CMakeFiles/P7_KMeans.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green --bold --progress-dir=/home/erik/Documents/ESCOM/Computer_Vision/P7_KMeans/cmake-build-debug/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable P7_KMeans"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/P7_KMeans.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/P7_KMeans.dir/build: P7_KMeans
.PHONY : CMakeFiles/P7_KMeans.dir/build

CMakeFiles/P7_KMeans.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/P7_KMeans.dir/cmake_clean.cmake
.PHONY : CMakeFiles/P7_KMeans.dir/clean

CMakeFiles/P7_KMeans.dir/depend:
	cd /home/erik/Documents/ESCOM/Computer_Vision/P7_KMeans/cmake-build-debug && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/erik/Documents/ESCOM/Computer_Vision/P7_KMeans /home/erik/Documents/ESCOM/Computer_Vision/P7_KMeans /home/erik/Documents/ESCOM/Computer_Vision/P7_KMeans/cmake-build-debug /home/erik/Documents/ESCOM/Computer_Vision/P7_KMeans/cmake-build-debug /home/erik/Documents/ESCOM/Computer_Vision/P7_KMeans/cmake-build-debug/CMakeFiles/P7_KMeans.dir/DependInfo.cmake "--color=$(COLOR)"
.PHONY : CMakeFiles/P7_KMeans.dir/depend
