# SARgonauts AI Agents

This repository contains two distinct AI agents developed for the SARgonauts project, focusing on marine health advocacy and communication.

## 1. Ocean Tweet Agent

This agent leverages LangGraph and Google's Gemini-2.5-Flash model to generate and post tweets about ocean conditions based on satellite data. It also logs the posted tweets into an SQLite database.

### Features

- **Tweet Generation:** Uses `ChatGoogleGenerativeAI` (Gemini-2.5-Flash) to craft tweets from the perspective of "the ocean," summarizing provided marine data.
- **Twitter Integration:** Posts generated tweets to Twitter via the `tweepy` library.
- **Database Logging:** Records tweet content, post timestamp, and a summary of the data used into an SQLite database for historical tracking.
- **LangGraph Workflow:** Orchestrates the tweet generation, posting, and logging processes into a defined state machine.

### How it Works

The agent follows a simple workflow:

1. **`generate_tweet`**: Takes satellite data as input and prompts the LLM to create a tweet.
2. **`post_tweet`**: Attempts to post the generated tweet to Twitter.
3. **`log_tweet`**: Logs the tweet content and data summary into `ocean_tweets.db`.

### Setup

**Install Dependencies:**
```bash
pip install langgraph langchain_google_genai tweepy python-dotenv sqlite3
```

**Environment Variables:** Create a `.env` file in the root directory with your Twitter API credentials and Google API key:

```
API_KEY="YOUR_TWITTER_API_KEY"
API_KEY_SECRET="YOUR_TWITTER_API_KEY_SECRET"
ACCESS_TOKEN="YOUR_TWITTER_ACCESS_TOKEN"
ACCESS_TOKEN_SECRET="YOUR_TWITTER_ACCESS_TOKEN_SECRET"
GOOGLE_API_KEY="YOUR_GOOGLE_GEMINI_API_KEY" # (If not already set globally)
```

**Run the Agent:**
The script includes an example_data string. You can modify this or feed in dynamic satellite data.

```bash
python dheu-agent.py
```

*(Note: If you combine both agents into one file, adjust the execution command as needed).*

### Database

The agent creates an `ocean_tweets.db` SQLite database with a `tweets_log` table to store tweet history.

---

## 2. Marine Health AI Letter Generator

This agent automatically generates advocacy letters for marine conservation organizations, targeting different audiences (policy makers, industry leaders, and communities), using the OpenRouter API with the x-ai/grok-4-fast:free model.

### Features

- **Dynamic Letter Generation:** Creates tailored advocacy letters based on current simulated marine health data.
- **Multiple Audiences:** Generates letters for "Ocean Policy Institute," "Sustainable Marine Industries Coalition," and "Coastal Communities Alliance," each with a specific tone, focus, and call to action.
- **OpenRouter API Integration:** Utilizes x-ai/grok-4-fast:free via OpenRouter for advanced letter composition.
- **Data Simulation:** Includes a function to simulate real-time marine health data, including a "SARgonauts Index," region, severity, and key issues.
- **Fallback Mechanism:** Provides a basic fallback letter template if the OpenRouter API call fails.
- **Automated Output:** Saves generated letters and a daily report in a structured `output/` directory.

### How it Works

1. **Initialization:** The MarineHealthAI class is initialized with your OpenRouter API key and pre-defined OrganizationProfiles for different target audiences.
2. **get_current_marine_data:** Simulates fetching up-to-date marine health statistics, including an overall health index, region, severity, and recent changes.
3. **generate_letter_with_grok:** Constructs a detailed prompt using the marine data and the specific organization's profile, then sends it to the OpenRouter API to generate the letter.
4. **generate_all_letters:** Iterates through all defined organizations, generates a letter for each, and saves them as `.txt` files in the `output/` directory.
5. **save_daily_report:** Compiles all generated letters and organizational data into a JSON report.

### Setup

**Install Dependencies:**
```bash
pip install python-dotenv requests
```

**Environment Variables:** Create a `.env` file in the root directory with your OpenRouter API key:

```
OPENROUTER_API_KEY="YOUR_OPENROUTER_API_KEY"
```

**Run the Agent:**
```bash
python dheu-agent.py
```

*(Note: If you combine both agents into one file, ensure the main() function is called correctly for this part of the script).*

### Output

Generated letters will be saved in the `output/` directory, named with the organization key and a timestamp (e.g., `letter_policy_makers_YYYYMMDD_HHMMSS.txt`). A `daily_report_YYYY-MM-DD.json` file will also be created, summarizing the day's generated letters.

---

## Contribution

Feel free to fork this repository, suggest improvements, or add new agents relevant to marine conservation and communication.