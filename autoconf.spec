%define docheck 1
%{?_without_check: %global docheck 0}

Summary:	A GNU tool for automatically configuring source code
Name:		autoconf
Epoch:		1
Version:	2.69
Release:	13
License:	GPLv2+ with exceptions
Group:		Development/Other
Url:		http://www.gnu.org/software/autoconf/
Source0:	ftp://ftp.gnu.org/gnu/autoconf/autoconf-%{version}.tar.xz
Source1:	autoconf-site-start.el
Patch0:		autoconf-2.62-fix-multiline-string.patch
Patch1:		autoconf-2.64-drop-failing-parallel-test.patch
Patch2:		autoreconf-default-i.patch
BuildArch:	noarch

BuildRequires:	help2man
BuildRequires:	m4
BuildRequires:	texinfo
# for tests
%if %docheck
BuildRequires:	bison
BuildRequires:	flex
%endif
Requires:	m4
Provides:	autoconf2.5 = %{EVRD}

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
%setup -q
%apply_patches

%build
%configure2_5x \
	--build=%_host
%make

%install
%makeinstall_std

# We don't want to include the standards.info stuff in the package,
# because it comes from binutils...
rm -f %{buildroot}%{_infodir}/standards*

# emacs stuff
install -D -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/emacs/site-start.d/%{name}.el

# if emacs-bin was not here, *.el and *.elc files will be missing - install *.el files anyway
if [ ! -d %{buildroot}/%{_datadir}/emacs/site-lisp ]; then
	mkdir -p %{buildroot}/%{_datadir}/emacs/site-lisp
	install -m644 lib/emacs/*.el %{buildroot}/%{_datadir}/emacs/site-lisp
fi

%if %docheck
%check
make check	# VERBOSE=1
%endif

%files
%doc AUTHORS BUGS COPYING INSTALL NEWS README THANKS TODO
%config(noreplace) %{_sysconfdir}/emacs/site-start.d/*.el
%{_bindir}/*
%{_datadir}/autoconf
%{_datadir}/emacs/site-lisp/*.el*
%{_infodir}/*
%{_mandir}/*/*

