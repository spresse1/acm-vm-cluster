#!/bin/bash

#KVERMAJ=3.6
#KVER=${KVERMAJ}.9
#
#rpmdev-setuptree
#cd ~/rpmbuild/SOURCES
#
#wget "http://www.kernel.org/pub/linux/kernel/v3.0/linux-${KVER}.tar.bz2"
#cp ~/acm-vm-cluster/kernel/config-${KVER} config-i686
#cp ~/acm-vm-cluster/kernel/config-${KVER} config-i686-NONPAE
#cp ~/acm-vm-cluster/kernel/config-${KVER} config-x86_64
#cp ~/acm-vm-cluster/kernel/config-${KVER} config-x86_64-NONPAE
#
#rpmbuild -ba ~/acm-vm-cluster/kernel/kernel-i${KVERMAJ}.spec
#

BUILDOPENAFS=0
BUILDMX=0

if [ $# -eq 0 ];
then
	BUILDOPENAFS=1
	BUILDMX=1
fi

while (( "$#" )); do
case $1 in
mx)
	BUILDMX=1
	;;
openafs)
	BUILDOPENAFS=1
	;;
esac

shift

done

if [ $BUILDOPENAFS -eq 1 ]; then

cd
rm -rf openafs*

git clone git://git.openafs.org/openafs.git
cd openafs && git checkout openafs-stable-1_6_x
./regen.sh
cd
mv openafs openafs-1.6.1
echo "1.6.1" > openafs-1.6.1/.version
rm -rf openafs-1.6.1/.git
tar cjf openafs-1.6.1-src.tar.bz2 openafs-1.6.1
wget 'http://www.openafs.org/dl/openafs/1.6.1/openafs-1.6.1-doc.tar.bz2'
cd openafs-1.6.1/src/packaging/RedHat/
./makesrpm.pl ~/openafs-1.6.1-src.tar.bz2 ~/openafs-1.6.1-doc.tar.bz2
yum install -y `rpmbuild --rebuild openafs-1.6.1-1.src.rpm 2>&1 | grep 'is needed by'`
rpmbuild --rebuild openafs-1.6.1-1.src.rpm

fi
#END OpenAFS Build

#BEGIN mx
if [ $BUILDMX -eq 1 ]; then
cd ~/rpmbuild/SOURCES
wget 'https://raw.github.com/spresse1/acm-vm-cluster/master/mx/mx.spec'
wget 'http://www.myricom.com/pub/MX2G/mx2g_1.2.16.tar.gz'
wget 'https://raw.github.com/spresse1/acm-vm-cluster/master/mx/mx-update-k%5Bun%5Dmap_atomic.patch'
wget 'https://raw.github.com/spresse1/acm-vm-cluster/master/mx/mx-update-struct-ethtools_opt.patch'
wget 'https://raw.github.com/spresse1/acm-vm-cluster/master/mx/mx-dkms.conf'
rpmbuild -ba mx.spec

fi
