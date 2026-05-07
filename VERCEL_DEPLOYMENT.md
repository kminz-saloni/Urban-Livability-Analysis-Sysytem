# Vercel Frontend Deployment Guide

## Environment Variables Setup

To connect the frontend to the Azure backend API, you must set environment variables in Vercel:

### Steps:

1. **Go to Vercel Dashboard**
   - Visit: https://vercel.com/dashboard

2. **Select Your Project**
   - Click on `Urban-Livability-Analysis-Sysytem`

3. **Navigate to Settings → Environment Variables**

4. **Add the following environment variables:**

   | Name | Value | Environments |
   |------|-------|--------------|
   | `NEXT_PUBLIC_API_URL` | `https://urban-backend.azurewebsites.net` | Production, Preview, Development |
   | `NEXT_PUBLIC_SUPABASE_URL` | `https://onwsdqfcisezshmvsmek.supabase.co` | All |
   | `NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY` | `sb_publishable_kVZRlrLgdC7AhiToVoRWGg_7_N2FxcU` | All |

5. **Save and Redeploy**
   - After saving, trigger a new deployment by pushing to the `main` branch or using the "Redeploy" button in Vercel

### Verification:

Once redeployed, check the browser console:
- ✅ API calls should go to `https://urban-backend.azurewebsites.net` instead of `localhost:8000`
- ✅ Map should render without glyph errors
- ✅ Rankings, analytics, and reports data should load from the backend

## Current Frontend URL

- **Production**: https://urban-livability-analysis-sysytem.vercel.app/

## Backend Status

- **API**: https://urban-backend.azurewebsites.net
- **Deployed via**: GitHub Actions + Azure App Service
