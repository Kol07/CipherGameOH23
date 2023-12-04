#Developed by Rayden 222395U, 2023
#Any form of distribution is prohibited unless given permission by Rayden

from flask import Flask, render_template,redirect,url_for,session,request
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired
import random
from datetime import datetime, timezone
import json
app = Flask(__name__)
app.config['SECRET_KEY'] = 'myverysecretkey'

#Ciphers
#---------------------------
#From https://www.geeksforgeeks.org/caesar-cipher-in-cryptography/
#A python program to illustrate Caesar Cipher Technique
def encryptCaesar(text,s):
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
#From https://www.geeksforgeeks.org/rail-fence-cipher-encryption-decryption/
# function to encrypt a message
def encryptRailFence(text, key):
 
    # create the matrix to cipher
    # plain text key = rows ,
    # length(text) = columns
    # filling the rail matrix
    # to distinguish filled
    # spaces from blank ones
    rail = [['\n' for i in range(len(text))]
                for j in range(key)]
     
    # to find the direction
    dir_down = False
    row, col = 0, 0
     
    for i in range(len(text)):
         
        # check the direction of flow
        # reverse the direction if we've just
        # filled the top or bottom rail
        if (row == 0) or (row == key - 1):
            dir_down = not dir_down
         
        # fill the corresponding alphabet
        rail[row][col] = text[i]
        col += 1
         
        # find the next row using
        # direction flag
        if dir_down:
            row += 1
        else:
            row -= 1
    # now we can construct the cipher
    # using the rail matrix
    result = []
    for i in range(key):
        for j in range(len(text)):
            if rail[i][j] != '\n':
                result.append(rail[i][j])
    return("" . join(result))
#---------------------------
#Forms
class UsernameForm(FlaskForm):
    username = StringField('Username', validators=[])

class ChooseCipherForm(FlaskForm):
    cipher = SelectField('Cipher', validators=[DataRequired()], choices=[('caesar','Caesar Cipher'),('railfence','Railfence Cipher')])

class CipherForm(FlaskForm):
    word = StringField('Word', validators=[DataRequired()])
    
#Wordlist
wordlist = ['TomCruise','Rayden','Python','Flask','Cryptography','CaesarCipher','Encryption','Decrypt'] #Change to a bigger list and list of same number of characters

#File Paths
caesarlbpath = './leaderboards/caesarleaderboard.json'
railfencelbpath = './leaderboards/railfenceleaderboard.json'

#Routes
@app.route('/',methods=['GET','POST'])
def home():
    form = UsernameForm(request.form)
    try:
        if session['starttime']:
            session.clear()
    except:
        pass

    if form.validate_on_submit():
        print('Form validated')
        session['username'] = form.username.data
        return redirect(url_for('cipher',ciphertype='caesar'))
    
    try:
        if session['starttime']:
            session.clear()
    except:
        pass
    try:
        with open(caesarlbpath,'r') as f:
            caesarleaderboard = json.load(f)
        caesarleaderboard = [entry for entry in caesarleaderboard if entry['time'] != '']
        caesarleaderboard.sort(key=lambda x: x['time'])
    except:
        caesarleaderboard = []
    try:
        with open(railfencelbpath,'r') as f:
            railfenceleaderboard = json.load(f)
        railfenceleaderboard = [entry for entry in railfenceleaderboard if entry['time'] != '']
        railfenceleaderboard.sort(key=lambda x: x['time'])
    except:
        railfenceleaderboard = []
    return render_template('home.html',caesarleaderboard=caesarleaderboard,railfenceleaderboard=railfenceleaderboard, form=form)

@app.route('/leaderboard')
def leaderboard():
    try:
        if session['starttime']:
            session.clear()
    except:
        pass
    try:
        with open(caesarlbpath,'r') as f:
            caesarleaderboard = json.load(f)
        
        caesarleaderboard = [entry for entry in caesarleaderboard if entry['time'] != '']
        caesarleaderboard.sort(key=lambda x: x['time'])
    except:
        caesarleaderboard = []
    try:
        with open(railfencelbpath,'r') as f:
            railfenceleaderboard = json.load(f)
        
        railfenceleaderboard = [entry for entry in railfenceleaderboard if entry['time'] != '']
        railfenceleaderboard.sort(key=lambda x: x['time'])
    except:
        railfenceleaderboard = []

    return render_template('leaderboard.html',caesarleaderboard=caesarleaderboard,railfenceleaderboard=railfenceleaderboard, top10=request.args.get('top10'))

""" @app.route('/cipher',methods=['GET','POST'])
def choosecipher():
    form = ChooseCipherForm(request.form)
    if form.validate_on_submit():
        print('Form validated')
        return redirect(url_for('cipher',ciphertype=form.cipher.data))
    return render_template('choosecipher.html',form=form) """

@app.route('/cipher/<ciphertype>',methods=['GET','POST'])
def cipher(ciphertype):
    form = CipherForm(request.form)
    if form.validate_on_submit():
        print('Form validated')
        endtime = datetime.now(timezone.utc)
        starttime = session['starttime']
        print(starttime)
        print(endtime)
        timediff = endtime - starttime
        #Save to JSON database here
        datadict = {}
        if ciphertype == 'caesar':
            lbpath = caesarlbpath
        elif ciphertype == 'railfence':
            lbpath = railfencelbpath
            
        try:
            with open(lbpath,'r') as f:
                leaderboard = json.load(f)
                leaderboard.sort(key=lambda x: x['time'], reverse=True)
                #If time is faster than any of the times in the leaderboard, replace it
                lbcounter = 0
                top10 = False
                for i in leaderboard:
                    print(i['time'])
                    if str(timediff) < i['time']:
                        datadict['username'] = session['username']
                        datadict['time'] = str(timediff)
                        leaderboard.insert(lbcounter,datadict)
                        leaderboard.sort(key=lambda x: x['time'])
                        leaderboard.pop()
                        top10=1
                        break
                    else:
                        lbcounter += 1
                
            with open(lbpath,'w') as f:
                json.dump(leaderboard,f, indent=4)

        except: #If file does not exist
            with open(lbpath,'w') as f:
                datadict['username'] = session['username']
                datadict['time'] = str(timediff)
                leaderboard = []
                leaderboard.append(datadict)
                #Populate leaderboard with 10 empty entries
                for i in range(9):
                    leaderboard.append({'username':'','time':''})
                json.dump(leaderboard,f, indent=4)
                top10 = 1
            
        session.clear()
        return redirect(url_for('leaderboard',top10=top10))
    
    randomword = wordlist[random.randint(0,len(wordlist)-1)]
    print(randomword)
    #Caesar Cipher
    if ciphertype == 'caesar':
        shift = random.randint(1,25)
        encryptedword = encryptCaesar(randomword,shift)
        print('Caesar chosen')
    #Railfence Cipher
    if ciphertype == 'railfence':
        encryptedword = encryptRailFence(randomword,3) #Number of rows is 3
        print('Railfence chosen')
    
    try:
        session['starttime']    
    except:
        session['starttime'] = datetime.now(timezone.utc)
        
    return render_template('cipher.html',form=form,encryptedword=encryptedword, actualword=randomword)
    
if __name__ == '__main__':
    app.run(debug=True)