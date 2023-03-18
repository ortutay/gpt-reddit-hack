import praw
import os
import pprint

from praw.models import MoreComments
try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    print('could not load from dotenv')
    pass

pp = pprint.PrettyPrinter()

print(os.environ.get('CLIENT_SECRET'))


reddit = praw.Reddit(
    client_id='EAPwAfreYOSxNx8fVZXElA',
    client_secret=os.environ.get('CLIENT_SECRET'),
    user_agent='comment extraction')


def get_ids(sub_name, limit):
    sub = reddit.subreddit(sub_name)
    ids = []
    for submission in sub.hot(limit=limit):
        ids.append(submission.id)
    return ids


def get_pairs(id, limit):
    pairs = []
    submission = reddit.submission(id)
    submission.comments.replace_more(limit=0)
    for top_level in submission.comments:
        for reply in top_level.replies:
            pairs.append({
                'comment': top_level.body,
                'reply': reply.body,
            })


def main():
    sub_name = 'politics'
    ids = get_ids(sub_name, 5)
    print(ids)
    for id in ids:
        pairs = get_pairs(id, 10)
    pp.pprint(pairs)


main()
