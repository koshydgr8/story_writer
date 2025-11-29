# 📚 Autonomous AI Storybook Generator  
### Freestyle Track Submission — Creative Multi-Agent System

---

## 🏆 Project Summary

This project implements a **fully autonomous multi-agent storytelling pipeline** using Google's Agent Development Kit (ADK) and Gemini models.

Rather than generating text from a single prompt, this system models a real creative workflow:

> An Idea Writer → A Story Architect → A Chapter Author → A Critic → An Emotional Editor

Each agent performs a specialized function, and the entire system operates as a **self-refining generative system**.

---

## 🎯 Freestyle Track Focus

This project was built under the **Freestyle Track** — designed for participants to experiment freely and build original AI systems.

The system demonstrates:
- Autonomous generation
- Loop-based self-improvement
- Narrative quality evaluation
- Emotion-aware rewriting
- Session-based state control
- Agent orchestration patterns

---

## 🧩 Architecture

### Agent Pipeline

> User Prompt 
-> InitialIdeaAgent (Draft Writer)
-> StoryChapterAgent (Story Architect)
-> ChapterWriter
-> CriticAgent
-> EmotionWriter
↺ Loop until APPROVED

---

## 🧠 Intelligence & Autonomy

### Self-Revision Loop

The story is automatically reviewed by an internal critic.

- If "APPROVED" → pipeline advances  
- Otherwise → chapter is rewritten  
- Loop ends only when quality is acceptable  

This introduces:
✅ Judgment  
✅ Iteration  
✅ Reasoning  
✅ Self-correction  

---

## 🧬 Session Isolation

Each chapter runs inside its own memory context:

```python
await session_service.create_session(
    app_name="agents",
    user_id="book_user",
    session_id="chapter_1"
)

```

This ensures:

No data leakage between chapters
Clean model behavior
Repeatable output

🚀 How to Run
1. Install dependencies

```
pip install google-adk google-generativeai
```

