from vk_api import VkApi
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from config import vk_id,vk_token,openai_key
import openai
from googletrans import Translator




openai.api_key = openai_key
translator=Translator()
vk_session = VkApi(token=vk_token)
longpoll = VkBotLongPoll(vk_session, vk_id)
vk = vk_session.get_api()

def main():
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW and event.from_chat:
            id = event.chat_id
            msg = event.object.message['text']
            retranslate = True
            if msg[:4].lower() == "huba":
                msg = msg[4:]
                vk_session.method('messages.send', {'chat_id': id, 'message': "Задумался о :\"{0}\"".format(msg), 'random_id': 0})
                if "-translate" in msg:
                    retranslate = False
                    msg = msg.replace("-translate", '')
                msg = translate(msg, "ru", "en")
                sender(id, msg, retranslate)

def translate(text, orig, new):
    try:
        return translator.translate(text,src = orig, dest = new).text
    except:
        return text


def sender(id, text, retranslate):

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt= text,
        temperature=0.5,
        max_tokens=1000,
        top_p=1.0,
        frequency_penalty=0.5,
        presence_penalty=0.0,
    )
    answer = response["choices"][0]["text"]
    if retranslate:
        answer = translate(answer, "en", "ru")
    vk_session.method ('messages.send', {'chat_id': id, 'message': answer, 'random_id': 0})

try:
    main()
except:
    main()
