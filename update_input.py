import os
import re
import tweepy

consumer_key = "wyFdy4BiMma9iDN0r8Z75rie3"
consumer_secret = "mCqsXly78oomDjeRxyDUdPrlpKkg6OtkwzORAsNkecXd26xxu0"
access_key = "1378519265423323144-EESiwp2PRVzhvuIN0JaSknWKejVIYW"
access_secret = "g0yvxghwatOP5NgRj8LMWOvgfHbBHWbl5nQGXzWv9Sa9u"

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

def remove_duplicates(file_directory):
    lines_seen = set()
    with open(file_directory, 'r') as file:
        for line in file:
            if line != "":
                lines_seen.add(line.strip('\n'))
        file.close()
    with open(file_directory, 'w') as file:
        for line in lines_seen:
            file.write(f"{line}\n")
        file.close()

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
    try:
        os.mkdir("user_data/" + user)
        os.mkdir("user_data/" + user + "/trained_model")
    except FileExistsError:
        pass
    print(f"✓ {user}")
    return [process_tweet_text(tweet.full_text) for tweet in alltweets if process_tweet_text(tweet.full_text) != ""]

def update_user(user):
    user = user.strip('\n')
    user_input = get_all_tweets(user)
    data_file = "user_data/__tweet_data__/" + user + ".txt"
    with open(data_file, 'a') as file:
        for tweet in user_input:
            file.write(f"{tweet}\n")
        file.close()
    remove_duplicates(data_file)
    print("==========================================")

def update_all_users():
    with open("guycode.txt", "r") as file:
        for user in file:
            user = user.strip('\n')
            update_user(user)
        file.close()
    word_count()

def word_count():
    current_count = 0
    with open("user_data/_word_count.txt", 'r') as file:
        current_count = int(file.readline())
        file.close()
    print(f"Previous dataset word-new_count: {current_count}")

    new_count = 0
    with open("guycode.txt") as file:
        for user in file:
            user = user.strip('\n')
            data_file = "user_data/" + user + ".txt"
            with open(data_file, 'r') as user_file:
                data = user_file.read()
                data = data.split()
                new_count += len(data)
            user_file.close()
        file.close()
    with open("user_data/_word_count.txt", "w") as file:
        file.write(str(new_count))
        file.close()
    print(f"Current dataset word-new_count:  {new_count}")

update_all_users()