import os
from google.adk.agents import Agent, SequentialAgent, ParallelAgent, LlmAgent
from google.adk.cli.built_in_agents.adk_agent_builder_assistant import root_agent
from google.adk.runners import InMemoryRunner, Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools import google_search
from google.genai import types
import asyncio

from agents import initial_idea_agent, story_chapter_agent, chapter_elaborator_agent, elaborate_chapters, \
    story_pipeline_agent
from utils import get_chapters_from_events

GOOGLE_API_KEY='AIzaSyBKUNz46YKNuD4XK4V9rr4bW6e5Hb9WmgQ'
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY


def main():

    story_pipeline = story_pipeline_agent()

    chapter_elaborator = chapter_elaborator_agent()

    story_writer = LlmAgent(
        model="gemini-2.0-flash",
        name="story_writer",
        description="You are a master story writer",
        instruction="""
        Based on the input prompt you will call the story_pipeline which give an outline with chapters. 
        You will use the chapters from the story_pipeline and call the chapter_elaborator tool and get detailed chapters. 
        Finally, you will compile all the outputs into a story book format as the output.
        """,
        tools=[story_pipeline, chapter_elaborator]  # Provide the function directly
    )


    runner =InMemoryRunner(agent=story_writer)

    print("✅ Runner created.")

    response = asyncio.run(
            runner.run_debug("Can you write for me a children's story?"))

    print("The output is:")
    #chapters = get_chapters_from_events(response)

    print("⏳ Elaborating chapters in parallel...")


if __name__ == "__main__":
    main()

def assemble_book(results):
    book = []

    for result in results:
        chapter_text = result.get("chapter_text")
        book.append(chapter_text)

    return "\n\n".join(book)

