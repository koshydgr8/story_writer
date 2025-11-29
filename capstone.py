import asyncio
import json
import os
import types

from google.adk.runners import InMemoryRunner

from agents import chapter_elaborator_agent, story_pipeline_agent
from utils import get_chapters_from_events

GOOGLE_API_KEY=''
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY


def main():

    story_pipeline = story_pipeline_agent()

    chapter_elaborator = chapter_elaborator_agent()

    runner =InMemoryRunner(agent=story_pipeline)

    print("✅ Runner created.")

    response = asyncio.run(runner.run_debug("Can you write for me a children's story?"))

    print("The output is:")

    chapters = get_chapters_from_events(response)
    full_book = []
    for chapter in chapters:
        chapter_prompt = f"""
            CHAPTER JSON:
            {json.dumps(chapter, indent=2)}

            TASK:
            Write the full chapter based on title and summary.
            """

        response =  runner.run(
            user_id="book_user",
            session_id=f"chapter_{chapter['id']}",
            new_message=types.Content(
            role="user",
            parts=[types.Part(text=chapter_prompt)]
            )
        )

        full_book.append({
            "id": chapter["id"],
            "title": chapter["title"],
            "content": response.output_text
        })

    print("⏳ Elaborating chapters in parallel...")



if __name__ == "__main__":
    main()

def assemble_book(results):
    book = []

    for result in results:
        chapter_text = result.get("chapter_text")
        book.append(chapter_text)

    return "\n\n".join(book)

