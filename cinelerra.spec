#
# TODO:
# - build guicast as separate, shared library to use in xmovie,
#   mix2005 and cinelerra
# - get rid of bootstrap stuff:
#   https://init.linpro.no/pipermail/skolelinux.no/cinelerra/2004-April/001413.html
#
Summary:	Cinelerra - capturing, editing and production of audio/video material
Summary(pl.UTF-8):	Cinelerra - nagrywanie, obróbka i produkcja materiału audio/video
Name:		cinelerra
Version:	4
Release:	3
License:	GPL v2+
Group:		X11/Applications
Source0:	http://dl.sourceforge.net/heroines/%{name}-%{version}-src.tar.bz2
# Source0-md5:	0faf7158859646c5ea6181283594b19a
Patch0:		%{name}-system-libs.patch
Patch1:		%{name}-strip.patch
Patch2:		%{name}-fontsdir.patch
Patch3:		%{name}-locale_h.patch
Patch4:		%{name}-guicast_bootstrap.patch
Patch5:		%{name}-fix.patch
Patch6:		%{name}-plugindir.patch
Patch7:		%{name}-ffmpeg.patch
Patch8:		%{name}-fade_error.patch
URL:		http://www.heroinewarrior.com/cinelerra.php
BuildRequires:	OpenEXR-devel >= 1.6.1
BuildRequires:	OpenGL-devel >= 2.0
BuildRequires:	alsa-lib-devel >= 1.0.8
BuildRequires:	esound-devel
BuildRequires:	flac-devel >= 1.1.4
BuildRequires:	freetype-devel >= 2.1.4
BuildRequires:	lame-libs-devel >= 3.93.1
BuildRequires:	libavc1394-devel >= 0.5.1
BuildRequires:	libiec61883-devel >= 1.0.0
BuildRequires:	libmpeg3-devel >= 1.8
BuildRequires:	libraw1394-devel >= 1.2.0
BuildRequires:	libsndfile-devel >= 1.0.11
BuildRequires:	libstdc++-devel >= 5:3.2.2
BuildRequires:	libtheora-devel >= 1.0-0.alpha4
BuildRequires:	libtiff-devel >= 3.5.7
BuildRequires:	libuuid-devel
%ifarch %{ix86}
BuildRequires:	nasm
%endif
BuildRequires:	quicktime4linux-devel >= 2.3
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXv-devel
BuildRequires:	xorg-lib-libXxf86vm-devel
Requires:	OpenEXR >= 1.6.1
Requires:	alsa-lib >= 1.0.8
Requires:	freetype >= 2.1.4
Requires:	libavc1394 >= 0.5.1
Requires:	libiec61883 >= 1.0.0
Requires:	libmpeg3 >= 1.8
Requires:	libraw1394 >= 1.2.0
Requires:	libsndfile >= 1.0.11
Requires:	libtheora >= 1.0-0.alpha4
Requires:	quicktime4linux >= 2.3
Obsoletes:	bcast
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautostrip	.*/microtheme.plugin

%description
There are two types of moviegoers: producers who create new content,
going back over their content at future points for further refinement,
and consumers who want to acquire the content and watch it. Cinelerra
is not intended for consumers. Cinelerra has many features for
uncompressed content, high resolution processing, and compositing,
with very few shortcuts. Producers need these features because of the
need to retouch many generations of footage with alterations to the
format, which makes Cinelerra very complex.

Cinelerra was meant to be a Broadcast 2000 replacement.

%description -l pl.UTF-8
Są dwa rodzaje użytkowników zajmujących się filmami: producenci
tworzący nowe filmy, wracający do nich w przyszłości w celu dalszego
wygładzenia, oraz konsumenci, którzy chcą tylko zdobyć film i go
obejrzeć. Cinelerra nie jest dla konsumentów. Program ma wiele
możliwości do edycji nieskompresowanej zawartości, obróbki w wysokiej
rozdzielczości oraz montażu, z bardzo małą liczbą skrótów. Producenci
potrzebują tych możliwości ze względu na konieczność retuszowania oraz
modyfikacji formatu, co czyni program bardzo złożonym.

Cinelerra była tworzona z myślą o zastąpieniu programu Broadcast 2000.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1

# assume we have <linux/videodev2.h> and <linux/dvb/*> (present in llh)
cat > hvirtual_config.h <<EOF
#define HAVE_VIDEO4LINUX2
#define HAVE_DVB
#define HAVE_GL
#define PACKAGE_STRING "cinelerra"
EOF

%{__rm} -r libmpeg3 quicktime \
	thirdparty/{audiofile,esound,fftw-*,flac-*,freetype-*,ilmbase-*,libavc1394-*,libiec61883-*,libraw1394-*,libsndfile-*,libtheora-*,mjpegtools-*,openexr-*,tiff-*,uuid}

%build
export CFLAGS="%{rpmcflags}"
%{__make} -f build/Makefile.toolame \
	STRIP="true" \
	GCC="%{__cc}"
%{__make} -C mpeg2enc \
	STRIP="true" \
	CC="%{__cc}"
%{__make} -C mplexlo \
	STRIP="true" \
	CC="%{__cc}"
%{__make} -C guicast \
	STRIP="true" \
	GCC="%{__cc}" \
	CC="%{__cxx}"
# cinelerra, defaulttheme and microtheme are stripped before running "bootstrap"
%{__make} -C cinelerra \
	STRIP="true" \
	GCC="%{__cc}" \
	CC="%{__cxx}" \
	LINKER='%{__cxx} -o $(OUTPUT)'
%{__make} -C plugins \
	STRIP="true" \
	CC="%{__cxx}" \

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir}/cinelerra,%{_datadir}/locale}
cp -a bin/* $RPM_BUILD_ROOT%{_libdir}/cinelerra
mv $RPM_BUILD_ROOT{%{_libdir}/cinelerra,%{_bindir}}/cinelerra
mv $RPM_BUILD_ROOT{%{_libdir}/cinelerra/locale/*,%{_datadir}/locale}
rm -rf $RPM_BUILD_ROOT%{_libdir}/cinelerra/{doc,README,COPYING,c_flags}
%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc doc/{*.png,*.html,press} cinelerra/{CHANGELOG*,TODO}
%attr(755,root,root) %{_bindir}/cinelerra
%dir %{_libdir}/cinelerra
%attr(755,root,root) %{_libdir}/cinelerra/*.plugin
%attr(755,root,root) %{_libdir}/cinelerra/mpeg3*
%{_libdir}/cinelerra/fonts
%{_libdir}/cinelerra/shapes
