## ec2-net-utils for RHEL/systemd

ec2-net-utils RPM contains a fork of Amazon's ec2-net-utils with modifications to support Elastic Network Interfaces (ENI) under systemd.
It allows you to attach an ENI to a running instance and have it work as you would expect.

## Build RPM
```bash
git clone https://github.com/21stcaveman/ec2-net-utils && cd ec2-net-utils
rpmbuild --define "_topdir $(pwd)" -ba SPECS/ec2-net-utils.spec
```

## Install
* Imporant! Don't forget to enable the `elastic-network-interfaces` systemd unit, or ENI's won't work at boot!

```bash
rpm -i RPMS/noarch/ec2-net-utils*.rpm
systemctl enable elastic-network-interfaces
```

## OS Support

* ✓ RHEL 7

## How does it work

A udev rule runs `ec2net.hotplug` when a device is added or removed, which is a script that writes interface config, including source route setup. It relies on the primary interface having come up so it can query AWS metadata.

Another udev rule starts the `ec2net-ifup@` service when an interface is added, and a third one runs `/sbin/ifdown` on device removal. The original version from AWS relied on net.hotplug to do this.

Finally, `elastic-network-interfaces.service` is run late in the boot process.  It calls `ec2ifscan` which fires another udev add event for any interface which is not configured.  This handles the case of booting with an ENI that `ec2net.hotplug` hasn't had a chance to configure yet.

## Complications

* udev add events are fired during boot, during 'attach', and a second time during boot for the unconfigured case.  Meanwhile, network-scripts expects to manage any interface with a cfg that exists at boot.  So the udev events have to be ignored in the appropriate cases.
* Systemd kills any long-running processes that are spawned by scripts that are run by udev.  To be kept alive, dhclient must be started by a service started by udev (hence `ec2net-ifup@`).
