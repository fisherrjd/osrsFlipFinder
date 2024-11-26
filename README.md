# OSRS Flip Finder

[![Python Style: Black](https://img.shields.io/badge/python%20style-black-000000.svg?style=flat-square)](https://github.com/ambv/black)
[![Python 3.11+ Supported](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/release/python-3100/)
[![Uses Nix](https://img.shields.io/badge/uses-nix-%237EBAE4)](https://nixos.org/)

## Project Overview

OSRS Flip Finder is a tool designed to help Old School RuneScape (OSRS) players identify profitable item trading opportunities by providing real-time market data and advanced filtering capabilities.

## Project Goals

### 1. Connect to the Prices API

Fetch up-to-date OSRS item data in real-time to provide accurate market information.

### 2. Store Data in SQLite

Continuously update the database with the latest prices every minute, ensuring users have access to the most current market data.

### 3. Connect to Discord

Integrate the tool seamlessly with Discord for easy access and interaction.

### 4. Define Item Embed Card

Create a comprehensive item embed to highlight key item trading information, including:

- Item name
- Insta Buy/Sell Price
- Margin for the Item
- Trading Volume
- Insta Buy/Sell Timestamp
- Item Picture
- Membership Status

### 5. Define Margin Table

Display margins based on user-defined input criteria, with features like:

- Sorting by largest margins
- Volume filtering
- Time-based transaction tracking
- Value-based item selection

## Development Checklist

### API & Data Management

- [ ] Implement OSRS Prices API connection
- [ ] Design SQLite database schema
- [ ] Create data synchronization mechanism
- [ ] Develop real-time price update system

### Discord Integration

- [ ] Set up Discord bot authentication
- [ ] Define bot command structure
- [ ] Implement user interaction flows
- [ ] Create help and usage documentation

### Item Embed Development

- [ ] Design embed card template
- [ ] Integrate Mapping API for item images
- [ ] Add membership status tracking
- [ ] Implement timestamp generation
- [ ] Create margin calculation logic

### Margin Table Features

- [ ] Develop dynamic sorting algorithm
- [ ] Implement volume-based filtering
- [ ] Create time-based transaction tracking
- [ ] Design value-based item selection
- [ ] Build user preference configuration

### Additional Features

- [ ] Implement user profile system
- [ ] Create custom filtering preferences
- [ ] Add data visualization components
- [ ] Develop comprehensive logging
- [ ] Set up error handling and monitoring

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

## Future Roadmap

- Expand filtering capabilities
- Improve user experience
- Add more advanced trading analytics
- Create mobile and web interface options

## Contributing

Interested in contributing? Please read our contributing guidelines and feel free to submit pull requests.
