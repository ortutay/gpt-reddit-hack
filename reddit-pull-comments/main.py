import praw
import os

from praw.models import MoreComments
from dotenv import load_dotenv
load_dotenv()

print(os.environ.get('CLIENT_SECRET'))


reddit = praw.Reddit(
    client_id='EAPwAfreYOSxNx8fVZXElA',
    client_secret=os.environ.get('CLIENT_SECRET'),
    user_agent='comment extraction')


def get_pairs(url, limit):
    pairs = []
    submission = reddit.submission(url=url)
    q = []

    submission.comments.replace_more(limit=0)
    for top_level in submission.comments:
        for reply in top_level.replies:
            print('reply', top_level.body, '==>', reply.body)


def main():
    print('main')

    url = "https://www.reddit.com/r/funny/comments/3g1jfi/buttons/"
    pairs = get_pairs(url, 10)


main()
