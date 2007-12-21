# bcond default logic is nicely backwards...
%bcond_without tcl
%bcond_with static
%bcond_with check

Summary: Library that implements an embeddable SQL database engine
Name: sqlite
Version: 3.5.4
Release: 1%{?dist}
License: Public Domain
Group: 	Applications/Databases
URL: http://www.sqlite.org/
Source: http://www.sqlite.org/sqlite-%{version}.tar.gz
Obsoletes: sqlite3 sqlite3-devel
BuildRequires: ncurses-devel readline-devel glibc-devel
BuildRequires: /usr/bin/tclsh
%if %{with tcl}
BuildRequires: tcl-devel
%endif
BuildRoot: %{_tmppath}/%{name}-root

%description
SQLite is a C library that implements an SQL database engine. A large
subset of SQL92 is supported. A complete database is stored in a
single disk file. The API is designed for convenience and ease of use.
Applications that link against SQLite can enjoy the power and
flexibility of an SQL database without the administrative hassles of
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

%if %{with tcl}
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
export CFLAGS="$RPM_OPT_FLAGS -DSQLITE_DISABLE_DIRSYNC=1 -Wall"
%configure %{!?with_tcl:--disable-tcl} \
           --enable-threadsafe \
           --enable-threads-override-locks 
make %{?_smp_mflags}
make doc

%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=${RPM_BUILD_ROOT} install

%{__install} -D -m0644 sqlite3.1 %{buildroot}%{_mandir}/man1/sqlite3.1

%if ! %{with static}
rm -f $RPM_BUILD_ROOT/%{_libdir}/*.{la,a}
%endif

%if %{with check}
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
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%if %{with static}
%{_libdir}/*.a
%exclude %{_libdir}/*.la
%endif
%if %{with tcl}
%files tcl
%defattr(-, root, root)
%{_datadir}/tcl*/sqlite3
%endif

%changelog
* Fri Dec 21 2007 Panu Matilainen <pmatilai@redhat.com> - 3.5.4-1
- Update to 3.5.4 (#413801)

* Fri Sep 28 2007 Panu Matilainen <pmatilai@redhat.com> - 3.4.2-3
- Add another build conditional for enabling %%check

* Fri Sep 28 2007 Panu Matilainen <pmatilai@redhat.com> - 3.4.2-2
- Use bconds for the spec build conditionals
- Enable -tcl subpackage again (#309041)

* Wed Aug 15 2007 Paul Nasrat <pnasrat@redhat.com> - 3.4.2-1
- Update to 3.4.2

* Sat Jul 21 2007 Paul Nasrat <pnasrat@redhat.com> - 3.4.1-1
- Update to 3.4.1

* Sun Jun 24 2007 Paul Nasrat <pnsarat@redhat.com> - 3.4.0-2
- Disable load for now (#245486)

* Tue Jun 19 2007 Paul Nasrat <pnasrat@redhat.com> - 3.4.0-1
- Update to 3.4.0

* Fri Jun 01 2007 Paul Nasrat <pnasrat@redhat.com> - 3.3.17-2
- Enable load 
- Build fts1 and fts2
- Don't sync on dirs (#237427)

* Tue May 29 2007 Paul Nasrat <pnasrat@redhat.com> - 3.3.17-1
- Update to 3.3.17

* Mon Mar 19 2007 Paul Nasrat <pnasrat@redhat.com> - 3.3.13-1
- Update to 3.3.13

* Fri Aug 11 2006 Paul Nasrat <pnasrat@redhat.com> - 3.3.6-2
- Fix conditional typo (patch from Gareth Armstrong)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 3.3.6-1.1
- rebuild

* Mon Jun 26 2006 Paul Nasrat <pnasrat@redhat.com> - 3.3.6-1
- Update to 3.3.6
- Fix typo  (#189647)
- Enable threading fixes (#181298)
- Conditionalize static library

* Mon Apr 17 2006 Paul Nasrat <pnasrat@redhat.com> - 3.3.5-1
- Update to 3.3.5

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 3.3.3-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 3.3.3-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Tue Jan 31 2006 Christopher Aillon <caillon@redhat.com> - 3.3.3-1
- Update to 3.3.3

* Tue Jan 31 2006 Christopher Aillon <caillon@redhat.com> - 3.3.2-1
- Update to 3.3.2

* Tue Jan 24 2006 Paul Nasrat <pnasrat@redhat.com> - 3.2.8-1
- Add --enable-threadsafe (Nicholas Miell)
- Update to 3.2.8

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Tue Oct  4 2005 Jeremy Katz <katzj@redhat.com> - 3.2.7-2
- no more static file or libtool archive (#169874) 

* Wed Sep 28 2005 Florian La Roche <laroche@redhat.com>
- Upgrade to 3.2.7 release.

* Thu Sep 22 2005 Florian La Roche <laroche@redhat.com>
- Upgrade to 3.2.6 release.

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
