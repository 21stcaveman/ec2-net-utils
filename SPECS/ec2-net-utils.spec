%define _buildid %{nil}

Name:		ec2-net-utils
Summary:	A set of tools for automatic discovery and configuration of network interfaces in AWS cloud
Version:	1.4
Release:	1%{?_buildid}%{?dist}
License:	Apache License 2.0
Group:		System Tools
Packager:	Hamid Maadani <hamid@dexo.tech>
Vendor:		Amazon Web Services (AWS)
URL:       https://github.com/aws/amazon-ec2-net-utils
BuildArch: noarch
BuildRoot: %{name}-%{version}-root
BuildRequires: systemd-units
Requires:  initscripts, bash >= 4, curl, iproute

Source0:	53-ec2-network-interfaces.rules
Source1:	75-persistent-net-generator.rules
Source2:	ec2net-functions
Source3:	ec2net.hotplug
Source4:	ec2ifup
Source5:	ec2ifdown
Source6:	ec2dhcp.sh
Source7:	ec2ifup.8
Source8:	ec2ifscan
Source9:	elastic-network-interfaces.conf
Source10:	ec2ifscan.8
Source20:	ixgbevf.conf
Source21:	acpiphp.modules
Source22:	rule_generator.functions
Source23:	write_net_rules
# rhel stuff
Source30:	elastic-network-interfaces.service
Source31:	ec2net-ifup@.service
Source32:	ec2net-scan.service
# ebs related stuff
Source40:	51-ec2-hvm-devices.rules
Source41:	70-ec2-nvme-devices.rules
Source42:	ebsnvme-id
Source43:	ec2udev-vbd

%description
A set of tools for automatic discovery and configuration of network interfaces in AWS cloud.

%prep

%build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/sbin
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d/
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/network-scripts/
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/dhcp/dhclient.d/
mkdir -p $RPM_BUILD_ROOT/usr/lib/udev
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man8/

%{__install} -m755 %{SOURCE4} $RPM_BUILD_ROOT/sbin/
%{__install} -m755 %{SOURCE5} $RPM_BUILD_ROOT/sbin/
%{__install} -m755 %{SOURCE8} $RPM_BUILD_ROOT/sbin/
%{__install} -m644 %{SOURCE0} $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d/
%{__install} -m644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d/
%{__install} -m644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/network-scripts/
%{__install} -m755 %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/network-scripts/
%{__install} -m755 %{SOURCE6} $RPM_BUILD_ROOT%{_sysconfdir}/dhcp/dhclient.d/
%{__install} -m644 %{SOURCE7} $RPM_BUILD_ROOT%{_mandir}/man8/ec2ifup.8
ln -s ./ec2ifup.8.gz $RPM_BUILD_ROOT%{_mandir}/man8/ec2ifdown.8.gz
%{__install} -m644 %{SOURCE10} $RPM_BUILD_ROOT%{_mandir}/man8/ec2ifscan.8
%{__install} -m644 %{SOURCE22} $RPM_BUILD_ROOT/usr/lib/udev
%{__install} -m644 %{SOURCE23} $RPM_BUILD_ROOT/usr/lib/udev

%{__install} -d -m 0775 ${RPM_BUILD_ROOT}%{_unitdir}
%{__install} -m 0644 %{SOURCE30} ${RPM_BUILD_ROOT}%{_unitdir}
%{__install} -m 0644 %{SOURCE31} ${RPM_BUILD_ROOT}%{_unitdir}
%{__install} -m 0644 %{SOURCE32} ${RPM_BUILD_ROOT}%{_unitdir}

# add module configs
%{__install} -m644 -D %{SOURCE20} $RPM_BUILD_ROOT/etc/modprobe.d/ixgbevf.conf
%{__install} -m755 -D %{SOURCE21} $RPM_BUILD_ROOT/etc/sysconfig/modules/acpiphp.modules

# add ebs renaming modules
%{__install} -m644 %{SOURCE40} $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d/
%{__install} -m644 %{SOURCE41} $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d/
%{__install} -m755 %{SOURCE42} $RPM_BUILD_ROOT/sbin/
%{__install} -m755 %{SOURCE43} $RPM_BUILD_ROOT/sbin/

%clean
rm -rf $RPM_BUILD_ROOT

%files
/sbin/ec2ifup
/sbin/ec2ifdown
/sbin/ec2ifscan

%attr(755, -, -) %{_prefix}/lib/udev/write_net_rules
%{_prefix}/lib/udev/rule_generator.functions

%{_sysconfdir}/udev/rules.d/53-ec2-network-interfaces.rules
%{_sysconfdir}/udev/rules.d/75-persistent-net-generator.rules
%{_sysconfdir}/modprobe.d/ixgbevf.conf
%{_sysconfdir}/sysconfig/modules/acpiphp.modules
%{_sysconfdir}/sysconfig/network-scripts/ec2net-functions
%{_sysconfdir}/sysconfig/network-scripts/ec2net.hotplug
%{_sysconfdir}/dhcp/dhclient.d/ec2dhcp.sh
%{_mandir}/man8/ec2ifup.8.gz
%{_mandir}/man8/ec2ifdown.8.gz
%{_mandir}/man8/ec2ifscan.8.gz

%{_sysconfdir}/udev/rules.d/51-ec2-hvm-devices.rules
%{_sysconfdir}/udev/rules.d/70-ec2-nvme-devices.rules
/sbin/ebsnvme-id
/sbin/ec2udev-vbd

%{_unitdir}/elastic-network-interfaces.service
%{_unitdir}/ec2net-ifup@.service
%{_unitdir}/ec2net-scan.service

%post
%systemd_post elastic-network-interfaces.service
%systemd_post ec2net-ifup@.service

%preun
%systemd_preun elastic-network-interfaces.service
%systemd_preun ec2net-ifup@.service

%postun
%systemd_postun elastic-network-interfaces.service
%systemd_postun ec2net-ifup@.service
