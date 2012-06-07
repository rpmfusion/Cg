%define maj_version 3.1
%define min_version 0013
%define date April2012

# No debuginfo
%define debug_package %{nil}
# Disable strip
%define __strip /bin/true

%ifarch x86_64
%define priority 10
%else
%define priority 5
%endif

Summary: NVIDIA Cg Toolkit
Name: Cg
Version: %{maj_version}.%{min_version}
Release: 1%{?dist}
URL: http://developer.nvidia.com/object/cg_toolkit.html
Group: Development/Languages
Source0: http://developer.download.nvidia.com/cg/Cg_%{maj_version}/Cg-%{maj_version}_%{date}_x86.tgz
Source1: http://developer.download.nvidia.com/cg/Cg_%{maj_version}/Cg-%{maj_version}_%{date}_x86_64.tgz
License: Redistributable, no modification permitted and MIT
%if 0%{?fedora} > 11 || 0%{?rhel} > 5
ExclusiveArch: i686 x86_64
%else 0%{?fedora} == 11
ExclusiveArch: i586 x86_64
%else
ExclusiveArch: i386 x86_64
%endif
Requires: lib%{name}(%{_target_cpu}) = %{version}-%{release}
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  freeglut-devel
BuildRequires:  glew-devel >= 1.5.1
BuildRequires:  libXi-devel
BuildRequires:  libXmu-devel

Requires(post): /usr/sbin/alternatives
Requires(preun): /usr/sbin/alternatives


%description
The Cg Toolkit provides a compiler for the Cg language, runtime
libraries for use with both leading graphics APIs, runtime libraries for
CgFX, example applications, and extensive documentation. Supporting over
20 different OpenGL and DirectX profile targets, Cg will allow you to
incorporate stunning interactive effects into your 3D applications.

This is the %{date} release

%package docs
Summary: NVIDIA Cg Toolkit documentation
Group: Documentation

%description docs
NVIDIA Cg Toolkit documentation.

%package -n lib%{name}
Summary: NVIDIA Cg Toolkit shared support library
Group: System Environment/Libraries
Provides: lib%{name}(%{_target_cpu}) = %{version}-%{release}

%description -n lib%{name}
This package contains Cg shared support library.

%prep
%ifarch %{ix86}
%setup -q -c %{name}-%{version}
%endif
%ifarch x86_64
%setup -q -c %{name}-%{version} -D -T -a 1
%endif

#Remove binary bundled tools
rm usr/bin/{cginfo,cgfxcat}

#Clean exemples.
for d in $(find usr/local/Cg/examples/OpenGL/{basic,advanced} -type d); do
  pushd ${d} ; make clean ; popd
done

for d in usr/local/Cg/examples/Tools/{cgfxcat,cginfo} usr/local/Cg/examples/OpenGL/glew ; do
  pushd ${d} ; make clean ; popd
done


%build
# Nothing to build
echo "Nothing to build,... Well not exactly"

for b in cgfxcat cginfo ; do
    make -C usr/local/Cg/examples/Tools/${b} clean
    sed -i -e 's/-DGLEW_STATIC//' usr/local/Cg/examples/Tools/${b}/Makefile
    sed -i -e 's/-Wall/%{optflags}/' usr/local/Cg/examples/Tools/${b}/Makefile
    make -C usr/local/Cg/examples/Tools/${b} \
    GLEW=%{_prefix} \
    CG_INC_PATH=%{_builddir}/%{buildsubdir}/usr/include \
    CG_LIB_PATH=%{_builddir}/%{buildsubdir}/%{_libdir}
    mv usr/local/Cg/examples/Tools/${b}/${b} usr/bin
    strip usr/bin/${b}
    make -C usr/local/Cg/examples/Tools/${b} clean
