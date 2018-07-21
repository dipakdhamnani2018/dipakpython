from flask import Flask, render_template
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from flask import request
from flask import render_template
from flask import flash
from flask import jsonify
from flask import session
from chatterbot.trainers import ListTrainer

app = Flask( __name__ )

app.secret_key = 'You Will Never Guess'

english_bot = ChatBot("zee")
english_bot.set_trainer(ChatterBotCorpusTrainer)



@app.route("/")
def home1():

    return render_template("get.html")

@app.route( "/ask", methods=['POST'] )
def ask():
	message = (request.form['messageText'])
	test = '1'
	while True:
		if message == "listen":
			bot_response = str( "what" )
			session["var"] = "first"
			# print bot_response
			return jsonify( {'status': 'OK', 'answer': bot_response} )

		else:
			if session.get( "var" ) is not None:
				if session["var"] == "first":
					session["que"] = message
					session["var"] = "second"
					bot_response = str( "What should i reply then?" )
					# print bot_response
					return jsonify( {'status': 'OK', 'answer': bot_response} )

				else:
					que = session["que"]
					for x in range( 5 ):
						conversation = [
							que,
							message
						]

						english_bot.set_trainer( ListTrainer )
						english_bot.train( conversation )
					session.pop( "var" )
					session.pop( "que" )
					bot_response = str( "Ok got it" )
			else:
				bot_response = str( english_bot.get_response( message ) )
			# print bot_response
			return jsonify( dict( status='OK', answer=bot_response ) )


if __name__ == "__main__":
    app.run()