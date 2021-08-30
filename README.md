# BottyG
The father of modern rocketry, now in bot form!

## Capabilities
BottyG can:
* Send rockets
* Fire payloads into space 
* Send reaction images
* Give advice
* Convert (some) time zones [beta]
* Respond to messages that mention things from Robert Goddard's life
* More (hopefully) coming soon!

## Technical Overview
The driver is botty_g.py, which implements a simple discord.Client.

Different kinds of behavior are largely grouped together, and an attempt has been made to split them out into separate classes when it made sense to do so.

All behaviors are tested, all code paths are tested the unit test level and each behavior has at least one integration test at the botty_g_test level.
Unfortunately there is a slight testing gap in verifying that the discord library calls are being made correctly.
However, there's no fake library for discord.py, and even if there was, I don't really want to put that much time into this.

Honestly the most complicated thing about this bot has been organizing everything so that the unit tests work, since unittest doesn't play nice with asyncio.
