# Desktop Remote Integration for Home Assistant

This is a integration for a quick lightweight API designed to expose the system's current metrics of a linux desktop as a simple JSON endpoint that your Home Assistant instance can query.

## Install
To install the component, just clone and move ```desktop-monitor``` folder into ```custom_components``` directory.

```
git clone https://github.com/cazbrat/ha-desktop-monitor.git
mv custom_components/desktop_monitor <config_directory>/custom_components/
```

Example configuration.yaml:
```
# Example configuration.yaml entry
sensor:
  - platform: desktop_remote
    name: desktop_monitor
    hosts:
      - 192.168.1.35
    port: 9999
    resources:
      - system
      - cpu
      - memory
      - drive
```
### Configuration Variables
#### name
(string)(optional) A name for sensor ```sensor.<name>_<hostname>_<resource>```

#### hosts
(list)(required) The hostname or IP address to monitored


#### port
(integer)(optional) The port of your desktop to monitored. Default value: 9999

#### resources
(list)(required) The resources to monitored: ```system```, ```cpu```, ```memory```, ```drive```
