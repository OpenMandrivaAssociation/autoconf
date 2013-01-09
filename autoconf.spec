%define docheck 1
%{?_without_check: %global docheck 0}

Name:		autoconf
Summary:	A GNU tool for automatically configuring source code
Version:	2.69
Release:	2
Epoch:		1
License:	GPLv2+ with exceptions
Group:		Development/Other
URL:		http://www.gnu.org/software/autoconf/
BuildArch:	noarch

Source:		ftp://ftp.gnu.org/gnu/autoconf/autoconf-%{version}.tar.xz
Source1:	autoconf-site-start.el
Patch0:		autoconf-2.62-fix-multiline-string.patch
Patch1:		autoconf-2.64-drop-failing-parallel-test.patch
BuildRequires:	texinfo m4
BuildRequires:	help2man
Requires:	m4 mktemp
Obsoletes:	autoconf2.5
Provides:	autoconf2.5 = %{epoch}:%{version}-%{release}
Conflicts:	autoconf2.1 < 1:2.13-26

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
%patch0 -p1 -b .multiline
%patch1 -p1 -b .droptest

%build
%configure2_5x --build=%_host
%make

%install
rm -rf %{buildroot}
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

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS BUGS COPYING INSTALL NEWS README THANKS TODO
%config(noreplace) %{_sysconfdir}/emacs/site-start.d/*.el
%{_bindir}/*
%{_datadir}/autoconf
%{_datadir}/emacs/site-lisp/*.el*
%{_infodir}/*
%{_mandir}/*/*


%changelog
* Wed Apr 25 2012 Bernhard Rosenkraenzer <bero@bero.eu> 1:2.69-1
+ Revision: 793320
- Update to 2.69

* Mon May 02 2011 Oden Eriksson <oeriksson@mandriva.com> 1:2.68-2
+ Revision: 662893
- mass rebuild

* Thu Sep 23 2010 Funda Wang <fwang@mandriva.org> 1:2.68-1mdv2011.0
+ Revision: 580689
- new version 2.68

* Tue Aug 03 2010 Funda Wang <fwang@mandriva.org> 1:2.67-1mdv2011.0
+ Revision: 565627
- New version 2.67

* Sun Jul 11 2010 Funda Wang <fwang@mandriva.org> 1:2.66-2mdv2011.0
+ Revision: 550604
- add upstream patch to fix regression on AC_CHECK_SIZEOF

* Sun Jul 11 2010 Funda Wang <fwang@mandriva.org> 1:2.66-1mdv2011.0
+ Revision: 550566
- new version 2.66

* Fri Dec 04 2009 Funda Wang <fwang@mandriva.org> 1:2.65-1mdv2010.1
+ Revision: 473236
- new version 2.65

* Tue Oct 06 2009 Thierry Vignaud <tv@mandriva.org> 1:2.64-3mdv2010.0
+ Revision: 454722
- do not package huge ChangeLogs

* Sun Aug 30 2009 Guillaume Rousse <guillomovitch@mandriva.org> 1:2.64-2mdv2010.0
+ Revision: 422469
- drop failing parallel test
- fix hard failure test

  + Oden Eriksson <oeriksson@mandriva.com>
    - rebuild

  + Funda Wang <fwang@mandriva.org>
    - New version 2.64

* Fri Sep 12 2008 Funda Wang <fwang@mandriva.org> 1:2.63-1mdv2009.0
+ Revision: 284016
- New version 2.63

* Wed Aug 06 2008 Thierry Vignaud <tv@mandriva.org> 1:2.62-3mdv2009.0
+ Revision: 264324
- rebuild early 2009.0 package (before pixel changes)

* Sat Apr 19 2008 Per Øyvind Karlsen <peroyvind@mandriva.org> 1:2.62-2mdv2009.0
+ Revision: 195751
- parallel build works now, so let's reenable it!
- make oden a happy camper (aka fix bug with multine variables that br0ke build of mysql, php etc., P0)

* Wed Apr 16 2008 Guillaume Rousse <guillomovitch@mandriva.org> 1:2.62-1mdv2009.0
+ Revision: 194448
- new version

* Fri Jan 11 2008 Thierry Vignaud <tv@mandriva.org> 1:2.61-7mdv2008.1
+ Revision: 148881
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Fri Sep 21 2007 Pixel <pixel@mandriva.com> 1:2.61-6mdv2008.0
+ Revision: 91811
- conflict on autoconf2.1 must include its epoch

* Thu Aug 23 2007 Thierry Vignaud <tv@mandriva.org> 1:2.61-5mdv2008.0
+ Revision: 69351
- kill file require on info-install

* Wed Jun 20 2007 Anssi Hannula <anssi@mandriva.org> 1:2.61-4mdv2008.0
+ Revision: 41869
- add conflict with old autoconf2.1 to ensure smooth upgrade

* Thu Jun 14 2007 Christiaan Welvaart <spturtle@mandriva.org> 1:2.61-3mdv2008.0
+ Revision: 39545
- rename to autoconf
- drop wrapper script
- rename autoconf2.5 to autoconf

  + David Walluck <walluck@mandriva.org>
    - include other documentation in addition to just README in %%doc
    - move make check to %%check

