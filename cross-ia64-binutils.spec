##
## This a generated specfile from binutils.spec
##
%define cross ia64
##
# RH 2.16.91.0.2-2, SuSE 2.13.90.0.18-6
%define name		%{package_prefix}binutils
%define version		2.16.91.0.2
%define release		 %mkrel 3

%define lib_major	2
%define lib_name_orig	%{package_prefix}%mklibname binutils
%define lib_name	%{lib_name_orig}%{lib_major}

# Define if building a cross-binutils
%define package_prefix	%{nil}
%{expand: %{?cross:	%%define target_cpu %{cross}}}
%{expand: %{?cross:	%%define target_platform %{target_cpu}-linux}}
%{expand: %{?cross:	%%define package_prefix cross-%{target_cpu}-}}

Summary:	GNU Binary Utility Development Utilities
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Development/Other
URL:		http://sources.redhat.com/binutils/
Source0:	http://ftp.kernel.org/pub/linux/devel/binutils/binutils-%{version}.tar.bz2
Source1:	build_cross_binutils.sh
Buildroot:	%{_tmppath}/%{name}-%{version}-root
%if "%{name}" == "binutils"
Requires:	%{lib_name} = %{version}-%{release}
Requires(post):	info-install
Requires(preun):info-install
%endif
Conflicts:	gcc-c++ < 3.2.3-1mdk
BuildRequires:	autoconf automake bison flex gcc gettext texinfo
BuildRequires:	dejagnu
# make check'ing requires libdl.a
BuildRequires:	glibc-static-devel
Patch0:		binutils-2.15.92.0.2-x86_64-testsuite.patch.bz2
Patch1:		binutils-2.14.90.0.5-testsuite-Wall-fixes.patch.bz2
Patch2:		binutils-2.14.90.0.5-lt-relink.patch.bz2
Patch3:		binutils-2.15.92.0.2-linux32.patch.bz2
Patch4:		binutils-2.15.94.0.2-place-orphan.patch.bz2
Patch5:		binutils-2.15.92.0.2-ppc64-pie.patch.bz2
Patch6:		binutils-2.16.91.0.2-ppc32-got2.patch.bz2
Patch7:		binutils-2.16.91.0.1-deps.patch.bz2

%description
Binutils is a collection of binary utilities, including:

   * ar: creating modifying and extracting from archives
   * nm: for listing symbols from object files
   * objcopy: for copying and translating object files
   * objdump: for displaying information from object files
   * ranlib: for generating an index for the contents of an archive
   * size: for listing the section sizes of an object or archive file
   * strings: for listing printable strings from files
   * strip: for discarding symbols (a filter for demangling encoded C++ symbols
   * addr2line: for converting addresses to file and line
   * nlmconv: for converting object code into an NLM

Install binutils if you need to perform any of these types of actions on
binary files.  Most programmers will want to install binutils.

%package -n %{lib_name}
Summary: Main library for %{name}
Group: System/Libraries
Provides: %{lib_name_orig}

%description -n %{lib_name}
This package contains the library needed to run programs dynamically
linked with binutils.

%package -n %{lib_name}-devel
Summary: Main library for %{name}
Group: System/Libraries
Requires: %{lib_name} = %{version}-%{release}
Provides: %{lib_name_orig}-devel, %{name}-devel

%description -n %{lib_name}-devel
This package contains the library needed to run programs dynamically
linked with binutils.

This is the development headers for %{lib_name}

%prep
%setup -q -n binutils-%{version}
%patch0 -p1 -b .x86_64-testsuite
%patch1 -p1 -b .testsuite-Wall-fixes
%patch2 -p1 -b .lt-relink
%patch3 -p1 -b .linux32
%patch4 -p0 -b .place-orphan
%patch5 -p0 -b .ppc64-pie
%patch6 -p0 -b .ppc32-got2
%patch7 -p1 -b .deps

%build
# Additional targets
ADDITIONAL_TARGETS=
%ifarch ia64
ADDITIONAL_TARGETS="--enable-targets=i586-mandrake-linux"
%endif
%ifarch %{ix86}
ADDITIONAL_TARGETS="--enable-targets=x86_64-mandrake-linux"
%endif
ENABLE_SHARED="--enable-shared"
%if "%{name}" != "binutils"
%define _program_prefix %{target_platform}-
ADDITIONAL_TARGETS="--target=%{target_platform}"
case %{target_cpu} in
ppc | powerpc)
  ADDITIONAL_TARGETS="$ADDITIONAL_TARGETS --enable-targets=powerpc-unknown-macos10"
  ADDITIONAL_TARGETS="$ADDITIONAL_TARGETS --enable-targets=powerpc64-mandrake-linux"
  ;;
