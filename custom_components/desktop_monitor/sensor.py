"""
    configuration.yaml
    sensor:
      - platform: desktop_monitor
(opt)   name: desktop_monitor
        hosts:
          - 192.168.1.35
(opt)   port: 9999
        resources:
          - system
          - cpu
          - memory
          - drive
"""
import logging
import voluptuous as vol
from datetime import timedelta

from homeassistant.helpers.entity import Entity
import homeassistant.helpers.config_validation as cv
from homeassistant.util import Throttle
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import (
    CONF_NAME, CONF_SCAN_INTERVAL, CONF_HOSTS, CONF_RESOURCES
    )

from datetime import datetime
import requests

_LOGGER = logging.getLogger(__name__)

MIN_TIME_BETWEEN_UPDATES = timedelta(seconds=30)
DEFAULT_NAME = "Desktop Monitor"
CONF_PORT = "port"
DEFAULT_PORT = 9999
RESOURCES_TYPES = {
    "system": ["mdi:sensor"],
    "cpu": ["mdi:sensor"],
    "memory": ["mdi:sensor"],
    "drive": ["mdi:sensor"]
}

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    vol.Required(CONF_HOSTS): cv.ensure_list,
    vol.Optional(CONF_PORT, default=DEFAULT_PORT): cv.string,
    vol.Required(CONF_RESOURCES): vol.All(cv.ensure_list, [vol.In(list(RESOURCES_TYPES.keys()))]),
})

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Setup the desktop_monitor sensors."""

    default_name = config.get(CONF_NAME)
    hosts = config.get(CONF_HOSTS)
    port = config.get(CONF_PORT)
    resources = config.get(CONF_RESOURCES)
    # scan_interval = config.get(CONF_SCAN_INTERVAL)
    
    for host in hosts:
        monitor = Monitor(host, port)
        try:
            await monitor.async_update()
        except ValueError as err:
            _LOGGER.error("Error while fetching data from desktop_monitor: %s", err)
            return

        for resource in resources:
            host = monitor.latest_data["system"][0][0]
            name = default_name + " " + host + " " + resource
            icon = RESOURCES_TYPES[resource][0]
            async_add_entities([DesktopMonitorSensor(monitor, resource, name, icon)], True)

class Monitor(object):
    """Handle desktop_monitor object and limit updates."""

    def __init__(self, host, port):
        """Initialize."""
        self._url = "http://{0}:{1}".format(host, port)
        self._data = None

    @property
    def latest_data(self):
        """Return the latest data object."""
        if self._data:
            return self._data
        return None

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    async def async_update(self):
        """Get the data using host and port."""
        try:
            ## OJO: esta forma es incorrecta: https://developers.home-assistant.io/docs/creating_platform_code_review/#5-communication-with-devicesservices
            self._data = requests.get(self._url, timeout=5).json()
        except (requests.exceptions.RequestException) as error:
            _LOGGER.error("(async_update) Unable to get data from desktop_monitor: %s", error)

class DesktopMonitorSensor(Entity):
    """Implementation of a Desktop Monitor Sensor."""

    def __init__(self, monitor, resource, name, icon):
        """Initialize the sensor."""
        self._monitor = monitor
        self._resource = resource
        self._name = name
        self._state = None
        self._icon = icon
        self._attributes = {}

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def icon(self):
        """Icon to use in the frontend"""
        return self._icon

    @property
    def device_state_attributes(self):
        """Return the state attributes of this device."""
        return self._attributes

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    async def async_update(self):
        """Get the latest data and use it to update our sensor state."""

        await self._monitor.async_update()
        data = self._monitor.latest_data[self._resource]
        self._state = data[0][0]
        unit_of_measurement = data[0][2]
        data.pop(0)
        for attribute in data:
            self._attributes[attribute[1]] = attribute[0]
        if unit_of_measurement:
            self._attributes["unit_of_measurement"] = unit_of_measurement



