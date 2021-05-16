import setuptools.archive_util
import tweepy
import re
consumer_key = "wyFdy4BiMma9iDN0r8Z75rie3"
consumer_secret = "mCqsXly78oomDjeRxyDUdPrlpKkg6OtkwzORAsNkecXd26xxu0"
access_key = "1378519265423323144-EESiwp2PRVzhvuIN0JaSknWKejVIYW"
access_secret = "g0yvxghwatOP5NgRj8LMWOvgfHbBHWbl5nQGXzWv9Sa9u"

input_file = "/Users/iyinoluwatugbobo/Desktop/Development/guyCodeAI/combined_guycode_model/combined_input.txt"
users_file = "/Users/iyinoluwatugbobo/Desktop/Development/guyCodeAI/combined_guycode_model/users.txt"

def process_tweet_text(text):
    if "RT" in text:
        return ""
    elif "play " in text:
        return ""

    text = re.sub(r'http\S+', '', text)   # Remove URLs
    text = re.sub(r'@[a-zA-Z0-9_]+', '', text)  # Remove @ mentions
    text = text.strip(" ")   # Remove whitespace resulting from above
    text = re.sub(r' +', ' ', text)   # Remove redundant spaces

    # Handle common HTML entities
    text = re.sub(r'&lt;', '<', text)
    text = re.sub(r'&gt;', '>', text)
    text = re.sub(r'&amp;', '&', text)
    return text

def get_all_tweets(screen_name):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    alltweets = []
    new_tweets = api.user_timeline(screen_name=screen_name, count=200, tweet_mode='extended')
    alltweets.extend(new_tweets)
    oldest = alltweets[-1].id - 1

    while len(new_tweets) > 0:
        new_tweets = api.user_timeline(screen_name=screen_name, count=200, max_id=oldest, tweet_mode='extended')
        alltweets.extend(new_tweets)
        oldest = alltweets[-1].id - 1

    user = screen_name.strip("\n")
    print(f"✓ {user}")

    return [process_tweet_text(tweet.full_text) for tweet in alltweets if process_tweet_text(tweet.full_text) != ""]

def get_all_users():
    all_input = []
    with open(users_file, "r") as file:
        for username in file:
            all_input += get_all_tweets(username)
        file.close()
    return all_input


def update_input():
    all_input = get_all_users()
    lines_seen = set()  # holds lines already seen
    with open(input_file, "r") as file:
        for line in file:
            lines_seen.add(line.strip('\n'))
        lines_seen.update(all_input)
        file.close()
    f = list(lines_seen)
    with open(input_file, "w") as file:
        for line in f:
            file.write("%s\n" % line)
        file.close()

update_input()