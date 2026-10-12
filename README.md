# Pipeline Test App

Minimal FastAPI app used to validate the self-hosted GitHub Actions runner →
ACR → Azure Container Apps pipeline end to end.

## What it does

- `GET /`        → greeting + the deployed version (the commit SHA)
- `GET /health`  → `{"status": "healthy"}`

On each deploy the workflow sets `APP_VERSION` to the commit SHA, so you can
confirm a new revision actually went live by watching the version change.

## One-time setup

### 1. Repository variables

In this repo: **Settings → Secrets and variables → Actions → Variables tab →
New repository variable**. Add:

| Variable | Value |
|---|---|
| `ACR_NAME` | your Azure Container Registry name (no `.azurecr.io`) |
| `AZURE_RESOURCE_GROUP` | the resource group of the Container App |
| `CONTAINER_APP` | the existing Container App name |

No secrets are needed — the self-hosted runner's VM uses its attached
User-Assigned Managed Identity (`az login --identity`).

### 2. Confirm the runner is online

**Settings → Actions → Runners** should show the runner as **Idle** (green).

### 3. Confirm the VM can reach Azure + ACR

SSH to the runner VM and run:

```bash
az login --identity
az acr login --name <ACR_NAME>
```

`az acr login` must succeed — it proves the runner can reach the (private) ACR.

## Run the pipeline

- Push any change to `main`, **or**
- **Actions** tab → "Build and Deploy (self-hosted runner)" → **Run workflow**.

The job runs on your self-hosted runner and:
1. builds the image with `az acr build` (build happens in ACR),
2. pushes it to your registry,
3. updates the Container App to the new image,
4. prints the app URL at the end.

## Verify it worked

Open the URL printed in the final step, or:

```bash
curl https://<container-app-fqdn>/health
```

You should see `"status": "healthy"` and a `version` equal to the commit SHA
that was just deployed. Change the code, push again, and watch the version
change — that confirms the full CI/CD loop.

## Local test (optional)

```bash
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8080
curl http://localhost:8080/health
```
