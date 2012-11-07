%define lname libxml2

Name:           libxml2
Version:        2.8.0
Release:        0
Summary:        A Library to Manipulate XML Files
License:        MIT
Group:          System/Libraries
Url:            http://xmlsoft.org
# Source ftp://xmlsoft.org/libxml2/libxml2-git-snapshot.tar.gz changes every day
Source:         ftp://xmlsoft.org/libxml2/%{name}-%{version}.tar.gz
Source2:        baselibs.conf
Patch0:         fix-perl.diff
BuildRequires:  pkg-config
BuildRequires:  readline-devel
BuildRequires:  xz-devel
BuildRequires:  zlib-devel

%description
The XML C library was initially developed for the GNOME project. It is
now used by many programs to load and save extensible data structures
or manipulate any kind of XML files.

This library implements a number of existing standards related to
markup languages, including the XML standard, name spaces in XML, XML
Base, RFC 2396, XPath, XPointer, HTML4, XInclude, SGML catalogs, and
XML catalogs. In most cases, libxml tries to implement the
specification in a rather strict way. To some extent, it provides
support for the following specifications, but does not claim to
implement them: DOM, FTP client, HTTP client, and SAX.

The library also supports RelaxNG. Support for W3C XML Schemas is in
progress.


%package tools
Summary:        Tools using libxml
Group:          System/Libraries

%description tools
This package contains xmllint, a very useful tool proving libxml's power.

%package devel
Summary:        Include Files and Libraries mandatory for Development
Group:          Development/Libraries/C and C++
Requires:       %{lname} = %{version}
Requires:       %{name}-tools = %{version}
Requires:       glibc-devel
Requires:       readline-devel
Requires:       xz-devel
Requires:       zlib-devel

%description devel
This package contains all necessary include files and libraries needed
to develop applications that require these.

%package doc
Summary:        A Library to Manipulate XML Files
Group:          System/Libraries
Requires:       %{lname} = %{version}
BuildArch:      noarch

%description doc
The XML C library was initially developed for the GNOME project. It is
now used by many programs to load and save extensible data structures
or manipulate any kind of XML files.

This library implements a number of existing standards related to
markup languages, including the XML standard, name spaces in XML, XML
Base, RFC 2396, XPath, XPointer, HTML4, XInclude, SGML catalogs, and
XML catalogs. In most cases, libxml tries to implement the
specification in a rather strict way. To some extent, it provides
support for the following specifications, but does not claim to
implement them: DOM, FTP client, HTTP client, and SAX.

The library also supports RelaxNG. Support for W3C XML Schemas is in
progress.

%prep
%setup -q
%patch0

%build
%configure --disable-static \
    --docdir=%_docdir/%name \
    --with-html-dir=%_docdir/%name/html \
    --with-fexceptions \
    --with-history \
    --without-python \
    --enable-ipv6 \
    --with-sax1 \
    --with-regexps \
    --with-threads \
    --with-reader \
    --with-http

make %{?_smp_mflags} BASE_DIR="%_docdir" DOC_MODULE="%name"

%check
# qemu-arm can't keep up atm, disabling check for arm
%ifnarch %arm
make check
%endif

%install
make install DESTDIR="%buildroot" BASE_DIR="%_docdir" DOC_MODULE="%name"
mkdir -p "%buildroot/%_docdir/%name"
cp -a AUTHORS NEWS README COPYING* Copyright TODO* %{buildroot}%{_docdir}/%{name}/
ln -s libxml2/libxml %{buildroot}%{_includedir}/libxml


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files 
%defattr(-, root, root)
%{_libdir}/lib*.so.*
%doc %dir %{_docdir}/%{name}
%doc %{_docdir}/%{name}/[ANRCT]*

%files tools
%defattr(-, root, root)
%{_bindir}/xmllint
%{_bindir}/xmlcatalog
%doc %{_mandir}/man1/xmllint.1*
%doc %{_mandir}/man1/xmlcatalog.1*

%files devel
%defattr(-, root, root)
%{_bindir}/xml2-config
%dir %{_datadir}/aclocal
%{_datadir}/aclocal/libxml.m4
%{_includedir}/libxml
%{_includedir}/libxml2
%{_libdir}/lib*.so
# libxml2.la is needed for the python-libxml2 build. Deleting it breaks build of python-libxml2.
%{_libdir}/libxml2.la
%{_libdir}/*.sh
%{_libdir}/pkgconfig/*.pc
%doc %{_mandir}/man1/xml2-config.1*
%doc %{_mandir}/man3/libxml.3*

%files doc
%defattr(-, root, root)
%{_datadir}/gtk-doc/html/*
%doc %{_docdir}/%{name}/examples
%doc %{_docdir}/%{name}/html
# owning these directories prevents gtk-doc <-> libxml2 build loop:
%dir %{_datadir}/gtk-doc
%dir %{_datadir}/gtk-doc/html

%changelog
