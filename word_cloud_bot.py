# Word Cloud Bot -- Loops through user's history, creates a word cloud image with their most used words
#
# By Eli Anderson
#
# Last edited July 10, 2017
#
# TODO -- 1) save the matplotlab image to file

# praw is a tool that makes interacting with reddit much easier.
#

import praw

# time module is used so the bot won't go crazy

import time
import os

# wordcloud module will make this about a million times easier

from wordcloud import WordCloud

# To display the word cloud

import matplotlib.pyplot as plt

# To upload WordCloud to imgur

import pyimgur

# Login the bot into reddit


def authenticate_reddit() :
    print('Authenticating reddit account...')
    reddit = praw.Reddit('WordCloudBot', user_agent='yeah_bot_test v0.1')
    print('Authenticated as ' + str(reddit.user.me()))
    return reddit

# Login the bot into imgur

def authenticate_imgur() :
    print('Authenticating imgur account...')
    client_id = '58b015847759ef5'
    imgur = pyimgur.Imgur(client_id)
    print('Imgur account authenticated.')
    return imgur

def run_bot(reddit, comments_replied_to5) :

    # Loop through the top 100 comments in all recent posts on a certain subreddit

    for comment in reddit.subreddit('test').comments(limit=100) :

        # check if keyword '!wordcloud' is in any of those comments and comment has already been replied to

        if '!wordcloud' in comment.body and comment.id not in comments_replied_to5:

            print('String with \'!wordcloud\' found!!')

            # Fetch username of author of the comment to be replied to
            username = comment.author.name

            # If the file already exists, erase its contents
            if os.path.isfile('comment_history.txt') :
                open('comment_history.txt', 'w').close()

            # Go through user's recent comment history

            for comment2 in reddit.redditor(username).comments.new(limit=100) :

                # Add past 1000 comments to .txt file

                comment_history = []

                # Put each comment into the file
                with open('comment_history.txt', 'a') as file :
                    file.write(comment2.body + '\n')
                    print(comment2.body)

            # Read file
            with open('comment_history.txt', 'r') as file:
                comment_history = file.read()

            # Generate the word cloud
            create_cloud(comment_history)

            # Save image to Pictures as wordcloud.png



            # Upload image to imgur
            filepath = 'Pictures\wordcloud.png'
            image = imgur.upload_image(filepath, title='/u/'+ username + '\'s Word Cloud')
            print(str(image.url))
            # reply via comment

            # comment.reply('Here is a word cloud of your past 100 comments: ' + image.url)
            print('Replied to ' + comment.id)

            # Add comment ID to replied to list
            comments_replied_to5.append(comment.id)

            # Save comment ID to comments_replied_to5.txt (the 'a' means I am appending to the file)

            with open('comments_replied_to5.txt', 'a') as file:
                file.write(comment.id + '\n')

    # Sleep for ten seconds

    print('Sleeping for 10 seconds...')
    time.sleep(10)

# Save the comments that have been replied to in the past so the bot doesn't reply to same comments the after each time
# it is run
#
# Uses .txt file to store the comment IDs


def get_saved_comments() :

    # If .txt file with comment IDs doesnt exist, create one and return a blank array

    if not os.path.isfile('comments_replied_to5.txt') :
        comments_replied_to5 = []

    else :
        with open('comments_replied_to5.txt', 'r') as file :

            # Read contents of the file
            comments_replied_to5 = file.read()

            # split() by new line
            comments_replied_to5 = comments_replied_to5.split('\n')

            # Filter out the empty string at end of the .txt file
            # filter() filters out the first argument from the second argument
            # comments_replied_to5 = filter('', comments_replied_to5)

    return comments_replied_to5

def create_cloud(comment_history) :

    wordcloud = WordCloud().generate(comment_history)

    # display image
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()

reddit = authenticate_reddit()
imgur = authenticate_imgur()

# To prevent spam, create list of comments already replied to

comments_replied_to5 = get_saved_comments()
print(comments_replied_to5)

# To automatically reply to comments, a while loop is used

while True :
    run_bot(reddit, comments_replied_to5)