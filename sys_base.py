from flask import Flask, render_template, redirect, url_for
import tweepy
import re

user_fetch = "cryptob_chain"

user_auth = "admin"

pass_auth = "8afD44k6jYy3uqSR"

urls = r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+'

consumer_key = "Fo8vwJeEEBmWqCFFJtC5xhfoH"
consumer_secret = "mx3y6KzMukecsQtlY2oJ83DYvSYBDOKZQ1wdHRRA5kGMfOU9uD"

auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret)

api = tweepy.API(auth)

app = Flask(__name__)

@app.route('/')
def index():
    datos_front = []

    user = api.get_user(screen_name=user_fetch)
    image_url = user.profile_image_url_https.replace('_normal', '_200x200')
    name = user.name
    screen_name = user.screen_name

    tweets = api.user_timeline(screen_name=user_fetch, count=5, include_entities=True)

    for i in tweets:
        cleaned_text = re.sub(r'https://t.co/[a-zA-Z0-9]+', '', i.text)
        if 'media' in i.entities:
            for media in i.entities['media']:
                url = media['media_url_https']
                datos_front.append([cleaned_text, url])
        else:
            datos_front.append([cleaned_text])

    return render_template('index.html', tweets=datos_front, image_url=image_url, name=name, screen_name=screen_name)

@app.route("/update_user/<user_valor>:<pass_valor>/<new_valor>", methods=["GET"])
def update_user(new_valor, user_valor, pass_valor):
    global user_fetch

    if user_valor == user_auth and pass_valor == pass_auth:
        user_fetch = new_valor

        return redirect('/')

@app.route("/<path:path>")
def catch_all(path):
    return redirect(url_for("index"))

@app.errorhandler(500)
def internal_server_error(error):
    return render_template('500.html'), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)
