# Cmake file for a sample cross-platform project with dear imgui.
# The aim here is to have most of the stuff (including cmake files)
# be the same throughout platforms.

cmake_minimum_required(VERSION 3.1)

project(TriangleBinNative)
set(CMAKE_C_STANDARD 99)
set(CMAKE_CXX_STANDARD 20)

set(CMAKE_MODULE_PATH ${PROJECT_SOURCE_DIR}/cmake)

find_package(SDL2 REQUIRED)
include(GNUInstallDirs)
set(IMGUI_PATH ${PROJECT_SOURCE_DIR}/imgui)
set(IMGUI_IMPL_PATH ${PROJECT_SOURCE_DIR}/src/imgui_impl)

file(GLOB IMGUI_FILES
        ${IMGUI_PATH}/*.cpp
        ${IMGUI_IMPL_PATH}/*.cpp
)

set(GL_PROFILES "GL_PROFILE_GL3")

file(GLOB DEMO_FILES
        src/*.cpp
)



set(DEMO_SOURCES ${IMGUI_FILES} ${DEMO_FILES}
        #${GLLOAD_FILES}
)

# Build as a library for Android, as an executable otherwise
    add_executable(demo
            ${DEMO_SOURCES}
    )
install(TARGETS demo RUNTIME)
set_target_properties(demo PROPERTIES OUTPUT_NAME "triangle")
    target_compile_options(demo PRIVATE -Wno-error=return-type)
    find_package(GLEW REQUIRED)
        find_package(OpenGL REQUIRED)
        find_package(GLEW REQUIRED)
        set(OpenGL_GL_PREFERENCE GLVND)
        find_package(OpenGL REQUIRED)
        find_package(glm REQUIRED)
        target_link_libraries(demo GLEW ${OPENGL_LIBRARY})
        target_include_directories(demo PRIVATE ${GLEW_INCLUDE_DIR})
        target_include_directories(demo PRIVATE ${GLEW_INCLUDE_DIR})

target_link_libraries(demo ${SDL2_LIBRARY})
target_include_directories(demo PRIVATE ${SDL2_INCLUDE_DIR})
target_include_directories(demo PRIVATE ${IMGUI_PATH})
target_include_directories(demo PRIVATE ${IMGUI_IMPL_PATH})
target_include_directories(demo PRIVATE ${GLLOAD_PATH})
target_compile_definitions(demo PRIVATE ${GL_PROFILES})

target_include_directories(demo PRIVATE ${glm_INCLUDE_DIR})
