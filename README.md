# 📅 Outlook Meeting AI Agent

An advanced, modular, and production-ready GenAI assistant built using **LangGraph**, **LangChain**, and **FastAPI**, designed to help professionals manage missed Outlook meetings by analyzing minutes and transcripts to provide actionable insights.

---

## 🚀 Features

- ✅ Load and analyze missed Outlook calendar meetings
- ✅ Intelligent summarization of MoMs or transcripts
- ✅ Recommends tasks, follow-ups, or status updates
- ✅ Fully modular OOP architecture
- ✅ Interactive chatbot UI using FastAPI + HTML/CSS
- ✅ Outlook-themed design with automatic browser launch
- ✅ In-memory session handling via LangGraph’s `MemorySaver`

---

## 🧠 Tech Stack

| Layer        | Technology                          |
|--------------|--------------------------------------|
| LLM Engine   | OpenAI (gpt-4o via LangChain)        |
| Workflow     | LangGraph                           |
| Memory       | LangGraph `MemorySaver`             |
| Backend      | FastAPI                             |
| UI           | HTML, CSS (with Outlook branding)    |
| Session Mgmt | UUID-based thread management        |

---

## 🗂️ Updated Project Structure

```
INFY_HACKATHON/
├── Agent/                      # LangGraph-based agent definition
│   └── agentic_wrkflw.py       # Workflow logic class (LangGraph)
├── config/                     # Configurations (if needed)
├── data/                       # Data files like meeting CSV
├── data_models/                # TypedDicts or Pydantic schemas
├── exception/                  # Custom exceptions (if implemented)
├── loggings/                   # Logging utilities
├── notebooks/                  # Experiment notebooks
├── PPTs/                       # Hackathon presentation assets
├── prompts/                    # Prompt templates
├── static/                     # CSS, images
│   └── outlook-bg.jpg
├── templates/                  # HTML UI
│   └── chat.html
├── toolkit/                    # Custom tools or utilities
├── utils/                      # Helper functions
├── main.py                     # FastAPI entrypoint
├── outlook_ai_agent.eg...      # VS Code environment settings (safe to ignore)
├── requirements.txt            # Python dependencies
├── setup.py                    # Setup script for packaging (optional)
├── README.md                   # Project documentation (you are here!)
└── .env                        # API keys and environment secrets
```

---

## ⚙️ How to Run

### 1. 📦 Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. 🔑 Add OpenAI API Key in `.env`

```
OPENAI_API_KEY=your-openai-api-key
```

### 3. 🚀 Start the Application

```bash
uvicorn main:app --reload
```

✨ This auto-launches a browser tab at `http://127.0.0.1:8000`

---

## 🧠 How It Works

1. User enters the chat and requests to analyze missed meetings.
2. The agent loads meetings from a structured CSV file.
3. Each meeting is processed:
   - If `MoM` exists → used for summarization.
   - Else, fallback to transcript content.
4. GPT-4o generates concise summaries and recommended actions.
5. Responses are delivered through a clean, browser-based UI.

---

## 💡 Screenshots

![alt text](C:\Users\Yaseen Khan\Documents\Data Sceince\Hackathon\Infy_Hackathon\data\sample_chatbot.png)

---

## 🔮 Future Enhancements

- 🔗 Microsoft Graph API integration for real Outlook sync
- 💾 Persistent memory using Redis
- 🔒 User authentication for per-user history
- 🧠 Feedback loop for continual learning

---

## 👨‍💻 Developed By

**Yaseen Khan** — GenAI Enthusiast | ULTRON 
_Infy Hackathon 2025 Participant_

---

## 📄 License

This is a proprietary internal project. Contact the author for permissions or collaboration opportunities.