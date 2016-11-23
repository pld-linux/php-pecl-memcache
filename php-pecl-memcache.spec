%define		php_name	php%{?php_suffix}
%define		modname	memcache
%define		php_min_version 5.0.0
%include	/usr/lib/rpm/macros.php
Summary:	%{modname} - a memcached extension
Summary(pl.UTF-8):	%{modname} - rozszerzenie memcached
Name:		%{php_name}-pecl-%{modname}
Version:	3.0.9
Release:	1
License:	PHP 3.01
Group:		Development/Languages/PHP
#Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
Source0:	https://github.com/websupport-sk/pecl-memcache/archive/NON_BLOCKING_IO_php7.tar.gz
# Source0-md5:	7751d8191302a726449d7c6506b8783d
Source1:	%{modname}.ini
Source2:	%{modname}-apache.conf
Source3:	%{modname}-lighttpd.conf
Source4:	config.php
Patch0:		%{modname}-webapp.patch
URL:		http://pecl.php.net/package/memcache/
BuildRequires:	%{php_name}-devel >= 3:5.0.0
BuildRequires:	%{php_name}-xml
BuildRequires:	php-packagexml2cl
BuildRequires:	rpm-php-pearprov >= 4.4.2-11
BuildRequires:	rpmbuild(macros) >= 1.650
%{?requires_php_extension}
Requires:	%{php_name}-session
Requires:	%{php_name}-zlib
Suggests:	memcached
Provides:	php(memcache) = %{version}
Obsoletes:	php-pecl-memcache < 3.0.8-5
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		%{modname}
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		_appdir		%{_datadir}/%{_webapp}

# bad depsolver
%define		_noautopear	pear

# put it together for rpmbuild
%define		_noautoreq	%{?_noautophp} %{?_noautopear}

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

%package web
Summary:	Web interface for memcache
Group:		Libraries
# does not require extension itself
Requires:	php(core) >= %{php_min_version}
Requires:	php(date)
Requires:	php(gd)
Requires:	php(pcre)
Requires:	webapps
Requires:	webserver(php) >= 5.0
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description web
Via this web interface script you can manage and view statistics of
memcache.

%prep
%setup -qc
mv pecl-%{modname}-*/{.??*,*} .
%patch0 -p1

%build
packagexml2cl package.xml > ChangeLog
phpize
%configure \
	--with-zlib-dir=/usr
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{php_sysconfdir}/conf.d,%{php_extensiondir},%{_examplesdir}/%{name}-%{version}}
install -p modules/%{modname}.so $RPM_BUILD_ROOT%{php_extensiondir}
# we use "session_" prefix in inifile to get loader *after* session extension
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/session_%{modname}.ini
cp -p example.php $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_appdir}}
cp -p memcache.php $RPM_BUILD_ROOT%{_appdir}
cp -p %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/config.php
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
cp -p $RPM_BUILD_ROOT%{_sysconfdir}/{apache,httpd}.conf
cp -p %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/lighttpd.conf

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

%triggerin web -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun web -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin web -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun web -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%triggerin web -- lighttpd
%webapp_register lighttpd %{_webapp}

%triggerun web -- lighttpd
%webapp_unregister lighttpd %{_webapp}

%files
%defattr(644,root,root,755)
%doc CREDITS README ChangeLog
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/session_%{modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{modname}.so
%{_examplesdir}/%{name}-%{version}

%files web
%defattr(644,root,root,755)
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lighttpd.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/config.php
%{_appdir}
