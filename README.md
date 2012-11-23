acm-vm-cluster
==============

Resources related to the JHU ACM VM Cluster

Resources available
==============

xen.spec - spec file for building xen on CentOS.  May contain tuning specifically for this cluster, though I've done my best to keep it out. (Not yet known to work)
mx.spec.in - spec file that is used to build the MX driver.  Likely of little interest to anyone not in the ACm as MX is the driver for a now-obsolete PCI-x fiber card
binkernel.spec - a modified version of the default linux kernel spec file.  Used to build our modified kernel package.
