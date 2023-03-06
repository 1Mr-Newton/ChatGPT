from telethon import TelegramClient, events
import os
import openai
import json
from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv('API_KEY')
api_id = os.getenv('api_id')
api_hash = os.getenv('api_hash')
botToken = os.getenv('botToken')

client = TelegramClient('chatgpt', api_id, api_hash)
client.start(bot_token=botToken)


@client.on(events.NewMessage)
async def event_handler(event):
    user = event.sender_id
    message = event.raw_text

    respose = get_response(message, user)

    await event.respond(respose)


def get_response(message, user):
    prompt = [

    ]
    if not os.path.exists(f'chats/{user}.json'):
        data = {
            "messages": [
                {
                    "role": "system",
                    "content": "You are a large ai language model. you know everything. Your job is to provide solutions / suggestion to problems. Your name is Scyther Alpha. You were created by @newton_jnr."
                }

            ]

        }
        with open(f'chats/{user}.json', 'w') as f:
            json.dump(data, f, indent=4)

    with open(f'chats/{user}.json', 'r') as f:
        data = json.load(f)['messages']

    # for item in data:
    #   prompt.append(item)
    [prompt.append(item) for item in data]

    prompt.append(
        {
            "role": "user",
            "content": message
        }
    )

    completion = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=prompt
    )

    response = completion.choices[0].message.content

    with open(f'chats/{user}.json', 'r') as f:
        data = json.load(f)
    data['messages'].append(
        {
            "role": "user",
            "content": message
        }
    )
    data['messages'].append(
        {
            "role": "assistant",
            "content": response
        }
    )
    with open(f'chats/{user}.json', 'w') as f:
        json.dump(data, f, indent=4)

    return response


client.run_until_disconnected()
