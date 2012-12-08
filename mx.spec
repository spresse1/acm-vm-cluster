Name: mx
Version: 1.2.16
Release: 1
License: Myricom
Summary: MX software for Myrinet
Group: Cluster software
#This is just wrong.  See http://www.rpm.org/max-rpm/s1-rpm-inside-tags.html
# for what this tag ACTUALLY does.
#Buildroot: /root/mx-1.2.16/rpm-buildroot
Prefix: /usr/local
Source: http://www.myricom.com/pub/MX2G/mx2g_1.2.16.tar.gz
Patch0: mx-update-to-3.x.patch

#%define _rpmdir .
#%define _rpmfilename %%{NAME}-%%{VERSION}-%%{RELEASE}.%%{ARCH}.rpm

%description
MX software for Myrinet

%prep
%setup
%patch0 -p1
echo "BUILDDIR: $RPM_BUILD_DIR"

%build
./configure --prefix="$RPM_BUILDROOT_DIR"
make

%install
echo "beginning insall"
make DESTDIR="$RPM_BUILD_ROOT" install
rm "$RPM_BUILD_ROOT/lib"

%files
%defattr(-,root,root)
#"/opt/mx/*/*"
#"/opt/mx/productinfo"
"/opt/mx/bin/*"
"/opt/mx/include/*"
"/opt/mx/lib64/*"
"/opt/mx/sbin/*"
"/opt/mx/productinfo/"

%post
/bin/grep -q /opt/mx/lib32/ /etc/ld.so.conf || echo /opt/mx/lib32/ >> /etc/ld.so.conf
/bin/grep -q /opt/mx/lib64 /etc/ld.so.conf || echo /opt/mx/lib64/ >> /etc/ld.so.conf
/sbin/ldconfig
if [ -n "`/sbin/lspci -d 14c1:`" ] ; then
  /opt/mx/sbin/mx_local_install
   chkconfig --add mx || /bin/true
fi

%preun
chkconfig --del mx || /bin/true

