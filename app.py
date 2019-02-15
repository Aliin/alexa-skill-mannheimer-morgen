from flask import Flask, render_template
from flask_ask import Ask, statement, question

app = Flask(__name__)
ask = Ask(app, '/')

@ask.launch
def launched():
    speech = render_template("welcome")
    return question(speech)

@ask.intent("EventsIntent")
def events():
    speech = render_template("events")
    return statement(speech)

@ask.intent("DummyIntent", convert={})
def dummy_intent(name):
    speech = "Freut mich {}".format(name)
    return statement(speech)

if __name__ == '__main__':
    app.run(debug=True)
