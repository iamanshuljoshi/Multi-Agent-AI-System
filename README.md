# 🤖 Multi-Agent AI Research System

A Multi-Agent AI system built using **LangChain**, **Mistral AI**, **LCEL (LangChain Expression Language)**, **Runnables**, and **Tool Calling**.

The system uses multiple AI agents to collaboratively research a topic, analyze information, generate a report, and review the final output.

---

# 🚀 Features

- Multi-Agent Architecture
- Mistral AI Integration
- LangChain Agents
- LCEL (LangChain Expression Language)
- Runnable Chains
- Tavily Web Search Tool
- BeautifulSoup Web Scraping
- AI Research Pipeline
- Report Generation
- Critic Agent for Report Review
- Modular Project Structure

---

# 🛠 Tech Stack

- Python
- LangChain
- LangChain Core
- Mistral AI
- LCEL
- RunnableSequence
- RunnableLambda
- Prompt Templates
- Tavily Search API
- BeautifulSoup
- Requests
- Python Dotenv

---

# 📂 Project Structure

```
Multi-Agent-System/
│
├── app.py                  # Main application
├── agents.py               # AI Agents
├── tools.py                # Custom Tools
├── pipeline.py             # Research Pipeline
├── requirements.txt
├── .env
└── README.md
```

---

# 🧠 System Architecture

```
                    User
                      │
                      ▼
             Research Pipeline
                      │
        ┌─────────────┴─────────────┐
        ▼                           ▼
 Search Agent                 Writer Agent
        │                           │
        ▼                           ▼
 Tavily Search Tool          Report Generation
        │
        ▼
 BeautifulSoup Tool
        │
        ▼
     Research Data
              │
              ▼
        Critic Agent
              │
              ▼
        Final Feedback
```

---

# ⚙️ Workflow

### Step 1

User enters a research topic.

Example

```
Impact of AI on Healthcare
```

---

### Step 2

Search Agent starts working.

It calls

- Tavily Search API
- BeautifulSoup

to gather reliable information.

---

### Step 3

Collected information is passed to the Writer Agent.

Writer Agent creates

- Summary
- Report
- Analysis

---

### Step 4

The report is sent to the Critic Agent.

Critic Agent reviews

- Accuracy
- Clarity
- Missing Information
- Improvements

---

### Step 5

Final report and feedback are returned to the user.

---

# 🛠 Tools Used

## 1️⃣ Tavily Search

Purpose

- Search latest information
- Reliable sources
- Research articles

Example

```
Latest AI jobs in India
```

---

## 2️⃣ BeautifulSoup

Purpose

- Scrape web pages
- Extract article text
- Parse HTML

Example

```
Website

↓

HTML

↓

BeautifulSoup

↓

Text
```

---

# 🤖 AI Agents

## Search Agent

Responsibilities

- Search the web
- Gather information
- Return research data

---

## Writer Agent

Responsibilities

- Read research
- Write structured report
- Summarize information

---

## Critic Agent

Responsibilities

- Review report
- Suggest improvements
- Find missing points

---

# 🧩 LangChain Concepts Used

## Prompt Templates

Creates reusable prompts.

Example

```python
prompt = ChatPromptTemplate.from_template(...)
```

---

## LCEL

LangChain Expression Language

Allows chaining components using

```
|
```

Example

```python
prompt | llm | parser
```

---

## Runnable

Everything in LangChain is a Runnable.

Examples

- Prompt
- LLM
- Output Parser
- Chain

Methods

```python
invoke()

batch()

stream()

ainvoke()
```

---

## Chain

A sequence of runnables.

Example

```
Prompt

↓

LLM

↓

Parser
```

---

# 📦 Installation

Clone repository

```bash
git clone https://github.com/yourusername/Multi-Agent-System.git
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create

```
.env
```

Add

```env
MISTRAL_API_KEY=YOUR_API_KEY

TAVILY_API_KEY=YOUR_API_KEY
```

---

# ▶️ Run

```bash
python app.py
```

---

# Example

Input

```
Impact of War on Stock Market
```

Output

```
Search Agent

↓

Writer Agent

↓

Critic Agent

↓

Final Report
```

---

# 📚 Concepts Learned

- LangChain
- Multi-Agent Systems
- Prompt Engineering
- LCEL
- Runnable
- Chains
- Tool Calling
- Tavily Search
- BeautifulSoup
- Web Scraping
- API Integration
- Mistral AI
- Python

---

# 🎯 Future Improvements

- LangGraph
- Memory
- PDF Export
- Streamlit UI
- Docker
- Deployment
- Conversation History
- Vector Database Integration
- RAG Support

---

# 👨‍💻 Author

Anshul Joshi

B.Tech Computer Science and Business Systems

Passionate about Generative AI, AI Agents, Backend Development, and Full-Stack AI Applications.
