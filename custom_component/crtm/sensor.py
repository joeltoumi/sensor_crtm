import logging
from typing import List
from datetime import datetime, timedelta
from homeassistant.components.sensor import SensorEntity
from homeassistant.util.dt import utc_from_timestamp
import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
from .const import DOMAIN, CONF_STOP_NUMBER, API_URL, SCAN_INTERVAL
import pytz

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities) -> None:
    """Set up bus stop sensor from a config entry."""
    config = hass.data[DOMAIN][config_entry.entry_id]
    stop_number = config[CONF_STOP_NUMBER]
    sensors = [
        BusStopSensor(
            stop_number=stop_number
        )
    ]
    async_add_entities(sensors, update_before_add=True)


class BusStopSensor(SensorEntity):
    """Representation of a bus stop sensor."""

    UPDATE_INTERVAL = timedelta(minutes=3)

    def __init__(self, stop_number: str):
        """Initialize the sensor."""
        self._stop_number = stop_number
        self._state = None
        self._attributes = {}
        self._arrivals = []
        self._last_request_time = None

    @property
    def update_interval(self):
        """Return the update interval."""
        return self.UPDATE_INTERVAL

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"Bus stop {self._stop_number}"

    @property
    def state(self) -> str:
        """State."""
        return len(self.arrivals)

    @property
    def last_updated(self):
        """Returns date when it was last updated."""
        if self._last_updated != "unknown":
            stamp = float(self._last_updated)
            return utc_from_timestamp(int(stamp))

    @property
    def arrivals(self) -> List[dict]:
        """Arrivals."""
        return self._arrivals

    @property
    def stop_number(self):
        """Stop number"""
        return self._stop_number

    @property
    def url(self):
        """URL"""
        return f"{API_URL}{self.stop_number}"

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return {
            "data": self.arrivals,
            "last_request_time": self._last_request_time,
        }

    @property
    def headers(self) -> dict:
        """Headers."""
        return {
            "User-Agent": "Mozilla/5.0",
        }

    async def async_update(self) -> None:
        """Update sensor data."""
        await self.hass.async_add_executor_job(self.update)

    def get_next_arrivals(self, times) -> []:
        """Get the next arrivals from the list of times."""
        if not times:
            return []

        arrivals = []

        now = datetime.now(pytz.utc)
        local_tz = pytz.timezone('Europe/Madrid')

        for t in times:
            if "arrivalDate" in t:
                try:
                    arrival_time_utc = datetime.fromisoformat(t["arrivalDate"].replace("Z", "+00:00"))
                    arrival_time = arrival_time_utc.astimezone(local_tz)
                    time_diff = (arrival_time - now).total_seconds()

                    if time_diff < 0:
                        continue

                    if time_diff < 3600:
                        arrivals.append(f"{int(time_diff // 60)} min")
                    else:
                        arrivals.append(arrival_time.strftime("%H:%M"))
                except ValueError as e:
                    _LOGGER.error(f"Error parsing arrival date: {e}")

        arrivals.sort(key=lambda x: (int(x.split()[0]) if "min" in x else float("inf")))
        return arrivals

    def update(self) -> None:
        """Update sensor."""
        _LOGGER.debug("%s - Running update", self.name)
        retry_strategy = Retry(
            total=3,
            status_forcelist=[400, 401, 500, 502, 503, 504],
            method_whitelist=["GET"],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        http = requests.Session()
        http.mount("https://", adapter)
        arrivals = http.get(self.url, headers=self.headers)
        routes = arrivals.json()["routes"]
        self._arrivals.clear()
        if arrivals.ok:
            for route in routes:
                self._arrivals.append(
                    {
                        "title": route.get("lineCode"),
                        "nextArrivals": self.get_next_arrivals(route.get("times")),
                        "longName": route.get("routeName")
                    }
                )
                self._last_request_time = datetime.now().strftime("%d-%m %H:%M")
                _LOGGER.debug("Payload received: %s", arrivals.json())
            else:
                _LOGGER.debug("Error received: %s", arrivals.content)

