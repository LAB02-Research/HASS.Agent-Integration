from __future__ import annotations
import json

import logging
from typing import Any

from homeassistant.components.mqtt.models import ReceiveMessage
from homeassistant.helpers import device_registry as dr

from .const import DOMAIN


from homeassistant.components.mqtt.subscription import (
    async_prepare_subscribe_topics,
    async_subscribe_topics,
)
from homeassistant.config_entries import ConfigEntry

from homeassistant.components.media_player import (
    MediaPlayerEntity,
    MediaPlayerEntityFeature,
)

from homeassistant.components.media_player.const import MEDIA_TYPE_MUSIC, MediaType

from homeassistant.components.media_player.browse_media import (
    async_process_play_media_url,
)

from homeassistant.const import (
    STATE_IDLE,
    STATE_OFF,
    STATE_PAUSED,
    STATE_PLAYING,
)

from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.components import media_source, mqtt

_logger = logging.getLogger(__name__)

SUPPORT_HAMP = (
    MediaPlayerEntityFeature.VOLUME_MUTE
    | MediaPlayerEntityFeature.PAUSE
    | MediaPlayerEntityFeature.STOP
    | MediaPlayerEntityFeature.PREVIOUS_TRACK
    | MediaPlayerEntityFeature.NEXT_TRACK
    | MediaPlayerEntityFeature.VOLUME_STEP
    | MediaPlayerEntityFeature.PLAY
    | MediaPlayerEntityFeature.PLAY_MEDIA
)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> bool:

    sub_state = hass.data[DOMAIN][entry.entry_id]["mqtt"]

    device_registry = dr.async_get(hass)
    device = device_registry.async_get_device(identifiers={(DOMAIN, entry.unique_id)})

    if device is None:
        return False

    entity = HassAgentMediaPlayerDevice(
        entry.unique_id,
        device,
        f"hass.agent/media_player/{device.name}/cmd",
    )

    def updated(message: ReceiveMessage):
        payload = json.loads(message.payload)
        entity.apply_payload(payload)

    sub_state = async_prepare_subscribe_topics(
        hass,
        sub_state,
        {
            f"{entry.unique_id}-state": {
                "topic": f"hass.agent/media_player/{device.name}/state",
                "msg_callback": updated,
                "qos": 0,
            }
        },
    )

    await async_subscribe_topics(hass, sub_state)

    hass.data[DOMAIN][entry.entry_id]["mqtt"] = sub_state

    async_add_entities([entity])

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    print("unload!")


class HassAgentMediaPlayerDevice(MediaPlayerEntity):
    """HASS.Agent MediaPlayer Device"""

    @callback
    def apply_payload(self, payload):
        self._state = payload["state"].lower()
        self._playing = payload["title"]
        self._volume_level = payload["volume"]
        self._muted = payload["muted"]
        self._available = True

        self.async_write_ha_state()

    def __init__(self, unique_id, device: dr.DeviceEntry, command_topic):
        """Initialize"""
        self._name = device.name
        self._attr_device_info = {
            "identifiers": device.identifiers,
            "name": device.name,
            "manufacturer": device.manufacturer,
            "model": device.model,
            "sw_version": device.sw_version,
        }
        self._command_topic = command_topic
        self._attr_unique_id = f"hass.agent-{unique_id}"
        self._available = False
        self._muted = False
        self._volume_level = 0
        self._playing = ""
        self._state = ""

    async def _send_command(self, command, data=None):
        """Send a command"""
        _logger.debug("Sending command: %s", command)

        payload = {"command": command, "data": data}

        await mqtt.async_publish(self.hass, self._command_topic, json.dumps(payload))

    @property
    def name(self):
        """Return the name of the device"""
        return self._name

    @property
    def state(self):
        """Return the state of the device"""
        if self._state is None:
            return STATE_OFF
        if self._state == "idle":
            return STATE_IDLE
        if self._state == "playing":
            return STATE_PLAYING
        if self._state == "paused":
            return STATE_PAUSED

        return STATE_IDLE

    @property
    def available(self):
        """Return if we're available"""
        return self._available

    @property
    def media_title(self):
        """Return the title of current playing media"""
        return self._playing

    @property
    def volume_level(self):
        """Return the volume level of the media player (0..1)"""
        return self._volume_level / 100.0

    @property
    def is_volume_muted(self):
        """Return if volume is currently muted"""
        return self._muted

    @property
    def media_duration(self):
        """Return the duration of the current playing media in seconds"""
        """ NOT IMPLEMENTED """
        return 0

    @property
    def supported_features(self):
        """Flag media player features that are supported"""
        return SUPPORT_HAMP

    @property
    def device_class(self):
        """Announce ourselve as a speaker"""
        return "DEVICE_CLASS_SPEAKER"

    @property
    def media_content_type(self):
        """Content type of current playing media"""
        return MEDIA_TYPE_MUSIC

    async def async_volume_up(self):
        """Volume up the media player"""
        super().async_volume_up()
        await self._send_command("volumeup")

    async def async_volume_down(self):
        """Volume down media player"""
        super().async_volume_down()
        await self._send_command("volumedown")

    async def async_mute_volume(self, mute):
        """Mute the volume"""
        await self._send_command("mute")

    async def async_media_play(self):
        """Send play command"""
        self._state = STATE_PLAYING
        await self._send_command("play")

    async def async_media_pause(self):
        """Send pause command"""
        self._state = STATE_PAUSED
        await self._send_command("pause")

    async def async_media_stop(self):
        """Send stop command"""
        self._state = STATE_PAUSED
        await self._send_command("stop")

    async def async_media_next_track(self):
        """Send next track command"""
        await self._send_command("next")

    async def async_media_previous_track(self):
        """Send previous track command"""
        await self._send_command("previous")

    async def async_play_media(
        self, media_type: MediaType | str, media_id: str, **kwargs: Any
    ):
        """Play media source"""
        if media_type != MEDIA_TYPE_MUSIC:
            _logger.error(
                "Invalid media type %r. Only %s is supported!",
                media_type,
                MEDIA_TYPE_MUSIC,
            )
            return

        if media_source.is_media_source_id(media_id):
            play_item = await media_source.async_resolve_media(self.hass, media_id)

            # play_item returns a relative URL if it has to be resolved on the Home Assistant host
            # This call will turn it into a full URL
            media_id = async_process_play_media_url(self.hass, play_item.url)

        _logger.debug("Received media request from HA: %s", media_id)

        self._state = STATE_PLAYING
        await self._send_command("playmedia", media_id)
