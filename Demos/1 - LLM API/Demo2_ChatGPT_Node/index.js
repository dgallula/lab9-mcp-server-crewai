const {Configuration, OpenAIApi} = require("openai")
const {openai: OPENAI_KEY} = require("./secret_key")

const configuration = new Configuration({
    apiKey: OPENAI_KEY
})

const client = new OpenAIApi(configuration)


async function callChatGPT() {
    const chatHistory = []
    chatHistory.push({role: "user", content: "Tell me a joke"})
    const response = await client.createChatCompletion({
        messages: chatHistory,
        model: "gpt-4o"
    })
    console.log(response.data.choices[0].message.content)
}

callChatGPT()