from telethon import TelegramClient, events, sync, json

api_id = YOUR_API_ID
api_hash = 'YOUR_API_HASH'

client = TelegramClient('t_session', api_id, api_hash)
client.start()
print(client.get_me().stringify())
