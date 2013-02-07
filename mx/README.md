#MX - The Driver for Myricom Fiber#

This directory contains everything we need to build the mx kernel module, except for the actual source.  If you're running this, you should have source you get from Myricom.

##Files##

*```mx.spec``` - A spec file tailored to building the mx kernel module.  At the moment it builds a kernel-version dependant kernel, though I plan to update this to build a DKMS module.
*```

##Procedure##
Copy ```*.patch``` and your mx2g source tarball to ```rpmbuild/SOURCES```
<pre>$ rpmbuild -ba mx.spec</pre>
