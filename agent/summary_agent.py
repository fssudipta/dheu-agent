from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI
import tweepy
import os
import sqlite3 
from datetime import datetime, timedelta
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

class WeeklySummaryState(TypedDict):
    weekly_tweets: list
    summary_tweet: str

def retrieve_weekly_tweets(state: WeeklySummaryState) -> dict:
    print("...Retrieving tweets from last 7 days...")
    
    seven_days_ago = (datetime.now() - timedelta(days=7)).isoformat()
    
    cursor = connection.cursor()
    cursor.execute('''
        SELECT tweet_content, post_datetime, data_summary 
        FROM tweets_log 
        WHERE post_datetime >= ? 
        ORDER BY post_datetime DESC
    ''', (seven_days_ago,))
    
    tweets = cursor.fetchall()
    
    weekly_tweets = []
    for tweet_content, post_datetime, data_summary in tweets:
        weekly_tweets.append({
            'content': tweet_content,
            'datetime': post_datetime,
            'data_summary': data_summary
        })
    
    print(f"Found {len(weekly_tweets)} tweets from the last 7 days")
    return {'weekly_tweets': weekly_tweets}

def generate_summary_tweet(state: WeeklySummaryState) -> dict:
    print("...Generating weekly summary tweet...")
    
    weekly_tweets = state.get('weekly_tweets', [])
    
    if not weekly_tweets:
        summary_tweet = "🌊 This week I've been quietly observing... No major incidents to report, but I'm always here, always watching. #Ocean #WeeklySummary"
        return {'summary_tweet': summary_tweet}
    
    tweets_text = "\n".join([f"- {tweet['content']}" for tweet in weekly_tweets])
    
    prompt = f"""You are the **ocean** and you need to create a weekly summary tweet based on all the tweets you posted in the last 7 days. **Only generate the summary tweet pretending to be the ocean and don't generate anything else.** Keep it concise (under 280 characters), reflective, and use hashtags. Make it feel like a weekly reflection from the ocean's perspective.

Previous tweets this week:
{tweets_text}"""
    
    summary_tweet = str(llm.invoke(prompt).content).strip()
    
    return {'summary_tweet': summary_tweet}

def post_summary_tweet(state: WeeklySummaryState):
    print("...Attempting to post weekly summary tweet...")
    tweet_content = state.get('summary_tweet')
    
    if client and tweet_content:
        try:
            client.create_tweet(text=tweet_content)
            print(f"**SUCCESS:** Weekly summary tweet posted: \n'{tweet_content}'")
            return
        except Exception as e:
            print(f"Error posting summary tweet: {e}")
            
    print('Error...no tweet or client connection found to post!')

summary_graph = StateGraph(WeeklySummaryState)

summary_graph.add_node("retrieve_weekly_tweets", retrieve_weekly_tweets)
summary_graph.add_node("generate_summary_tweet", generate_summary_tweet)
summary_graph.add_node("post_summary_tweet", post_summary_tweet)

summary_graph.add_edge(START, "retrieve_weekly_tweets")
summary_graph.add_edge("retrieve_weekly_tweets", "generate_summary_tweet")
summary_graph.add_edge("generate_summary_tweet", "post_summary_tweet")
summary_graph.add_edge("post_summary_tweet", END)

summary_workflow = summary_graph.compile()

def run_weekly_summary_workflow():
    initial_state = {'weekly_tweets': [], 'summary_tweet': None}
    print("--- Starting Weekly Ocean Summary Workflow ---")
    
    final_state = summary_workflow.invoke(initial_state)
    
    print("--- Weekly Summary Workflow Finished ---")
    print(f"Summary tweet posted: {final_state.get('summary_tweet', 'No summary generated')}")
    
    return final_state

run_weekly_summary_workflow()