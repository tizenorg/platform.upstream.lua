Name:           lua
Version:        5.1.4
Release:        0
License:        MIT
Summary:        Small Embeddable Language with Simple Procedural Syntax
Url:            http://www.lua.org
Group:          System/Libraries
Source:         %{name}-%{version}.tar.gz
Source1:        macros.lua
Source2:        baselibs.conf
%define major_version 5.1
BuildRequires:  pkg-config
BuildRequires:  readline-devel
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
Lua is a programming language originally designed for extending
applications, but also frequently used as a general-purpose,
stand-alone language.

Lua combines simple procedural syntax (similar to Pascal) with powerful
data description constructs based on associative arrays and extensible
semantics. Lua is dynamically typed, interpreted from byte codes, and
has automatic memory management, making it ideal for configuration,
scripting, and rapid prototyping. Lua is implemented as a small library
of C functions, written in ANSI C, and the implementation goals are
simplicity, efficiency, portability, and low embedding cost.

%package devel
Summary:        Development files for lua
Group:          Development/Libraries/C and C++
Requires:       %{name} = %{version}

%description devel
Lua is a programming language originally designed for extending
applications, but also frequently used as a general-purpose,
stand-alone language.

This package contains files needed for embedding lua into your
application.

%package -n liblua
Summary:        Small Embeddable Language with Simple Procedural Syntax
Group:          System/Libraries

%description -n liblua
Lua is a programming language originally designed for extending
applications, but also frequently used as a general-purpose,
stand-alone language.

Lua combines simple procedural syntax (similar to Pascal) with powerful
data description constructs based on associative arrays and extensible
semantics. Lua is dynamically typed, interpreted from byte codes, and
has automatic memory management, making it ideal for configuration,
scripting, and rapid prototyping. Lua is implemented as a small library
of C functions, written in ANSI C, and the implementation goals are
simplicity, efficiency, portability, and low embedding cost.

%package doc
Summary:        Small Embeddable Language with Simple Procedural Syntax
Group:          System/Libraries
BuildArch:      noarch

%description doc
Lua is a programming language originally designed for extending
applications, but also frequently used as a general-purpose,
stand-alone language.

Lua combines simple procedural syntax (similar to Pascal) with powerful
data description constructs based on associative arrays and extensible
semantics. Lua is dynamically typed, interpreted from byte codes, and
has automatic memory management, making it ideal for configuration,
scripting, and rapid prototyping. Lua is implemented as a small library
of C functions, written in ANSI C, and the implementation goals are
simplicity, efficiency, portability, and low embedding cost.

%prep
%setup -q -n lua-%{version}

%build
sed -i 's:LUA_ROOT2 "LIBDIR/lua/%{major_version}/":LUA_ROOT2 \"%{_lib}/lua/%{major_version}/":' src/luaconf.h
make %{?_smp_mflags} -C src CC="gcc" MYCFLAGS="%{optflags} -fPIC -DLUA_USE_LINUX" MYLIBS="-Wl,-E -ldl -lreadline -lhistory -lncurses" V=%{major_version} all

%install
make install INSTALL_TOP="%{buildroot}%{_prefix}" INSTALL_LIB="%{buildroot}%{_libdir}" INSTALL_CMOD=%{buildroot}%{_libdir}/lua/%{major_version} INSTALL_MAN="%{buildroot}%{_mandir}/man1"
install -D -m644 etc/lua.pc %{buildroot}%{_libdir}/pkgconfig/lua.pc
for file in lua luac ; do
    mv "%{buildroot}%{_bindir}/${file}"        "%{buildroot}%{_bindir}/${file}%{major_version}"
    mv "%{buildroot}%{_mandir}/man1/${file}.1" "%{buildroot}%{_mandir}/man1/${file}%{major_version}.1"
done
install -d -m 0755 %{buildroot}%{_libdir}/lua/%{major_version}
install -d -m 0755 %{buildroot}%{_datadir}/lua/%{major_version}
install -D %{SOURCE1} %{buildroot}%{_sysconfdir}/rpm/macros.lua

#ln -sf liblua.so.%{major_version} %{buildroot}/%{_libdir}/liblua-%{major_version}.so
chmod +x %{buildroot}/%{_libdir}/liblua.so.%{major_version}

%post -n liblua -p /sbin/ldconfig

%postun -n liblua -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc COPYRIGHT HISTORY README
%{_mandir}/man1/lua%{major_version}.1*
%{_mandir}/man1/luac%{major_version}.1*
%{_bindir}/lua%{major_version}
%{_bindir}/luac%{major_version}
%dir %{_libdir}/lua
%dir %{_libdir}/lua/%{major_version}
%dir %{_datadir}/lua
%dir %{_datadir}/lua/%{major_version}
%{_sysconfdir}/rpm/macros.lua

%files -n liblua
%defattr(-,root,root)
%{_libdir}/liblua.so.%{major_version}
###%{_libdir}/liblua-%{major_version}.so

%files devel
%defattr(-,root,root)
%{_includedir}/lauxlib.h
%{_includedir}/lua.h
%{_includedir}/lua.hpp
%{_includedir}/luaconf.h
%{_includedir}/lualib.h
%{_libdir}/pkgconfig/lua.pc
%{_libdir}/liblua.a
%{_libdir}/liblua.so

%files doc
%defattr(-,root,root)
%doc doc/*

%changelog
