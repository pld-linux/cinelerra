Summary:	-
Summary(pl):	-
Name:		cinelerra
Version:	1.1.5
Release:	1
License:	GPL
Group:		X11/Applications
Source0:	http://dl.sourceforge.net/heroines/%{name}-%{version}-src.tar.bz2
# yes, it's the same source
# TODO: build guicast as separate, shared library to use in
#       xmovie, mix2000, cinerella and bcast 
Patch0:		xmovie-c++.patch
Patch1:		%{name}-system-libs.patch
Patch2:		%{name}-libsndfile1.patch
Patch3:		%{name}-c++.patch
Patch4:		%{name}-mpeg2.patch
URL:		http://heroinewarrior.com/cinelerra.php3
BuildRequires:	XFree86-devel
# it's sick, but it's true - it used libuuid functions
BuildRequires:	e2fsprogs-devel
BuildRequires:	esound-devel
BuildRequires:	libavc1394-devel >= 0.4.0
BuildRequires:	libmpeg3-devel >= 1.5.0
BuildRequires:	libsndfile-devel >= 1.0.0
BuildRequires:	libstdc++-devel
BuildRequires:	libtiff-devel
BuildRequires:	quicktime4linux-devel >= 1.6.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description

%description -l pl

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
CFLAGS="%{rpmcflags} -fno-rtti"; export CFLAGS
%{__make} -C mplexhi
%{__make} -C mplexlo
%{__make} -C guicast
%{__make} -C cinerella
# TODO: titler (w/freetype) fails
%{__make} -C plugins

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir}

install cinerella/*/cinerella $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%{_libdir}/cinerella
