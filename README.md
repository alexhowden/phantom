# Phantom - Clash of Clans Attack Bot

**Phantom** is a modular, extensible automation bot for Clash of Clans designed to perform repeated attacks with extreme reliability and zero manual intervention.
It uses image-recognition and configurable valid deployment points to reliably navigate and operate within the game UI.
Currently built for the iPhone Mirroring "emulator" on MacOS.

---

## Overview

Phantom operates as a state-driven bot:
- **State Detection** — YOLO models interpret the game’s current screen (home, scouting, attack, etc.).
- **Dynamic Control** — Coordinates and valid attack regions are fully configurable and normalized to screen size.
- **Strategy Layer** — Custom attack routines define how and when troops deploy based on current state.
- **Autonomy & Safety** — Built-in error handling that allows the bot to navigate to any desired state from anywhere in the game, and randomized input patterns emulate human play.
