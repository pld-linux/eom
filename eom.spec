#
# Conditional build:
%bcond_without	apidocs		# disable API documentation

Summary:	The Eye of MATE image viewer
Summary(pl.UTF-8):	Oko MATE - przeglądarka obrazków
Summary(pt_BR.UTF-8):	Visualizador de imagem Eye of MATE
Name:		eom
Version:	1.8.0
Release:	2
License:	GPL v2+
Group:		X11/Applications/Graphics
Source0:	http://pub.mate-desktop.org/releases/1.8/%{name}-%{version}.tar.xz
# Source0-md5:	0e80c19eb58d337ff25a7492967d0e4a
Patch0:		%{name}-codegen.patch
URL:		http://mate-desktop.org/
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake >= 1:1.9
BuildRequires:	dbus-glib-devel >= 0.71
BuildRequires:	docbook-dtd412-xml
BuildRequires:	exempi-devel >= 1.99.5
BuildRequires:	gdk-pixbuf2-devel >= 2.4.0
BuildRequires:	gettext-devel >= 0.10.40
BuildRequires:	glib2-devel >= 1:2.26.0
BuildRequires:	gtk+2-devel >= 2:2.18.0
%{?with_apidocs:BuildRequires:	gtk-doc >= 1.9}
BuildRequires:	intltool >= 0.40.0
BuildRequires:	lcms-devel
BuildRequires:	libexif-devel >= 1:0.6.14
BuildRequires:	libjpeg-devel
BuildRequires:	librsvg-devel >= 2.26.0
BuildRequires:	libtool >= 1:1.4.3
BuildRequires:	libxml2-devel >= 2.0
BuildRequires:	mate-common
BuildRequires:	mate-desktop-devel >= 1.5.0
BuildRequires:	mate-icon-theme-devel >= 1.1.0
BuildRequires:	pkgconfig >= 1:0.9.0
BuildRequires:	python-devel >= 2.3
BuildRequires:	python-pygobject-devel >= 2.16.0
BuildRequires:	python-pygtk-devel >= 2:2.14.0
BuildRequires:	rpmbuild(find_lang) >= 1.36
BuildRequires:	rpmbuild(macros) >= 1.311
BuildRequires:	scrollkeeper
BuildRequires:	shared-mime-info >= 0.20
BuildRequires:	tar >= 1:1.22
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xz
BuildRequires:	yelp-tools
BuildRequires:	zlib-devel
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	glib2 >= 1:2.26.0
Requires(post,postun):	gtk-update-icon-cache
Requires(post,postun):	hicolor-icon-theme
Requires(post,postun):	scrollkeeper
Requires:	dbus-glib >= 0.71
Requires:	exempi >= 1.99.5
Requires:	glib2 >= 1:2.26.0
Requires:	gtk+2 >= 2:2.18.0
Requires:	libexif >= 1:0.6.14
Requires:	librsvg >= 2.26.0
Requires:	mate-icon-theme >= 1.1.0
Requires:	shared-mime-info >= 0.20
Obsoletes:	mate-image-viewer
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Eye of MATE is a tool for viewing/cataloging images. It's a fork of
Eye of GNOME.

%description -l pl.UTF-8
Eye of MATE (Oko MATE) jest narzędziem do oglądania i katalogowania
obrazków. Jest to odgałęzienie programu Eye of GNOME.

%description -l pt_BR.UTF-8
Aplicativo para visualizar imagens chamado Eye of MATE.

%package devel
Summary:	Header files for Eye of MATE plugins
Summary(pl.UTF-8):	Pliki nagłówkowe dla wtyczek Eye of MATE
Group:		X11/Development/Libraries
# doesn't require base
Requires:	glib2-devel >= 1:2.26.0
Requires:	gtk+2-devel >= 2:2.18.0
Obsoletes:	mate-image-viewer-devel

%description devel
Header files for Eye of MATE plugins.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla wtyczek Eye of MATE.

%package apidocs
Summary:	Eye of MATE API documentation
Summary(pl.UTF-8):	Dokumentacja API Eye of MATE
Group:		Documentation
Requires:	gtk-doc-common
Obsoletes:	mate-image-viewer-apidocs
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description apidocs
Eye of MATE API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API Eye of MATE.

%prep
%setup -q
%patch0 -p1

%build
%{?with_apidocs:%{__gtkdocize}}
%{__intltoolize}
%{__libtoolize}
%{__aclocal}
%{__automake}
%{__autoheader}
%{__autoconf}
%configure \
	--enable-gtk-doc%{!?with_apidocs:=no} \
	--disable-scrollkeeper \
	--disable-silent-rules \
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/eom/plugins/*.la

%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/cmn

# mate < 1.5 did not exist in PLD, avoid dependency on mate-conf
%{__rm} $RPM_BUILD_ROOT%{_datadir}/MateConf/gsettings/eom.convert

%find_lang eom --with-mate --with-omf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%glib_compile_schemas
%scrollkeeper_update_post
%update_desktop_database_post
%update_icon_cache hicolor

%postun
%glib_compile_schemas
%scrollkeeper_update_postun
%update_desktop_database_postun
%update_icon_cache hicolor

%files -f eom.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README THANKS TODO
%attr(755,root,root) %{_bindir}/eom
%dir %{_libdir}/eom
%dir %{_libdir}/eom/plugins
%attr(755,root,root) %{_libdir}/eom/plugins/libfullscreen.so
%{_libdir}/eom/plugins/fullscreen.eom-plugin
%attr(755,root,root) %{_libdir}/eom/plugins/libreload.so
%{_libdir}/eom/plugins/reload.eom-plugin
%attr(755,root,root) %{_libdir}/eom/plugins/libstatusbar-date.so
%{_libdir}/eom/plugins/statusbar-date.eom-plugin
%{_datadir}/glib-2.0/schemas/org.mate.eom.gschema.xml
%{_datadir}/eom
%{_desktopdir}/eom.desktop
%{_iconsdir}/hicolor/*/apps/eom.*
%{_mandir}/man1/eom.1*

%files devel
%defattr(644,root,root,755)
%{_includedir}/eom-2.20
%{_pkgconfigdir}/eom.pc

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/eom
%endif
