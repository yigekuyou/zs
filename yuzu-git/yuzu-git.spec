#
# spec file for package yuzu
#
# Copyright (c) 2023 SUSE LLC
# Copyright © 2017–2020 Markus S. <kamikazow@opensuse.org>
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#
%define __builder ninja
Name:           yuzu
Version:        0.0.1git
Release:        0
Summary:        Nintendo Switch emulator/debugger
License:        GPL-3.0-or-later
Group:          System/Emulators/Other
URL:            https://yuzu-emu.org/
Source0:        _service
# wget https://api.yuzu-emu.org/gamedb/ -O compatibility_list.json
# It is dynamically changed so we should not use source URL in spec,
# otherwise it will fail source check when submitted to Factory...
Source1:        compatibility_list.json
BuildRequires:  cmake
BuildRequires:  discord-rpc-devel
BuildRequires:  doxygen
BuildRequires:  gcc-PIE
BuildRequires:  pkgconfig(INIReader)
BuildRequires:  gcc-c++
BuildRequires:  glslang-devel
BuildRequires:  graphviz
BuildRequires:  hicolor-icon-theme
BuildRequires:  libboost_context-devel-impl >= 1.75.0
BuildRequires:  libboost_filesystem-devel-impl >= 1.75.0
BuildRequires:  mold
BuildRequires:  renderdoc-devel
BuildRequires:  pkgconfig(stb)
BuildRequires:  ninja
BuildRequires:  shaderc
BuildRequires:  sndio-devel
BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(catch2) 
BuildRequires:  pkgconfig(cpp-httplib)
BuildRequires:  pkgconfig(fmt) 
BuildRequires:  pkgconfig(hidapi-hidraw)
BuildRequires:  pkgconfig(hidapi-libusb)
BuildRequires:  pkgconfig(inih)
BuildRequires:  pkgconfig(jack)
BuildRequires:  pkgconfig(libenet)
BuildRequires:  pkgconfig(liblz4)
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(libswscale)
BuildRequires:  pkgconfig(libusb-1.0)
BuildRequires:  pkgconfig(libva)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(libzip)
BuildRequires:  libzstd-devel-static
BuildRequires:  pkgconfig(nettle)
BuildRequires:  pkgconfig(nlohmann_json)
BuildRequires:  pkgconfig(openssl)
BuildRequires:  pkgconfig(opus)
BuildRequires:  pkgconfig(sdl2) 
BuildRequires:  pkgconfig(speexdsp)
BuildRequires:  pkgconfig(tinfo)
BuildRequires:  pkgconfig(vulkan) 
BuildRequires:  cmake(VulkanUtilityLibraries)
#BuildRequires:  cmake(VulkanMemoryAllocator)
BuildRequires:  git 
BuildRequires:  cmake(tsl-robin-map) 
#Qt
BuildRequires:  qt6-gui-private-devel
BuildRequires:  cmake(Qt6LinguistTools)
BuildRequires:  pkgconfig(Qt6Concurrent)
BuildRequires:  pkgconfig(Qt6Core)
BuildRequires:  pkgconfig(Qt6DBus)
BuildRequires:  pkgconfig(Qt6Multimedia)
BuildRequires:  pkgconfig(Qt6MultimediaWidgets)
BuildRequires:  pkgconfig(Qt6Network)
BuildRequires:  pkgconfig(Qt6OpenGL)
BuildRequires:  pkgconfig(Qt6Qml)
BuildRequires:  pkgconfig(Qt6Svg)
BuildRequires:  pkgconfig(Qt6WebEngineCore)
BuildRequires:  pkgconfig(Qt6WebEngineWidgets)
BuildRequires:  pkgconfig(Qt6Widgets)
# ffmpeg
BuildRequires:  pkgconfig(libavcodec)
BuildRequires:  pkgconfig(libavutil)
BuildRequires:  pkgconfig(libswscale)
%description
yuzu is an open source Nintendo Switch emulator/debugger.

