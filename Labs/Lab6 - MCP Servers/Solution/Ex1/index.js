import {McpServer} from "@modelcontextprotocol/sdk/server/mcp.js"
import {StdioServerTransport} from "@modelcontextprotocol/sdk/server/stdio.js"
import axios from "axios"
const server = new McpServer(
    {
        name: "Weather Service",
        version: "1.0.0",
    
    }
)


server.tool(
    "GetProducts",
    {},
    async ({}) => {
        const resp = await axios.get("https://fakestoreapi.com/products")
        return {
            content: [
                {
                    type: "text",
                    text: JSON.stringify(resp.data)
                }
            ]
        }
    }
)

const transport = new StdioServerTransport()
await server.connect(transport)


