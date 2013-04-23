%define kversion %( uname -r | awk -F[-_] '{print $1}' )
%define mxversion 1.2.16

Name: mx
Release: 1
Version: %{mxversion}
Source: http://www.myricom.com/pub/MX2G/mx2g_1.2.16.tar.gz
License: Myricom
Summary: MX software for Myrinet
Patch0: mx-update-k[un]map_atomic.patch
Patch1: mx-update-struct-ethtools_opt.patch
Patch2: mx-update-daemonize.patch

%description
MX software for Myrinet Fiber cards

# This is just wrong.  See http://www.rpm.org/max-rpm/s1-rpm-inside-tags.html
# for what this tag ACTUALLY does.
#Buildroot: /root/mx-1.2.16/rpm-buildroot

%package -n kmod-mx

#Name: kmod-mx
Version: %{mxversion}_%(echo %{kversion} | sed s/-/_/g )
Group: System Environment/Kernel
Summary: mx2g driver built for kernel %{kversion}
Prefix: /usr/local

%description -n kmod-mx
mx2g driver built for kernel %{kversion}

# OpenAFS used %{_target_cpu} here.  I disagree
Requires: kernel = %{kversion}

%package -n dkms-mx
Version: %{mxversion}
Group: System Environment/Kernel
Summary: dkms verison of mx2g driver
Requires: dkms

%description -n dkms-mx
DKMS version of mx2g driver

%prep
%setup -n mx-%{mxversion} # tell it we're expecting to go to the mx folder
%patch0 -p1
%patch1 -p1
echo "BUILDDIR: $RPM_BUILD_DIR"

%build
./configure --prefix="$RPM_BUILDROOT_DIR/"
#mkdir -p "$RPM_BUILD_ROOT/usr/src/mx-%{mxversion}/"
#cp -r `pwd` "$RPM_BUILD_ROOT/usr/src/mx-%{mxversion}"
make

%install
# make install
make DESTDIR="$RPM_BUILD_ROOT" install

#Some random cleanup
rm "$RPM_BUILD_ROOT/lib"

# copy in DKMS config
mkdir -p "$RPM_BUILD_ROOT/usr/src/mx-%{mxversion}/"
cp "$RPM_SOURCE_DIR/mx-dkms.conf" "$RPM_BUILD_ROOT/usr/src/mx-%{mxversion}/dkms.conf"

#Get sources for DKMS
mkdir -p "$RPM_BUILD_ROOT/usr/src/"
tar xf %{S:0} -C "$RPM_BUILD_ROOT/usr/src/"
cd "$RPM_BUILD_ROOT/usr/src/mx-%{mxversion}"
./configure --prefix=/
#make

%files -n kmod-mx
%defattr(-,root,root)
#"/opt/mx/*/*"
#"/opt/mx/productinfo"
"/bin/*"
"/include/*"
"/lib64/*"
"/sbin/*"
"/productinfo/"

%preun -n kmod-mx
chkconfig --del mx || /bin/true

%files -n dkms-mx
%defattr(-,root,root)
/usr/src/mx-%{mxversion}/

%post -n kmod-mx
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

%pre -n dkms-mx
dkms -m mx -v 1.2.16 --all || true

%post -n dkms-mx
dkms add -m mx -v %{mxversion}
