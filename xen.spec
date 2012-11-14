#
# Xen on CentOS 6
#
Summary: xen virtualization software for CentOS6
Name: xen
Version: 4.2.0
Release: 1
License: GPLv2
#Group: 
Source: http://bits.xensource.com/oss-xen/release/4.2.0/xen-4.2.0.tar.gz
URL: http://www.xen.org/
Distribution: CentOS6
Vendor: Citrix Systems with RPM built by JHUACM
Packager: Steven Presser <spresse1@acm.jhu.edu>

%description
Lets face it - if you're looking at this, you already know what Xen is.  Its a hypervisor so you can run your VMs.  Its rather featureful.

%prep
%setup

%build
./configure

%install
#make install
#DISTDIR="$RPM_BUILD_ROOT" make dist
DESTDIR="$RPM_BUILD_ROOT" make install
mkdir -p "$RPM_BUILD_ROOT/etc/ld.so.conf.d"
echo "/usr/lib/
/usr/lib64" >> "$RPM_BUILD_ROOT/etc/ld.so.conf.d/xen.conf"
echo "Build root is: $RPM_BUILD_ROOT"
#cp -rnp "$RPM_BUILD_ROOT/install" "$RPM_BUILD_ROOT/usr"

%files
%defattr(-,root,root)
/boot/*
/etc/*
/usr/*
/var/*

%post
ldconfig
ln -s /etc/init.d/xendomains /etc/rc0.d/S10xendomains
ln -s /etc/init.d/xendomains /etc/rc6.d/S10xendomains
ln -s /etc/init.d/xencommons /etc/rc3.d/S98xencommons
ln -s /etc/init.d/xendomains /etc/rc3.d/S98xendomains
ln -s /root/xendom0caps /etc/rc3.d/S98xendom0caps

%postun
ldconfig
rm /etc/rc0.d/S10xendomains
rm /etc/rc6.d/S10xendomains
rm /etc/rc3.d/S98xencommons
rm /etc/rc3.d/S98xendomains
rm /etc/rc3.d/S98xendom0caps

