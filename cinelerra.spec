#
# TODO:
# - build guicast as separate, shared library to use in xmovie,
#   mix2005 and cinelerra
# - get rid of bootstrap stuff:
#   https://init.linpro.no/pipermail/skolelinux.no/cinelerra/2004-April/001413.html
#
Summary:	Cinelerra - capturing, editing and production of audio/video material
Summary(pl.UTF-8):   Cinelerra - nagrywanie, obróbka i produkcja materiału audio/video
Name:		cinelerra
Version:	2.1
Release:	1
License:	GPL
Group:		X11/Applications
Source0:	http://dl.sourceforge.net/heroines/%{name}-%{version}-src.tar.bz2
# Source0-md5:	0f0523ef1aa94efb5152dcc494009b56
Patch0:		%{name}-system-libs.patch
Patch1:		%{name}-strip.patch
Patch2:		%{name}-fontsdir.patch
Patch3:		%{name}-locale_h.patch
Patch4:		%{name}-guicast_bootstrap.patch
Patch5:		%{name}-fix.patch
URL:		http://heroinewarrior.com/cinelerra.php3
BuildRequires:	OpenEXR-devel >= 1.2.1
#BuildRequires:	OpenGL-devel >= 2.0
BuildRequires:	alsa-lib-devel >= 1.0.8
BuildRequires:	esound-devel
BuildRequires:	freetype-devel >= 2.1.4
BuildRequires:	lame-libs-devel >= 3.93.1
BuildRequires:	libavc1394-devel >= 0.5.1
BuildRequires:	libiec61883-devel >= 1.0.0
BuildRequires:	libmpeg3-devel >= 1.7
BuildRequires:	libraw1394-devel >= 1.2.0
BuildRequires:	libsndfile-devel >= 1.0.11
BuildRequires:	libstdc++-devel >= 5:3.2.2
BuildRequires:	libtheora-devel >= 1.0-0.alpha4
BuildRequires:	libtiff-devel >= 3.5.7
BuildRequires:	libuuid-devel
%ifarch %{ix86}
BuildRequires:	nasm
%endif
BuildRequires:	quicktime4linux-devel >= 2.2
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXv-devel
BuildRequires:	xorg-lib-libXxf86vm-devel
Requires:	OpenEXR-devel >= 1.2.1
Requires:	alsa-lib >= 1.0.8
Requires:	freetype >= 2.1.4
Requires:	libavc1394 >= 0.5.1
Requires:	libiec61883 >= 1.0.0
Requires:	libmpeg3 >= 1.7
Requires:	libraw1394 >= 1.2.0
Requires:	libsndfile >= 1.0.11
Requires:	libtheora >= 1.0-0.alpha4
Requires:	quicktime4linux >= 2.2
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
potrzebują tych możliwości ze względu na konieczność retuszowania
oraz modyfikacji formatu, co czyni program bardzo złożonym.

Cinelerra była tworzona z myślą o zastąpieniu programu Broadcast 2000.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

# assume we have <linux/videodev2.h> and <linux/dvb/*> (present in llh)
# don't define HAVE_GL as Mesa doesn't support OpenGL 2.0 (e.g. glUseProgram()) yet
cat > hvirtual_config.h <<EOF
#define HAVE_VIDEO4LINUX2
#define HAVE_DVB
#define PACKAGE_STRING "cinelerra"
EOF

rm -rf OpenEXR-* alsa-lib-* audiofile esound fftw-* freetype-* libavc1394-* libiec61883-* libmpeg3 libraw1394-* libsndfile-* libtheora-* mjpegtools-* quicktime tiff-* uuid

%build
CFLAGS="%{rpmcflags}"; export CFLAGS
%{__make} -f build/Makefile.toolame
%{__make} -C mpeg2enc
%{__make} -C mplexlo
%{__make} -C guicast
# cinelerra, defaulttheme and microtheme are stripped before running "bootstrap"
%{__make} -C cinelerra \
	STRIP="%{?debug:true}%{!?debug:strip -R.note -R.comment}"
%{__make} -C plugins \
	STRIP="%{?debug:true}%{!?debug:strip -R.note -R.comment}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir}/cinelerra}

install cinelerra/*/cinelerra $RPM_BUILD_ROOT%{_bindir}
install plugins/`uname -m`/*.plugin $RPM_BUILD_ROOT%{_libdir}/cinelerra

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc doc/{*.png,*.html,press} cinelerra/{CHANGELOG*,TODO}
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/cinelerra
