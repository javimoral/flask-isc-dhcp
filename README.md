# Flask DHCP Leases
## Introduction
Provides a web interface for checking current DHCP leases when using ISC-DHCP.

By default, ISC-DHCP writes leases into a file, we read the file and present the
result in a friendly web interface.

Also provides a mechanism for store historical logs, using ISC hooks and MongoDB

## Deploying
This software uses Flask (Python) as web framework. Any deploy method that works with Flask should work, but only Gunicorn has been tested.

### Setup historical log
To keep a log of leases, we use ISC-DHCP hooks to execute the script ``isc-dhcp-hook.py`` which stores the data into MongoDB.

ISC-DHCP configuration file should be modified to execute this script on each action. Despite this being dependent on your own configuration, as a rule of thumb, inserting this snippet into ``subnet`` section should work.

```
# Hooks
on commit {
    set clip = binary-to-ascii(10, 8, ".", leased-address);
    set clhw = binary-to-ascii(16, 8, ":", substring(hardware, 1, 6));
    set clnm = pick-first-value(host-decl-name, option fqdn.hostname, option host-name, "none");
    set lstime = binary-to-ascii(10, 32, "", encode-int(lease-time, 32));
    execute ("/path/to/script/isc-dhcp-hook.py", "commit", clip, clhw, clnm, lstime);
}

on release {
    set clip = binary-to-ascii(10, 8, ".", leased-address);
    set clhw = binary-to-ascii(16, 8, ":", substring(hardware, 1, 6));
    set clnm = pick-first-value(host-decl-name, option fqdn.hostname, option host-name, "none");
    execute ("/path/to/script/isc-dhcp-hook.py", "release", clip, clhw, clnm);
}

on expiry {
    set clip = binary-to-ascii(10, 8, ".", leased-address);
    set clhw = binary-to-ascii(16, 8, ":", substring(hardware, 1, 6));
    set clnm = pick-first-value(host-decl-name, option fqdn.hostname, option host-name, "none");
    execute ("/path/to/script/isc-dhcp-hook.py", "expiry", clip, clhw, clnm);
}
```

## Configuration
Configuration is made using environmental variables.

### DHCP Leases Files
Indicate where we should look for the leases file written by ISC-DHCP.

```
export LEASES_FILE=/var/lib/dhcp/dhcpd.leases
```

### Pagination
Indicate the amount of entries shown by each page in the historical log. By default is 100.
```
export ENTRIES_PER_PAGE=100
```
