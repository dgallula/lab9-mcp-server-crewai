import OpenAI from 'openai';

const messages = [{"role": "user", "content": "Tell me a joke"}]

const client = new OpenAI({
  apiKey: "",
});

const response = await client.chat.completions.create({
  model: 'gpt-4o',
  messages: messages
  
});

console.log(response.choices[0].message.content);