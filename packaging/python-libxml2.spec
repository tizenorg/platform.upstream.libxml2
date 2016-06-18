Name:           python-libxml2
Version:        2.9.1
Release:        0
Summary:        Python Bindings for libxml2
License:        MIT
Group:          Development/Python
Url:            http://xmlsoft.org
Source:         ftp://xmlsoft.org/libxml2/libxml2-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildRequires:  libxml2-devel
BuildRequires:  python-devel
BuildRequires:  python-xml
Requires:       libxml2 = %{version}
Obsoletes:      libxml2-python < %{version}
Provides:       libxml2-python = %{version}

%description
The libxml2-python package contains a module that permits applications
written in the Python programming language to use the interface
supplied by the libxml2 library to manipulate XML files.

This library allows manipulation of XML files. It includes support for
reading, modifying, and writing XML and HTML files. There is DTD
support that includes parsing and validation even with complex DTDs,
either at parse time or later once the document has been modified.

%prep
%setup -q -n libxml2-%{version}

%build
export CFLAGS="%{optflags} -fno-strict-aliasing"
%configure \
    --with-fexceptions \
    --with-history \
    --enable-ipv6 \
    --with-sax1 \
    --with-regexps \
    --with-threads \
    --with-reader \
    --with-http

# use libxml2 as built by libxml2 source package
mkdir .libs
cp -v %{_libdir}/libxml2.la .
make -C python %{?_smp_mflags}

%install
make -C python install \
    DESTDIR=%{buildroot} \
    pythondir=%{py_sitedir} \
    PYTHON_SITE_PACKAGES=%{py_sitedir}
chmod a-x python/tests/*.py
# Unwanted doc stuff
rm -fr %{buildroot}%{_datadir}/doc
rm -f python/tests/Makefile*
# #223696
rm -f %{buildroot}%{py_sitedir}/*.{la,a}

%files
%defattr(-, root, root)
%doc python/libxml2class.txt
%doc python/tests
%{py_sitedir}/*

%changelog
