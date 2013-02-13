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
BuildRequires: git, patch, make, texinfo, python-devel, dev86, iasl, yajl-devel
BuildRequires: libuuid-devel, ncurses-devel, glib2-devel, openssl-devel

%description
Lets face it - if you're looking at this, you already know what Xen is.  Its a hypervisor so you can run your VMs.  Its rather featureful.

%prep
%setup

%build
./configure

%install
#make install
#DISTDIR="$RPM_BUILD_ROOT" make dist
make xen
make tools
make stubdom
DESTDIR="$RPM_BUILD_ROOT" make install
#mkdir -p "$RPM_BUILD_ROOT/etc/ld.so.conf.d"
#echo "/usr/lib/
#/usr/lib64" >> "$RPM_BUILD_ROOT/etc/ld.so.conf.d/xen.conf"
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
chkconfig --level 345 xencommons on
chkconfig --level 345 xend on

%preun
chkconfig xencommons off
chkconfig xend off

%postun
ldconfig
rm /etc/rc0.d/S10xendomains
rm /etc/rc6.d/S10xendomains
rm /etc/rc3.d/S98xencommons
rm /etc/rc3.d/S98xendomains
rm /etc/rc3.d/S98xendom0caps

#!/bin/sh

#This script adds the xen kernel to the relevent grub boot files, tehn repoints
#the default kernel to be a xen kernel

#/etc/grub.conf is a symlink to this file anyway...
FILES="/boot/grub/grub.conf /etc/grub.conf"

for FILE in $FILES
do
	XENVER="`rpm --qf '%{VERSION}' -qa xen`" #get xen version, if any
	if [[ -n "XENVER" && -f "$FILE" && ! -L "$FILE" ]] #file exists and is not a symlink
	then
		NUMKER=`cat $FILE | grep title | wc -l`
		BOOTKER=`cat $FILE | grep default | awk -F= '{print $2}'`
		echo "Updating $FILE"
		echo "Contains $NUMKER kernel configurations"
		echo "With $BOOTKER as default"
		#Oh god.  spresse1/spressel is reposible for this terrible
		#awk script.  Go bash him over the head
		cat "$FILE" | awk -v XENVER="$XENVER" \
			'/[Tt][Ii][Tt][Ll][Ee]/,/^\s*$/ { #match lines that start with
							# title to one that is 0 or 
							#more space charaters 
			if(tolower($1)=="title") { #if line starts with title
				# Append "on Xen (version)", then a kernel line for xen
				print $0,"on Xen",XENVER,"\n\tkernel /boot/xen-"XENVER".gz" 
			} else if (tolower($1)=="kernel") { 
				#kernel becomes module, but only at the start of the line
				sub(/[Kk][Ee][Rr][Nn][Ee][Ll]/, "module", $0); 
				print $0 
			}  else if (tolower($1)=="initrd") { 
				#initrd becomes module at start of line
				sub(/[Ii][Nn][Ii][Tt][Rr][Dd]/, "module", $0); 
				print $0 
			} else { 
				#everything else gets left alone
				print $0 
			}
		}' >>"$FILE" #and append modified kernel record
		
		#change to the new record's equivalent of the old one
		cat "$FILE" | sed "s/default=$BOOTKER/default=$(( $BOOTKER + $NUMKER ))/gim" | tee "$FILE"
	fi
done
