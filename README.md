Radarr Agent
============

What is the Radarr Agent?
-------------------------
It's a metadata agent for Plex. It retrieves metadata from the Radarr API. This agent can come in handy for people using both Plex and Radarr.

How do I install this agent?
----------------------------
You can install the agent:

 - From within the Unsupported AppStore, or:
 - Manually: See the support article "[How do I manually install a channel?](https://support.plex.tv/hc/en-us/articles/201187656-How-do-I-manually-install-a-channel-)" over at the Plex support website.

How do I use this agent?
------------------------
There are 2 options you have:

1. You can use the agent as a standalone (primary) agent. That way only data from Radarr will be used. Please note that this will not give you the same data rich library you're probably used to. Some data will be present, but some pieces will be missing, because Radarr only provides some basic data.
2. You can use the agent as a secondary agent to the Plex Movie or The Movie Database agent. Activate it under Plex Movie or The Movie Database in *Settings* > *Server* > *Agents* > *Movies*. Drag it to just below Plex Movie or The Movie Database to let this agent fill in the blanks from Plex Movie or The Movie Database.

Before using the agent, go into the agent's preferences and enter your Radarr URL and API key (you can find your Radarr API key in Radarr under *Settings* > *General* > *Security*).

Where do I download this agent?
-------------------------------
If you want to install the agent manually or if you are interested in the source code, you can download the latest copy of the agent from Github directly: [ZIP](https://github.com/piplongrun/Radarr.bundle/archive/master.zip)

Where do I report issues?
-------------------------
Create an [issue on Github](https://github.com/piplongrun/Radarr.bundle/issues) and add as much information as possible:
 - Plex Media Server version
 - Primary agent and order of any secondary agents
 - Log files, `com.plexapp.agents.radarr.log`
