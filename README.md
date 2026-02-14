# 💖 Will You Be My Valentine? (Streamlit)

Run locally:

```bash
cd valentine-streamlit
pip install -r requirements.txt
streamlit run streamlit_app.py
```

Open **http://localhost:8501**  
Personalized: **http://localhost:8501/?name=Yash**

---

- **Hero** → "Click Here 💌" → **Journey** (4 sections) → **Continue** → **Proposal**
- **YES** → celebration (confetti + balloons + message)
- **NO** → button moves to another column each time; funny messages; disappears after 5 clicks

Edit `LOVE_MESSAGE` and `NO_MESSAGES` in `streamlit_app.py` to customize.
