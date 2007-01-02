%define		_modname	memcache
%define		_status		stable
Summary:	%{_modname} - a memcached extension
Summary(pl):	%{_modname} - rozszerzenie memcached
Name:		php-pecl-%{_modname}
Version:	2.1.0
Release:	1
License:	PHP 2.02
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{_modname}-%{version}.tgz
# Source0-md5:	2374d871015017829494dd85c0f63a23
URL:		http://pecl.php.net/package/memcache/
BuildRequires:	php-devel >= 3:5.0.0
BuildRequires:	rpmbuild(macros) >= 1.344
%{?requires_php_extension}
Requires:	php-common >= 4:5.0.4
Requires:	php(zlib)
#Sugests:	memcached
Obsoletes:	php-pear-%{_modname}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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
%configure \
	--with-zlib-dir=/usr
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{php_sysconfdir}/conf.d,%{php_extensiondir}}

install %{_modname}-%{version}/modules/%{_modname}.so $RPM_BUILD_ROOT%{php_extensiondir}
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{_modname}.ini
; Enable %{_modname} extension module
extension=%{_modname}.so
;memcache.allow_failover=1
;memcache.chunk_size=8192
;memcache.default_port=11211
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%doc %{_modname}-%{version}/{CREDITS,README}
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{_modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{_modname}.so
