cmake_minimum_required(VERSION 3.18)
project(my_proj LANGUAGES C Fortran) # C is needed to discover Homebrew OpenBLAS

set(CMAKE_Fortran_FLAGS "${CMAKE_Fortran_FLAGS} -Wno-line-truncation")

# Find BLAS and LAPACK
include(CMakeFindDependencyMacro)
find_dependency(BLAS)
find_dependency(LAPACK)
find_package(BLAS)
find_package(LAPACK)

# Find flint
find_package(PkgConfig)
pkg_check_modules(GMP REQUIRED gmp)
pkg_check_modules(FLINT REQUIRED flint)
# find arb for flint < 3
if(FLINT_VERSION VERSION_LESS "3")
  pkg_check_modules(ARB REQUIRED arb)
endif()
# flint has a bug with PkgConfig
if(FLINT_VERSION VERSION_LESS "3.0.2")
  find_library(FLINT_BUG_LIB NAMES flint REQUIRED)
endif()

# Find OpenMP
  find_package(OpenMP)

# Find graphics libraries
  find_library(
    dislin
    NAMES dislin_d
    PATHS ${DISLIN_DIR} )
  find_library(Xm NAMES Xm)
  message("-- Found DISLIN: ${dislin}")
  message("-- Found OpenMotif: ${Xm}")

# Turn on preprocessor
set(CMAKE_Fortran_PREPROCESS ON)

# Add source files
file(
  GLOB
  srcs
  CONFIGURE_DEPENDS
  ${PROJECT_SOURCE_DIR}/*.f90
  ${PROJECT_SOURCE_DIR}/*.F
  ${PROJECT_SOURCE_DIR}/ext/*.f90
  ${PROJECT_SOURCE_DIR}/ext/*.c
  ${PROJECT_SOURCE_DIR}/libreta_hybrid/*.f90)
if(NOT ${dislin_FOUND})
  list(APPEND srcs ${PROJECT_SOURCE_DIR}/noGUI/dislin_d_empty.f90)
endif()

# Add executable
add_executable(multiwfn ${srcs})
target_link_libraries(
  multiwfn
  PRIVATE ${BLAS_LIBRARIES}
          ${LAPACK_LIBRARIES}
          ${FLINT_BUG_LIB}
          ${FLINT_LINK_LIBRARIES}
          ${ARB_LINK_LIBRARIES}
          ${GMP_LINK_LIBRARIES}
          OpenMP::OpenMP_Fortran
          $<$<BOOL:${dislin_FOUND}>:${dislin}>
          $<$<BOOL:${xm_FOUND}>:${Xm}>
  )
target_include_directories(multiwfn PRIVATE ${GMP_INCLUDE_DIRS} ${FLINT_INCLUDE_DIRS} ${ARB_INCLUDE_DIRS})

# Add compiler flags to GFortran
target_compile_options(
  multiwfn
  PRIVATE
    $<$<AND:$<COMPILE_LANGUAGE:Fortran>,$<STREQUAL:$<Fortran_COMPILER_ID>,GNU>>:-ffree-line-length-none>
)

# Install
install(TARGETS multiwfn)
install(FILES settings.ini DESTINATION ${CMAKE_INSTALL_PREFIX}/etc/multiwfn)
