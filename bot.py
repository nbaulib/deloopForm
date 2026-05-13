import os
import threading
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from forms import *

load_dotenv()

app = App(token=os.environ["SLACK_BOT_TOKEN"])


@app.event("app_mention")
def handle_mention(event, say):
    # remove the "@delooper"
    raw = event.get("text", "")
    if ">" in raw:
        raw = raw[raw.index(">") + 1 :].strip()

    # if blank
    if not raw:
        say(
            "You didn't send anything. Format as such:\n"
            "```\nemail\nname\nschool\ndate\n\nworkshop\nweek\nsummary\nissues\ninventory\n```"
        )
        return

    # submit_batch(raw, say)
    threading.Thread(target=submit_batch, args=(raw, say), daemon=True).start()


if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
