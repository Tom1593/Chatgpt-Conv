from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

enteries = [
    {
        'owner': 'me',
        'content': "i ask a q for chat"
    },
    {
        'owner': 'chat-gpt',
        'content': "i ask a q for chat",
        'voice' : "voice"
    }    
]



@app.route("/")
def home():
    return render_template('home.html', title='Home')

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/saved")
def saved_Conv():
    return render_template('past.html', enteries=enteries, title='Database')

if __name__ == "__main__":
    app.run(debug=True)