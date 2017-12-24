## PhoneBuzz

The application calls (verified) phone numbers after a specified delay. A voice prompt indicates for the caller to enter a number. The correct output of the FizzBuzz game (starting at 1 and ending with the entered number) is read back to the caller.

# Deployment
To deploy this on a new server, the following edits are suggested:

Update `accountSid`, `authToken`, `twiloNumber` and `baseUrl` in `app.py`. On the server run `pip install -r requirements.txt`. `Procfile` is included for easier deployment (especially on Heroku).

# Demo
Visit http://fizzbuzzlend.herokuapp.com/ for demo.
