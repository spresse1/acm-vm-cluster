#MX - The Driver for Myricom Fiber#

This directory contains everything we need to build the mx kernel module, except for the actual source.  If you're running this, you should have source you get from Myricom.

##Files##

*```mx.spec``` - A spec file tailored to building the mx kernel module.  At the moment it builds a kernel-version dependant kernel, though I plan to update this to build a DKMS module.

*```mx-update-k[un]map_atomic.patch``` - As of linux 2.6.37, the function prototype for kmap_atomic() and kunmap_atomic() changed.  This patch adds preprocessor conditionals to account for this to that the kernel can build on multiple systems.

*```mx-update-struct-ethtools_opt.patch``` - Removes struct ethtool_opt members which no longer exist as of 3.3.0.  Ideally this patch would remove the relevent functions too, so the driver built without warnings, but.. lazt.  Its a todo.

##Procedure##
Copy ```*.patch``` and your mx2g source tarball to ```rpmbuild/SOURCES```
<pre>$ rpmbuild -ba mx.spec</pre>
