# DebateMate — AI Debate Coach
### Build Document & Project Specification

---

## What Is DebateMate?

DebateMate is an AI-powered debate training application where a user argues any topic against an intelligent AI opponent. The AI counters every argument in real time, scores the user's performance using NLP, and gives a full breakdown report at the end. Built for students preparing for placement GDs, debate competitions, or anyone who wants to think sharper.

---

## The Problem It Solves

Debating requires practice. But practice requires a partner. Most students never practice because:
- You need another person
- That person needs to know the topic
- They need to argue back intelligently
- They need to give feedback

DebateMate replaces all of that. Available 24/7, infinitely patient, brutally challenging.

---

## Core Features

### 1. Topic Selection
- User picks from 3 modes:
  - **Choose from list** — 50+ preloaded topics across Tech, Education, Society, Politics, Business
  - **Random topic** — AI picks a surprise topic
  - **Custom topic** — User types any topic they want
- User picks their **stance** — For or Against
- AI automatically takes the opposite stance

### 2. Live Debate
- User types their argument
- AI responds immediately with a sharp counter-argument
- Conversation continues for up to 10 rounds
- AI never repeats itself — each counter is unique and builds on previous points
- AI has a **difficulty setting**:
  - **Beginner** — AI argues gently, gives room to breathe
  - **Intermediate** — AI is firm and logical
  - **Expert** — AI is aggressive, uses data, cuts every weak point

### 3. Real-Time Argument Scoring (HuggingFace)
Each user argument is scored live across 3 parameters:
- **Clarity** — Is the point clear and understandable?
- **Relevance** — Is it actually on topic?
- **Logical Strength** — Is it well-reasoned or just an opinion?

Score shown as a mini badge after each argument (e.g. 7.2/10)

### 4. End-of-Debate Report
After the debate ends, user gets a full performance card:
- Overall debate score (out of 100)
- Breakdown of Clarity / Relevance / Logic across all rounds
- Best argument of the session (highlighted)
- Weakest argument (with suggestion on how to improve it)
- AI verdict: "Who won the debate and why"
- Personalized tip: one specific thing to work on

### 5. Transcript Download
- Full debate saved as a clean .txt file
- Includes timestamps, scores per round, and final report
- User can study it later or show it to someone

### 6. Topic Bank
50+ debate topics organized by category:
- Technology (AI replacing jobs, social media bans, screen time limits)
- Education (online vs offline, exams vs projects, uniforms)
- Society (feminism, reservation, age of voting)
- Business (startups vs jobs, remote work, gig economy)
- Environment (electric vehicles, plastic ban, nuclear energy)

---

## Tech Stack

| Layer | Technology | Why |
|---|---|---|
| Language | Python 3.14 | Core logic |
| UI Framework | Streamlit | Fast to build, looks clean |
| AI Responses | OpenAI API (GPT-4o) | Powers AI debate opponent |
| Conversation Memory | LangChain ConversationBufferMemory | AI remembers all previous arguments |
| Argument Scoring | HuggingFace (cardiffnlp/twitter-roberta-base-sentiment) | NLP-based scoring |
| Environment Variables | python-dotenv | Keeps API key safe |
| Data Handling | Pandas | Stores scores per round |
| Visualization | Matplotlib / Plotly | Score chart in final report |
| File Export | Python built-in | Transcript .txt download |
| Styling | Custom Streamlit CSS | Neo-brutalist UI theme |

---

## UI Design — Neo Brutalism

### What Is Neo Brutalism?
Raw, bold, unapologetic design. Heavy black borders. Flat colors. Bold typography. No gradients. No soft shadows — only hard offset box shadows. Everything looks like it was designed to make a statement.

### Color Palette
- Background: `#FFFBE6` (cream/off-white)
- Primary: `#000000` (black — borders, text)
- Accent 1: `#FF3F3F` (red — AI arguments, danger)
- Accent 2: `#3BFF6E` (green — user arguments, success)
- Accent 3: `#FFD600` (yellow — scores, highlights)
- Card Background: `#FFFFFF`

