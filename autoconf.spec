%define name	autoconf
%define version	2.61
%define release %mkrel 4

%define docheck 1
%{?_without_check: %global docheck 0}

Name:		%{name}
Summary:	A GNU tool for automatically configuring source code
Version:	%{version}
Release:	%{release}
Epoch:		1
License:	GPL
Group:		Development/Other
URL:		http://www.gnu.org/software/autoconf/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot/
BuildArch:	noarch

Source:		ftp://ftp.gnu.org/gnu/autoconf/autoconf-%{version}.tar.bz2
Source1:	autoconf-site-start.el

Requires(post):	/sbin/install-info
Requires(preun):	/sbin/install-info
BuildRequires:	texinfo m4
BuildRequires:	help2man
Requires:	m4 mktemp
Obsoletes:	autoconf2.5
Provides:	autoconf2.5 = %{epoch}:%{version}-%{release}
Conflicts:	autoconf2.1 < 2.13-26

# for tests
%if %docheck
BuildRequires:	flex
BuildRequires:	bison
%endif

%description
GNU's Autoconf is a tool for configuring source code and Makefiles.
Using Autoconf, programmers can create portable and configurable
packages, since the person building the package is allowed to 
specify various configuration options.

You should install Autoconf if you are developing software and you'd
like to use it to create shell scripts which will configure your 
source code packages. If you are installing Autoconf, you will also
need to install the GNU m4 package.

Note that the Autoconf package is not required for the end user who
may be configuring software with an Autoconf-generated script; 
Autoconf is only required for the generation of the scripts, not
their use.

%prep
%setup -q -n autoconf-%{version}

%build
%configure2_5x
# parallel build does not work
make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

# We don't want to include the standards.info stuff in the package,
# because it comes from binutils...
rm -f $RPM_BUILD_ROOT%{_infodir}/standards*

# emacs stuff
install -D -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/emacs/site-start.d/%{name}.el

# if emacs-bin was not here, *.el and *.elc files will be missing - install *.el files anyway
if [ ! -d $RPM_BUILD_ROOT/%{_datadir}/emacs/site-lisp ]; then
	mkdir -p $RPM_BUILD_ROOT/%{_datadir}/emacs/site-lisp
	install -m644 lib/emacs/*.el $RPM_BUILD_ROOT/%{_datadir}/emacs/site-lisp
fi

%if %docheck
%check
make check	# VERBOSE=1
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
%_install_info autoconf.info

%preun
%_remove_install_info autoconf.info

%files
%defattr(-,root,root)
%doc AUTHORS BUGS ChangeLog* COPYING INSTALL NEWS README THANKS TODO
%config(noreplace) %{_sysconfdir}/emacs/site-start.d/*.el
%{_bindir}/*
%{_datadir}/autoconf
%{_datadir}/emacs/site-lisp/*.el*
%{_infodir}/*
%{_mandir}/*/*
