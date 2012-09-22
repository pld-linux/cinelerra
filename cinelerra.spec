#
# imho, it is pointless to build this app with system libraries until we
# start submitting patches to the author (is that possible with his
# current development and release strategy?)... anyway, the todo follows
# - make a patch for plugin dir in preferences.C, i.e.
#       get_exe_path(plugin_dir); -> sprintf(plugin_dir, PLUGIN_DIR);
#   or move plugins to %{_bindir}... otherwise you cannot run it 
# - review existing, but commented out patches
# - send the existing patches to the author (so we do not have to maintain
#   them forever)
# - build with set of current systems libs
# - quicktime4linux seems to be dead as separate library, use the provided
#   one
# - build guicast as separate, shared library to use in xmovie,
#   mix2005 and cinelerra
#
Summary:	Cinelerra - capturing, editing and production of audio/video material
Summary(pl.UTF-8):	Cinelerra - nagrywanie, obróbka i produkcja materiału audio/video
Name:		cinelerra
Version:	4.4
Release:	0.1
License:	GPL v2+
Group:		X11/Applications
Source0:	http://dl.sourceforge.net/heroines/%{name}-%{version}-src.tar.xz
# Source0-md5:	252d811546025470ae4d7fa31c1f52d4
Patch0:		%{name}-system-libs.patch
Patch1:		%{name}-strip.patch
Patch2:		%{name}-fontsdir.patch
Patch3:		%{name}-locale_h.patch
Patch4:		%{name}-guicast_bootstrap.patch
Patch6:		%{name}-libpng.patch
Patch7:		%{name}-ffmpeg.patch
Patch8:		%{name}-typo.patch
# see speech_tools package
Patch9:		%{name}-st.patch
URL:		http://www.heroinewarrior.com/cinelerra.php
BuildRequires:	OpenEXR-devel >= 1.6.1
BuildRequires:	OpenGL-GLU-devel
BuildRequires:	OpenGL-devel >= 2.0
BuildRequires:	alsa-lib-devel >= 1.0.8
BuildRequires:	bzip2-devel
#x#BuildRequires:	esound-devel
BuildRequires:	ffmpeg-devel >= 0.6
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
#x#BuildRequires:	quicktime4linux-devel >= 2.3
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
#x#Requires:	quicktime4linux >= 2.3
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
#x#%patch0 -p1
#x#%patch1 -p1
%patch2 -p1
#x#%patch3 -p1
#x#%patch4 -p1
#x#%patch5 -p1
%patch6 -p0
#x#%patch7 -p1
%patch8 -p1
%patch9 -p0

#x## assume we have <linux/videodev2.h> and <linux/dvb/*> (present in llh)
#x#cat > hvirtual_config.h <<EOF
#x##define HAVE_VIDEO4LINUX2
#x##define HAVE_DVB
#x##define HAVE_GL
#x##define PACKAGE_STRING "cinelerra"
#x#EOF

#x#%{__rm} -r libmpeg3 quicktime \
#x#        thirdparty/{audiofile,esound,fftw-*,flac-*,freetype-*,ilmbase-*,libavc1394-*,libiec61883-*,libraw1394-*,libsndfile-*,libtheora-*,mjpegtools-*,openexr-*,tiff-*,uuid}

%build
export CFLAGS="%{rpmcflags}"
#x#%{__make} -f build/Makefile.toolame \
#x#    STRIP="true" \
#x#    GCC="%{__cc}"
#x#%{__make} -C mpeg2enc \
#x#    STRIP="true" \
#x#    CC="%{__cc}"
#x#%{__make} -C mplexlo \
#x#    STRIP="true" \
#x#    CC="%{__cc}"
#x#%{__make} -C guicast \
#x#    STRIP="true" \
#x#    GCC="%{__cc}" \
#x#    CC="%{__cxx}"
#x## cinelerra, defaulttheme and microtheme are stripped before running "bootstrap"
#x#%{__make} -C cinelerra \
#x#    STRIP="true" \
#x#    GCC="%{__cc}" \
#x#    CC="%{__cxx}" \
#x#    LINKER='%{__cxx} -o $(OUTPUT)'
#x#%{__make} -C plugins \
#x#    STRIP="true" \
#x#    CC="%{__cxx}" \

(
    # to replace -ltermcap with -tncurses
    cd thirdparty/speech_tools
    rm ./config.cache
    ./configure
)

./configure
make

(
    # to link with libva
    cd cinelerra
    g++ -o ../bin/cinelerra `cat x86_64/objs` -lva
)

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir}/cinelerra}
cp -a bin/* $RPM_BUILD_ROOT%{_libdir}/cinelerra
mv $RPM_BUILD_ROOT{%{_libdir}/cinelerra,%{_bindir}}/cinelerra
rm -r $RPM_BUILD_ROOT%{_libdir}/cinelerra/c_flags

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc doc/{*.png,*.html,press} cinelerra/{CHANGELOG*,TODO}
%attr(755,root,root) %{_bindir}/cinelerra
%dir %{_libdir}/cinelerra
%attr(755,root,root) %{_libdir}/cinelerra/*.plugin
%{_libdir}/cinelerra/Cinelerra_plugins
