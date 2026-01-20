Streamlit quick-start for this project

Goal: start the app when you need it, view in browser, then stop it when you're done.

Quick manual (recommended for beginners)

1) Open PowerShell in the project root (where `app.py` is).
2) Activate the virtual environment:

```powershell
. .\venv\Scripts\Activate.ps1
```

3) Start the app (foreground, development):

```powershell
.\venv\Scripts\streamlit.exe run app.py --server.headless true
```

Leave that terminal open while demoing. Stop with Ctrl+C.

Easy background start/stop (scripts included)

To start the app in the background and free your terminal, run:

```powershell
.\start_streamlit.ps1
```

This starts Streamlit (headless) and writes a `streamlit.pid` file containing the process id.

Open in your browser:

http://localhost:8501

When you're finished, stop it with:

```powershell
.\stop_streamlit.ps1
```

Alternative: Run at login

If you want the app to start automatically when you log in, consider creating a Scheduled Task (Windows). This is useful if you want the app to be available without manually starting it, but it's more permanent and runs whenever you sign in.

Public demos (interview)

- Streamlit Cloud: push this repo to GitHub and deploy via share.streamlit.io for a persistent public URL.
- ngrok: run the app locally and use `ngrok http 8501` to create a temporary public URL for an interview. Stop ngrok when done.

Security and notes

- Don't expose sensitive credentials in this repo.
- If you need LAN access, ensure Windows Firewall allows inbound connections on the port.
- The helper scripts assume the venv is at `./venv` and `app.py` is at the project root.

If you want, I can:
- Create a `requirements.txt` from your venv. 
- Create a Scheduled Task to start the app at logon.
- Help deploy to Streamlit Cloud or prepare an ngrok demo script.
