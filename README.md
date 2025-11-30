# 📚 Story Forge: AI Storybook Generator  
### Freestyle Track Submission — Creative Multi-Agent System

---

## 🏆 Project Summary

This project implements a **fully autonomous multi-agent storytelling pipeline** using Google's Agent Development Kit (ADK) and Gemini models.

Rather than generating text from a single prompt, this system models a real creative workflow:

> An Idea Writer → A Story Architect → A Chapter Author → A Critic → An Emotional Editor

Each agent performs a specialized function, and the entire system operates as a **self-refining generative system**.

---

## 🎯 Freestyle Track Focus

This project was built under the **Freestyle Track** of the **Agents Intensive - Capstone Project**

---

###  Problem Statement 

Writing a complete, coherent book is not a single-step task. It requires:
- Ideation
- Structuring
- Expansion
- Refinement
- Quality control
- Final compilation

Most AI tools can write text, but they struggle to:
- Maintain structure across chapters
- Improve quality iteratively
- Recover from partial failures
- Separate planning from execution
- Provide control over the creative pipeline

This project solves that problem by building an agent-orchestrated AI book generator that plans, writes, critiques, improves, and compiles a full story.

The goal is not just to generate text — but to create a robust automated storytelling pipeline that behaves like a real publishing workflow.

---

### Why agents?

A single AI prompt cannot realistically do this:
- Architect a story
- Expand chapters
- Critique content
- Refine weak sections
- Manage failures
- Produce a structured book

Agents bring:

✅ Separation of Responsibilities : Each agent does ONE thing well.

✅ Iterative Improvement : The critic loop revises weak chapters instead of accepting bad output.

✅ Reliability : Retry logic and loops allow recovery from errors.

✅ Control over Creativity : Different agents = different mindsets.

✅ Scalability : More agents = better workflows, not bigger prompts.

This approach is closer to a human team of writers and editors than a chatbot.

---

### What you created

This system contains a multi-layer agent architecture, built using Google ADK.


*User Prompt*

   ↓

*StoryPipeline Agent*

   ├─ *InitialIdeaAgent (draft story)*

   └─ *StoryChapterAgent (split into chapters as JSON)*

   ↓

*ChapterElaborator (runs for each chapter)*

   ├─ *ChapterWriter (write chapter)*

   ├─ *CriticAgent (review)*

   └─ *EmotionWriter (refine) ← loop until approved*

   ↓

*StoryCompilerAgent(Currently not implemented)*

   └─ *Outputs finished book*


**🧩 Agents & Roles**

1️⃣ InitialIdeaAgent

Creates the rough story draft.

2️⃣ StoryChapterAgent

Turns draft into:


`
{
  "chapters": [
    { "id": 1, "title": "...", "summary": "..." }
  ]
}
`

3️⃣ChapterWriter

Expands each chapter into a full narrative.

4️⃣ CriticAgent

- Acts as editor 
- Reviews plot
- Detects missing emotion
- Judges completeness

5️⃣ EmotionWriter

Refines the chapter and improves depth.

6️⃣ LoopAgent

Repeats process until:


`
APPROVED
`


7️⃣ StoryCompilerAgent **(NOT IMPLEMENTED)**

Combines chapters into a book.

---

### Demo

Input:

`
"Write a children’s book for a 6-year-old about a brave squirrel who learns to share."

`

Output:

`
TITLE: The Brave Little Squirrel

Chapter 1: Squeaky’s Great Hoard
...
Chapter 2: The Sharing Forest
...

[Emotionally refined, logical progression, child-friendly tone]

`

---

### The Build -- How you created it, what tools or technologies you used.
- IDE: Pycharm
- ADK: Google ADK
- AI: Gemini 2.5 Lite
- Logging: Logging Pluging
- Runtime : Python

---

### If I had more time, this is what I'd do

1. Character Memory Agent : Persist character traits across stories.
2. Genre Agent : Change writing style by genre.
3. Visual Illustration Agent : Generate images per chapter.
4. Audio Narration Agent : Auto-generate audiobooks.
5. Quality Scoring Agent : Give each chapter a rating.
6. Reader Persona Agent : Rewrite based on age/reading level.
7. Publishing Mode : Export to: EPUB, PDF, Kindle, Website
8. Web Interface

Let users generate books with one click.

---

### ✅ SUMMARY

This is not a story generator.

This is a:
- ✅ publishing pipeline
- ✅ writing factory
- ✅ scalable agent system
- ✅ AI creative workflow
- ✅ fault-tolerant content engine

