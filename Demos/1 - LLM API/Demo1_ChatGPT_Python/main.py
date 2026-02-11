from secret_key import openai_key
from openai import OpenAI

client = OpenAI(api_key=openai_key)

messages = []
messages.append({"role": "system", "content": "You are a java developer"})

while True:
    user_input = input(" ")
    messages.append({"role": "user", "content": user_input})
    response = client.chat.completions.create(model="gpt-4", messages=messages)
    ai_reply = response.choices[0].message.content
    messages.append({"role": "assistant", "content": ai_reply})
    print(ai_reply)



