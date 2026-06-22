# MCP Server Setup Guide for Data Engineers

## Quick Start

Add to your project's `.mcp.json`:

```json
{
  "mcpServers": {
    "server-name": {
      "command": "npx",
      "args": ["-y", "@scope/package-name"],
      "env": {
        "ENV_VAR": "value"
      }
    }
  }
}
```

---

## Database MCP Servers

### PostgreSQL / Redshift
```json
"postgres": {
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-postgres"],
  "env": {
    "POSTGRES_CONNECTION_STRING": "postgresql://user:pass@host/dbname"
  }
}
```

### SQLite / DuckDB (local dev)
```json
"sqlite": {
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-sqlite", "./data/dev.db"]
}
```

### Snowflake
```json
"snowflake": {
  "command": "npx",
  "args": ["-y", "mcp-snowflake"],
  "env": {
    "SNOWFLAKE_ACCOUNT": "your-account",
    "SNOWFLAKE_USER": "your-user",
    "SNOWFLAKE_PASSWORD": "${SNOWFLAKE_PASSWORD}",
    "SNOWFLAKE_DATABASE": "ANALYTICS",
    "SNOWFLAKE_SCHEMA": "PUBLIC",
    "SNOWFLAKE_WAREHOUSE": "COMPUTE_WH"
  }
}
```

---

## Code & Project Management

### GitHub
```json
"github": {
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-github"],
  "env": {
    "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"
  }
}
```

### Filesystem (scoped)
```json
"filesystem": {
  "command": "npx",
  "args": [
    "-y",
    "@modelcontextprotocol/server-filesystem",
    "./dbt_project",
    "./pipelines"
  ]
}
```

---

## Microsoft Fabric

```bash
# Clone the official skills repo
git clone https://github.com/microsoft/skills-for-fabric
cd skills-for-fabric

# Claude Code auto-discovers .claude-plugin directory
claude  # skills available automatically
```

Available skill bundles: `fabric-skills`, `fabric-authoring`, `fabric-consumption`, `fabric-operations`, `powerbi-authoring`

Authentication: requires Azure CLI (`az login`)

---

## Monitoring & Observability

### Sentry
```json
"sentry": {
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-sentry"],
  "env": {
    "SENTRY_AUTH_TOKEN": "${SENTRY_TOKEN}",
    "SENTRY_ORG": "your-org"
  }
}
```

---

## Security Best Practices

1. **Never put credentials directly in `.mcp.json`** — use `${ENV_VAR}` syntax
2. **Scope filesystem MCP to project directories only** — not `/` or `~`
3. **Use read-only credentials for analytics MCP servers**
4. **Separate MCP servers for separate permission levels**:
   - `warehouse-readonly` for analytics
   - `warehouse-pipeline` for ETL (INSERT/UPDATE only, specific schemas)
5. **Add `.mcp.json` to `.gitignore` if it contains any non-template values**

---

## Recommended `.mcp.json` for a DE Team

```json
{
  "mcpServers": {
    "warehouse-readonly": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "POSTGRES_CONNECTION_STRING": "${WAREHOUSE_READONLY_URL}"
      },
      "description": "Analytics queries — SELECT only"
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"
      }
    },
    "project-files": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "./dbt_project",
        "./pipelines",
        "./docs"
      ],
      "description": "Project files — scoped to dbt, pipelines, docs only"
    }
  }
}
```
