import requests


def fetch_highscores(username: str) -> dict:
    """
    Fetch OSRS Highscores data for a given username.
    Returns a dictionary with relevant stats or an error message.
    """
    api_url = f"https://secure.runescape.com/m=hiscore_oldschool/index_lite.ws?player={username}"

    try:
        response = requests.get(api_url, timeout=10)
        if response.status_code != 200:
            return {
                "error": f"Could not fetch data for '{username}'. Make sure the username is correct."
            }

        data = response.text.splitlines()
        if not data or len(data) < 24:
            return {"error": f"Unexpected data format for '{username}'."}

        # Get overall data (the first line)
        overall_data = data[0].split(",")
        total_level = overall_data[1] if len(overall_data) > 1 else "N/A"
        total_xp = overall_data[2] if len(overall_data) > 2 else "N/A"

        # Skill names in order (excluding the first overall entry)
        skill_names = [
            "Attack",
            "Defence",
            "Strength",
            "Hitpoints",
            "Ranged",
            "Prayer",
            "Magic",
            "Cooking",
            "Woodcutting",
            "Fletching",
            "Fishing",
            "Firemaking",
            "Crafting",
            "Smithing",
            "Mining",
            "Herblore",
            "Agility",
            "Thieving",
            "Slayer",
            "Farming",
            "Runecrafting",
            "Hunter",
            "Construction",
        ]

        skill_levels = {}

        # Iterate over the skill data (starting from index 1)
        for i, skill_name in enumerate(skill_names, start=1):
            if i >= len(data):
                break  # Avoid out-of-range errors

            skill_data = data[i].split(",")
            skill_levels[skill_name] = {
                "level": skill_data[1] if len(skill_data) > 1 else "N/A",
                "xp": skill_data[2] if len(skill_data) > 2 else "N/A",
            }

        return {
            "username": username,
            "total_level": total_level,
            "total_xp": total_xp,
            "skills": skill_levels,
        }

    except requests.RequestException as e:
        return {"error": f"Request error: {str(e)}"}
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
