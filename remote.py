"""Platform for BOINC integration."""
from __future__ import annotations

import logging
from pprint import pformat

import voluptuous as vol

from homeassistant.components.remote import PLATFORM_SCHEMA
from homeassistant.const import CONF_API_KEY, CONF_HOST, CONF_NAME, CONF_PORT
from homeassistant.core import HomeAssistant
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .boinc import BoincRemote

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_HOST): cv.string,
        vol.Required(CONF_NAME): cv.string,
        vol.Optional(CONF_PORT): cv.positive_int,
        vol.Optional(CONF_API_KEY): cv.string,
    }
)

_LOGGER = logging.getLogger("boinc")


def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the BOINC Remote platform."""

    _LOGGER.info(pformat(config))

    platform = {
        "host": config[CONF_HOST],
        "name": config[CONF_HOST],
        "port": config[CONF_PORT],
        "apikey": config[CONF_API_KEY],
    }

    boinc_client = BoincRemote(
        platform["host"],
        platform["name"],
        platform["port"],
        platform["apikey"],
        _LOGGER,
    )

    add_entities([boinc_client])
