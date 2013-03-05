Name: xen-tools
Version: 4.2
Release: 1
Summary: Assist in administering Xen VMs
Packager: spresse1 on behalf of JHUACM <steve@pressers.name>
Source: xen-tools-4.2.tar.gz
License: GPLv2
BuildArch: noarch

# RPMbuild picks bad dependancies
AutoReqProv: no
Requires: /bin/sh /usr/bin/perl perl(Carp) perl(Digest::MD5) perl(English) perl(Env) perl(File::Copy) perl(File::Path) perl(File::Slurp) perl(File::Spec) perl(File::Temp) perl(Getopt::Long) perl(Moose) perl(POSIX) perl(Pod::Usage) perl(Text::Template) perl(strict) perl(warnings) rpmlib(CompressedFileNames) <= 3.0.4-1 rpmlib(FileDigests) <= 4.6.0-1 rpmlib(PayloadFilesHavePrefix) <= 4.0-1 rpmlib(VersionedDependencies) <= 3.0.3-1 rpmlib(PayloadIsXz) <= 5.2-1 debootstrap


%description
xen-tools accompanies the xen daemon and is very useful in administration.

%prep
%setup

%build

%install
make install prefix="$RPM_BUILD_ROOT"

%clean

%files
/etc/bash_completion.d/xen-tools
/etc/xen-tools/*
/usr/bin/*
/usr/lib/xen-tools/*
/usr/share/man/man8/*
/usr/share/perl5/Xen/*
