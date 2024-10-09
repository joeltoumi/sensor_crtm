from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.exceptions import ConfigEntryAuthFailed
import logging
from .const import DOMAIN, CONF_STOP_NUMBER, API_URL
from typing import Optional, Union
import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

PLATFORMS = [Platform.SENSOR]
_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up the bus stop integration from a config entry."""
    if await get_data(
            hass=hass,
            stop_number=entry.data.get(CONF_STOP_NUMBER)
    ):
        hass.data.setdefault(DOMAIN, {})
        hass.data[DOMAIN][entry.entry_id] = entry.data

        for platform in PLATFORMS:
            hass.async_create_task(
                hass.config_entries.async_forward_entry_setup(entry, platform)
            )
    else:
        raise ConfigEntryAuthFailed("Invalid credentials")

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload the bus stop integration."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok


async def get_data(
    hass, stop_number: str
) -> Union[dict, Optional[None]]:
    def get():
        url = f"{API_URL}{stop_number}"
        retry_strategy = Retry(
            total=3,
            status_forcelist=[400, 401, 500, 502, 503, 504],
            method_whitelist=["GET"],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        http = requests.Session()
        http.mount("https://", adapter)

        return http.get(url, headers={"User-Agent": "Mozilla/5.0"})

    response = await hass.async_add_executor_job(get)
    _LOGGER.debug("API Response: %s", response.json())

    if response.ok:
        return response.json()
    return None

