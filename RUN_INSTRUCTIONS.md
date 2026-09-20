# How to Run AI Project Manager

## If "This site can't be reached" or ERR_CONNECTION_REFUSED

The app needs **two servers** running: Backend and Frontend. If either isn't running, the site won't load.

---

## Method 1: Double-click start.bat

1. Open the folder: `project_manager`
2. Double-click **start.bat**
3. **Two black command windows** will open (Backend and Frontend)
4. **Do not close them.** Leave both open.
5. Wait until you see:
   - In one window: `Uvicorn running on http://127.0.0.1:8000`
   - In the other: `Local: http://localhost:3000/`
6. Open your browser and go to: **http://127.0.0.1:3000**

If you see errors in either window (e.g. "python is not recognized" or "npm is not recognized"), use Method 2.

---

## Method 2: Run manually (recommended if start.bat fails)

### Step 1: Open a terminal (Command Prompt or PowerShell)

- In Cursor: **Terminal → New Terminal**
- Or press **Ctrl+`** (backtick)

### Step 2: Start the Backend

In the terminal, run:

```cmd
cd c:\Users\ADMIN\Desktop\project_manager\backend
python -m uvicorn app.main:app --reload --port 8000
```

Leave this running. You should see: **Uvicorn running on http://127.0.0.1:8000**

### Step 3: Open a second terminal

- **Terminal → New Terminal** (or split the terminal)

### Step 4: Start the Frontend

In the **new** terminal, run:

```cmd
cd c:\Users\ADMIN\Desktop\project_manager\frontend
npm run dev
```

Leave this running. You should see: **Local: http://localhost:3000/**

### Step 5: Open the site

In your browser go to: **http://127.0.0.1:3000** or **http://localhost:3000**

---

## Checklist if it still doesn’t work

- [ ] **Both** Backend and Frontend terminals are open and running (no errors).
- [ ] You waited at least 10–15 seconds after starting before opening the browser.
- [ ] You’re opening **http://127.0.0.1:3000** (with **:3000**), not just `localhost`.
- [ ] Python is installed: run `python --version` in a terminal.
- [ ] Node.js is installed: run `node --version` and `npm --version` in a terminal.
- [ ] Dependencies are installed:
  - Backend: `cd backend` then `pip install -r requirements.txt`
  - Frontend: `cd frontend` then `npm install`

---

## Ports used

| Service  | URL                     | Port |
|----------|-------------------------|------|
| Frontend | http://127.0.0.1:3000   | 3000 |
| Backend  | http://127.0.0.1:8000   | 8000 |
| API docs | http://127.0.0.1:8000/docs | 8000 |
