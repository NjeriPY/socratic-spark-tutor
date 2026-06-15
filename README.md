# 🎓 The Socratic Spark: Independent AI Learning Assistant

>![Status: Work in Progress](https://img.shields.io/badge/Status-Work%20in%20Progress-orange?style=flat-square&logo=github)
>![Stage: MVP v1.0](https://img.shields.io/badge/Stage-MVP%20v1.0-blue?style=flat-square)

> 🛠️ **Active Development / Work in Progress:** This project is actively being developed as part of an iterative learning cycle. The core architecture is live, and structural optimizations for advanced agent evaluation pipelines are currently underway.


The Socratic Spark is an autonomous, state-driven educational agent designed to guide students through complex concepts using pedagogical inquiry. Unlike standard QA chatbots that immediately provide answers, this agent utilizes behavioral engineering to break down topics into step-by-step learning milestones, evaluating student comprehension dynamically.

 **Live Application:** https://socratic-spark-tutor-9grkbykcvexlsfxdhbejut.streamlit.app/

---

##  Architecture & Core Engineering Patterns

This project was built to move past simple API wrappers and explore the complexities of state management, resilient backend execution boundaries, and targeted agentic tools.

### 1. State Machine Management (Streamlit Lifecycle Armor)
Streamlit executes scripts top-to-bottom on every user interaction, which inherently causes data wiping. This application mitigates state fragmentation by establishing a secure key-value store using `st.session_state`. Chat histories are maintained chronologically inside a persistent list of dictionaries (`{"role": "...", "content": "..."}`), preventing amnesia across execution turns.

### 2. Isolated Transaction Layer (Fault Tolerance)
To handle API instability or token latency spikes, the inference transaction with the upstream provider (Groq/Llama-3.3) is wrapped in a strict execution-safety boundary (`try/except`). State changes are committed *only* upon successful API response delivery, leaving the user data layer clean and allowing seamless user-driven retries if an interruption occurs.

### 3. Conditional Tool Execution (Contextual Grounding)
To prevent prompt inflation and excessive token consumption, the system integrates a single-turn tool execution hook. The web search client (Tavily AI) runs **only** during the initial lesson initialization step ($len(\text{messages}) == 2$) to fetch real-time semantic grounding data, which is locked into memory for all subsequent chat iterations.

---

## Tech Stack

* **Language:** Python 3.13
* **Frontend/Interface:** Streamlit
* **Inference Engine:** Groq Cloud (Llama-3.3-70b-versatile)
* **Search Engine Tool:** Tavily AI Client
* **Environment Management:** Python-dotenv (OS-decoupled key architecture)

---
