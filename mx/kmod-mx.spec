%define kversion %( uname -r | awk -F[-_] '{print $1}' )
%define mxversion 1.2.16

Name: kmod-mx
Version: %{mxversion}_%(echo %{kversion} | sed s/-/_/g )
Release: 1
License: Myricom
Summary: MX software for Myrinet
Group: Cluster software
#This is just wrong.  See http://www.rpm.org/max-rpm/s1-rpm-inside-tags.html
# for what this tag ACTUALLY does.
#Buildroot: /root/mx-1.2.16/rpm-buildroot
Prefix: /usr/local
Source: http://www.myricom.com/pub/MX2G/mx2g_1.2.16.tar.gz
#Patch0: mx-update-to-3.x.patch # Obsoleted by a better patch
Patch0: mx-update-k[un]map_atomic.patch
Patch1: mx-update-struct-ethtools_opt.patch

# OpenAFS used %{_target_cpu} here.  I disagree
Requires: kernel = %{kversion}

%description
MX software for Myrinet

%prep
%setup -n mx-%{mxversion} # tell it we're expecting to go to the mx folder
%patch0 -p1
%patch1 -p1
echo "BUILDDIR: $RPM_BUILD_DIR"

%build
./configure --prefix="$RPM_BUILDROOT_DIR/"
make

%install
echo "beginning insall"
make DESTDIR="$RPM_BUILD_ROOT" install
rm "$RPM_BUILD_ROOT/lib"

%files
%defattr(-,root,root)
#"/opt/mx/*/*"
#"/opt/mx/productinfo"
"/bin/*"
"/include/*"
"/lib64/*"
"/sbin/*"
"/productinfo/"

%post
#/bin/grep -q /opt/mx/lib32/ /etc/ld.so.conf || echo /opt/mx/lib32/ >> /etc/ld.so.conf
#/bin/grep -q /opt/mx/lib64 /etc/ld.so.conf || echo /opt/mx/lib64/ >> /etc/ld.so.conf
#/sbin/ldconfig

#Fake /lib links
ln -s /lib64/libmyriexpress.so /lib/libmyriexpress.so
ln -s /lib64/libmyriexpress.a /lib/libmyriexpress.a

if [ -n "`/sbin/lspci -d 14c1:`" ] ; then
  /sbin/mx_local_install
  chkconfig --add mx || /bin/true
fi

%preun
chkconfig --del mx || /bin/true

