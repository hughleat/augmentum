# Copyright (c) 2021, Hugh Leather
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

# extensions/augmentum/CMakeLists.txt
add_library(augmentum SHARED augmentum.cpp type.cpp internal.cpp python.cpp)

target_include_directories (augmentum PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})
target_link_libraries(augmentum PRIVATE pybind11::embed)
