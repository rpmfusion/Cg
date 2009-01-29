%define maj_version 2.1
%define min_version 0016
%define date November2008

# No debuginfo
%define debug_package %{nil}

%ifarch x86_64
%define priority 10
%else
%define priority 5
%endif

Summary: NVIDIA Cg Toolkit
Name: Cg
Version: %{maj_version}.%{min_version}
Release: 1
URL: http://developer.nvidia.com/object/cg_toolkit.html
Group: Development/Languages
Source0: http://developer.download.nvidia.com/cg/Cg_%{maj_version}/%{version}/Cg-%{maj_version}_%{date}_x86.tgz
Source1: http://developer.download.nvidia.com/cg/Cg_%{maj_version}/%{version}/Cg-%{maj_version}_%{date}_x86_64.tgz
License: Redistributable, no modification permitted
ExclusiveArch: i386 x86_64
Requires: lib%{name}(%{_target_cpu}) = %{version}-%{release}
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires(post): /usr/sbin/alternatives
Requires(preun): /usr/sbin/alternatives


%description
The Cg Toolkit provides a compiler for the Cg language, runtime
libraries for use with both leading graphics APIs, runtime libraries for
CgFX, example applications, and extensive documentation. Supporting over
20 different OpenGL and DirectX profile targets, Cg will allow you to
incorporate stunning interactive effects into your 3D applications.

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
%ifarch i386
%setup -q -c %{name}-%{version}
%endif
%ifarch x86_64
%setup -q -c %{name}-%{version} -D -T -a 1
%endif

# Tweak to have debuginfo - part 2/2
%if "%fedora" > "7"
cp -p %{_prefix}/lib/rpm/find-debuginfo.sh .
sed -i -e 's|strict=true|strict=false|' find-debuginfo.sh
%endif

%build
# Nothing to build
echo "Nothing to build"

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT{%{_bindir},%{_includedir},%{_libdir},%{_mandir}}
cp -pr usr/bin/* $RPM_BUILD_ROOT%{_bindir}/
cp -pr usr/include/* $RPM_BUILD_ROOT%{_includedir}/
cp -pr .%{_libdir}/* $RPM_BUILD_ROOT%{_libdir}/
cp -pr usr/share/man/* $RPM_BUILD_ROOT%{_mandir}/

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
%defattr(644,root,root,755)
%ghost %{_bindir}/cgc
%attr(755,root,root) %{_bindir}/cgc-%{_lib}
%{_includedir}/Cg/
%{_mandir}/man*/*

%files docs
%defattr(644,root,root,755)
%doc usr/local/Cg/docs usr/local/Cg/examples usr/local/Cg/include

%files -n libCg
%{_libdir}/*.so


%changelog
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
