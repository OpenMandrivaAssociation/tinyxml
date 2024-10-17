%define realver 2_6_2
# (tpg) please don't change major, it should be set to 0
%define major 0
%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d

Summary:	A small and simple XML parser
Name:		tinyxml
Version:	%(echo %realver| tr '_' '.')
Release:	19
License:	zlib
Group:		System/Libraries
Url:		https://www.grinninglizard.com/tinyxml/
Source0:	http://downloads.sourceforge.net/tinyxml/%{name}_%{realver}.tar.bz2
Patch0:		%{name}-2.5.3-stl.patch
Source1:	https://src.fedoraproject.org/rpms/tinyxml/raw/rawhide/f/tinyxml.pc.in

%description
TinyXML is a simple, small, C++ XML parser.

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
%autosetup -n %{name} -p1

%build
for i in tinyxml.cpp tinystr.cpp tinyxmlerror.cpp tinyxmlparser.cpp; do
 	%{__cxx} %{optflags} -fPIC -o $i.o -c $i
done
%{__cxx} %{optflags} -shared -o lib%{name}.so.0.%{version} \
    %{build_ldflags} -Wl,-soname,lib%{name}.so.0 *.cpp.o 


%install
# Not really designed to be build as lib, DYI
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_includedir}
install -m 755 lib%{name}.so.0.%{version} %{buildroot}%{_libdir}
ln -s lib%{name}.so.%{major}.%{version} %{buildroot}%{_libdir}/lib%{name}.so.%{major}
ln -s lib%{name}.so.%{major}.%{version} %{buildroot}%{_libdir}/lib%{name}.so
install -p -m 644 *.h %{buildroot}%{_includedir}

mkdir -p %{buildroot}%{_libdir}/pkgconfig
sed -e 's![@]prefix[@]!%{_prefix}!g' \
 -e 's![@]exec_prefix[@]!%{_exec_prefix}!g' \
 -e 's![@]libdir[@]!%{_libdir}!g' \
 -e 's![@]includedir[@]!%{_includedir}!g' \
 -e 's![@]version[@]!%{version}!g' \
 %{SOURCE1} > %{buildroot}%{_libdir}/pkgconfig/%{name}.pc

%files -n %{libname}
%{_libdir}/libtinyxml.so.%{major}*

%files -n %{develname}
%doc changes.txt readme.txt
%{_includedir}/*.h
%{_libdir}/libtinyxml.so
%{_libdir}/pkgconfig/tinyxml.pc
