import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";

const server = new McpServer({
  name: "Users Service",
  version: "1.0.0",
});



import { z } from "zod";
import axios from "axios";

server.tool(
  "getUser",
  { id: z.number() },
  async ({ id }) => {
    try {
      const resp = await axios.get(`https://jsonplaceholder.typicode.com/users/${id}`);
      const name = resp.data && resp.data.name ? resp.data.name : null;
      return {
        content: [
          {
            type: "text",
            text: name,
          },
        ],
      };
    } catch (err) {
      return {
        content: [
          {
            type: "text",
            text: null,
          },
        ],
      };
    }
  },
);

import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

const transport = new StdioServerTransport();
await server.connect(transport);