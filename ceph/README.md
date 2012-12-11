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

##Build Process##
* set up your RPM build root
* download ceph-0.48argonaut.tar.bz2
* untar one and apply the patch in fix-spec.patch
* copy ceph-0.48.tar.bz2 into rpmbuild/SOURCES
* run:
```$ rpmbuild -ba ceph.spec```
