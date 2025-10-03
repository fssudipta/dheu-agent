from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI
import facebook as fb
import sqlite3 
from datetime import datetime 
from typing import TypedDict
from dotenv import load_dotenv
import os

load_dotenv()

PAGE_ID = ""
PAGE_ACCESS_TOKEN = ""
poster = fb.GraphAPI(access_token=PAGE_ACCESS_TOKEN)

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

DB_NAME = 'ocean_posts.db'
connection = sqlite3.connect(database=DB_NAME, check_same_thread=False)

def init_posts_log_table():
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS posts_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            post_content TEXT NOT NULL,
            post_datetime TIMESTAMP NOT NULL,
            event TEXT,
            coordinates TEXT
        )
    ''')
    connection.commit()

init_posts_log_table()


class OceanPostState(TypedDict):
    event: str
    coordinates: str
    post: str


def generate_post(state: OceanPostState) -> dict:
    prompt = f"""
    You are the **ocean**. Generate a Facebook post about your current condition 
    based on satellite imagery and ML analysis. Pretend to be the ocean. Use hashtags if needed.
    Event: {state['event']}
    Coordinates: {state['coordinates']}
    """
    
    post = str(llm.invoke(prompt).content).strip()
    return {'post': post}


def post_facebook_node(state: OceanPostState):
    post_content = state.get('post')
    if post_content:
        try:
            poster.put_object("me", "feed", message=post_content)
            print(f"✅ Posted to Facebook Page:\n{post_content}")
        except Exception as e:
            print(f"❌ Error posting to Facebook: {e}")
    return {}


def log_post(state: OceanPostState) -> dict:
    post_content = state.get('post')
    if post_content:
        now = datetime.now()
        try:
            cursor = connection.cursor()
            cursor.execute('''
                INSERT INTO posts_log (post_content, post_datetime, event, coordinates)
                VALUES (?, ?, ?, ?)
            ''', (post_content, now.isoformat(), state.get('event'), state.get('coordinates')))
            connection.commit()
        except Exception as e:
            print(f"❌ Error logging post: {e}")
    return {} 


graph = StateGraph(OceanPostState)
graph.add_node("generate_post", generate_post)
graph.add_node("post_facebook", post_facebook_node)
graph.add_node("log_post", log_post)

graph.add_edge(START, "generate_post")
graph.add_edge("generate_post", "post_facebook")
graph.add_edge("post_facebook", "log_post")
graph.add_edge("log_post", END)

workflow = graph.compile()


def post_update(event: str, coordinates: str):
    """
    Generates, posts, and logs a Facebook post given an event and coordinates.
    """
    initial_state = {'event': event, 'coordinates': coordinates, 'post': None}
    final_state = workflow.invoke(initial_state)
    return final_state


if __name__ == "__main__":
    sample_event = "Plastic waste accumulation detected"
    sample_coordinates = "15.30°S, 125.70°E"

    post_update(sample_event, sample_coordinates)
