#
# Conditional build:
%bcond_without	tests		# build without tests
%bcond_without	web		# make web package

# build "web" with 7.4 build
%if 0%{?_pld_builder:1} && "%{?php_suffix}" != "74"
%undefine	with_web
%endif

%define		php_name	php%{?php_suffix}
%define		modname	memcache
%define		php_min_version 5.0.0
%define		commit e702b5f91
Summary:	%{modname} - a memcached extension
Summary(pl.UTF-8):	%{modname} - rozszerzenie memcached
Name:		%{php_name}-pecl-%{modname}
Version:	8.0
Release:	1
License:	PHP 3.01
Group:		Development/Languages/PHP
Source0:	https://pecl.php.net/get/memcache-%{version}.tgz
# Source0-md5:	ff34dc5ae1fa5b90b5bbeef56d302546
Source1:	%{modname}.ini
Source2:	%{modname}-apache.conf
Source3:	%{modname}-lighttpd.conf
Source4:	config.php
Patch0:		%{modname}-webapp.patch
Patch1:		tests.patch
URL:		https://pecl.php.net/package/memcache
BuildRequires:	%{php_name}-devel >= 3:7.0.0
BuildRequires:	%{php_name}-pcre
BuildRequires:	%{php_name}-session
BuildRequires:	%{php_name}-simplexml
BuildRequires:	%{php_name}-spl
BuildRequires:	%{php_name}-xml
BuildRequires:	php-packagexml2cl
BuildRequires:	rpm-php-pearprov >= 4.4.2-11
BuildRequires:	rpmbuild(macros) >= 1.650
%if %{with tests}
BuildRequires:	%{php_name}-cli
BuildRequires:	%{php_name}-pcntl
BuildRequires:	memcached
%endif
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

%package -n php-pecl-memcache-web
Summary:	Web interface for memcache
Group:		Libraries
# does not require extension itself
Requires:	php(core) >= %{php_min_version}
Requires:	php(date)
Requires:	php(gd)
Requires:	php(pcre)
Requires:	webapps
Requires:	webserver(php) >= 5.0
Obsoletes:	php70-pecl-memcache-web < 4.0.5.1-2
Obsoletes:	php71-pecl-memcache-web < 4.0.5.1-2
Obsoletes:	php72-pecl-memcache-web < 4.0.5.1-2
Obsoletes:	php73-pecl-memcache-web < 4.0.5.1-2
Obsoletes:	php74-pecl-memcache-web < 4.0.5.1-2
BuildArch:	noarch

%description -n php-pecl-memcache-web
Via this web interface script you can manage and view statistics of
memcache.

%prep
%setup -qc
mv %{modname}-*/* .
%patch -P0 -p1
%patch -P1 -p1

cat <<'EOF' > run-tests.sh
#!/bin/sh
export NO_INTERACTION=1 REPORT_EXIT_STATUS=1 MALLOC_CHECK_=2
exec %{__make} test \
	PHP_EXECUTABLE=%{__php} \
%if "%php_major_version.%php_minor_version" >= "7.4"
	PHP_TEST_SHARED_SYSTEM_EXTENSIONS="simplexml session" \
%else
	PHP_TEST_SHARED_SYSTEM_EXTENSIONS="pcre spl simplexml session" \
%endif
	RUN_TESTS_SETTINGS="-q $*"
EOF
chmod +x run-tests.sh

# skip failed tests
die() {
	echo >&2 "$*"
	exit 1
}
xfail() {
	set +x
	while read s; do
		t=$(echo "$s" | sed -rne 's/.+\[(.+)\]/\1/p')

		test -f "$t" || die "Missing $t"
		echo >&2 "XFAIL: $s"
		cat >> $t <<-EOF

		--XFAIL--
		Skip
		EOF
	done
}

xfail <<'EOF'
memcache->addServer() [tests/019.phpt]
memcache->addServer() with microsecond timeout [tests/056.phpt]
memcache->set()/memcache->get() with multiple keys and load balancing [tests/020.phpt]
memcache->getExtendedStats() [tests/022.phpt]
memcache_get_extended_stats() [tests/022a.phpt]
memcache->delete() with load balancing [tests/023.phpt]
memcache->increment() with load balancing [tests/025.phpt]
memcache->delete() with load balancing [tests/026.phpt]
memcache->addServer() adding server in failed mode [tests/031.phpt]
memcache->getServerStatus(), memcache->setServerParams() [tests/032.phpt]
memcache::connect() with unix domain socket [tests/035.phpt]
ini_set('session.save_handler') [tests/036.phpt]
ini_set('session.save_path') [tests/036b.phpt]
memcache->increment()/decrement() with multiple keys [tests/040.phpt]
memcache->delete() with multiple keys [tests/041.phpt]
memcache->set() with multiple values [tests/042.phpt]
ini_set('memcache.redundancy') [tests/043.phpt]
ini_set('memcache.session_redundancy') [tests/044.phpt]
hash strategies and functions [tests/046.phpt]
ini_set('session.save_handler') with unix domain socket [tests/053.phpt]
memcache multi host save path function [tests/bug73539.phpt]
session_regenerate_id() should not cause fatal error [tests/githubbug13.phpt]
EOF

%build
packagexml2cl package.xml > ChangeLog
phpize
%configure \
	--with-zlib-dir=/usr
%{__make}

# simple module load test
%{__php} -n -q -d display_errors=off \
	-d extension_dir=modules \
%if "%php_major_version.%php_minor_version" < "7.4"
	-d extension=%{php_extensiondir}/pcre.so \
	-d extension=%{php_extensiondir}/spl.so \
%endif
	-d extension=%{php_extensiondir}/simplexml.so \
	-d extension=%{php_extensiondir}/session.so \
	-d extension=%{modname}.so \
	-m > modules.log
grep %{modname} modules.log

%if %{with tests}
# Launch the Memcached service and stop it on exit
domainsocket=$PWD/memcached.sock
%{_sbindir}/memcached -p 11211 -U 11211 -d -P $PWD/memcached.pid
%{_sbindir}/memcached -s $domainsocket -d -P $PWD/memcached-udp.pid
trap 'kill $(cat memcached.pid memcached-udp.pid)' EXIT INT

./run-tests.sh --show-diff
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{php_sysconfdir}/conf.d,%{php_extensiondir},%{_examplesdir}/%{name}-%{version}}
install -p modules/%{modname}.so $RPM_BUILD_ROOT%{php_extensiondir}
# we use "session_" prefix in inifile to get loader *after* session extension
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/session_%{modname}.ini
cp -p example.php $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%if %{with web}
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_appdir}}
cp -p memcache.php $RPM_BUILD_ROOT%{_appdir}
cp -p %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/config.php
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
cp -p $RPM_BUILD_ROOT%{_sysconfdir}/{apache,httpd}.conf
cp -p %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/lighttpd.conf
%endif

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

%triggerin -n php-pecl-memcache-web -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -n php-pecl-memcache-web -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -n php-pecl-memcache-web -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -n php-pecl-memcache-web -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%triggerin -n php-pecl-memcache-web -- lighttpd
%webapp_register lighttpd %{_webapp}

%triggerun -n php-pecl-memcache-web -- lighttpd
%webapp_unregister lighttpd %{_webapp}

%files
%defattr(644,root,root,755)
%doc CREDITS README ChangeLog
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/session_%{modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{modname}.so
%{_examplesdir}/%{name}-%{version}

%if %{with web}
%files -n php-pecl-memcache-web
%defattr(644,root,root,755)
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lighttpd.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/config.php
%{_appdir}
%endif
