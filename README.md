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

Tests are split between focused module tests and pytest-based integration tests for
the Discord client behavior in `tests/test_botty_g_integration.py`.

## Running Tests

Install dev dependencies:

```
./.venv/bin/pip install -r requirements-dev.txt
```

Run tests:

```
./.venv/bin/python -m pytest -q
```