done


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT{%{_bindir},%{_includedir},%{_libdir},%{_mandir}}
cp -pr usr/bin/* $RPM_BUILD_ROOT%{_bindir}/
cp -pr usr/include/* $RPM_BUILD_ROOT%{_includedir}/
cp -pr .%{_libdir}/* $RPM_BUILD_ROOT%{_libdir}/

mv $RPM_BUILD_ROOT%{_bindir}/cgc $RPM_BUILD_ROOT%{_bindir}/cgc-%{_lib}

# Owernship of the alternative provides
touch $RPM_BUILD_ROOT%{_bindir}/cgc


%clean
rm -rf $RPM_BUILD_ROOT

%post
/usr/sbin/alternatives --install %{_bindir}/cgc cgc %{_bindir}/cgc-%{_lib} %{priority}  || :

%preun
if [ $1 -eq 0 ]; then
/usr/sbin/alternatives --remove cgc %{_bindir}/cgc-%{_lib} || :
fi

%post -n libCg -p /sbin/ldconfig

%postun -n libCg -p /sbin/ldconfig

%files
%defattr(755,root,root,755)
%ghost %{_bindir}/cgc
%{_bindir}/cgc-%{_lib}
%{_bindir}/cgfxcat
%{_bindir}/cginfo
%defattr(644,root,root,755)
%{_includedir}/Cg/

%files docs
%defattr(644,root,root,755)
%doc usr/local/Cg/docs usr/local/Cg/examples

%files -n libCg
%defattr(755,root,root,755)
%{_libdir}/*.so


%changelog
* Thu Jun 07 2012 Nicolas Chauvet <kwizart@gmail.com> - 3.1.0013-1
- Update to 3.1.0013 (April2012)

* Thu Mar 08 2012 Nicolas Chauvet <kwizart@gmail.com> - 3.0.0016-3
- Rebuilt for c++ ABI breakage

* Thu Feb 09 2012 Nicolas Chauvet <kwizart@gmail.com> - 3.0.0016-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Mar 22 2011 Nicolas Chauvet <kwizart@gmail.com> - 3.0.0016-1
- Update to 3.0.0016 (February2011)

* Thu Feb 03 2011 Nicolas Chauvet <kwizart@gmail.com> - 3.0.0015-1
- Update to 3.0.0015 (November2010)

* Mon Oct 11 2010 Nicolas Chauvet <kwizart@gmail.com> - 3.0.0007-2
- rebuilt for compiler bug

* Fri Sep 17 2010 Nicolas Chauvet <kwizart@gmail.com> - 3.0.0007-1
- Update to 3.0.007 (July2010)

* Sun Feb 28 2010 Nicolas Chauvet <kwizart@fedoraproject.org> - 2.2.0017-1
- Update to 2.2.0017 (February2010)

* Sat Nov 14 2009 Nicolas Chauvet <kwizart@fedoraproject.org> - 2.2.0008-1
- Update to 2.2.0008 (October2009)

* Fri May 15 2009 kwizart < kwizart at gmail.com > - 2.2-2
- Clean exemples.

* Wed Apr 22 2009 kwizart < kwizart at gmail.com > - 2.2-1
- Update to 2.2.0006 (April2009)

* Fri Mar 27 2009 kwizart < kwizart at gmail.com > - 2.1.0017-1
- Update to 2.1.0017 (February2009)
- Re-introduce disttag
- Disable strip
- Fix some conditionnals

* Fri Jan  9 2009 kwizart < kwizart at gmail.com > - 2.1.0016-1
- Update to 2.1.0016 (November2008)

* Sun May 18 2008 kwizart < kwizart at gmail.com > - 2.0.0015-1
- Update to 2.0.0015 (May2008)
- No debuginfo anymore

* Sat May 10 2008 kwizart < kwizart at gmail.com > - 2.0.0012-2
- Ghost to have the owenrship of the alternative provides.

* Sat Feb 16 2008 kwizart < kwizart at gmail.com > - 2.0.0012-1
- Update to Jan2008
- Tweak to have debuginfo
- Add alternatives to choose between cgc x86 or x86_64

* Thu Jan  3 2008 kwizart < kwizart at gmail.com > - 2.0.0010-1
- Update to 2.0.0010 (Dec2007)

* Thu Nov 29 2007 kwizart < kwizart at gmail.com > - 1.5.0023-1
- Update to 1.5.0023 (Sep2007)

* Tue Jul 24 2007 Dominik Mierzejewski <rpm@greysector.net> 1.5-1
- updated to 1.5
- split off docs
- call ldconfig for libCg
- per-arch Requires:

* Mon May 22 2006 Dominik Mierzejewski <rpm@greysector.net> 1.4.1-1
- initial build