### Typography
- Headings: **Space Grotesk Bold** or **Syne ExtraBold**
- Body: **IBM Plex Mono** (gives a terminal/raw feel)

### UI Components
- All cards have: `border: 3px solid black`, `box-shadow: 4px 4px 0px black`
- Buttons are flat with hard shadow — shift on hover
- User chat bubble: green left border, cream background
- AI chat bubble: red left border, white background
- Score badge: yellow pill with black border
- No rounded corners anywhere — everything is sharp rectangle

### Pages / Screens

**Screen 1 — Home / Setup**
- Big bold title: "DEBATEMATE" in massive black font
- Subtitle: "argue better. think sharper."
- Topic selector (dropdown + random button + text input)
- Stance picker (two big toggle buttons: FOR / AGAINST)
- Difficulty selector (3 buttons: BEGINNER / INTERMEDIATE / EXPERT)
- Big black "START DEBATE" button

**Screen 2 — Debate Arena**
- Top bar: Topic name | Round counter (Round 3/10) | Timer
- Left column: Debate chat (alternating user/AI bubbles)
- Right column: Live score tracker (bar chart updating each round)
- Bottom: Text input box + "ARGUE" button
- "END DEBATE" button (triggers final report)

**Screen 3 — Report Card**
- Big "DEBATE REPORT" header
- Score ring or bar: Overall score out of 100
- 3 metric bars: Clarity / Relevance / Logic
- Best argument highlighted in green box
- Weakest argument in red box with suggestion
- AI verdict in a yellow bordered box
- Download transcript button
- "DEBATE AGAIN" button back to home

---

## File Structure

```
debatemate/
│
├── app.py              ← Main Streamlit app (all screens)
├── ai_opponent.py      ← LangChain + OpenAI debate logic
├── scorer.py           ← HuggingFace argument scoring
├── topics.py           ← Topic bank (50+ topics)
├── report.py           ← End report generation
├── .env                ← API key (never share this)
├── requirements.txt    ← All dependencies
└── README.md           ← Project documentation
```

---

## Build Order (Step by Step)

### Week 1
- Day 1-2: Set up project, get OpenAI API key, build basic chat in Streamlit
- Day 3-4: Add LangChain memory so AI remembers previous arguments
- Day 5-6: Add HuggingFace scoring on each user argument
- Day 7: Connect everything — topic selection → debate → scoring working end to end

### Week 2
- Day 8-9: Build the final report screen
- Day 10: Add transcript download
- Day 11: Apply full neo-brutalist CSS styling
- Day 12: Add topic bank + difficulty levels
- Day 13: Test everything, fix bugs
- Day 14: Deploy on Streamlit Cloud, write README, push to GitHub

---

## What You Can Say in Your Interview

> "DebateMate is an AI debate coach I built using Python, LangChain, and OpenAI API. The user argues any topic and the AI counters in real time using LangChain's conversation memory so it never repeats itself and always builds on previous points. I also integrated HuggingFace NLP models to score each argument across clarity, relevance, and logical strength, and generate a full performance report at the end. I built the UI in Streamlit with a custom neo-brutalist design."

That answer covers: Python ✅ LangChain ✅ OpenAI ✅ HuggingFace ✅ NLP ✅ Streamlit ✅

---

## Requirements.txt

```
streamlit
openai
langchain
langchain-openai
python-dotenv
transformers
torch
pandas
plotly
```

---

## Resume Bullets (Final Version)

```
DebateMate — AI Debate Coach | Python, OpenAI API, LangChain, HuggingFace, Streamlit

• Built an AI debate simulator where users argue any topic against an intelligent AI 
  opponent that counters arguments in real time using LangChain ConversationBufferMemory 
  and OpenAI GPT-4o, maintaining full context across 10 debate rounds

• Implemented real-time argument scoring using HuggingFace transformer models evaluating 
  each user argument across clarity, relevance and logical strength with a personalized 
  end-of-session performance report

• Designed neo-brutalist UI in Streamlit with live score visualization using Plotly, 
  topic bank of 50+ debate topics across 5 categories, and full transcript export
```

---

*Built by Vaishnavi Dubey | B.Tech CSE, PTU 2027*