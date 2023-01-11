from flask import Flask, render_template, redirect
import tweepy
import re

user_fetch = "Agus"

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

    print(name, screen_name)

    return render_template('index.html', tweets=datos_front, image_url=image_url, name=name, screen_name=screen_name)

@app.route("/update_user/<new_valor>", methods=["GET"])
def update_user(new_valor):
    global user_fetch
    user_fetch = new_valor

    return redirect('/')

if __name__ == "__main__":
    app.run()
