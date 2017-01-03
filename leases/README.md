# ISC-DHCP Web Status
Muestra las concesiones de ISC-DHCP y mantiene un histórico de eventos
en una base de datos MongoDB

## Configuration
### Server
El servidor hace uso del fichero `dhcpd.leases` de ISC-DHCP para conocer leases
concesiones actuales. Tenemos que indicar donde se encuentra dicho fichero
usando la variable de entorno `LEASES_FILE`

```
export LEASES_FILE="/path/to/dhcpd.leases"
```

### Vendors de MAC Address
Para evitar problemas con el parseo de ficheros, la relación de vendors y
direcciones MAC se almacena en MongoDB.

Para configurarla, ejecutar el script
```
python oui_populate_script.py
```

El script buscará el fichero `oui.txt` en el mismo directorio desde el que se
ejecuta.

### DHCP Config
En la sección subnet añadimos los hooks para el script de eventos
```
# Hooks para el histórico
on commit {
    set clip = binary-to-ascii(10, 8, ".", leased-address);
    set clhw = binary-to-ascii(16, 8, ":", substring(hardware, 1, 6));
    set clnm = pick-first-value(host-decl-name, option fqdn.hostname, option host-name, "none");
    set lstime = binary-to-ascii(10, 32, "", encode-int(lease-time, 32));
    execute ("/path/to/isc-dhcp-hook.py", "commit", clip, clhw, clnm, lstime);
}

on release {
    set clip = binary-to-ascii(10, 8, ".", leased-address);
    set clhw = binary-to-ascii(16, 8, ":", substring(hardware, 1, 6));
    set clnm = pick-first-value(host-decl-name, option fqdn.hostname, option host-name, "none");
    execute ("/path/to/isc-dhcp-hook.py", "release", clip, clhw, clnm);
}

on expiry {
    set clip = binary-to-ascii(10, 8, ".", leased-address);
    set clhw = binary-to-ascii(16, 8, ":", substring(hardware, 1, 6));
    set clnm = pick-first-value(host-decl-name, option fqdn.hostname, option host-name, "none");
    execute ("/path/to/isc-dhcp-hook.py", "expiry", clip, clhw, clnm);
}
```
