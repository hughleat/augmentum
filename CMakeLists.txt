# Copyright (c) 2021, Hugh Leather
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

# CMakeLists.txt
cmake_minimum_required(VERSION 3.18)
project(augmentum)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

include(extern/extern.cmake)
add_subdirectory(extensions)
add_subdirectory(tools)
