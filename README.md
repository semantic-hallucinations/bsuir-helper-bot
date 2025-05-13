# BSUIR assistant telegram bot
Telegram-bot project

## Structure:
- **conig** dir contains logger configuration and bot's config
- **handlers** contains handlers for group and private chats. Also private chats supports bot commands
- **services** implements communication with [answer-pipeline](https://github.com/semantic-hallucinations/answer_pipeline) service
- **middlewares** flood filters for different chat types
 
## Basic usage

Chat with @BotFather in Telegram messenger to create a chat with bot.

Also, to use bot in group chats, set enable groups and disable privacy mod in @BotFather

Check .env.example to init eviroment variable correctly


## Local running
```docker compose up --build``` and run example.py

## Chech publication history
You can check publishing history in organisation -> packages

## Using docker image
```
services:
  microservice:
    image: ghcr.io/semantic-hallucinations/py-microservice-template:latest   # or commit sha, or tag name instead of <latest>
```
