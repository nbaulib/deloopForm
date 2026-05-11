# Deloop
Submitting multiple forms through Slack

### Problem Statement
Providing feedback after every class is is important but filling out multiple forms with similar information is tedious. The current process creates more friction and leads to rushed answers.

## Tech Stack
- Python
- Slack Bolt
- Selenium

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/nbaulib/deloopForm.git
cd deloopForm
```
### 2. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

Note:
If you have dependency or Pylance issues, make sure your IDE is opened with `deloopForm` as the root project folder and select the correct interpreter.

### 4. Create Slack App
Go to https://app.slack.com/ and make a new Slack App using this App Manifest (YAML)
```
display_information:
  name: Deloop
  description: Fill multiple forms through Slack
  background_color: "#271142"
features:
  bot_user:
    display_name: Deloop
    always_online: false
oauth_config:
  scopes:
    bot:
      - chat:write
      - incoming-webhook
      - channels:history
      - app_mentions:read
  pkce_enabled: false
settings:
  event_subscriptions:
    bot_events:
      - app_mention
  interactivity:
    is_enabled: true
  org_deploy_enabled: false
  socket_mode_enabled: true
  token_rotation_enabled: false
  is_mcp_enabled: false
```
Then invite deloop to the desired channels


### 5. Create `.env`

```env
SLACK_BOT_TOKEN=xoxb_your_bot_token
SLACK_APP_TOKEN=xapp_your_app_token
```

### 5. Run bot.py

```
python bot.py
```

## Usage

The bot listens for `@deloop` and parses the message into multiple form entries.

### Example Message

```text
@Deloop

email@example.com
First LastName
Cool School
today

Intro to 3D Modeling
week 2
Students used the union and subtract tools in TinkerCAD to design a skatepark.
none
none

Intro to Data Science
week 3
Students used seaborn to visualize NFL data.
no issues
no materials
```
## How It Works
1. User mentions the bot in Slack
2. The message is parsed into the correct format
3. Selenium opens parallel form sessions
4. Forms are filled automatically
5. Submission progress is posted back into Slack