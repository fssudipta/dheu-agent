from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI
import tweepy
import os
import sqlite3 
from datetime import datetime 
from typing import TypedDict, Annotated
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()


api_key_secret = os.getenv('API_KEY_SECRET')
api_key = os.getenv('API_KEY')
access_token = os.getenv('ACCESS_TOKEN')
access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')

try:
    client = tweepy.Client(
        consumer_key=api_key, 
        consumer_secret=api_key_secret, 
        access_token=access_token, 
        access_token_secret=access_token_secret
    )
except Exception as e:
    print(f"Error initializing Tweepy client: {e}")
    client = None 


llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")


DB_NAME = 'ocean_tweets.db'
connection = sqlite3.connect(database=DB_NAME, check_same_thread=False)

def init_tweets_log_table():
    """Creates the table to log posted tweets if it doesn't exist."""
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tweets_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tweet_content TEXT NOT NULL,
            post_datetime TIMESTAMP NOT NULL,
            data_summary TEXT
        )
    ''')
    connection.commit()

init_tweets_log_table()



class OceanTweetState(TypedDict):
    """The state of the LangGraph workflow."""
    data: str  
    tweet: str 

def generate_tweet(state: OceanTweetState) -> dict:
    """Generates the tweet content based on the input data."""
    print("...Generating tweet...")
    prompt = f"""You are the **ocean** and you have to generate a tweet about your current condition based on the images captured by satellite and data analyzed by a machine learning model. **Only generate the tweet pretending to be the ocean and don't generate anything else.** Use hashtags if needed.
    Data: {state['data']}"""
    
    
    tweet = str(llm.invoke(prompt).content).strip() if state.get('data') else "Error: No data to generate tweet."
    
    return {'tweet': tweet}

def post_tweet(state: OceanTweetState):
    """Posts the generated tweet to Twitter."""
    print("...Attempting to post tweet...")
    tweet_content = state.get('tweet')
    
    if client and tweet_content:
        try:
            client.create_tweet(text=tweet_content)
            print(f"**SUCCESS:** Tweet content generated and ready to post: \n'{tweet_content}'")
            return
        except Exception as e:
            print(f"Error posting tweet: {e}")
            
    print('Error...no tweet or client connection found to post!')

def log_tweet(state: OceanTweetState) -> dict:
    """Logs the posted tweet content and datetime to the SQLite database."""
    tweet_content = state.get('tweet')
    data_summary = state.get('data', 'No data provided')
    
    if tweet_content:
        now = datetime.now()
        try:
            cursor = connection.cursor()
            cursor.execute('''
                INSERT INTO tweets_log (tweet_content, post_datetime, data_summary)
                VALUES (?, ?, ?)
            ''', (tweet_content, now.isoformat(), data_summary))
            connection.commit()
            print(f"...Tweet successfully logged in {DB_NAME} at {now.strftime('%Y-%m-%d %H:%M:%S')}")
        except Exception as e:
            print(f"Error logging tweet to database: {e}")
            
    return {} 


graph = StateGraph(OceanTweetState)

graph.add_node("generate_tweet", generate_tweet)
graph.add_node("post_tweet", post_tweet)
graph.add_node("log_tweet", log_tweet) 

graph.add_edge(START, "generate_tweet")
graph.add_edge("generate_tweet", "post_tweet")

graph.add_edge("post_tweet", "log_tweet")

graph.add_edge("log_tweet", END) 


workflow = graph.compile()



def run_ocean_tweet_workflow(satellite_data: str):
    """
    Runs the full workflow: generates a tweet, attempts to post it, 
    and logs the result to the database.
    """
    initial_state = {'data': satellite_data, 'tweet': None}
    print("--- Starting Ocean Tweet Workflow ---")
    
    final_state = workflow.invoke(initial_state)
    
    print("--- Workflow Finished ---")
    print(f"Final State: {final_state}")
    print(f"Check '{DB_NAME}' for the logged entry.")
    
    return final_state


example_data = """On September 20, 2025, satellite imagery from NASA's MODIS sensor detected an oil spill anomaly in the Bay of Bengal, approximately 40 km south of Chittagong, Bangladesh. The detected slick appears to cover an area of about 12 square kilometers. Machine learning analysis confirmed with 92% confidence that the anomaly corresponds to an oil spill rather than natural discoloration or cloud shadows. The incident has been flagged as requiring urgent attention."""


run_ocean_tweet_workflow(example_data)