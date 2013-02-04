#Ceph related things#

This directory contains all the things related to building and customizing ceph in our setup.

##Files##
* fix-spec.patch - the spec file that comes bundled in ceph-0.48argonaut.tar.bz doesn't reference a couple of files which get built.  This causes the RPM build to fail.  This patch fixes that.  Apply with:
<pre>
$ cd ceph-0.48argonaut
$ patch -p1 < fix-spec.patch
</pre>
Youll also want to change who owns the spec file (as RPM tosses an error if it can't find a real user who owns the spec file):
```$ chown USER:GROUP ceph.spec```

This patch is obsolete with the 0.56.1 (bobtail) release, which comes with RPMs from http://ceph.com/docs/master/install/rpm/

* cephNodeChange.pm - a perl script which runs within the xCat plugin architecture to take care of server side ceph cluster adds/leaves as part of the install process.  To install it:
<pre># cp cephNodeChange.pm /opt/xcat/lib/perl/xCAT_monitoring
# monadd cephNodeChange
# monstart cephNodeChange</pre>
This script logs to ```/var/log/cephNodeChange.log```

##Build Process##
* set up your RPM build root
* download ceph-0.48argonaut.tar.bz2
* untar one and apply the patch in fix-spec.patch
* copy ceph-0.48.tar.bz2 into rpmbuild/SOURCES
* run:
```$ rpmbuild -ba ceph.spec```
