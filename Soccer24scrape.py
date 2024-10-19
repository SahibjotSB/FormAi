from playwright.sync_api import sync_playwright
import json
import os

def extract_float(locator, index, default=0.0):
    try:
        value = locator.nth(index).inner_text().strip()
        return float(value)
    except (ValueError, IndexError) as e:
        print(f"Failed to extract float at index {index} - {e}. Defaulting to {default}.")
        return default

def extract_int(locator, index, default=0):
    try:
        value = locator.nth(index).inner_text().strip()
        return int(value)
    except (ValueError, IndexError) as e:
        print(f"Failed to extract integer at index {index} - {e}. Defaulting to {default}.")
        return default

def scrape_soccer_data(url):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            print(f"Navigating to {url}...")
            page.goto(url)

            page.wait_for_selector('div.container__detail', timeout=10000)

            home_name = page.locator('div.participant__participantName.participant__overflow').nth(0).inner_text().strip()
            away_name = page.locator('div.participant__participantName.participant__overflow').nth(1).inner_text().strip()

            home_score = extract_int(page.locator('div.duelParticipant__score span'), 0)
            away_score = extract_int(page.locator('div.duelParticipant__score span'), 2)
            
            home_xg = extract_float(page.locator('div._value_7ptpb_4._homeValue_7ptpb_9 strong'), 0)
            away_xg = extract_float(page.locator('div._value_7ptpb_4._awayValue_7ptpb_13 strong'), 0)

            home_corners = extract_int(page.locator('div._value_7ptpb_4._homeValue_7ptpb_9 strong'), 6)
            away_corners = extract_int(page.locator('div._value_7ptpb_4._awayValue_7ptpb_13 strong'), 6)

            home_fouls = extract_int(page.locator('div._value_7ptpb_4._homeValue_7ptpb_9 strong'), 10)
            away_fouls = extract_int(page.locator('div._value_7ptpb_4._awayValue_7ptpb_13 strong'), 10)

            browser.close()

            return {
                "teams": [home_name, away_name],
                "goals": [home_score, away_score],
                "x_goals": [home_xg, away_xg],
                "corners": [home_corners, away_corners],
                "fouls": [home_fouls, away_fouls]
            }
    except Exception as e:
        print(f"An error occurred while scraping {url}: {e}")
        return None

def create_match_data(matches):
    match_data = {
        "fixture": matches[0]["teams"] if matches else ["n/a", "n/a"],
        "stadium": "Get from external site",
        "weather": "Get from weather site",
        "pitch_condition": "Get from external site",
        "type_of_match": "Regular",
        "referee": {
            "name": "n/a",
            "fouls_per_tackle": 0,
            "yellow_per_game": 0
        },
        "head_to_head": {
            "teams": {f"match_{i + 1}": match["teams"] for i, match in enumerate(matches)},
            "goals": {f"match_{i + 1}": match["goals"] for i, match in enumerate(matches)},
            "x_goals": {f"match_{i + 1}": match["x_goals"] for i, match in enumerate(matches)},
            "corners": {f"match_{i + 1}": match["corners"] for i, match in enumerate(matches)},
            "fouls": {f"match_{i + 1}": match["fouls"] for i, match in enumerate(matches)},
            "HT_cards": {f"match_{i + 1}": [] for i in range(len(matches))},
            "FT_cards": {f"match_{i + 1}": [] for i in range(len(matches))}
        }
    }
    return match_data

def load_history(filename='match_history.json'):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                print("Warning: Corrupted history file. Starting fresh.")
                return []
    return []

def save_to_json(data, filename='match_output.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4, separators=(",", ":"))
    print(f"Data saved to {filename}")

def update_history(matches, filename='match_history.json'):
    history = load_history(filename)
    history.extend(matches)
    save_to_json(history, filename)

if __name__ == "__main__":
    urls = [
        'https://www.soccer24.com/match/SxFxJ44k/#/match-summary/match-statistics/0',
        'https://www.soccer24.com/match/fFL2l4A6/#/match-summary/match-statistics/0',
        'https://www.soccer24.com/match/8raD0wPk/#/match-summary/match-statistics/0',
        'https://www.soccer24.com/match/O2F7p3IJ/#/match-summary/match-statistics/0',
        'https://www.soccer24.com/match/lx53l5La/#/match-summary/match-statistics/0'
    ]

    matches = []
    for i, url in enumerate(urls):
        print(f"Scraping match #{i + 1}...")
        match_data = scrape_soccer_data(url)
        if match_data:
            matches.append(match_data)
        else:
            print(f"Failed to scrape match {i + 1}")

    if matches:
        final_data = create_match_data(matches)
        save_to_json(final_data)
        print("Match data saved to match_output.json")

        update_history(matches)
        print("Match history updated in match_history.json")
    else:
        print("No matches were scraped successfully.")
