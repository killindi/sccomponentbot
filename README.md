# Star Citizen Discord Bot

This is a custom-built Discord bot that lets users track and share Star Citizen components using real game data from the UEX API.

## Features

- `/collect [component]`: Add a component to your inventory with autocomplete
- `/search [component]`: Get detailed information about a component
- Real-time validation using the UEX API
- Local storage using SQLite
- Component cache updates every hour

## Setup

### 1. Clone the project and install dependencies

```bash
pip install -r requirements.txt
```

### 2. Create Your Bot in Discord

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application
3. Go to the "Bot" tab, click "Add Bot"
4. Copy your bot token
5. Enable `MESSAGE CONTENT INTENT` in the "Bot" settings
6. Invite your bot using this URL (replace `YOUR_CLIENT_ID`):

```
https://discord.com/oauth2/authorize?client_id=YOUR_CLIENT_ID&scope=bot+applications.commands&permissions=277025508352
```

### 3. Add Your Bot Token

Open `bot.py` and replace:

```python
bot.run("YOUR_BOT_TOKEN")
```

with your actual bot token.

### 4. Run the Bot

```bash
python bot.py
```

You should see a message like:

```
Logged in as YourBotName
```

### 5. Use the Commands

- Type `/collect` and start typing a component name to see suggestions.
- Use `/search` to get full details about a specific component.

---

## Notes

- Data is sourced from the community-maintained [UEX API](https://api.uexcorp.space)
- All component data is cached and refreshed hourly
- SQLite database `components.db` will be created in the same folder

## To-Do / Future Ideas

- Add `/wishlist` and notification support
- Web dashboard for managing components
- Ship loadout assignment

Enjoy and fly safe!
