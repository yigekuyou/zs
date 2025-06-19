cmake_minimum_required(VERSION 3.18)
project(my_proj LANGUAGES C Fortran) # C is needed to discover Homebrew OpenBLAS

# Add compiler flags to GFortran
set(CMAKE_Fortran_FLAGS "${CMAKE_Fortran_FLAGS} -ffree-line-length-none -Wno-error=return-type -Wno-unused-dummy-argument -Wno-tabs")

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
${PROJECT_SOURCE_DIR}/0123dim.f90
${PROJECT_SOURCE_DIR}/AdNDP.f90
${PROJECT_SOURCE_DIR}/atmraddens.f90
${PROJECT_SOURCE_DIR}/basin.f90
${PROJECT_SOURCE_DIR}/bondorder.f90
${PROJECT_SOURCE_DIR}/Bspline.f90
${PROJECT_SOURCE_DIR}/CDA.f90
${PROJECT_SOURCE_DIR}/CDFT.f90
${PROJECT_SOURCE_DIR}/cp2kmate.f90
${PROJECT_SOURCE_DIR}/define.f90
${PROJECT_SOURCE_DIR}/deloc_aromat.f90
${PROJECT_SOURCE_DIR}/dislin_d.f90
${PROJECT_SOURCE_DIR}/DOS.f90
${PROJECT_SOURCE_DIR}/EDA.f90
${PROJECT_SOURCE_DIR}/edflib.f90
${PROJECT_SOURCE_DIR}/ETS_NOCV.f90
${PROJECT_SOURCE_DIR}/excittrans.f90
${PROJECT_SOURCE_DIR}/fileIO.f90
${PROJECT_SOURCE_DIR}/fparser.f90
${PROJECT_SOURCE_DIR}/function.f90
${PROJECT_SOURCE_DIR}/fuzzy.f90
${PROJECT_SOURCE_DIR}/grid.f90
${PROJECT_SOURCE_DIR}/hyper_polar.f90
${PROJECT_SOURCE_DIR}/integral.f90
${PROJECT_SOURCE_DIR}/LSB.f90
${PROJECT_SOURCE_DIR}/minpack.f90
${PROJECT_SOURCE_DIR}/Multiwfn.f90
${PROJECT_SOURCE_DIR}/NAONBO.f90
${PROJECT_SOURCE_DIR}/O1.f90
${PROJECT_SOURCE_DIR}/orbcomp.f90
${PROJECT_SOURCE_DIR}/orbloc.f90
${PROJECT_SOURCE_DIR}/otherfunc2.f90
${PROJECT_SOURCE_DIR}/otherfunc3.f90
${PROJECT_SOURCE_DIR}/otherfunc.f90
${PROJECT_SOURCE_DIR}/PBC.f90
${PROJECT_SOURCE_DIR}/plot.f90
${PROJECT_SOURCE_DIR}/population.f90
${PROJECT_SOURCE_DIR}/procgriddata.f90
${PROJECT_SOURCE_DIR}/spectrum.f90
${PROJECT_SOURCE_DIR}/sub.f90
${PROJECT_SOURCE_DIR}/surfana.f90
${PROJECT_SOURCE_DIR}/topology.f90
${PROJECT_SOURCE_DIR}/util.f90
${PROJECT_SOURCE_DIR}/visweak.f90
${PROJECT_SOURCE_DIR}/DFTxclib.F
${PROJECT_SOURCE_DIR}/Lebedev-Laikov.F
${PROJECT_SOURCE_DIR}/sym.F
)
list(APPEND srcs
${PROJECT_SOURCE_DIR}/ext/2F2.f90
${PROJECT_SOURCE_DIR}/ext/2F2.c
${PROJECT_SOURCE_DIR}/ext/frj.f90
)
list(APPEND srcs
${PROJECT_SOURCE_DIR}/libreta_hybrid/blockhrr_012345.f90
${PROJECT_SOURCE_DIR}/libreta_hybrid/boysfunc.f90
${PROJECT_SOURCE_DIR}/libreta_hybrid/ean.f90
${PROJECT_SOURCE_DIR}/libreta_hybrid/eanvrr_012345.f90
${PROJECT_SOURCE_DIR}/libreta_hybrid/hrr_012345.f90
${PROJECT_SOURCE_DIR}/libreta_hybrid/libreta.f90
${PROJECT_SOURCE_DIR}/libreta_hybrid/naiveeri.f90
${PROJECT_SOURCE_DIR}/libreta_hybrid/ryspoly.f90
)
list(APPEND srcs
${PROJECT_SOURCE_DIR}/ext/xlib.f90
${PROJECT_SOURCE_DIR}/GUI.f90
${PROJECT_SOURCE_DIR}/mouse_rotate.f90
)

if(NOT ${dislin})
list(APPEND srcs
${PROJECT_SOURCE_DIR}/noGUI/dislin_d_empty.f90
)
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
          $<$<BOOL:${dislin}>:${dislin}>
          $<$<BOOL:${xm_FOUND}>:${Xm}>
  )
target_include_directories(multiwfn PRIVATE ${GMP_INCLUDE_DIRS} ${FLINT_INCLUDE_DIRS} ${ARB_INCLUDE_DIRS})


# Install
include(GNUInstallDirs)
install(TARGETS multiwfn)
install(FILES settings.ini DESTINATION ${SYSCONF_INSTALL_DIR}/multiwfn )
