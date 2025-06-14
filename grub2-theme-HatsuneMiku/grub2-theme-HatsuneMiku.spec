#
# spec file for package grub2-theme-HatsuneMiku
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


Name:		grub2-theme-HatsuneMiku
Version:	20250430
Release:	0
Summary:	A theme of Hatsune Miku for Grub!
# FIXME: Select a correct license from https://github.com/openSUSE/spec-cleaner#spdx-licenses
License:	nofree
URL:		https://github.com/yorunoken/HatsuneMiku.git
Source:		_service
Requires:	grub2
BuildRequires:  grub2
BuildRequires:  fdupes
BuildArch:      noarch
%description
A theme of Hatsune Miku for Grub!

%package 1080p
Summary:	A theme of Hatsune Miku for Grub!

%description 1080p
A theme of Hatsune Miku for Grub!

%package 4k
Summary:	A theme of Hatsune Miku for Grub!

%description 4k
A theme of Hatsune Miku for Grub!

%prep
%setup -q -n %_sourcedir/%name-%version -T -D
%__mkdir -p %_builddir/%_sourcedir
%__ln -rs %_sourcedir/%name-%version %_builddir/%_sourcedir
%build


%install

%__mkdir -p %{buildroot}/boot/grub2/themes/
cp -rp 1080-HatsuneMiku  %{buildroot}/boot/grub2/themes
cp -rp 4k-HatsuneMiku  %{buildroot}/boot/grub2/themes
%fdupes %{buildroot}/boot/grub2/themes/1080-HatsuneMiku
%fdupes %{buildroot}/boot/grub2/themes/4k-HatsuneMiku
%check


%files 4k
%doc README.md
%dir /boot/grub2/themes
/boot/grub2/themes/4k-HatsuneMiku


%files 1080p
%doc README.md
%dir /boot/grub2/themes
/boot/grub2/themes/1080-HatsuneMiku
%changelog

