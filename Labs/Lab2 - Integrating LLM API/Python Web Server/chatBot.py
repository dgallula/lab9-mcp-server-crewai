from secret_key import key
from openai import OpenAI

from flask import Flask, request, jsonify



app = Flask(__name__)
# localhost:3001

@app.route("/", methods=["POST"])
def prompt():
    data = request.json["data"]
    return jsonify({"msg": f"You sent: {data} "})
    
    

app.run(port=3001)






client = OpenAI(api_key=key)


# messages = []
# messages.append({"role": "system", "content": "You are a java developer"})

# while True:
#     user_input = input("How can I help you?")
#     messages.append({"role": "user", "content": user_input})

#     resp = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages)

#     reply = resp.choices[0].message.content
#     messages.append({"role": "assistant", "content": reply})
#     print(f"ChatGPT says: {reply} ")
