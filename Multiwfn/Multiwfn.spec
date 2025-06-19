#
# spec file for package Multiwfn
#
# Copyright (c) 2025 SUSE LLC
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


Name:		Multiwfn
Version:	0
Release:	0
Summary:如果使用了Multiwfn（包括其中任何功能）的文章中没在文章正文里引用的话，一经发现，作者会被列入黑名单，并禁止在未来使用Multiwfn。
# FIXME: Select a correct license from https://github.com/openSUSE/spec-cleaner#spdx-licenses
License:	not-free
URL:		http://sobereva.com/multiwfn/
Source:		Multiwfn_3.8_dev_src_Linux.zip
Source1:	CMakeLists.txt
BuildRequires:	cmake
BuildRequires:	gcc-c++
BuildRequires:	gcc-fortran
BuildRequires:	cmake(lapacke)
BuildRequires:	libopenblas_openmp-devel
BuildRequires:	pkgconfig(flint)
BuildRequires:	unzip
%description
Tian Lu, Feiwu Chen, J. Comput. Chem., 33, 580-592 (2012)
Tian Lu, J. Chem. Phys., 161, 082503 (2024)
如果使用了Multiwfn（包括其中任何功能）的文章中甚至连上面红字提到的这篇Multiwfn原文都没在文章正文里引用的话，一经发现，作者会被列入黑名单，并禁止在未来使用Multiwfn。
%prep
%autosetup -p1 -n Multiwfn_3.8_dev_src_Linux
rm dislin_d-11.0.a
%__sed -i 's|	      |        |g' Lebedev-Laikov.F
%__cp %{S:1} .
%build
%cmake  -DBLAS_VENDOR:STRING=OpenBLAS
%cmake_build

%install
%cmake_install

%files
%_bindir/multiwfn
%_sysconfdir/*
%changelog

