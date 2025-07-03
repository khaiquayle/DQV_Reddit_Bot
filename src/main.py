import os
from dotenv import load_dotenv
import praw
from openai import OpenAI
load_dotenv()  # Load environment variables from .env

reddit = praw.Reddit(
    client_id=os.getenv('REDDIT_CLIENT_ID'),
    client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
    user_agent=os.getenv('REDDIT_USER_AGENT'),
    username=os.getenv('REDDIT_USERNAME'),
    password=os.getenv('REDDIT_PASSWORD')
)

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=os.getenv('DEEPSEEK_API_KEY'),
)


def fetch_new_posts(subreddit_name, limit=5):
    """
    Fetch the newest posts from a subreddit.
    Returns a list of praw.models.Submission objects.
    """
    subreddit = reddit.subreddit(subreddit_name)
    return list(subreddit.new(limit=limit))



def extract_post_content(submission):
    """
    Extracts and returns the title and body from a submission.
    """
    title = submission.title
    body = submission.selftext
    return title, body



def prepare_llm_prompt(title, body, scripts=None):
    """
    Prepares the prompt for the LLM, placing the style scripts first, then the instruction and post content.
    """
    prompt = ""
    if scripts:
        prompt += f"Mimic the following quotes and speaking style:\n{scripts}\n\n"
    prompt += (
        "You are a YouTube vlogger named David Quayle. Respond to the following Reddit post in David's style. Do not include any other side comments. Respond as if you were typing directly into reddit. Do not include any special characters for emphasis (for example, no asterisks * to indicate style). Respond in plain English as anyone would on reddit. Keep response to under 2 paragraphs.\n\n"
        f"Title: {title}\n\nBody: {body}\n"
    )
    return prompt



def post_reply(submission, reply_text):
    """
    Posts a reply to the given submission.
    """
    try:
        reply_text = str(reply_text).strip()
        print(f"Reply text (repr): {repr(reply_text)}")
        
        if not reply_text:
            print("Reply text is empty after stripping. Not posting.")
            return None
        
        comment = submission.reply(reply_text)
        print(f"Comment created successfully! Comment ID: {comment.id}")
        return comment
    except Exception as e:
        print(f"An error occurred while posting reply: {e}")
        return None
    

    
def call_llm_api(prompt):
    completion = client.chat.completions.create(
        extra_body={},
        model="deepseek/deepseek-chat-v3-0324:free",
        messages=[
            {
            "role": "user",
            "content": prompt
            }
        ]
    )
    print(completion.choices[0].message.content)
    return completion.choices[0].message.content

def main():
    print('Reddit bot is running!')
    subreddit_name = 'DavidQuayleVlogs'
    posts = fetch_new_posts(subreddit_name, limit=5)
    if not posts:
        print("No new posts found.")
        return
    submission = posts[4]
    title, body = extract_post_content(submission)
    print("Title:", title)
    print("Body:", body)
    # Placeholder for LLM integration:
    scripts = "Example 1: \"A thousand subscribers—that's not just a number, it's a milestone, a dream, and a reminder that people out there actually want to follow my journey.\" Example 2: \"I don't make videos to flex or to show off—I make them because I have a true passion for putting my life on display and sharing growth.\" Example 3: \"Every time I pick up the camera, it's a chance to be myself, to express who I really am, and to get creative.\" Example 4: \"I've uploaded a video every single Monday for the last three years—not because it's easy, but because consistency beats everything.\" Example 5: \"If you want to start a YouTube channel, pick a schedule you can realistically stick to—it's better to be consistent than to burn out fast.\" Example 6: \"Sometimes social media makes it look like I'm rolling in cash, but truth is, I'm juggling bills, expensive rent, and auto insurance just like anyone else.\" Example 7: \"I don't call my family enough, and honestly, that bugs me—because no matter where life takes me, they're the reason I am who I am today.\" Example 8: \"You gotta never forget your roots—even if you move across the country or change careers, always remember where you came from.\" Example 9: \"I tend to think too much about the future, and sometimes I have to remind myself to just survive today and make the day as good as possible.\" Example 10: \"Putting pressure on yourself to be the best can be a double-edged sword—drive is good, but don't hold a grudge against yourself when things don't go perfect.\" Example 11: \"I'm one year out of college, with a decent job, but I'm far from rich—there's a lot behind the scenes that people don't see.\" Example 12: \"Quality over quantity is my mantra—I'd rather drop one solid, full-day project video a week than rush out two half-baked ones.\" Example 13: \"Life isn't perfect, and my life certainly isn't either—I'm constantly working to improve and I want you to know that too.\" Example 14: \"Sleep is no joke. I thought I could function on six hours a night forever, but it's catching up to me—I need to prioritize my health more.\" Example 15: \"Lifting weights isn't just about looking good—it's a passion of mine that keeps me mentally and physically strong.\" Example 16: \"Social media can paint a false reality. I want to be real with you because none of us have it all figured out.\" Example 17: \"When I hit 100 subscribers, we celebrated with Topgolf and a few beers—those milestones matter because they mark progress.\" Example 18: \"Every subscriber, every comment, every like—it fuels my motivation to keep sharing my story.\" Example 19: \"If I never gain another subscriber, I'd still be happy because this channel is about my growth, not just numbers.\" Example 20: \"The journey is as important as the destination—whether it's life, work, or YouTube, it's about loving the process.\" Example 21: \"You are your own competition.\" Example 22: \"The only person I'm trying to impress is my future self.\" Example 23: \"If you want to do something, go do it — because you know it's gonna benefit you and your life overall.\" Example 24: \"I'm not perfect. I'm nowhere near perfect. I still got a lot of problems, but I'm working on it. It's a work in progress.\" Example 25: \"I think I am much more confident, outgoing, and extroverted now than I was back in high school.\" Example 26: \"When you start to realize these two things — that you yourself are your only competition, and that you're so fortunate to have everything that you do — your mind just becomes open to all the potential possibilities of what you could accomplish.\" Example 27: \"Every time I get a new subscriber, I get a smile on my face. It just feels awesome.\" Example 28: \"I value staying fit. I want to put up good weight in the gym. I want to have a good looking body. I want to be active.\" Example 29: \"You would get more energized, more determined to crush everything you need to do that day.\" Example 30: \"It's not you versus the world. It's not you versus your friends. Not your social media. It's you versus you. That's it.\""
    prompt = prepare_llm_prompt(title, body, scripts)
    print(prompt)
    llm_response = call_llm_api(prompt)
    post_reply(submission, llm_response)



def get_hot_posts(subreddit_name, limit=10):
    """
    Prints the titles of the top hot posts in a subreddit.
    """
    subs = reddit.subreddit(subreddit_name).hot(limit=limit)
    for submission in subs:
        print(submission.title)



if __name__ == '__main__':
    main() 