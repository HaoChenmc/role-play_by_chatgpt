from config import special_instructions
from chat_api import get_model_response
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv, find_dotenv
import os


def make_new_role():
    name = input("Name:")
    setting: str = input("Character Setting:")
    a_new_role = [
        {
            "role": "system",
            "content": "Now, you need to play as a person named " + name + ". And your setting is " + setting
        },
    ]

    return a_new_role


if __name__ == '__main__':

    # get information from .env.
    load_dotenv(find_dotenv(), verbose=True)
    # api_openai = os.environ.get("OPENAI_API_KEY")
    new_role = os.environ.get("NEW_ROLE")
    model = os.environ.get("MODEL")
    role = os.environ.get("ROLE")
    web = os.environ.get("WEB")

    # the default conversation
    conversation_history = special_instructions("default")

    # choose a role to talk.
    if new_role == "False" or new_role == "0":
        conversation_history = special_instructions(role)
    else:
        conversation_history = make_new_role()

    # Debug
    # print(role)
    # print(conversation_history)

    # call function of chat_api.
    if web == '0':
        while True:
            user_input = input("You: ")
            if user_input.lower() == 'exit':
                break  # if the user input "exit", break.
            response = get_model_response(conversation_history, user_input, model)
            print("GPT:", response)
    else:

        def web(web_input):
            while True:
                if web_input.lower() == 'exit':
                    break  # if the user input "exit", break.
                response = get_model_response(conversation_history, web_input, model)
                return response


        app = Flask(__name__, static_folder='web', static_url_path='/web/')


        @app.route('/')
        def index():
            return app.send_static_file('index.html')


        @app.route('/send_message', methods=['POST'])
        def send_message():
            user_input = request.json['user_input']

            model_reply = web(user_input)

            return jsonify({'model_reply': model_reply})


        app.run(debug=False, port=7120)
