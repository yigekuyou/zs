#
# spec file for package ceserver
#
# Copyright (c) 2023 SUSE LLC
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


Name:           ceserver
Version:        0
Release:        0
Summary:        cheat engine linux service
# FIXME: Select a correct license from https://github.com/openSUSE/spec-cleaner#spdx-licenses
License:        no-license
URL:            https://github.com/cheat-engine/cheat-engine
Source:         _service

BuildRequires:  gcc pkgconfig(zlib)
%description
cheat engine linux service
you need wine cheat engine
%prep
%setup -q -n %_sourcedir/%name-%version/Cheat\ Engine/ceserver/gcc -T -D
%build
%make_build

%install
mkdir %{buildroot}%{_prefix} %{buildroot}%{_sbindir}
cp -rp %name %{buildroot}%{_sbindir}
%post
%postun

%files
%defattr(-,root,root,-)
%{_sbindir}/%name
%changelog

