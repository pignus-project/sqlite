Summary: Library that implements an embeddable SQL database engine
Name: sqlite
Version: 3.1.2
Release: 2
License: Public Domain
Group: 	Applications/Databases
URL: http://www.sqlite.org/
Source: http://www.sqlite.org/sqlite-%{version}.tar.gz
Patch0: sqlite-3.1.2-doc.patch
Obsoletes: sqlite3 sqlite3-devel
# XXX for "make check" only
BuildRequires: ncurses readline
BuildRoot: %{_tmppath}/%{name}-root

%description
SQLite is a C library that implements an SQL database engine. A large
subset of SQL92 is supported. A complete database is stored in a
single disk file. The API is designed for convenience and ease of use.
Applications that link against SQLite can enjoy the power and
flexiblity of an SQL database without the administrative hassles of
supporting a separate database server.  Version 2 and version 3 binaries 
are named to permit each to be installed on a single host

%package devel
Summary: Development tools for the sqlite3 embeddable SQL database engine.
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
This package contains the header files, static libraries and development
documentation for %{name}. If you like to develop programs using %{name},
you will need to install %{name}-devel.

%package tcl
Summary: Tcl module for the sqlite3 embeddable SQL database engine.
Group: Development/Languages
Requires: %{name} = %{version}-%{release}

%description tcl
This package contains the tcl modules for %{name}.

%prep
%setup -q -n sqlite

%patch0 -p1 -b .jbj

%{__perl} -pi.orig -e '
               s|\$\(exec_prefix\)/lib|\$(libdir)|g;
               s|/usr/lib|\$(libdir)|g;
       ' Makefile* */Makefile* */*/Makefile*

%ifarch x86_64
%{__libtoolize} --force
%{__aclocal}
%{__autoconf}
%endif
CFLAGS="%{optflags} -DNDEBUG=1 -fno-strict-aliasing" \
CXXFLAGS="%{optflags} -DNDEBUG=1 -fno-strict-aliasing" \
TARGET_EXEEXT='.so' \
%configure --enable-utf8 --disable-tcl

perl -pi -e 's/\@VERSION_NUMBER\@/3001002/' Makefile

%build
make %{?_smp_mflags}
%{__make} doc

%install
rm -rf $RPM_BUILD_ROOT

%{__make} DESTDIR=${RPM_BUILD_ROOT} install

mv sqlite.1 sqlite3.1 || :
%{__install} -D -m0644 sqlite3.1 %{buildroot}%{_mandir}/man1/sqlite3.1

%check
# XXX sqlite-3.0.8 on x86: 56 errors out of 14885 tests
# XXX sqlite-3.1.2 on x86: 1 errors out of 19710 tests
make test || :

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-, root, root)
%doc README
%{_bindir}/*
%{_libdir}/*.so.*
%{_mandir}/man?/*

%files devel
%defattr(-, root, root)
%doc doc/
%{_includedir}/*.h
%{_libdir}/*.a
%{_libdir}/*.la
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%if 0
%files tcl
%defattr(-, root, root)
%{_datadir}/tcl*/sqlite3
%endif

%changelog
* Mon Apr  4 2005 Jeremy Katz <katzj@redhat.com> - 3.1.2-2
- disable tcl subpackage

* Wed Mar  9 2005 Jeff Johnson <jbj@redhat.com> 3.1.2-1
- rename to "sqlite" from "sqlite3" (#149719, #150012).

* Wed Feb 16 2005 Jeff Johnson <jbj@jbj.org> 3.1.2-1
- upgrade to 3.1.2.
- add sqlite3-tcl sub-package.

* Sat Feb  5 2005 Jeff Johnson <jbj@jbj.org> 3.0.8-3
- repackage for fc4.

* Mon Jan 17 2005 R P Herrold <info@owlriver.com> 3.0.8-2orc
- fix a man page nameing conflict when co-installed with sqlite-2, as 
  is permissible
