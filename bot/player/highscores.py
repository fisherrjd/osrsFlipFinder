import requests

def fetch_highscores(username: str) -> dict:
    """
    Fetch OSRS Highscores data for a given username.
    Returns a dictionary with relevant stats or an error message.
    """
    api_url = f"https://secure.runescape.com/m=hiscore_oldschool/index_lite.ws?player={username}"
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.text.splitlines()

            # Get overall data (the first line is overall)
            overall_data = data[0].split(",")
            username = username
            total_level = overall_data[1]
            total_xp = overall_data[2]

            # Initialize an empty dictionary for skills
            skill_levels = {}

            # List of skill names in the order they appear in the response
            skill_names = [
                "Attack", "Defence", "Strength", "Hitpoints", "Ranged", "Prayer",
                "Magic", "Cooking", "Woodcutting", "Fletching", "Fishing", "Firemaking",
                "Crafting", "Smithing", "Mining", "Herblore", "Agility", "Thieving",
                "Slayer", "Hunter", "Construction", "Farming", "Runecrafting", "Hunter", "Construction", "Farming"
            ]
            
            # Iterate over the skill data in the response
            for i in range(1, len(data)):
                # Ensure we don't go out of range by checking the data length
                if i < len(skill_names):
                    skill_data = data[i].split(",")
                    skill_levels[skill_names[i - 1]] = {
                        "level": skill_data[1] if len(skill_data) > 1 else "N/A",
                        "xp": skill_data[2] if len(skill_data) > 2 else "N/A"
                    }

            return {
                "username": username,
                "total_level": total_level,
                "total_xp": total_xp,
                "skills": skill_levels
            }
        else:
            return {"error": f"Could not fetch data for '{username}'. Make sure the username is correct."}
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
