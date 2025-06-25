from flask import Flask

app = Flask(__name__)

@app.route('/')
def login():
    return render_template('login.html')

# For Vercel to recognize the entry point
# Do not include app.run()
