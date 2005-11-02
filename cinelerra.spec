# TODO: build guicast as separate, shared library to use in
#       xmovie, mix2005 and cinelerra
Summary:	Cinelerra - capturing, editing and production of audio/video material
Summary(pl):	Cinelerra - nagrywanie, obróbka i produkcja materia³u audio/video
Name:		cinelerra
Version:	2.0
Release:	1
License:	GPL
Group:		X11/Applications
Source0:	http://dl.sourceforge.net/heroines/%{name}-%{version}-src.tar.bz2
# Source0-md5:	2beb3f1df203cbdc8918f06ea573324c
Patch0:		%{name}-system-libs.patch
Patch1:		%{name}-strip.patch
Patch2:		%{name}-fontsdir.patch
Patch3:		%{name}-locale_h.patch
Patch4:		%{name}-guicast_bootstrap.patch
URL:		http://heroinewarrior.com/cinelerra.php3
BuildRequires:	OpenEXR-devel >= 1.2.1
BuildRequires:	XFree86-devel
BuildRequires:	alsa-lib-devel >= 1.0.8
BuildRequires:	esound-devel
BuildRequires:	freetype-devel >= 2.1.4
BuildRequires:	lame-libs-devel >= 3.93.1
BuildRequires:	libavc1394-devel >= 0.5.1
BuildRequires:	libiec61883-devel >= 1.0.0
BuildRequires:	libmpeg3-devel >= 1.6
BuildRequires:	libraw1394-devel >= 1.2.0
BuildRequires:	libsndfile-devel >= 1.0.11
BuildRequires:	libstdc++-devel >= 5:3.2.2
BuildRequires:	libtheora-devel >= 1.0-0.alpha4
BuildRequires:	libtiff-devel >= 3.5.7
BuildRequires:	libuuid-devel
%ifarch %{ix86}
BuildRequires:	nasm
%endif
BuildRequires:	quicktime4linux-devel >= 2.1
Requires:	OpenEXR-devel >= 1.2.1
Requires:	alsa-lib >= 1.0.8
Requires:	freetype >= 2.1.4
Requires:	libavc1394 >= 0.5.1
Requires:	libiec61883 >= 1.0.0
Requires:	libmpeg3 >= 1.6
Requires:	libraw1394 >= 1.2.0
Requires:	libsndfile >= 1.0.11
Requires:	libtheora >= 1.0-0.alpha4
Requires:	quicktime4linux >= 2.1
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

%description -l pl
S± dwa rodzaje u¿ytkowników zajmuj±cych siê filmami: producenci
tworz±cy nowe filmy, wracaj±cy do nich w przysz³o¶ci w celu dalszego
wyg³adzenia, oraz konsumenci, którzy chc± tylko zdobyæ film i go
obejrzeæ. Cinelerra nie jest dla konsumentów. Program ma wiele
mo¿liwo¶ci do edycji nieskompresowanej zawarto¶ci, obróbki w wysokiej
rozdzielczo¶ci oraz monta¿u, z bardzo ma³± liczb± skrótów. Producenci
potrzebuj± tych mo¿liwo¶ci ze wzglêdu na konieczno¶æ retuszowania
oraz modyfikacji formatu, co czyni program bardzo z³o¿onym.

Cinelerra by³a tworzona z my¶l± o zast±pieniu programu Broadcast 2000.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

# assume we have <linux/videodev2.h> (it's in llh)
echo '#define HAVE_VIDEO4LINUX2' > hvirtual_config.h
echo '#define PACKAGE_STRING "cinelerra"' >> hvirtual_config.h

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
