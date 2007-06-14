%define name	autoconf2.5
%define version	2.61
%define release %mkrel 2

%define docheck 1
%{?_without_check: %global docheck 0}

# Factorize uses of autoconf libdir home and
# handle only one exception in rpmlint
%define scriptdir %{_datadir}/autotools

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
Source2:	autoconf_special_readme2.5
Source3:	autoconf-ac-wrapper.pl
Patch0:		autoconf-2.59-fix-info.patch

Requires(post):	/sbin/install-info
Requires(preun):	/sbin/install-info
BuildRequires:	texinfo m4
BuildRequires:	help2man
Requires:	m4 mktemp
Requires:	autoconf2.1
Conflicts:	autoconf <= 1:2.13-19mdk
Provides:	autoconf = %{epoch}:%{version}-%{release}

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

%{expand:%(cat %{SOURCE2})}

%prep
%setup -q -n autoconf-%{version}
%patch0 -p1 -b .addinfo
install -m644 %{SOURCE2} IMPORTANT.README.MDK

%build
%configure2_5x
# parallel build does not work
make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std

# automatic autoconf wrapper
install -D -m 755 %{SOURCE3} $RPM_BUILD_ROOT%{scriptdir}/ac-wrapper.pl

# We don't want to include the standards.info stuff in the package,
# because it comes from binutils...
rm -f $RPM_BUILD_ROOT%{_infodir}/standards*

# links all scripts to wrapper
for i in $RPM_BUILD_ROOT%{_bindir}/*; do
	mv $i ${i}-2.5x
	ln -s %{scriptdir}/ac-wrapper.pl $i
done

mv $RPM_BUILD_ROOT%{_infodir}/autoconf.info $RPM_BUILD_ROOT%{_infodir}/autoconf-2.5x.info

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
%_install_info autoconf-2.5x.info

%preun
%_remove_install_info autoconf-2.5x.info

%files
%defattr(-,root,root)
%doc AUTHORS BUGS ChangeLog* COPYING IMPORTANT.README.MDK INSTALL NEWS README THANKS TODO
%config(noreplace) %{_sysconfdir}/emacs/site-start.d/*.el
%{_bindir}/*
%{_datadir}/autoconf
%{_datadir}/emacs/site-lisp/*.el*
%{_infodir}/*
%{_mandir}/*/*
%{scriptdir}
