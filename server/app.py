# author = rhnvrm <hello@rohanverma.net>
import os
from flask import Flask, request, render_template, jsonify, send_from_directory
from model import PerdictionClient

app = Flask(__name__, template_folder='../pages')
api = PerdictionClient()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/perdiction')
def prediction():
    """Return the perdiction of the KOS root directory."""
    # retweets_only = request.args.get('retweets_only')
    # api.set_retweet_checking(strtobool(retweets_only.lower()))
    # with_sentiment = request.args.get('with_sentiment')
    # api.set_with_sentiment(strtobool(with_sentiment.lower()))
    # query = request.args.get('query')
    # api.set_query(query)

    # tweets = api.get_tweets()
    perdiction = api.get_perdiction()

    return perdiction


port = int(os.environ.get('PORT', 5000))
app.run(host="0.0.0.0", port=port, debug=True)
