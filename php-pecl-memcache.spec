%define		_modname	memcache
%define		_status		stable

Summary:	%{_modname} - a memcached extension
Summary(pl):	%{_modname} - rozszerzenie memcached
Name:		php-pecl-%{_modname}
Version:	1.3
Release:	1
License:	PHP 2.02
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{_modname}-%{version}.tgz
# Source0-md5:	84736613e62cc66406c784f3aa89d7bc
URL:		http://pecl.php.net/package/memcached/
BuildRequires:	libtool
BuildRequires:	php-devel
Requires:	php-common
Obsoletes:	php-pear-%{_modname}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/php
%define		extensionsdir	%{_libdir}/php

%description
Memcached is a caching daemon designed especially for dynamic web
applications to decrease database load by storing objects in memory.

This extension allows you to work with memcached through handy OO and
procedural interfaces.

In PECL status of this extension is: %{_status}.

%description -l pl
Memcached to zaprojektowany dla dynamicznych aplikacji internetowych
daemon cachuj±cy maj±cy za zadanie zmniejszenie obci±¿enia bazy danych
przez przechowywanie w pamiêci obiektów.

To rozszerzenie umo¿liwia pracê z memcached za pomoc± porêcznego
zorientowanego obiektowo (oraz przez procedury) interfejsu.

To rozszerzenie ma w PECL status: %{_status}.

%prep
%setup -q -c

%build
cd %{_modname}-%{version}
phpize
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{extensionsdir}

install %{_modname}-%{version}/modules/%{_modname}.so $RPM_BUILD_ROOT%{extensionsdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{_sbindir}/php-module-install install %{_modname} %{_sysconfdir}/php-cgi.ini

%preun
if [ "$1" = "0" ]; then
	%{_sbindir}/php-module-install remove %{_modname} %{_sysconfdir}/php-cgi.ini
fi

%files
%defattr(644,root,root,755)
%doc %{_modname}-%{version}/{CREDITS,README}
%attr(755,root,root) %{extensionsdir}/%{_modname}.so
