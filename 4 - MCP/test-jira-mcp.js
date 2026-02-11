#!/usr/bin/env node
/**
 * Test script for Jira MCP Server
 * Validates the server configuration and connectivity
 */

const axios = require("axios");

// Configuration from environment
const JIRA_HOST = process.env.JIRA_HOST || "https://dgallula.atlassian.net";
const JIRA_USERNAME = process.env.JIRA_USERNAME || "davidev";
const JIRA_API_TOKEN = process.env.JIRA_API_TOKEN || "test_token";

console.log("\n🔍 Testing Jira MCP Server Configuration\n");
console.log("━".repeat(50));
console.log("📋 Configuration:");
console.log(`  Host: ${JIRA_HOST}`);
console.log(`  Username: ${JIRA_USERNAME}`);
console.log(`  Token: ${JIRA_API_TOKEN ? "✅ Set" : "❌ Not set"}`);
console.log("━".repeat(50));

// Create Jira client
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

async function testConnection() {
  try {
    console.log("\n🧪 Testing Jira Connection...");
    
    // Test 1: Get server info
    console.log("\n  Test 1: Fetching server information...");
    const serverInfo = await jiraClient.get("/serverInfo");
    console.log(`  ✅ Server: ${serverInfo.data.serverTitle} (v${serverInfo.data.version})`);

    // Test 2: List projects
    console.log("\n  Test 2: Listing Jira projects...");
    const projects = await jiraClient.get("/project");
    console.log(`  ✅ Found ${projects.data.length} project(s)`);
    
    if (projects.data.length > 0) {
      projects.data.slice(0, 3).forEach(p => {
        console.log(`     • ${p.key}: ${p.name}`);
      });
    }

    // Test 3: Test issue search
    if (projects.data.length > 0) {
      console.log("\n  Test 3: Searching for issues...");
      const projectKey = projects.data[0].key;
      const issues = await jiraClient.get("/search", {
        params: {
          jql: `project = "${projectKey}"`,
          maxResults: 5,
        },
      });
      console.log(`  ✅ Found ${issues.data.total} issue(s) in ${projectKey}`);
      if (issues.data.issues.length > 0) {
        issues.data.issues.slice(0, 3).forEach(i => {
          console.log(`     • ${i.key}: ${i.fields.summary}`);
        });
      }
    }

    console.log("\n" + "━".repeat(50));
    console.log("✅ All tests passed!");
    console.log("━".repeat(50));
    console.log("\n🚀 Server is ready to use with MCP!");
    
  } catch (error) {
    console.error("\n❌ Test failed:");
    if (error.response) {
      console.error(`  Status: ${error.response.status}`);
      console.error(`  Message: ${error.response.data.errorMessages?.[0] || error.message}`);
    } else {
      console.error(`  Error: ${error.message}`);
    }
    console.log("\n⚠️  Please check your credentials and try again.");
    process.exit(1);
  }
}

// Run tests
testConnection();
