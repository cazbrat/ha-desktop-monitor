# Desktop Monitor Integration for Home Assistant

This is a Home Assistant integration for the [Desktop Monitor](https://github.com/cazbrat/ha-desktop-monitor-api) API. With it, some current metrics of a Linux desktop are exposed.

## Install on Home Assistant
To install the component, just clone and move ```desktop-monitor``` folder into ```custom_components``` directory.
```
git clone https://github.com/cazbrat/ha-desktop-monitor.git
mv custom_components/desktop_monitor <config_directory>/custom_components/
```
And set it in configuration.yaml:
```
sensor:
  - platform: desktop_remote
    hosts:
      - 192.168.1.35
    resources:
      - system
      - cpu
      - lmsensor
      - memory
      - drive
    port: 9999
    name: desktop_monitor
```
### Configuration variables

#### hosts
(list)(required) The hostname or IP address to monitored

#### resources
(list)(required) The resources to monitored: ```system```, ```cpu```, ```lmsensor```, ```memory``` and ```drive```

#### name
(string)(optional) A name for sensor ```sensor.<name>_<hostname>_<resource>```. Default value: Desktop Monitor

#### port
(integer)(optional) The port of your desktop to monitored. Default value: 9999


## What is the idea
Control the resources of the computers in my office, to avoid any damage or malfunction that may will be suffer

## Collaboration
yes please !: comments, problems, improvements, anything ...