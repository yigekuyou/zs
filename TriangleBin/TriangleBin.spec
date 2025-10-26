#
# spec file for package TriangleBin
#
# Copyright (c) 2025 SUSE LLC and contributors
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


Name:		TriangleBin
Version:	20250104
Release:	0
Summary:Check whether you've got IMR or TBR GPU
# FIXME: Select a correct license from https://github.com/openSUSE/spec-cleaner#spdx-licenses
License:	MIT
URL:		https://github.com/Swung0x48/TriangleBin
Source0:	_service
Source1:	CMakeLists.txt
BuildRequires:	cmake
BuildRequires:	cmake(SDL2)
BuildRequires:	pkgconfig(glew)
BuildRequires:	pkgconfig(glew)
BuildRequires:	pkgconfig(gl)
BuildRequires:	cmake(glm)
BuildRequires:	c++_compiler
%description
Check whether you've got IMR or TBR GPU
%prep
%setup -q -n %_sourcedir/%name-%version -T -D
%__mkdir -p %_builddir/%_sourcedir
%__ln -rs %_sourcedir/%name-%version %_builddir/%_sourcedir
%__mv %_sourcedir/%name-%version/TriangleBinNative/src/main/cpp/* .
%__cp %{S:1} CMakeLists.txt
%__cp -r %_sourcedir/imgui-* imgui
%build
%cmake -DSYSTEM=linux-egl
%cmake_build

%install
%cmake_install

%files
%license LICENSE
%doc README.md
%_bindir/triangle
%changelog

