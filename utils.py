import json
import re


def get_chapters_from_events(events):
    for event in events:
        if event.author == "StoryChapterAgent":
            raw = event.actions.state_delta["chapters"]

            # remove markdown
            clean = re.sub(r"```json|```", "", raw).strip()

            # parse JSON
            parsed = json.loads(clean)

            return parsed["chapters"]

    raise ValueError("StoryChapterAgent did not produce chapters.")
