# Deployment Guide for Render

This project is configured for easy deployment on the [Render](https://render.com/) cloud platform using "Infrastructure as Code". The `render.yaml` file in the root of this repository automates the creation of all necessary services.

## Prerequisites

1.  A [Render](https://render.com/) account.
2.  A [GitHub](https://github.com/) account.
3.  A Google Gemini API Key.
4.  The code for this project pushed to your own GitHub repository.

## Deployment Steps

### 1. Create the Blueprint Service

- In your Render Dashboard, click **New** and then select **Blueprint Service**.
- Connect the GitHub repository where you have pushed this project's code.
- Render will automatically detect and parse the `render.yaml` file. You will see the three services (`memory-db`, `mcp-server`, and `conversation-feeder`) listed.
- Click **Approve** to create the services.

### 2. Set Environment Variables

- After approving the plan, Render will take you to a page to configure the services.
- Here, you must provide the values for the secrets required by the application. These are marked as `sync: false` in the `render.yaml` file.
- You will need to enter your:
    - `GEMINI_API_KEY`
    - `FEEDER_AUTH_TOKEN` (you can use any secure secret string)
- The `DATABASE_URL` will be automatically injected by Render.

### 3. Initial Deployment

- Once the environment variables are set, click **Deploy** (or **Apply**).
- Render will now build the Docker images and deploy your database and web services. This may take several minutes. You can monitor the progress in the deployment logs.

### 4. Manually Enable `pgvector` Extension

- The `pgvector` extension, which is required for the semantic search functionality, must be enabled manually after the database is created.
- **Wait** for the `memory-db` service to show a "Healthy" or "Available" status on your Render dashboard.
- In your local terminal (like Termux), ensure you have the PostgreSQL client installed. If not, you can install it with:
  ```bash
  pkg install postgresql
  ```
- In the Render Dashboard, navigate to your `memory-db` database page and find the **Connect** tab.
- Copy the command labeled **"PSQL Command"**.
- Paste and run this command in your local terminal to connect to your new database.
- Once connected, run the following SQL command:
  ```sql
  CREATE EXTENSION vector;
  ```

### 5. Final Step: Database Migration

The original `README.md` mentioned running `alembic upgrade head`. The `mcp_server` service is configured to do this automatically on startup. Check the logs for the `mcp-server` to ensure there are no errors related to the database migration. If the service is healthy, the migration has run successfully.

Your application is now fully deployed and operational.
