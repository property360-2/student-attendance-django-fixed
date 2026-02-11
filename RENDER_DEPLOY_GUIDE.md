# Deploying AttendLite to Render (Web Service)

This guide provides step-by-step instructions to host your Django application on **Render** using a **Persistent Disk** for the SQLite database.

---

## 🏗️ Pre-deployment Checklist
1. Your code is pushed to a GitHub or GitLab repository.
2. The `build.sh` file is in your root directory.
3. The `requirements.txt` file contains `gunicorn` and `whitenoise`.

---

## 🚀 Step 1: Create a Web Service
1. Log in to [dashboard.render.com](https://dashboard.render.com).
2. Click **New +** and select **Web Service**.
3. Connect your repository.
4. Fill in the basic details:
   - **Name:** `attendlite` (or your preferred name)
   - **Language:** `Python 3`
   - **Build Command:** `./build.sh`
   - **Start Command:** `gunicorn student_attendance.wsgi:application`

---

## 💾 Step 2: Configure Persistent Disk (Recommended)
*Render's filesystem is ephemeral. If you don't use a Disk, your database will be reset to empty on every restart/deploy.*

1. In your Web Service dashboard, go to the **Disk** tab.
2. Click **Add Disk**.
3. Set the following:
   - **Name:** `sqlite-data`
   - **Mount Path:** `/data`
   - **Size:** `1GB`
4. Click **Add Disk**.
5. **Alternatively:** If you really want the DB in the codebase and don't care about persistence across deploys, you can skip this step and remove `DATABASE_PATH` from environment variables.

---

## 🔑 Step 3: Set Environment Variables
1. Go to the **Environment** tab.
2. Add the following variables:
   - `PYTHON_VERSION`: `3.10.0` (or your preferred version)
   - `SECRET_KEY`: `(generate a random long string)`
   - `DEBUG`: `False`
   - `DATABASE_PATH`: `/data`  *(This tells Django to store the DB on the Persistent Disk)*
3. Click **Save Changes**.

---

## 🌐 Step 4: Finalize & Deploy
1. Go to the **Settings** tab.
2. Ensure the **Health Check Path** is set to `/` (optional but recommended).
3. Under **Build & Deploy**, ensure **Auto-Deploy** is `Yes`.
4. Render should automatically start the build process. Once finished, your site will be live at a URL like `https://attendlite.onrender.com`.

---

## 💡 Troubleshooting
- **Build Failure:** Check the logs. Ensure `build.sh` has executable permissions (`chmod +x build.sh` if committing from Linux/Mac).
- **Static Files Not Loading:** Ensure `whitenoise` is in `MIDDLEWARE` in `settings.py` (it is already configured in this project).
- **Database Errors:** Double check that `DATABASE_PATH` in Environment is exactly the same as the **Mount Path** you set in the Disk settings.
