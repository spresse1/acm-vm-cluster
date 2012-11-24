acm-vm-cluster
==============

Resources related to the JHU ACM VM Cluster

Resources available
==============

* xen.spec - spec file for building xen on CentOS.  May contain tuning specifically for this cluster, though I've done my best to keep it out. (Not yet known to work)
* mx.spec.in - spec file that is used to build the MX driver.  Likely of little interest to anyone not in the ACm as MX is the driver for a now-obsolete PCI-x fiber card
* kernel/
	* patch-1-mkinitrd.patch - A patch which can be applied to the kernels existing binkernel.spec file to make it build a initrd as well and include that.
	* config-3.6.6-acm - the example linux-3.6.6 configuration used by the ACM VM nodes.
