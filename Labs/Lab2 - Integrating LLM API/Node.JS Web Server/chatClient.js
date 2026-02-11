const express = require("express");
const http = require("http");
const cors = require("cors");
const { Configuration, OpenAIApi } = require("openai");

const app = express();
const server = http.createServer(app);




server.listen(5000, () => {
  console.log(":: server listening on 5000 :::");
});

const configuration = new Configuration({
  apiKey: process.env.OPENAI_API_KEY || ""  // Set your OpenAI API key,
});
const openai = new OpenAIApi(configuration);


async function callChatGPT()
{
    const chatHistory = [];

    chatHistory.push({ role: "user", content: "Tell me a joke" });
    const chatCompletion = await openai.createChatCompletion({
        model: "gpt-3.5-turbo",
        messages: chatHistory,
    });
    
    console.log(chatCompletion.data.choices[0].message.content);
}



callChatGPT();
