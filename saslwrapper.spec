%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
%{!?ruby_sitearch: %global ruby_sitearch %(ruby -rrbconfig -e 'puts Config::CONFIG["sitearchdir"]')}

Name:           saslwrapper
Version:        0.1.934605
Release:        2%{?dist}
Summary:        Ruby and Python wrappers for the cyrus sasl library.
Group:          System Environment/Libraries
License:        ASL 2.0
URL:            http://qpid.apache.org
Source0:        %{name}-%{version}.tar.gz
Patch0:         decode_overflow.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: doxygen
BuildRequires: libtool
BuildRequires: pkgconfig
BuildRequires: ruby
BuildRequires: ruby-devel
BuildRequires: python
BuildRequires: python-devel
BuildRequires: cyrus-sasl-devel
BuildRequires: cyrus-sasl-lib
BuildRequires: cyrus-sasl
BuildRequires: swig

%description
A simple wrapper for cyrus-sasl that permits easy binding into
scripting languages.

%package devel
Summary: Header files for developing with saslwrapper.
Group: System Environment/Libraries
Requires: %name = %version-%release

%description devel
The header files for developing with saslwrapper.

%package -n python-saslwrapper
Summary: Python bindings for saslwrapper.
Group: System Environment/Libraries
Requires: %name = %version-%release
Requires: python

%description -n python-saslwrapper
Python bindings for the saslwrapper library.

%package -n ruby-saslwrapper
Summary: Ruby bindings for saslwrapper.
Group: System Environment/Libraries
Requires: %name = %version-%release
Requires: ruby

%description -n ruby-saslwrapper
Ruby bindings for the saslwrapper library.

%prep
%setup -q
%patch0 -p5

%build
%configure
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
find %{buildroot} -name "*.la" | xargs rm

%clean
rm -rf %{buildroot}

%check
make check

%files
%defattr(-,root,root,-)
%doc LICENSE
%_libdir/libsaslwrapper.so.*

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files devel
%defattr(-,root,root,-)
%_libdir/libsaslwrapper.so
%_includedir/saslwrapper.h

%files -n python-saslwrapper
%defattr(-,root,root,-)
%python_sitelib/saslwrapper.py*
%python_sitearch/_saslwrapper.so

%files -n ruby-saslwrapper
%defattr(-,root,root,-)
%ruby_sitearch/saslwrapper.so

%changelog
* Fri May 28 2010 Justin Ross <jross@redhat.com> - 0.1.934605-2
- Resolves: rhbz#597290

* Mon Apr 19 2010 Rafael Schloming <rafaels@redhat.com> - 0.1.934605-1
- Rebased to 934605.

* Tue Jan 12 2010 Rafael Schloming <rafaels@redhat.com> - 0.1.897961-3
- Moved libsaslwrapper.so symlink into devel package.

* Tue Jan 12 2010 Rafael Schloming <rafaels@redhat.com> - 0.1.897961-2
- Bump release.
- Fixed manifest for python-saslwrapper.

* Tue Jan 12 2010 Rafael Schloming <rafaels@redhat.com> - 0.1.897961-1
- Added groups to subpackages.
- Replaced python_sitelib with python_sitearch, use %%global instead of %%define, and killed unused ruby_sitelib.

* Fri Jan  8 2010 Rafael H. Schloming <rafaels@redhat.com> - 0.1.897204-1
- Initial version.
