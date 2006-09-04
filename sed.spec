%ifos linux
%define _bindir /bin
%endif

Summary: A GNU stream text editor.
Name: sed
Version: 4.1.5
Release: 5%{?dist}
License: GPL
Group: Applications/Text
Source0: ftp://ftp.gnu.org/pub/gnu/sed/sed-%{version}.tar.gz
Source1: http://sed.sourceforge.net/sedfaq.txt
Patch0: sed-4.1.5-utf8performance.patch
Patch1: sed-4.1.5-bz185374.patch
Patch2: sed-4.1.5-relsymlink.patch
Prereq: /sbin/install-info
Prefix: %{_prefix}
Buildroot: %{_tmppath}/%{name}-root
BuildRequires: glibc >= 2.3.3-28, glibc-devel >= 2.3.3-28
Requires: glibc >= 2.3.3-28

%description
The sed (Stream EDitor) editor is a stream or batch (non-interactive)
editor.  Sed takes text as input, performs an operation or set of
operations on the text and outputs the modified text.  The operations
that sed performs (substitutions, deletions, insertions, etc.) can be
specified in a script file or from the command line.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%configure --without-included-regex
make %{_smp_mflags}
install -m 644 %{SOURCE1} sedfaq.txt
gzip -9 sedfaq.txt

echo ====================TESTING=========================
make check
echo ====================TESTING END=====================

%install
rm -rf ${RPM_BUILD_ROOT}

%makeinstall
rm -f ${RPM_BUILD_ROOT}/%{_infodir}/dir

%find_lang %{name}

%post
/sbin/install-info %{_infodir}/sed.info.gz %{_infodir}/dir

%preun
if [ $1 = 0 ]; then
   /sbin/install-info --delete %{_infodir}/sed.info.gz %{_infodir}/dir
fi

%clean
rm -rf ${RPM_BUILD_ROOT}

%files -f %{name}.lang
%defattr(-,root,root)
%doc BUGS NEWS THANKS README AUTHORS sedfaq.txt.gz
%{_bindir}/sed
%{_infodir}/*.info*
%{_mandir}/man*/*

%changelog
* Mon Sep  4 2006 Petr Machata <pmachata@redhat.com> - 4.1.5-5
- Fix handling of relative symlinks (#205122)

* Wed Aug  3 2006 Petr Machata <pmachata@redhat.com> - 4.1.5-4
- remove superfluous multibyte processing in str_append for UTF-8
  encoding (thanks Paolo Bonzini, #177246)

* Mon Jul 17 2006 Petr Machata <pmachata@redhat.com> - 4.1.5-3
- use dist tag

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 4.1.5-2.2.1
- rebuild

* Thu Jun 29 2006 Petr Machata <pmachata@redhat.com> - 4.1.5-2.2
- typo in patch name

* Thu Jun 29 2006 Petr Machata <pmachata@redhat.com> - 4.1.5-2.1
- rebuild

* Thu Jun 29 2006 Petr Machata <pmachata@redhat.com> - 4.1.5-2
- #185374:
  - Follow symlinks before rename (avoid symlink overwrite)
  - Add -c flag for copy instead of rename (avoid ownership change)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 4.1.5-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 4.1.5-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Feb 06 2006 Florian La Roche <laroche@redhat.com>
- 4.1.5

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Mar 17 2005 Jakub Jelinek <jakub@redhat.com> 4.1.4-1
- update to 4.1.4

* Sat Mar  5 2005 Jakub Jelinek <jakub@redhat.com> 4.1.2-5
- rebuilt with GCC 4

* Fri Oct  8 2004 Jakub Jelinek <jakub@redhat.com> 4.1.2-4
- fix up make check to run sed --version with LC_ALL=C
  in the environment (#129014)

* Sat Oct  2 2004 Jakub Jelinek <jakub@redhat.com> 4.1.2-3
- add sedfaq.txt to %{_docdir} (#16202)

* Mon Aug 23 2004 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 4.1.2

* Thu Jul  8 2004 Jakub Jelinek <jakub@redhat.com> 4.1.1-1
- update to 4.1.1

* Mon Jun 21 2004 Jakub Jelinek <jakub@redhat.com> 4.1-1
- update to 4.1

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue May 25 2004 Jakub Jelinek <jakub@redhat.com> 4.0.9-1
- update to 4.0.9
- BuildRequire recent glibc and glibc-devel (#123043)

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan  7 2004 Jakub Jelinek <jakub@redhat.com> 4.0.8-3
- if not -n, print current buffer after N command on the last line
  unless POSIXLY_CORRECT (#112952)
- adjust XFAIL_TESTS for the improved glibc regex implementation
  (#112642)

* Fri Nov 14 2003 Jakub Jelinek <jakub@redhat.com> 4.0.8-2
- enable --without-included-regex again
- use fastmap for regex searching

* Sat Oct 25 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 4.0.8
- simplify specfile
- disable --without-included-regex to pass the testsuite

* Thu Jun 26 2003 Jakub Jelinek <jakub@redhat.com> 4.0.7-3
- rebuilt

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sat Apr 12 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 4.0.7
- use "--without-included-regex"
- do not gzip info pages in spec file, "TODO" is not present anymore

* Thu Jan 23 2003 Jakub Jelinek <jakub@redhat.com> 4.0.5-1
- update to 4.0.5

* Tue Oct 22 2002 Jakub Jelinek <jakub@redhat.com>
- rebuilt to fix x86-64 miscompilation
- run make check in %%build

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri Apr  5 2002 Jakub Jelinek <jakub@redhat.com>
- Remove stale URLs from documentation (#62519)

* Sun Jun 24 2001 Elliot Lee <sopwith@redhat.com>
- Bump release + rebuild.

* Mon Dec 18 2000 Yukihiro Nakai <ynakai@redhat.com>
- Update to 2000.11.28 patch
- Rebuild for 7.1 tree

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Mon Jun  5 2000 Jeff Johnson <jbj@redhat.com>
- FHS packaging.

* Mon Feb  7 2000 Jeff Johnson <jbj@redhat.com>
- compress man pages.

* Tue Jan 18 2000 Jakub Jelinek <jakub@redhat.com>
- rebuild with glibc 2.1.3 to fix an mmap64 bug in sys/mman.h

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 4)

* Tue Aug 18 1998 Jeff Johnson <jbj@redhat.com>
- update to 3.02

* Sun Jul 26 1998 Jeff Johnson <jbj@redhat.com>
- update to 3.01

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Thu Oct 23 1997 Donnie Barnes <djb@redhat.com>
- removed references to the -g option from the man page that we add

* Fri Oct 17 1997 Donnie Barnes <djb@redhat.com>
- spec file cleanups
- added BuildRoot

* Mon Jun 02 1997 Erik Troan <ewt@redhat.com>
- built against glibc
