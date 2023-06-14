from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import openai

app = Flask(__name__)
CORS(app)

openai.api_key = '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'  # Replace with your actual API key

def chat_with_chatgpt(prompt):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": str(prompt)}]
    )
    message = completion.choices[0].message['content']
    print(message)
    return message

@app.route('/api/chat', methods=['POST'])
def chat():
    message_data = request.get_json()
    received_message = message_data.get('message', 'No message received')
    chatgpt_response = chat_with_chatgpt(received_message)
    return jsonify({"response": chatgpt_response})

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)

if __name__ == '__main__':
    app.run()

