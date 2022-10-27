[![Validate](https://github.com/LAB02-Research/HASS.Agent-Integration/workflows/Validate/badge.svg)](https://github.com/LAB02-Research/HASS.Agent-Integration/actions?query=workflow:"Validate")
[![GitHub release](https://img.shields.io/github/release/LAB02-Research/HASS.Agent-Integration?include_prereleases=&sort=semver&color=blue)](https://github.com/LAB02-Research/HASS.Agent-Integration/releases/)
[![License](https://img.shields.io/badge/License-MIT-blue)](#license)
[![buymeacoffee](https://img.shields.io/badge/BuyMeACoffee-Donate-blue.svg)](https://www.buymeacoffee.com/lab02research)
[![Discord](https://img.shields.io/badge/dynamic/json?color=blue&label=Discord&logo=discord&logoColor=white&query=presence_count&suffix=%20Online&url=https://discordapp.com/api/guilds/932957721622360074/widget.json)](https://discord.gg/nMvqzwrVBU)

[![hacs_badge](https://img.shields.io/badge/HACS-Default-41BDF5.svg)](https://github.com/hacs/integration)


----

⚠️❗**IMPORTANT ** ❗⚠️ 

**You need at least HASS.Agent [2022.13.0](https://github.com/LAB02-Research/HASS.Agent/releases/tag/2022.13.0) for this integration to work!**

----

# HASS.Agent Integration

This <a href="https://www.home-assistant.io" target="_blank">Home Assistant</a> integration by [@fillefilip8](https://github.com/fillefilip8) allows you to send notifications to <a href="https://github.com/LAB02-Research/HASS.Agent" target="_blank">HASS.Agent</a>, a Windows-based Home Assistant client. It also allows you to use it as a mediaplayer device: see and control what's playing and send text-to-speech. 

All communication is done through MQTT\*. It supports auto discovery, so you'll see your HASS.Agent devices show up automatically in the integrations page:

![image](https://user-images.githubusercontent.com/81011038/198246059-caa7f1cd-89f7-41f9-989e-724a1a67c2fe.png)

The new mediaplayer has a bunch of new features, like coverart:

![image](https://user-images.githubusercontent.com/81011038/198246217-cce288be-bbb7-4c5f-baff-510cc99c30b1.png)

You can use [actionable notifications](https://hassagent.readthedocs.io/en/latest/notifications/new/notification-actionable/) to interact with HA:

![image](https://user-images.githubusercontent.com/81011038/190643738-724dac45-4d03-4a19-a0e6-3a59b5de0aad.png)

Need help? Check [the documentation](https://hassagent.readthedocs.io/), visit the <a href="https://community.home-assistant.io/t/hass-agent-a-new-windows-based-client-to-receive-notifications-perform-quick-actions-and-much-more/369094" target="_blank">dedicated HA forum thread</a> or <a href="https://discord.gg/nMvqzwrVBU" target="_blank">join on Discord</a>.

Note: it won't be of much use if you don't have HASS.Agent installed & configured on at least one PC (or Windows based device).

\* you can still add your device manually (through the UI) if you want to use the local API instead.
