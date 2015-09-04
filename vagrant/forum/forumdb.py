#
# Database access functions for the web forum.
# 

import time
import bleach
import psycopg2

## Database connection
DB = []

## Get posts from database.
def GetAllPosts():
    '''Get all the posts from the database, sorted with the newest first.

    Returns:
      A list of dictionaries, where each dictionary has a 'content' key
      pointing to the post content, and 'time' key pointing to the time
      it was posted.
    '''
    #connect to the db first
    DB = psycopg2.connect("dbname=forum")
    #establish a cursor
    c = DB.cursor()
    c.execute("SELECT time, content FROM posts ORDER BY time DESC")
    #create a dictionay suited for fourm.py
    posts = ({'content': str(row[1]), 'time':str(row[0])}
      #getting data for the dictionary
      for row in c.fetchall())
    DB.close()
    return posts

## Add a post to the database.
def AddPost(content):
    '''Add a new post to the database.

    Args:
      content: The text content of the new post.
    '''
    DB = psycopg2.connect("dbname=forum")
    #establish a cursor
    c = DB.cursor()
    cleanContent = bleach.clean(content)
    c.execute("INSERT INTO posts VALUES (%s)", (cleanContent,))
    DB.commit()
    DB.close()
