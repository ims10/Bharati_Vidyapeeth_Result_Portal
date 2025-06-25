from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello from Flask deployed on Vercel!"

# For Vercel to recognize the entry point
# Do not include app.run()
