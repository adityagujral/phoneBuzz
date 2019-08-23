import os, time
from flask import Flask, request, redirect, render_template, url_for
from flask_wtf import FlaskForm
from twilio.twiml.voice_response import VoiceResponse
from twilio.rest import Client
from wtforms import StringField, SubmitField, validators

accountSid = ''
authToken = ''
twiloNumber = ''
baseUrl = ''

welcomeUrl = (baseUrl + '/welcome').strip()

class PhoneForm(FlaskForm):
    number = StringField('Enter phone number (twilio verified) to call (+1xxxyyyzzzz)',
        [validators.Required(), validators.Length(min=12, max=12)])
    delay = StringField('Enter delay before call (in seconds)')
    submit = SubmitField()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'randomSecretKey'

client = Client(accountSid, authToken)

@app.route('/', methods=['GET', 'POST'])
def index():
    form = PhoneForm(request.form)
    if request.method == 'POST':
        number = request.form['number']
        delay = request.form['delay']
        if not delay:
            delay = 0
        try:
            int (delay)
        except Exception:
            return render_template('index.html', displayError='Delay must be positive number', form=form)
        if int(delay) < 0:
            return render_template('index.html', displayError='Delay must be positive number', form=form)
        else:
            delay = int(delay)
        time.sleep(delay)
        try:
            call = client.calls.create( to=number, from_=twiloNumber, 
                       url=welcomeUrl)
        except Exception:
            return render_template('index.html', displayError='Number '
                'must be valid US/Canda number and verfied. '
                'If the number is not already verified, '
                'please contact aditya.gujral@tamu.edu to verify the number.'
                ' This limitation is because of the trial account.', form=form)
        return redirect(url_for('welcome'))
        
    return render_template('index.html', form=form)

@app.route('/welcome', methods=['GET', 'POST'])
def welcome():
    response = VoiceResponse()
    response.say('Welcome to Phone Buzz Game! Please enter a number')
    response.gather(action='/fizzbuzz', method='POST')
    return str(response)

@app.route('/fizzbuzz', methods=['GET', 'POST'])
def fizzBuzz():
    response = VoiceResponse()
    num = int(request.values.get('Digits', None))

    if not num:
        return redirect(url_for('welcome'))

    returnVal = ''
    for i in range(num + 1)[1:]:
        if i % 15 == 0:
            returnVal += 'Fizz Buzz '
        elif i % 3 == 0:
            returnVal += 'Fizz '
        elif i % 5 == 0:
            returnVal += 'Buzz '
        else:
            returnVal += str(i) + ' '
    response.say(returnVal)
    return str(response)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
