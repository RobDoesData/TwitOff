"""SQLAlchemy models for Twitoff."""

from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()

class User(DB.Model):
    """Twitter Users that we pull and analyze tweets for."""
    id = DB.Column(DB.BigInteger, primary_key=True)
    name = DB.Column(DB.String(15), nullable=False)
    newest_tweet_id = DB.Column(DB.BigInteger)

    def __repr__(self):
        return '<User {}>'.format(self.name)

class Tweet(DB.Model):
    """Tweets"""
    id = DB.Column(DB.BigInteger, primary_key=True)
    text = DB.Column(DB.Unicode(500))
    embedding = DB.Column(DB.PickleType, nullable=False)
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey('user.id'), nullable=False)
    user = DB.relationship('User', backref=DB.backref('tweets', lazy=True))
    
    def __repr__(self):
        return '<Tweet {}>'.format(self.text)

def tweet_generator(user,tweet):
    u1 = User(name=user)
    t1 = Tweet(text=tweet)
    u1.tweets.append(t1)
    DB.session.add(u1)
    DB.session.add(t1)
    DB.session.commit()
    return "Generated a tweet by " + str(user) + "with the tweet: " + str(tweet)


def add_user(user):
    """Get Twitter User Data stored in our database."""
    twitter_user = TWITTER.get_user(user)
    tweets = twitter_user.timeline(count=200, exclude_replies=True, include_rts=False, tweet_mode='extended')
    db_user = User(id=twitter_user.id, name=twitter_user.screen_name, newest_tweet_id=tweets[0].id)
    for tweet in tweets:
        embedding = BASILICA.embed_sentence(tweet.full_text, model='twitter')
        db_tweet = Tweet(id=tweet.id, text=tweet.full_text[:500], embedding=embedding)
        db_user.tweets.append(db_tweet)
        DB.session.add(db_tweet)
    DB.session.add(db_user)
    DB.session.commit()