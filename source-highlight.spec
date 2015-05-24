Summary:	GNU Source Highlight
Name:		source-highlight
Version:	3.1.8
Release:	1
License:	GPL v3+
Group:		Applications/Publishing
Source0:	http://ftp.gnu.org/gnu/src-highlite/%{name}-%{version}.tar.gz
# Source0-md5:	3243470706ef5fefdc3e43b5306a4e41
URL:		http://www.gnu.org/software/src-highlite/
BuildRequires:	automake
BuildRequires:	boost-devel
BuildRequires:	flex
BuildRequires:	libstdc++-devel
BuildRequires:	texinfo
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This program, given a source file, produces a document with syntax
highlighting.

%package libs
Summary:	Source highlight library
Group:		Libraries

%description libs
Source highlight library.

%package devel
Summary:	Header file for srchlite library
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header file for srchlite library.

%package -n bash-completion-%{name}
Summary:	BASH auto-complete site functions
Group:		Documentation
Requires:	%{name} = %{version}-%{release}
Requires:	bash

%description -n bash-completion-%{name}
BASH auto-complete site functions.


%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal} -I m4 -I gl/m4
%{__autoheader}
%{__automake}
%{__autoconf}
%configure \
	--disable-static	\
	--with-bash-completion=%{_datadir}/bash-completion/completions
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

mv -f $RPM_BUILD_ROOT%{_docdir}/%{name}/* \
	$RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /usr/sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%postun	-p /usr/sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%post	libs -p /usr/sbin/ldconfig
%postun	libs -p /usr/sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README THANKS TODO.txt doc/{*.css,*.html,*.java}
%attr(755,root,root) %{_bindir}/check-regexp
%attr(755,root,root) %{_bindir}/cpp2html
%attr(755,root,root) %{_bindir}/java2html
%attr(755,root,root) %{_bindir}/source-highlight
%attr(755,root,root) %{_bindir}/source-highlight-esc.sh
%attr(755,root,root) %{_bindir}/source-highlight-settings
%attr(755,root,root) %{_bindir}/src-hilite-lesspipe.sh
%{_mandir}/man1/check-regexp.1*
%{_mandir}/man1/source-highlight.1*
%{_mandir}/man1/source-highlight-settings.1*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*
%{_infodir}/source-highlight.info*
%{_infodir}/source-highlight-lib.info*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %ghost %{_libdir}/libsource-highlight.so.?
%attr(755,root,root) %{_libdir}/libsource-highlight.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsource-highlight.so
%{_includedir}/srchilite
%{_pkgconfigdir}/source-highlight.pc

%files -n bash-completion-%{name}
%attr(755,root,root)
%{_datadir}/bash-completion/completions/*

