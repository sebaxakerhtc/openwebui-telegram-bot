<div align="center">
  <br>
  <h1>🌏 Openwebui Telegram Bot 🦙</h1>
  <p>
    <b>Chat with your LLM and generate images, using Telegram bot!</b><br>
    <b>Feel free to contribute!</b><br>
  </p>
  <br>
</div>

## Features
Here's features that you get out of the box:

- [x] Fully dockerized bot
- [x] Response streaming without ratelimit with **SentenceBySentence** method
- [x] Mention [@] bot in group to receive answer
- [x] Generate image using `/image description`
- [x] Use models from OpenWebUI

## Roadmap
- [x] Docker config & automated tags by [StanleyOneG](https://github.com/StanleyOneG), [ShrirajHegde](https://github.com/ShrirajHegde)
- [x] History and `/reset` by [ShrirajHegde](https://github.com/ShrirajHegde)
- [ ] Add more API-related functions [System Prompt Editor, RAG, Voice, etc.]

## Prerequisites
- [Telegram-Bot Token](https://core.telegram.org/bots#6-botfather)

## Installation (Non-Docker)
+ Install latest [Python](https://python.org/downloads)
+ Clone Repository
    ```
    git clone https://github.com/sebaxakerhtc/openwebui-telegram-bot
    ```
+ Install requirements from requirements.txt
    ```
    pip install -r requirements.txt
    ```
+ Enter all values in .env.example

+ Rename .env.example -> .env

+ Launch bot

    ```
    python3 run.py
    ```

## Installation (Build your own Docker image)
+ Clone Repository
    ```
    git clone https://github.com/sebaxakerhtc/openwebui-telegram-bot
    ```

+ Enter all values in .env.example

+ Rename .env.example -> .env

+ Run ONE of the following docker compose commands to start:
    1. To run ollama in docker container (optionally: uncomment GPU part of docker-compose.yml file to enable Nvidia GPU)
        ```
        docker compose up --build -d
        ```

    2. To run ollama from locally installed instance (mainly for **MacOS**, since docker image doesn't support Apple GPU acceleration yet):
        ```
        docker compose up --build -d openwebui-tg
        ```

## Environment Configuration
|          Parameter          |                                                      Description                                                      | Required? |  Default Value  |                        Example                        |
|:---------------------------:|:---------------------------------------------------------------------------------------------------------------------:|:---------:|:---------------:|:-----------------------------------------------------:|
|           `TOKEN`           | Your **Telegram bot token**.<br/>[[How to get token?]](https://core.telegram.org/bots/tutorial#obtain-your-bot-token) |    Yes    |   `yourtoken`   |             MTA0M****.GY5L5F.****g*****5k             |
|        `WEBUI_TOKEN`        |                                               from your webui interface                                               |    Yes    |   `yourtoken`   |               sk-23nb536vynmbv534nmb345               |
|         `ADMIN_IDS`         |                     Telegram user IDs of admins.<br/>These can change model and control the bot.                      |    Yes    |                 | 1234567890<br/>**OR**<br/>1234567890,0987654321, etc. |
|         `USER_IDS`          |                       Telegram user IDs of regular users.<br/>These only can chat with the bot.                       |    Yes    |                 | 1234567890<br/>**OR**<br/>1234567890,0987654321, etc. |
|         `INITMODEL`         |                                                      Default LLM                                                      |    No     |`llama3.1:latest`|        mistral:latest<br/>mistral:7b-instruct         |
|      `WEBUI_BASE_URL`       |                                                  Your OpenWebUI URL                                                   |    No     |                 |          localhost<br/>host.docker.internal           |
|        `WEBUI_PORT`         |                                                  Your OpenWebUI port                                                  |    No     |      3000       |                                                       |
|          `TIMEOUT`          |                                    The timeout in seconds for generating responses                                    |    No     |      3000       |                                                       |
| `ALLOW_ALL_USERS_IN_GROUPS` |                Allows all users in group chats interact with bot without adding them to USER_IDS list                 |    No     |        0        |                                                       |



## Credits
+ [Ollama](https://github.com/jmorganca/ollama)
+ [OpenWebUI](https://github.com/open-webui/open-webui)
+ [Original project](https://github.com/ruecat/ollama-telegram)

## Libraries used
+ [Aiogram 3.x](https://github.com/aiogram/aiogram)
