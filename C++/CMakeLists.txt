cmake_minimum_required(VERSION 3.10)
project(GraphProcessor)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(OGDF_DIR ${CMAKE_SOURCE_DIR}/ogdf)

include_directories(${OGDF_DIR}/include)

link_directories(${OGDF_DIR})

add_executable(GraphProcessor GraphProcessor.cpp)

target_link_libraries(GraphProcessor OGDF) 