%prep
%setup -q -n %_sourcedir/%name-%version -T -D
cp %{SOURCE1} dist/compatibility_list/ 
# Enforce package versioning in GUI
sed -i \
-e 's|@GIT_REV@|%{release}|g' \
-e 's|@GIT_BRANCH@|mainline|g' \
-e 's|@GIT_DESC@|%{version}|g' \
-e 's|@BUILD_NAME@|%{name}|g' \
src/common/scm_rev.cpp.in
sed -i \
-e 's|${GIT_PROGRAM} clone --depth 1 "file://${TZ_SOURCE_DIR}" "${TZ_TMP_SOURCE_DIR}"|mv ${TZ_SOURCE_DIR} ${TZ_TMP_SOURCE_DIR} |g' \
./externals/nx_tzdb/tzdb_to_nx/externals/tz/CMakeLists.txt
sed -i \
-e 's|${GIT_PROGRAM} log --pretty=%at -n1 NEWS|echo %{version}|g' \
-e 's|FATAL_ERROR|WARNING|g'   \
./externals/nx_tzdb/tzdb_to_nx/src/tzdb/CMakeLists.txt
sed -i -e '/find_package/s:(Vulkan [1-9\.]* REQUIRED):(Vulkan REQUIRED):' \
        -e '/find_package/s:(FFmpeg [1-9\.]* REQUIRED):(FFmpeg REQUIRED):' \
        -e '/find_package(LLVM MODULE COMPONENTS Demangle)/d' \
        CMakeLists.txt
%build
ulimit -Sn 4000
%cmake \
        -DCMAKE_BUILD_TYPE=RelWithDebInfo \
        -DCMAKE_INSTALL_PREFIX="%{_prefix}" \
        -DCMAKE_INSTALL_LIBEXEC="%_libexecdir" \
        -DCMAKE_POSITION_INDEPENDENT_CODE=ON \
        -DTHREADS_PREFER_PTHREAD_FLAG=ON \
        -DCMAKE_BUILD_TYPE=Release \
        -DBUILD_SHARED_LIBS=OFF \
        -DYUZU_CHECK_SUBMODULES=OFF \
        -DYUZU_USE_EXTERNAL_SDL2=OFF \
        -DENABLE_PRECOMPILED_HEADERS=OFF \
        -DYUZU_ROOM=ON -DENABLE_LIBUSB=ON \
        -DSKIP_PRECOMPILE_HEADERS=ON \
        -DUSE_PRECOMPILED_HEADERS=OFF \
        -DYUZU_USE_PRECOMPILED_HEADERS=OFF \
        -DDYNARMIC_USE_PRECOMPILED_HEADERS=OFF \
        -DDYNARMIC_ENABLE_NO_EXECUTE_SUPPORT=OFF \
        -DDYNARMIC_USE_LLVM=OFF \
        -DENABLE_CUBEB=ON \
        -DUSE_SYSTEM_CURL=ON \
        -DYUZU_USE_FASTER_LD=ON \
        -DYUZU_USE_EXTERNAL_VULKAN_UTILITY_LIBRARIES=NO \
        -DYUZU_USE_EXTERNAL_VULKAN_HEADERS=OFF \
        -DUSE_DISCORD_PRESENCE=ON \
        -DYUZU_USE_QT_MULTIMEDIA=ON \
        -DENABLE_QT_TRANSLATION=ON \
        -DENABLE_QT6=ON \
        -DYUZU_USE_QT_WEB_ENGINE=ON \
        -DENABLE_OPENGL=ON \
        -DYUZU_TESTS=OFF \
        -DYUZU_USE_EXTERNAL_FFMPEG=OFF \
        -DCMAKE_CXX_COMPILER=g++ \
        -DCMAKE_C_COMPILER=gcc \
        -DYUZU_ENABLE_PORTABLE=OFF \
        -DYUZU_DOWNLOAD_ANDROID_VVL=NO
%cmake_build

%install
%cmake_install

%post
%postun

%files
%{_bindir}/%{name}
%{_datadir}/applications/org.yuzu_emu.yuzu.desktop
%{_datadir}/icons/hicolor/scalable/apps/org.yuzu_emu.yuzu.svg
%{_datadir}/metainfo/org.yuzu_emu.yuzu.metainfo.xml
%{_datadir}/mime/packages/org.yuzu_emu.yuzu.xml
%{_bindir}/%{name}-cmd
%{_bindir}/%{name}-room

%changelog
