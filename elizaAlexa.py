import logging

from flask import Flask, render_template

from flask_ask import Ask, statement, question, session

import eliza as ez
import mongo as mgdb

import datetime as dt
import EmailClient as ec

app = Flask(__name__)

ask = Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)
name = "Archit"
f = open("Transcript_"+name+".txt",'w')


@ask.launch
def begin_session():
	start_msg = render_template('start')
	f.write(str(dt.datetime.now())+"<br>")
	f.write("Eliza: "+start_msg+"<br>")
	session.attributes['answers']=""
	return question(start_msg)

@ask.intent("ResponseIntent",convert={'answer':str})
def start_conversation(answer):
	session.attributes['answers'] = answer
	f.write("You: "+answer+"<br>")
	if answer is None:
		return question("I didn't quite get that, can you please repeat?")
	if(answer.lower()=="send me an email" or answer.lower()=="send me an e mail"):
		f.close()
		ec.send_email("Archit","archit.941@gmail.com")
		mgdb.register_last_session("Archit","Last email sent on"+str(dt.datetime.now()))
		return statement("Email Sent, GoodBye!")
	elif(answer.lower()=="end session" or answer.lower()=="end"):
		f.close()
		ec.send_email("Archit","archit.941@gmail.com")
		mgdb.register_last_session("Archit","Last email sent on"+str(dt.datetime.now()))
		return statement("GoodBye, I have also sent you an email!")
	else:
		eliza_response = ez.analyze(session.attributes['answers'])
		curr_response_msg = str(eliza_response)
		f.write("Eliza: "+curr_response_msg+"<br>")
		return question(curr_response_msg)
if __name__=='__main__':
	app.run(debug=True)
	if not f.closed:
		f.close()
