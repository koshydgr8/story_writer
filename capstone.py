import asyncio
import json
import os


from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from agents import chapter_elaborator_agent, story_pipeline_agent
from utils import get_chapters_from_events

#Set this for Windows
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

GOOGLE_API_KEY=''
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY


async def main():

    print("Starting all pipelines...")

    #Initializing agents
    story_pipeline = story_pipeline_agent()
    chapter_elaborator = chapter_elaborator_agent()

    #sessions
    session_service = InMemorySessionService()
    await session_service.create_session(app_name="agents", user_id="book_user", session_id="outline")

    #Creating the Runners for the two Agents
    runner_sp = Runner(agent=story_pipeline, app_name="agents", session_service= session_service)
    runner_ce = Runner(agent=chapter_elaborator, app_name="agents", session_service = session_service)

    print("✅ Runners created.")

    #Generate the chapter outlines
    story_pipeline_res = runner_sp.run(user_id="book_user", session_id="outline", new_message=
                    types.Content(
                        role="user",
                        parts=[types.Part(text="Can you write a children's story")],
                    )
                  )

    print(f"The output is: {story_pipeline_res}")

    chapters = get_chapters_from_events(story_pipeline_res)

    #Create sessions for each chapter
    for chapter in chapters:
        print(f"A chapter is {chapter}")
        await session_service.create_session(app_name="agents", user_id="book_user", session_id=f"chapter_{chapter['id']}")

    #Elaborate Chapters

    full_book = []

    for chapter in chapters:
        chapter_prompt = f"""
            CHAPTER JSON:
            {json.dumps(chapter, indent=2)}
            TASK:
            Use the chapter json and elaborate only this chapter. It's part of a larger story
            """

        response_events =  runner_ce.run(
            user_id="book_user",
            session_id=f"chapter_{chapter['id']}",
            new_message=types.Content(
                role="user",
                parts=[types.Part(text=chapter_prompt)]
            )
        )

        chapter_text = ""

        for event in response_events:
            if event.is_final_response() and event.content:
                collected = ""
                if event.content.parts:
                    for part in event.content.parts:
                        if hasattr(part, "text"):
                            collected += part.text
                    if collected.strip():
                        chapter_text += collected.strip()

        full_book.append({
            "id": chapter["id"],
            "title": chapter["title"],
            "content": chapter_text
        })

        print("✅ Book generation completed.")

    for ch in full_book:
        print(f"\n\n📖 {ch['title']}\n")
        print(ch["content"])


if __name__ == "__main__":
    asyncio.run(main())

def assemble_book(results):
    book = []

    for result in results:
        chapter_text = result.get("chapter_text")
        book.append(chapter_text)

    return "\n\n".join(book)

