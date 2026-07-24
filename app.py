from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from groq import Groq
import os
from datetime import datetime
from dotenv import load_dotenv  # <-- IMPORTANTE ITO

# I-LOAD ANG .ENV FILE
load_dotenv()  # <-- IMPORTANTE ITO

app = Flask(__name__)
CORS(app)

# Kunin ang API key mula sa .env
api_key = os.environ.get("GROQ_API_KEY")

# Check kung may API key
if not api_key:
    print("❌ ERROR: Walang GROQ_API_KEY!")
    print("Gumawa ng .env file na may laman: GROQ_API_KEY=gsk_iyongkey")
    exit(1)

print("✅ API Key loaded successfully!")  # Para malaman mong gumana

# Initialize Groq client
client = Groq(api_key=api_key)

MODELS = {
    'fast': 'llama-3.1-8b-instant',
    'balanced': 'llama-3.3-70b-versatile',
    'powerful': 'mixtral-8x7b-32768'
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '')
        chat_history = data.get('history', [])
        model_choice = data.get('model', 'balanced')

        model = MODELS.get(model_choice, MODELS['balanced'])

        messages = [
            {"role": "system",
             "content": "You are Carl, a friendly and helpful AI assistant. Respond in a conversational and engaging manner."}
        ]

        for msg in chat_history:
            messages.append({"role": msg['role'], "content": msg['content']})

        messages.append({"role": "user", "content": user_message})

        completion = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.7,
            max_tokens=1024,
            top_p=1,
            stream=False
        )

        response = completion.choices[0].message.content

        return jsonify({
            'success': True,
            'response': response,
            'timestamp': datetime.now().isoformat()
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    # PARA MA-ACCESS SA MOBILE - host='0.0.0.0'
    app.run(host='0.0.0.0', debug=True, port=5000)

# For Vercel
app = app