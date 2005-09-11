# --with-tcl enables sqlite-tcl subpackage, and also makes %%check possible.
%define tcl 0%{?_with_tcl:1}

Summary: Library that implements an embeddable SQL database engine
Name: sqlite
Version: 3.2.5
Release: 1
License: Public Domain
Group: 	Applications/Databases
URL: http://www.sqlite.org/
Source: http://www.sqlite.org/sqlite-%{version}.tar.gz
Obsoletes: sqlite3 sqlite3-devel
BuildRequires: ncurses-devel readline-devel
BuildRequires: /usr/bin/tclsh
%if %{tcl}
BuildRequires: tcl-devel
%endif
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

%if %{tcl}
%package tcl
Summary: Tcl module for the sqlite3 embeddable SQL database engine.
Group: Development/Languages
Requires: %{name} = %{version}-%{release}

%description tcl
This package contains the tcl modules for %{name}.
%endif

%prep
%setup -q

%build
%configure %{!?with_tcl:--disable-tcl}
make %{?_smp_mflags}
make doc

%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=${RPM_BUILD_ROOT} install

%{__install} -D -m0644 sqlite3.1 %{buildroot}%{_mandir}/man1/sqlite3.1

%if %{tcl}
%check
make test
%endif

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

%if %{tcl}
%files tcl
%defattr(-, root, root)
%{_datadir}/tcl*/sqlite3
%endif

%changelog
* Sun Sep 11 2005 Florian La Roche <laroche@redhat.com>
- Upgrade to 3.2.5 release.

* Fri Jul  8 2005 Roland McGrath <roland@redhat.com> - 3.2.2-1
- Upgrade to 3.2.2 release.

* Sat Apr  9 2005 Warren Togami <wtogami@redhat.com> - 3.1.2-3
- fix buildreqs (#154298)

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
