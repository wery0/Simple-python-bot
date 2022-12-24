import random
import requests
import string
from flask import Flask, request, Response

TOKEN = ""
with open("token.txt", "r") as file:
    for line in file:
        TOKEN = line
app = Flask(__name__)


async def parse_message(message):
    print("message-->", message)
    chat_id = message['message']['chat']['id']
    print("chat_id-->", chat_id)
    try:
        txt = message['message']['text']
        print("txt-->", txt)
        return chat_id, txt
    except:
        print("MDA")
        return chat_id, ""


async def tel_send_message(chat_id, text):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': text
    }

    r = requests.post(url, json=payload)
    return r


@app.route('/', methods=['GET', 'POST'])
async def index():
    if request.method == 'POST':
        msg = request.get_json()

        try:
            chat_id, txt = await parse_message(msg)
        except:
            return "<h1>NOOB!</h1>"
        if txt == "/help":
            await tel_send_message(chat_id,
                                   "This bot can generate random numbers, chars, strings and passwords. Here is the list of commands:\n"
                                   "/help - Prints this message\n"
                                   "/number - Generate random number\n"
                                   "/char - Generate random character\n"
                                   "/string - Generate random string\n"
                                   "/password - Generate random password\n"
                                   "/what - What is the meaning of life?\n")
        elif txt == "/number":
            await tel_send_message(chat_id, random.randint(1, 100))
        elif txt == "/char":
            await tel_send_message(chat_id, ''.join(random.choices(string.printable, k=1)))
        elif txt == "/string":
            await tel_send_message(chat_id, ''.join(random.choices(string.ascii_lowercase, k=random.randint(3, 12))))
        elif txt == "/password":
            await tel_send_message(chat_id, ''.join(random.choices(string.printable, k=random.randint(8, 16))))
        elif txt == "/what":
            await tel_send_message(chat_id, "42")
        else:
            await tel_send_message(chat_id, 'Unknown command!')

        return Response('ok', status=200)
    else:
        return "<h1>Welcome!</h1>"


if __name__ == '__main__':
    app.run(debug=True)
