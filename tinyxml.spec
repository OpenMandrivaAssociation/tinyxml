%define realver 2_6_2
# (tpg) please don't change major, it should be set to 0
%define major 0
%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d

Summary:	A small and simple XML parser
Name:		tinyxml
Version:	%(echo %realver| tr '_' '.')
Release:	3
License:	zlib
Group:		System/Libraries
Url:		http://www.grinninglizard.com/tinyxml/
Source0:	http://downloads.sourceforge.net/tinyxml/%{name}_%{realver}.tar.bz2
Patch0:		%{name}-2.5.3-stl.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
TinyXML is a simple, small, C++ XML parser

%package -n %{libname}
Summary:	A small and simple XML parsing library
Group:		System/Libraries

%description -n %{libname}
TinyXML is a simple, small, C++ XML parser that can be easily 
integrating into other programs. Have you ever found yourself 
writing a text file parser every time you needed to save human 
readable data or serialize objects? TinyXML solves the text I/O 
file once and for all.

%package -n %{develname}
Summary:	Development files for %{name}
Group:		Development/C++
Provides:	%{name}-devel = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}

%description -n %{develname}
Development files and headers for %{name}.

%prep
%setup -qn %{name}
%patch0 -p1

%build

for i in tinyxml.cpp tinystr.cpp tinyxmlerror.cpp tinyxmlparser.cpp; do
 	g++ %{optflags} -fPIC -o $i.o -c $i
done
g++ %{optflags} -shared -o lib%{name}.so.0.%{version} \
    %{ldflags} -Wl,-soname,lib%{name}.so.0 *.cpp.o 


%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

# Not really designed to be build as lib, DYI
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_includedir}
install -m 755 lib%{name}.so.0.%{version} %{buildroot}%{_libdir}
ln -s lib%{name}.so.%{major}.%{version} %{buildroot}%{_libdir}/lib%{name}.so.%{major}
ln -s lib%{name}.so.%{major}.%{version} %{buildroot}%{_libdir}/lib%{name}.so
install -p -m 644 *.h %{buildroot}%{_includedir}

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/libtinyxml.so.%{major}*

%files -n %{develname}
%defattr(-,root,root)
%doc changes.txt readme.txt
%{_includedir}/*.h
%{_libdir}/libtinyxml.so


%changelog
* Tue Nov 01 2011 Tomasz Pawel Gajc <tpg@mandriva.org> 2.6.2-1mdv2012.0
+ Revision: 709263
- update to new version 2.6.2

* Sat Jul 31 2010 Tomasz Pawel Gajc <tpg@mandriva.org> 2.6.1-1mdv2011.0
+ Revision: 563984
- update to new version 2.6.1
- pass %%ldflags

* Sun Jan 31 2010 Tomasz Pawel Gajc <tpg@mandriva.org> 2.5.3-3mdv2010.1
+ Revision: 498904
- install all headers

* Wed Sep 09 2009 Thierry Vignaud <tv@mandriva.org> 2.5.3-2mdv2010.0
+ Revision: 434399
- rebuild

* Mon Aug 25 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 2.5.3-1mdv2009.0
+ Revision: 275847
- add spec file and sources
- make it work
- Created package structure for tinyxml.

