# Azure App Service Deployment (FastAPI Backend)

This guide deploys the backend to Azure App Service (Linux) and connects it to Supabase/Postgres.

## 1) Prerequisites

- Azure subscription + App Service plan
- Azure CLI installed
- Supabase Postgres connection string

## 2) Azure CLI login

```bash
az login
az account show
```

## 3) Create resources (if needed)

```bash
az group create --name urbanpulse-rg --location eastus

az appservice plan create \
  --name urbanpulse-plan \
  --resource-group urbanpulse-rg \
  --sku B1 \
  --is-linux

az webapp create \
  --resource-group urbanpulse-rg \
  --plan urbanpulse-plan \
  --name urbanpulse-backend \
  --runtime "PYTHON|3.11" \
  --deployment-local-git
```

## 4) Configure app settings

```bash
az webapp config appsettings set \
  --resource-group urbanpulse-rg \
  --name urbanpulse-backend \
  --settings \
  DATABASE_URL="<supabase-postgres-connection-string>" \
  CORS_ORIGINS="https://<your-frontend-domain>,http://localhost:3000" \
  ENVIRONMENT="production" \
  DEBUG="False"
```

## 5) Set startup command

```bash
az webapp config set \
  --resource-group urbanpulse-rg \
  --name urbanpulse-backend \
  --startup-file "./startup.sh"
```

## 6) Deploy via Git

```bash
cd backend

git init
az webapp deployment source config-local-git \
  --name urbanpulse-backend \
  --resource-group urbanpulse-rg

git remote add azure <deployment-git-url>

git add .
git commit -m "Deploy backend"

git push azure main
```

## 7) Verify

- API root: https://urbanpulse-backend.azurewebsites.net/
- Health check: https://urbanpulse-backend.azurewebsites.net/health

## 8) Frontend environment

Set the API base in the frontend:

```
NEXT_PUBLIC_API_URL=https://urbanpulse-backend.azurewebsites.net
```

---

## Notes

- Ensure `startup.sh` is executable. If needed:
  - `chmod +x backend/startup.sh`
- For Supabase, use the pooled connection string.
