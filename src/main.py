# TODO: Fill in your Reddit app credentials
import os
from dotenv import load_dotenv
import praw

load_dotenv()  # Load environment variables from .env

reddit = praw.Reddit(
    client_id=os.getenv('REDDIT_CLIENT_ID'),
    client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
    user_agent=os.getenv('REDDIT_USER_AGENT'),
    username=os.getenv('REDDIT_USERNAME'),
    password=os.getenv('REDDIT_PASSWORD')
)

def main():
    print('Reddit bot is running!')
    dqv = reddit.subreddit('DavidQuayleVlogs')
    recent_post = dqv.new(limit=5)
    for post in recent_post:
        print(post.id)
        submission = reddit.submission(id=post.id)
        comment_text = "I am a David Quayle bot currently in development. Stay tuned to see my progress. As always, I hope you enjoyed this reddit as much as DQV_Fan did making it. If you did please drop him a thumbs up, he would really appreciate it. Also subscribe to his channel if you haven't already, because he drops a new video every single Monday, that you don't wanna miss. As always, work hard and be nice to people. Beep."
        try:
            comment = submission.reply(comment_text)
            print(f"Comment created successfully! Comment ID: {comment.id}")
        except Exception as e:
            print(f"An error occurred: {e}")
    

def getHotPosts():
    subs = reddit.subreddit('DavidQuayleVlogs').hot(limit=10)

    for submission in subs:
        print(submission.title)

if __name__ == '__main__':
    main() 