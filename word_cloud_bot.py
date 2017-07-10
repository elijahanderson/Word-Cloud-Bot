# Word Cloud Bot -- Loops through user's history, creates a word cloud image with their most used words
#
# By Eli Anderson
#
# Last edited July 10, 2017
#


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

# Login the bot into reddit


def authenticate() :
    print('Authenticating...')
    reddit = praw.Reddit('WordCloudBot', user_agent='yeah_bot_test v0.1')
    print('Authenticated as ' + str(reddit.user.me()))
    return reddit


def run_bot(reddit, comments_replied_to5) :

    # Loop through the top 100 comments in all recent posts on a certain subreddit

    for comment in reddit.subreddit('test').comments(limit=100) :

        # check if keyword '!wordcloud' is in any of those comments and comment has already been replied to

        if '!wordcloud' in comment.body and comment.id not in comments_replied_to5:

            print('String with \'!wordcloud\' found!!')

            # Fetch username of author of the comment to be replied to
            username = comment.author.name

            # Go through user's recent comment history

            for comment2 in reddit.redditor(username).comments.new(limit=1000) :

                # Add past 1000 comments to .txt file

                comment_history = []

                # If the file already exists, erase its contents
                if os.path.isfile('comment_history.txt') :
                    open('comment_history.txt', 'w').close()

                # Put each comment into the file
                with open('comment_history.txt', 'a') as file :
                    file.write(comment.body + '\n')

            # Read file
            with open('comment_history.txt', 'r') as file:
                comment_history = file.read()

            # Generate the word cloud
            create_cloud(comment_history)

            # reply via comment

            # comment.reply('You have said the word \'yeah\' ' + str(yeah_count) + ' times in your commenting history.\n\n '
                                                                          #  '[Yeah!](https://byyeah.com/assets/img/product/outofstock.jpg)')
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

reddit = authenticate()

# To prevent spam, create list of comments already replied to

comments_replied_to5 = get_saved_comments()
print(comments_replied_to5)

# To automatically reply to comments, a while loop is used

while True :
    run_bot(reddit, comments_replied_to5)