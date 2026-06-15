# 🎓 The Socratic Spark: Independent AI Learning Assistant

> 🛠️ **Active Development / Work in Progress:** This project is actively being developed as part of an iterative learning cycle. The core architecture is live, and structural optimizations for advanced agent evaluation pipelines are currently underway. See the [Future Roadmap](#%EF%B8%8F-future-roadmap-work-in-progress) section below for upcoming releases.

The Socratic Spark is an autonomous, state-driven educational agent designed to guide students through complex concepts using pedagogical inquiry. Unlike standard QA chatbots that immediately provide answers, this agent utilizes behavioral engineering to break down topics into step-by-step learning milestones, evaluating student comprehension dynamically.

 **Live Application:** [Paste your Streamlit Cloud Link Here]

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
---

##  Future Roadmap (Work in Progress)

The Socratic Spark is an actively developing project. Upcoming optimization iterations include:
* **Pedagogical Evaluation Step:** Migrating from a single LLM generation call to an explicit **Evaluator-Optimizer pipeline** that grades user understanding before crafting the next question.
* **Granular State Variables:** Transitioning from an unstructured conversation history array to explicit state flags tracking specific metrics (e.g., `student_frustration_index`, `concept_mastery_score`).
* **UI/UX Refinements:** Enhancing the visual layout with dynamic progress bars to map a student's journey along a learning path.
