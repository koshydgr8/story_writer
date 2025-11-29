import asyncio
import json

from google.adk.agents import Agent, LoopAgent, SequentialAgent, LlmAgent
from google.adk.runners import InMemoryRunner
from google.adk.tools import google_search
from google.adk.models.google_llm import Gemini
from google.genai import types

retry_config=types.HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    exp_base=7,  # Delay multiplier
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504], # Retry on these HTTP errors
)

def initial_idea_agent():
    initial_idea = Agent(
        name="InitialIdeaAgent",
        model=Gemini(
            model="gemini-2.5-flash-lite",
            retry_options=retry_config
        ),
        instruction="""Based on the user's prompt, write the first draft of a short story (around 100-150 words).
        Output only the story text, with no introduction or explanation.""",
        output_key="story_idea",
    )

    print("✅ initial_writer_agent created.")

    return initial_idea

def story_chapter_agent():
    story_chapter = Agent(
        name="StoryChapterAgent",
        model=Gemini(
            model="gemini-2.5-flash-lite",
            retry_options=retry_config
        ),
        instruction="""
        You are a story architect.
        
        INPUT:
        Idea = {story_idea}
        
        TASK:
        Break this story into exactly 2 chapters.
        
        OUTPUT FORMAT (IMPORTANT):
        Return ONLY valid JSON in this exact format:
        {
          "chapters": [
            {"id": 1, "title": "...", "summary": "..."},
            {"id": 2, "title": "...", "summary": "..."}
          ]
        }
        
        No markdown.
        No explanation.
        Only JSON.
        """,
        output_key="chapters"
    )

    print("✅ chapter_agent created.")

    return story_chapter

def story_pipeline_agent():
    story_pipeline = SequentialAgent(
        name="StoryPipeline",
        sub_agents=[initial_idea_agent(), story_chapter_agent()]
    )

    print("Story pipeline agent created")

    return story_pipeline

def chapter_elaborator_agent():
    chapter_writer = Agent(
        name="ChapterWriter",
        model=Gemini(model="gemini-2.5-flash-lite",
            retry_options=retry_config),
        instruction="""
        You are elaborating the chapters of a book.

        INPUT:
        CHAPTER JSON will be provided by the user.
        
        TASK:
        Write the full chapter based on title and summary.
        
        OUTPUT:
        Return the chapter as plain text.
        """,
        output_key="chapter_text"
    )

    critic_agent = Agent(
        name="CriticAgent",
        model=Gemini(
            model="gemini-2.5-flash-lite",
            retry_options=retry_config
        ),
        instruction="""You are a constructive story critic. Review the chapter of a story provided below.
        Story: {chapter_text}

        Evaluate the chapters plot, characters, and pacing.
        - If the story is well-written and complete, you MUST respond with the exact phrase: "APPROVED"
        - Otherwise, provide 2-3 specific, actionable suggestions for improvement.""",
        output_key="critique",  # Stores the feedback in the state.
    )

    print("✅ critic_agent created.")

    # This is the function that the RefinerAgent will call to exit the loop.
    def exit_loop():
        """Call this function ONLY when the critique is 'APPROVED', indicating the story is finished and no more changes are needed."""
        return {"status": "approved", "message": "Story approved. Exiting refinement loop."}

    print("✅ exit_loop function created.")

    emotion_writer = Agent(
        name="EmotionWriter",
        model=Gemini(model="gemini-2.5-flash-lite"),
        instruction="""
        You are taking the chapter of a book and checking for it's emotion, based on feedback from critique.
        INPUT:
        Chapter = {chapter_text}
        Critic = {critique}

        TASK:
        Analyze the critique.
        - IF the critique is EXACTLY "APPROVED", you MUST call the `exit_loop` function and nothing else.
        - OTHERWISE, Write the chapter incorporating the critique's suggestion and emotions that can help the user connect with the story

        OUTPUT RULE:
        Return ONLY the chapter text.
        NO commentary.
        NO explanation.
        NO markdown.
        NO headers.
        NO notes.
        """,
        output_key="chapter_text",
        tools=[exit_loop]
    )

    story_refinement_loop = LoopAgent(
        name="StoryRefinementLoop",
        sub_agents=[critic_agent, emotion_writer],
        max_iterations=2,  # Prevents infinite loops
    )

    chapter_elaborator = SequentialAgent(
        name="ChapterElaborator",
        sub_agents=[chapter_writer, story_refinement_loop]
    )

    print("Chapter Elaborator created.")

    return chapter_elaborator