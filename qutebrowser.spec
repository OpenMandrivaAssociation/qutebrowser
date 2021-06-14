Name:		qutebrowser
Version:	2.2.3
Release:	1
Summary:	A keyboard-driven, vim-like browser based on PyQt5 and QtWebEngine

License:	GPLv3
URL:		http://www.qutebrowser.org
Source0:	https://github.com/qutebrowser/%{name}/releases/download/v%{version}/%{name}-%{version}.tar.gz
BuildArch:	noarch
BuildRequires:	pkgconfig(python)
BuildRequires:	a2x
BuildRequires:	asciidoc
BuildRequires:	desktop-file-utils
BuildRequires:	python3dist(setuptools)

Requires:	python3dist(setuptools)
Requires:	python-qt5
Requires:	qt5-qtwebengine
Requires:	python3dist(pyqtwebengine)
Requires:	python-qt5-webkit
Requires:	qt5-qtwebkit
Requires:	python3dist(jinja2)
Requires:	python3dist(pyyaml)
Recommends:	python3dist(pygments)
Recommends:	python-cssutils


%description
qutebrowser is a keyboard-focused browser with a minimal GUI. It’s based on
Python, PyQt5 and QtWebEngine and free software, licensed under the GPL.
It was inspired by other browsers/addons like dwb and Vimperator/Pentadactyl.


%prep
# Workaround for error ub 2.2.3
#tar: Pathname can't be converted from UTF-8 to current locale.
#tar: Error exit delayed from previous errors.
export LANG=en_US.UTF-8
%setup -qn %{name}-%{version}


%build
# Compile the man page
a2x -f manpage doc/qutebrowser.1.asciidoc

# Find all *.py files and if their first line is exactly '#!/usr/bin/env python3'
# then replace it with '#!/usr/bin/python3' (if it's the 1st line).
find . -type f -iname "*.py" -exec sed -i '1s_^#!/usr/bin/env python3$_#!/usr/bin/python3_' {} +

python setup.py build


%install
python setup.py install --root=%{buildroot}

# Install desktop and appdata files
	
desktop-file-install \
	--add-category="Network" \
	--delete-original \
	--dir=%{buildroot}%{_datadir}/applications \
	misc/org.qutebrowser.qutebrowser.desktop
	
install -Dm644 misc/org.qutebrowser.qutebrowser.appdata.xml -t %{buildroot}%{_datadir}/metainfo
	

# Install man page
install -Dm644 doc/%{name}.1 -t %{buildroot}%{_mandir}/man1

# Install icons
install -Dm644 icons/qutebrowser.svg \
	-t "%{buildroot}%{_datadir}/icons/hicolor/scalable/apps"
for i in 16 24 32 48 64 128 256 512; do
	install -Dm644 "icons/qutebrowser-${i}x${i}.png" \
		"%{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/apps/qutebrowser.png"
done

# Set __main__.py as executable
chmod 755 %{buildroot}%{python3_sitelib}/%{name}/__main__.py

# Remove zero-length files:
# https://fedoraproject.org/wiki/Packaging_tricks#Zero_length_files
find %{buildroot} -size 0 -delete

%files
#doc LICENSE README.asciidoc doc/changelog.asciidoc qutebrowser/html/doc
%{python3_sitelib}/%{name}-%{version}-py?.?.egg-info
%{python3_sitelib}/%{name}
%{_bindir}/%{name}
%{_datadir}/applications/org.qutebrowser.qutebrowser.desktop
%{_mandir}/man1/%{name}.1*
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg
%{_datadir}/icons/hicolor/16x16/apps/%{name}.png
%{_datadir}/icons/hicolor/24x24/apps/%{name}.png
%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
%{_datadir}/icons/hicolor/48x48/apps/%{name}.png
%{_datadir}/icons/hicolor/64x64/apps/%{name}.png
%{_datadir}/icons/hicolor/128x128/apps/%{name}.png
%{_datadir}/icons/hicolor/256x256/apps/%{name}.png
%{_datadir}/icons/hicolor/512x512/apps/%{name}.png
%{_datadir}/metainfo/org.qutebrowser.qutebrowser.appdata.xml
