# OSRS Flip Finder

[![Python Style: Black](https://img.shields.io/badge/python%20style-black-000000.svg?style=flat-square)](https://github.com/ambv/black)
[![Python 3.11+ Supported](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/release/python-3100/)
[![Uses Nix](https://img.shields.io/badge/uses-nix-%237EBAE4)](https://nixos.org/)

## Project Goals

### 1. Connect to the Prices API

- Fetch up-to-date OSRS item data in real-time

### 2. Store Data in SQLite

- Continuously update the database with the latest prices every minute

#### Sample Data Table

```
╔═══════════════════════╤════════════╤═════════════╤══════════╤══════════╗
║ Name                  │ InstaBuy   │ InstaSell   │ Margin   │ Volume   ║
╟───────────────────────┼────────────┼─────────────┼──────────┼──────────╢
║ Wine of zamorak       │ 800        │ 798         │ 2        │ 1.09M    ║
║ Maple longbow         │ 277        │ 275         │ 2        │ 2.01M    ║
║ Harralander potions   │ 785        │ 783         │ 2        │ 767.99K  ║
║ Mithril seeds         │ 945        │ 943         │ 2        │ 395.44K  ║
║ Grimy tarromin        │ 419        │ 417         │ 2        │ 671.34K  ║
╚═══════════════════════╧════════════╧═════════════╧══════════╧══════════╝
```

### 3. Connect to Discord

- **TODO:** Define required options (consult OSRS community)

### 4. Expand Features

- Incorporate additional tools such as:
  - Decanting
  - Crafting
  - Other utility functions

## Getting Started

### Update Database

To update the database with real-time pricing data from the OSRS API:

```bash
python bot/data_collection/osrs_to_db.py
```

### Run Discord Bot

To bring the bot online in the Discord server:

```bash
python bot/main.py
```
