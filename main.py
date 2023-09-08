#Developed by Rayden 222395U, 2023
#Any form of distribution is prohibited unless given permission by Rayden

from flask import Flask, render_template,redirect,url_for,session,request, Response
from flask_wtf import FlaskForm
from wtforms import StringField, ValidationError
from wtforms.validators import DataRequired
import random
from datetime import datetime, timezone
import json
app = Flask(__name__)
app.config['SECRET_KEY'] = 'myverysecretkey'


#---------------------------
#From https://www.geeksforgeeks.org/caesar-cipher-in-cryptography/
#A python program to illustrate Caesar Cipher Technique
def encrypt(text,s):
    result = ""
 
    # traverse text
    for i in range(len(text)):
        char = text[i]
 
        # Encrypt uppercase characters
        if (char.isupper()):
            result += chr((ord(char) + s-65) % 26 + 65)
 
        # Encrypt lowercase characters
        else:
            result += chr((ord(char) + s - 97) % 26 + 97)
 
    return result
#---------------------------
#Forms
class UsernameForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])

class CaesarCipherForm(FlaskForm):
    word = StringField('Word', validators=[DataRequired()])

@app.route('/',methods=['GET','POST'])
def home():
    form = UsernameForm(request.form)
    if form.validate_on_submit():
        print('Form validated')
        session['username'] = form.username.data
        return redirect(url_for('caesarcipher'))
    
    return render_template('home.html',form=form)

@app.route('/caesarcipher',methods=['GET','POST'])
def caesarcipher():
    form = CaesarCipherForm(request.form)
    if form.validate_on_submit():
        print('Form validated')
        endtime = datetime.now(timezone.utc)
        starttime = session['starttime']
        print(starttime)
        print(endtime)
        timediff = endtime - starttime
        #Save to JSON database here
        datadict = {}
        try:
            with open('leaderboard.json','r') as f:
                leaderboard = json.load(f)
                datadict['username'] = session['username']
                datadict['time'] = str(timediff)
                leaderboard.append(datadict)
            with open('leaderboard.json','w') as f:
                json.dump(leaderboard,f, indent=4)
        except:
            with open('leaderboard.json','w') as f:
                datadict['username'] = session['username']
                datadict['time'] = str(timediff)
                leaderboard = []
                leaderboard.append(datadict)
                json.dump(leaderboard,f, indent=4)
        session.clear()
        return redirect(url_for('leaderboard'))
    wordlist = ['TomCruise','Rayden','Python','Flask','Cryptography','CaesarCipher','Encryption','Decrypt'] #Change to a bigger list and list of same number of characters
    randomword = wordlist[random.randint(0,len(wordlist)-1)]
    shift = random.randint(1,25)
    print(randomword)
    encryptedword = encrypt(randomword,shift)
    try:
        session['starttime']    
    except:
        session['starttime'] = datetime.now(timezone.utc)
    return render_template('caesar.html',form=form,encryptedword=encryptedword, actualword=randomword)

@app.route('/leaderboard')
def leaderboard():
    with open('leaderboard.json','r') as f:
        leaderboard = json.load(f)
    leaderboard.sort(key=lambda x: x['time'])
    print(leaderboard)
    return render_template('leaderboard.html',leaderboard=leaderboard)
    
if __name__ == '__main__':
    app.run(debug=True)