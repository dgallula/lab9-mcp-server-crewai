#!/usr/bin/env node

const { Server } = require("@modelcontextprotocol/sdk/server/index.js");
const {
  StdioServerTransport,
} = require("@modelcontextprotocol/sdk/server/stdio.js");
const {
  CallToolRequestSchema,
  ErrorCode,
  ListToolsRequestSchema,
  TextContent,
} = require("@modelcontextprotocol/sdk/types.js");
const axios = require("axios");

// Configuration Jira
const JIRA_HOST = process.env.JIRA_HOST || "https://your-instance.atlassian.net";
const JIRA_USERNAME = process.env.JIRA_USERNAME || "your_email@example.com";
const JIRA_API_TOKEN = process.env.JIRA_API_TOKEN || "your_api_token";

// Créer le client Jira avec auth basique
const jiraClient = axios.create({
  baseURL: `${JIRA_HOST}/rest/api/3`,
  auth: {
    username: JIRA_USERNAME,
    password: JIRA_API_TOKEN,
  },
  headers: {
    "Content-Type": "application/json",
  },
});

// Initialiser le serveur MCP
const server = new Server({
  name: "jira-mcp-server",
  version: "1.0.0",
});

// Enregistrer les outils disponibles
server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: "list_projects",
      description: "List all Jira projects",
      inputSchema: {
        type: "object",
        properties: {},
        required: [],
      },
    },
    {
      name: "list_issues",
      description: "List issues from a project",
      inputSchema: {
        type: "object",
        properties: {
          project_key: {
            type: "string",
            description: "Project key (e.g., PROJ)",
          },
          max_results: {
            type: "number",
            description: "Maximum number of results (default: 10)",
          },
        },
        required: ["project_key"],
      },
    },
    {
      name: "get_issue",
      description: "Get details of a specific issue",
      inputSchema: {
        type: "object",
        properties: {
          issue_key: {
            type: "string",
            description: "Issue key (e.g., PROJ-123)",
          },
        },
        required: ["issue_key"],
      },
    },
    {
      name: "create_issue",
      description: "Create a new issue",
      inputSchema: {
        type: "object",
        properties: {
          project_key: {
            type: "string",
            description: "Project key",
          },
          summary: {
            type: "string",
            description: "Issue summary/title",
          },
          description: {
            type: "string",
            description: "Issue description",
          },
          issue_type: {
            type: "string",
            description: "Issue type (e.g., Bug, Task, Story)",
          },
        },
        required: ["project_key", "summary", "issue_type"],
      },
    },
    {
      name: "update_issue",
      description: "Update an existing issue",
      inputSchema: {
        type: "object",
        properties: {
          issue_key: {
            type: "string",
            description: "Issue key",
          },
          summary: {
            type: "string",
            description: "New summary",
          },
          description: {
            type: "string",
            description: "New description",
          },
          status: {
            type: "string",
            description: "New status",
          },
        },
        required: ["issue_key"],
      },
    },
  ],
}));

// Traiter les appels d'outils
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  try {
    const { name, arguments: args } = request;

    switch (name) {
      case "list_projects": {
        const response = await jiraClient.get("/project");
        return {
          content: [
            {
              type: "text",
              text: JSON.stringify(response.data, null, 2),
            },
          ],
        };
      }

      case "list_issues": {
        const { project_key, max_results = 10 } = args;
        const jql = `project = "${project_key}"`;
        const response = await jiraClient.get("/search", {
          params: {
            jql,
            maxResults: max_results,
          },
        });
        return {
          content: [
            {
              type: "text",
              text: JSON.stringify(response.data.issues, null, 2),
            },
          ],
        };
      }

      case "get_issue": {
        const { issue_key } = args;
        const response = await jiraClient.get(`/issue/${issue_key}`);
        return {
          content: [
            {
              type: "text",
              text: JSON.stringify(response.data, null, 2),
            },
          ],
        };
      }

      case "create_issue": {
        const { project_key, summary, description, issue_type } = args;
        const response = await jiraClient.post("/issue", {
          fields: {
            project: { key: project_key },
            summary,
            description,
            issuetype: { name: issue_type },
          },
        });
        return {
          content: [
            {
              type: "text",
              text: JSON.stringify(response.data, null, 2),
            },
          ],
        };
      }

      case "update_issue": {
        const { issue_key, summary, description, status } = args;
        const updateData = { fields: {} };
        if (summary) updateData.fields.summary = summary;
        if (description) updateData.fields.description = description;
        if (status)
          updateData.fields.status = { name: status };

        const response = await jiraClient.put(
          `/issue/${issue_key}`,
          updateData
        );
        return {
          content: [
            {
              type: "text",
              text: `Issue ${issue_key} updated successfully`,
            },
          ],
        };
      }

      default:
        return {
          content: [
            {
              type: "text",
              text: `Unknown tool: ${name}`,
            },
          ],
          isError: true,
        };
    }
  } catch (error) {
    return {
      content: [
        {
          type: "text",
          text: `Error: ${error.message}`,
        },
      ],
      isError: true,
    };
  }
});

// Démarrer le serveur
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("Jira MCP Server started");
}

main().catch((error) => {
  console.error("Fatal error:", error);
  process.exit(1);
});
