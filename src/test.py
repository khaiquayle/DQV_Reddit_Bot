from openai import OpenAI
import os

from dotenv import load_dotenv
load_dotenv()


client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=os.getenv('DEEPSEEK_API_KEY'),
)

completion = client.chat.completions.create(
  extra_headers={
    "HTTP-Referer": "<YOUR_SITE_URL>", # Optional. Site URL for rankings on openrouter.ai.
    "X-Title": "<YOUR_SITE_NAME>", # Optional. Site title for rankings on openrouter.ai.
  },
  extra_body={},
  model="deepseek/deepseek-chat-v3-0324:free",
  messages=[
    {
      "role": "user",
      "content": "What is the meaning of life?"
    }
  ]
)
print(completion.choices[0].message.content)