ppc64 )
  ADDITIONAL_TARGETS="$ADDITIONAL_TARGETS --enable-targets=powerpc-unknown-macos10"
  ;;
i*86 | athlon*)
  ADDITIONAL_TARGETS="$ADDITIONAL_TARGETS --enable-targets=x86_64-mandrake-linux"
  ;;
sparc)
  ADDITIONAL_TARGETS="$ADDITIONAL_TARGETS --enable-targets=sparc64-mandrake-linux --enable-64-bit-bfd"
  ;;
esac
# don't build shared libraries in cross binutils
unset ENABLE_SHARED
%endif
# Binutils comes with its own custom libtool
# [gb] FIXME: but system libtool also works and has relink fix
%define __libtoolize /bin/true
%configure $ENABLE_SHARED $ADDITIONAL_TARGETS
%make tooldir=%{_prefix} all info
%if "%{name}" != "binutils"
exit 0
%endif

# Disable gasp tests since the tool is deprecated henceforth neither
# built nor already installed
(cd gas/testsuite/gasp/; mv gasp.exp gasp.exp.disabled)

# All Tests must pass on x86 and x86_64
echo ====================TESTING=========================
%ifarch %{ix86} x86_64 ppc ppc64
%make check
%else
%make -k check || echo make check failed
%endif
echo ====================TESTING END=====================

logfile="%{name}-%{version}-%{release}.log"
rm -f $logfile; find . -name "*.sum" | xargs cat >> $logfile

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_prefix}
%makeinstall_std

%if "%{name}" == "binutils"
make prefix=$RPM_BUILD_ROOT%{_prefix} infodir=$RPM_BUILD_ROOT%{_infodir} install-info
install -m 644 include/libiberty.h $RPM_BUILD_ROOT%{_includedir}/
# Ship with the PIC libiberty
install -m 644 libiberty/pic/libiberty.a $RPM_BUILD_ROOT%{_libdir}/
rm -rf $RPM_BUILD_ROOT%{_prefix}/%{_target_platform}/
%else
rm -f  $RPM_BUILD_ROOT%{_libdir}/libiberty.a
rm -rf $RPM_BUILD_ROOT%{_infodir}
rm -rf $RPM_BUILD_ROOT%{_prefix}/%{target_cpu}-linux/lib/ldscripts/
rm -f  $RPM_BUILD_ROOT%{_prefix}/%{_target_platform}/%{target_cpu}-linux/lib/*.la
%endif

rm -f $RPM_BUILD_ROOT%{_mandir}/man1/{dlltool,nlmconv,windres}*
rm -f $RPM_BUILD_ROOT%{_infodir}/dir
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale/

%clean
rm -rf $RPM_BUILD_ROOT

%if "%{name}" == "binutils"
%post
%_install_info as.info
%_install_info bfd.info
%_install_info binutils.info
%_install_info gasp.info
%_install_info gprof.info
%_install_info ld.info
%_install_info standards.info
%endif

%if "%{name}" == "binutils"
%preun
%_remove_install_info as.info
%_remove_install_info bfd.info
%_remove_install_info binutils.info
%_remove_install_info gasp.info
%_remove_install_info gprof.info
%_remove_install_info ld.info
%_remove_install_info standards.info
%endif

%if %mdkversion < 200900
%post -n %{lib_name} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{lib_name} -p /sbin/ldconfig
%endif

%files
%defattr(-,root,root)
%doc README
%{_bindir}/*
%{_mandir}/man1/*
%if "%{name}" == "binutils"
%{_infodir}/*info*
%else
%{_prefix}/%{target_cpu}-linux/bin/*
%endif

%if "%{name}" == "binutils"
%files -n %{lib_name}
%defattr(-,root,root)
%doc README
%{_libdir}/libbfd-%{version}.so
%{_libdir}/libopcodes-%{version}.so
%endif

%if "%{name}" == "binutils"
%files -n %{lib_name}-devel
%defattr(-,root,root)
%doc README
%{_includedir}/*
%{_libdir}/libbfd.a
%{_libdir}/libbfd.so
%{_libdir}/libopcodes.a
%{_libdir}/libopcodes.so
%{_libdir}/libiberty.a
%endif

