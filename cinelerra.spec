# TODO: build guicast as separate, shared library to use in
#       xmovie, mix2000, cinelerra and bcast
Summary:	Cinelerra - capturing, editing and production of audio/video material
Summary(pl):	Cinelerra - nagrywanie, obróbka i produkcja materia³u audio/video
Name:		cinelerra
Version:	1.1.8
Release:	1
License:	GPL
Group:		X11/Applications
Source0:	http://dl.sourceforge.net/heroines/%{name}-%{version}-src.tar.bz2
# Source0-md5:	626b39c2013bdd9bea5c14421fe2ac66
Patch0:		%{name}-system-libs.patch
Patch1:		%{name}-libsndfile1.patch
Patch2:		%{name}-strip.patch
Patch3:		%{name}-fontsdir.patch
Patch4:		%{name}-freetype.patch
Patch5:		%{name}-alpha.patch
URL:		http://heroinewarrior.com/cinelerra.php3
BuildRequires:	XFree86-devel
BuildRequires:	esound-devel
BuildRequires:	freetype-devel >= 2.1.4
BuildRequires:	lame-libs-devel >= 3.93.1
BuildRequires:	libavc1394-devel >= 0.4.0
BuildRequires:	libmpeg3-devel >= 1.5.3
BuildRequires:	libsndfile-devel >= 1.0.5
BuildRequires:	libstdc++-devel
BuildRequires:	libtiff-devel
BuildRequires:	libuuid-devel
%ifarch %{ix86}
BuildRequires:	nasm
%endif
BuildRequires:	quicktime4linux-devel >= 2.0.1
Requires:	freetype >= 2.1.4
Requires:	libmpeg3 >= 1.5.3
Requires:	libsndfile >= 1.0.5
Requires:	quicktime4linux >= 2.0.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# defaulttheme and microtheme cannot be stripped
# (they have resources appended to linked binary :/)
%define		no_install_post_strip	1

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
%patch5 -p1

%build
CFLAGS="%{rpmcflags} -fno-rtti"; export CFLAGS
%{__make} -f build/Makefile.toolame
%{__make} -C mpeg2enc
%{__make} -C mplexhi
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

%if 0%{!?debug:1}
# strip all that can be stripped
find $RPM_BUILD_ROOT%{_libdir}/cinelerra -name '*.plugin' | \
	grep -v 'defaulttheme\|microtheme' | xargs strip -R.note -R.comment
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc doc/{*.png,*.html,press} cinelerra/{CHANGELOG*,TODO}
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/cinelerra
