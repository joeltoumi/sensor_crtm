import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
import homeassistant.helpers.config_validation as cv

from .const import DOMAIN


@callback
def configured_stops(hass):
    """Return a list of configured bus stops."""
    return {entry.title for entry in hass.config_entries.async_entries(DOMAIN)}


class BusStopConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for CRTM Integration."""

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            if user_input["stop_number"] in configured_stops(self.hass):
                stop_exists = self.hass.config.language["stop_exists"]
                errors["stop_exists"] = stop_exists
            else:
                return self.async_create_entry(title=user_input["stop_number"], data=user_input)

        schema = vol.Schema({
            vol.Required("stop_number"): cv.string
        })

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors,
        )
