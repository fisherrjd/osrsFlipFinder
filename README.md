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

### 3. Connect to Discord

- **TODO:** Define required options (consult OSRS community)

### 4. Define Item embed card

- **TODO:** Create an item embed to highlight item data
   1. Item name
   2. Insta Buy/Sell Price
   3. Margin for the Item
   4. Volume
   5. Insta Buy/Sell Time (ex: 5 min ago)
   6. Picture of Item (use data from mapping API and then URL endpoint for wiki tiems) (need to add to DB)
   7. Member non member (need to add to DB)

### 5. Define margin table

- **TODO:** Based off input criteria display solid margins in a table for a user
   1. Sort by largest margins above A
   2. Include volume over B
   3. Sold / Bought in the last C minutes
   4. Value of item over D

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
