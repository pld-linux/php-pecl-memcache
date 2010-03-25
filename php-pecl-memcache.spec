%define		modname	memcache
Summary:	%{modname} - a memcached extension
Summary(pl.UTF-8):	%{modname} - rozszerzenie memcached
Name:		php-pecl-%{modname}
Version:	3.0.4
Release:	3
License:	PHP 3.01
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
# Source0-md5:	07933ce0191274201ea6905cd509c5b0
Source1:	%{modname}.ini
URL:		http://pecl.php.net/package/memcache/
BuildRequires:	php-devel >= 3:5.0.0
BuildRequires:	rpmbuild(macros) >= 1.344
%{?requires_php_extension}
Requires:	php-common >= 4:5.0.4
Requires:	php-session
Requires:	php-zlib
#Suggests:	memcached
Obsoletes:	php-pear-%{modname}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Memcached is a caching daemon designed especially for dynamic web
applications to decrease database load by storing objects in memory.

This extension allows you to work with memcached through handy OO and
procedural interfaces.

%description -l pl.UTF-8
Memcached to zaprojektowany dla dynamicznych aplikacji internetowych
daemon cachujący mający za zadanie zmniejszenie obciążenia bazy danych
przez przechowywanie w pamięci obiektów.

To rozszerzenie umożliwia pracę z memcached za pomocą poręcznego
zorientowanego obiektowo (oraz przez procedury) interfejsu.

%prep
%setup -q -c
mv %{modname}-%{version}/* .

%build
phpize
%configure \
	--with-zlib-dir=/usr
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{php_sysconfdir}/conf.d,%{php_extensiondir},%{_examplesdir}/%{name}-%{version}}
install -p modules/%{modname}.so $RPM_BUILD_ROOT%{php_extensiondir}
# we use "session_" prefix in inifile to get loader *after* session extension
cp -a %{SOURCE1} $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/session_%{modname}.ini
cp -a example.php memcache.php $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%triggerpostun -- %{name} < 3.0.4-2
if [ -f %{php_sysconfdir}/conf.d/%{modname}.ini.rpmsave ]; then
	echo >&2 "Restoring old config: %{modname}.ini.rpmsave -> session_%{modname}.ini in %{php_sysconfdir}/conf.d"
	cp -f %{php_sysconfdir}/conf.d/session_%{modname}.ini{,.rpmnew}
	mv -f %{php_sysconfdir}/conf.d/{%{modname}.ini.rpmsave,session_%{modname}.ini}
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%doc CREDITS README
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/session_%{modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{modname}.so
%{_examplesdir}/%{name}-%{version}
