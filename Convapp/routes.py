from flask import render_template, url_for, redirect,request
from tempfile import TemporaryFile
from Convapp import app, db
from Convapp.models import Entry, Conv
import whisper
import torch

DEVICE = "cpu"

model = whisper.load_model("base", device=DEVICE)

owner = "me"
conv = Conv()

data = {
    "owner": owner,
    "state": 'rec',
    "conv_id": conv.id
    }

enteries = [
    {
        'id': 0,
        'owner': 'me',
        'content': "i ask a q for chat",
        'audio_file': "should be voice"
    },
    {
        'id': 1,
        'owner': 'chat-gpt',
        'content': "i ask a q for chat",
        'audio_file' : "voice"
    }    
]

@app.route("/", methods=['GET','POST'])
def home():

    db.session.add(conv)
    db.session.commit()

    return render_template('home.html', title='Home Page',data=data)

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/saved")
def saved_Conv():
    return render_template('saved.html', enteries=enteries, title='Database')

@app.route('/record_audio', methods=['POST'])
def record_audio():
    #create a new entry with trancscribe
    #we have the audio file saved so we need to upload to server
    audio_data = request.data
    
    audio_file = TemporaryFile()
    audio_file.write(audio_data)
    
    audio = whisper.load_audio(audio_file.name)
    audio = whisper.pad_or_trim(audio)
    
    # make log-Mel spectrogram and move to the same device as the model
    mel = whisper.log_mel_spectrogram(audio).to(model.device)
        
    # detect the spoken language
    _, probs = model.detect_language(mel)
    print(f"Detected language: {max(probs, key=probs.get)}")
    
    #decode the audio
    options = whisper.DecodingOptions(task ='transcribe')
    result = whisper.decode(model, mel, options)

    #create new entry = conv_id,owner,content,audio file
    new_entry = Entry(owner=data["owner"], conv_id=data["conv_id"],
                      content=result["text"], audio_file=audio_data)
    db.session.add(new_entry)
    db.session.commit()
    
    
    
    # process audio_data and return a response
    return "This is a response from the Flask endpoint."