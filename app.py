from flask import Flask, request, jsonify, render_template
import requests
import html

app = Flask(__name__)

API_KEY = "api-key-here"
API_URL = "https://api.openai.com/v1/chat/completions"

# Initialize conversation history
conversation_history = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def send_message():
    user_message = request.json.get('message')
    
    # Add user message to conversation history
    conversation_history.append({'role': 'user', 'content': user_message})
    
    # Prepare the payload with conversation history
    messages = [{'role': msg['role'], 'content': msg['content']} for msg in conversation_history]

    response = requests.post(API_URL, headers={
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }, json={
        'model': 'chatgpt-4o-latest',
        'messages': messages
    })

    if response.status_code == 200:
        bot_message = response.json()['choices'][0]['message']['content']
        
        # Add bot message to conversation history
        conversation_history.append({'role': 'assistant', 'content': bot_message})
        
        formatted_response = format_response(bot_message)
        return jsonify({'message': formatted_response})
    else:
        return jsonify({'error': 'Error contacting the API'}), 500

def format_response(message):
    escaped_message = html.escape(message).replace('\n', '<br>')  # Replace new lines with <br>
    return f"""
    <div class="bot-message">
        <strong>Bot:</strong>
        <pre><code>{escaped_message}</code></pre>
    </div>
    """

if __name__ == '__main__':
    app.run(debug=True)
