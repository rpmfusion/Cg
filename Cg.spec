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
Release: 21%{?dist}
URL: http://developer.nvidia.com/object/cg_toolkit.html
Source0: http://developer.download.nvidia.com/cg/Cg_%{maj_version}/Cg-%{maj_version}_%{date}_x86.tgz
Source1: http://developer.download.nvidia.com/cg/Cg_%{maj_version}/Cg-%{maj_version}_%{date}_x86_64.tgz
License: Redistributable, no modification permitted and MIT

ExclusiveArch: i686 x86_64

Requires: lib%{name}(%{_target_cpu}) = %{version}-%{release}

BuildRequires:  gcc-c++
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

%description docs
NVIDIA Cg Toolkit documentation.

%package -n lib%{name}
Summary: NVIDIA Cg Toolkit shared support library
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

# Clean Trace
make -C usr/local/Cg/examples/Trace clean


%build
# Nothing to build
echo "Nothing to build,... Well not exactly"

for b in cgfxcat cginfo ; do
    make -C usr/local/Cg/examples/Tools/${b} clean
    sed -i -e 's@-DGLEW_STATIC@@' usr/local/Cg/examples/Tools/${b}/Makefile
    sed -i -e 's@-Wall@$RPM_OPT_FLAGS@' usr/local/Cg/examples/Tools/${b}/Makefile
    make -C usr/local/Cg/examples/Tools/${b} \
    GLEW=%{_prefix} \
    CG_INC_PATH=%{_builddir}/%{buildsubdir}/usr/include \
    CG_LIB_PATH=%{_builddir}/%{buildsubdir}/%{_libdir}
    mv usr/local/Cg/examples/Tools/${b}/${b} usr/bin
    strip usr/bin/${b}
    make -C usr/local/Cg/examples/Tools/${b} clean
done


%install
mkdir -p $RPM_BUILD_ROOT{%{_bindir},%{_includedir},%{_libdir},%{_mandir}}
cp -pr usr/bin/* $RPM_BUILD_ROOT%{_bindir}/
cp -pr usr/include/* $RPM_BUILD_ROOT%{_includedir}/
cp -pr .%{_libdir}/* $RPM_BUILD_ROOT%{_libdir}/

mv $RPM_BUILD_ROOT%{_bindir}/cgc $RPM_BUILD_ROOT%{_bindir}/cgc-%{_lib}

# Owernship of the alternative provides
touch $RPM_BUILD_ROOT%{_bindir}/cgc


%post
/usr/sbin/alternatives --install %{_bindir}/cgc cgc %{_bindir}/cgc-%{_lib} %{priority}  || :

%preun
if [ $1 -eq 0 ]; then
/usr/sbin/alternatives --remove cgc %{_bindir}/cgc-%{_lib} || :
fi

%post -n libCg -p /sbin/ldconfig

%postun -n libCg -p /sbin/ldconfig

%files
%ghost %{_bindir}/cgc
%{_bindir}/cgc-%{_lib}
%{_bindir}/cgfxcat
%{_bindir}/cginfo
%{_includedir}/Cg/

%files docs
%doc usr/local/Cg/docs usr/local/Cg/examples

%files -n libCg
%{_libdir}/*.so


%changelog
* Fri Aug 02 2024 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 3.1.0013-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Feb 04 2024 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 3.1.0013-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Aug 03 2023 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 3.1.0013-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Aug 08 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 3.1.0013-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild and ffmpeg
  5.1

* Thu Feb 10 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 3.1.0013-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Aug 03 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 3.1.0013-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Feb 04 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 3.1.0013-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Aug 19 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 3.1.0013-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Feb 05 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 3.1.0013-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Aug 09 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 3.1.0013-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Mar 05 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 3.1.0013-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Aug 19 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 3.1.0013-10
- Rebuilt for Fedora 29 Mass Rebuild binutils issue

* Fri Jul 27 2018 RPM Fusion Release Engineering <sergio@serjux.com> - 3.1.0013-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Mar 02 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 3.1.0013-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 3.1.0013-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Mar 25 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 3.1.0013-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jul 05 2016 Julian Sikorski <belegdol@fedoraproject.org> - 3.1.0013-5
- Fixed build failure caused by presence of forward slashes in $RPM_OPT_FLAGS

* Sun Aug 31 2014 Sérgio Basto <sergio@serjux.com> - 3.1.0013-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Mar 12 2013 Nicolas Chauvet <kwizart@gmail.com> - 3.1.0013-3
- https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jun 13 2012 Nicolas Chauvet <kwizart@gmail.com> - 3.1.0013-2
- Clean the Trace directory - rfbz#1708#c3

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
