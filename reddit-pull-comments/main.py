import json
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


# def get_ids(sub_name, limit):
#     sub = reddit.subreddit(sub_name)
#     ids = []
#     for submission in sub.hot(limit=limit):
#         ids.append(submission.id)
#     return ids
def get_ids(sub_name, limit):
    sub = reddit.subreddit(sub_name)
    ids = []
    for i, submission in enumerate(sub.hot(limit=limit)):
        ids.append(submission.id)
        print(f"Fetched {i+1} submission IDs...")
    print(f"Fetched {len(ids)} submission IDs in total.")
    return ids


def get_pairs(id, limit):
    pairs = []
    submission = reddit.submission(id)
    submission.comments.replace_more(limit=0)
    num_top_level = len(submission.comments)
    ignore = ["[removed]", "[deleted]"]
    for i, top_level in enumerate(submission.comments):
        if top_level.body in ignore:
            continue

        for reply in sorted(top_level.replies, key=lambda comment: comment.score, reverse=True):
            if reply.body in ignore:
                continue

            pair = {
                'prompt': top_level.body,
                'completion': reply.body,
                'reply_score': reply.score,
                'reply_id': reply.id,
            }
            print('-->', pair['id'], pair['score'])
            pairs.append(pair)
        if (i+1) % 10 == 0:
            print(f"Processed {i+1} of {num_top_level} top-level comments...")
    print(f"Processed {num_top_level} top-level comments in total, generating {len(pairs)} pairs.")
    pairs = sorted(pairs, key=lambda p: p['score'], reverse=True)
    return pairs


def main():
    sub_name = 'politics'
    ids = get_ids(sub_name, 5)
    print(ids)
    pairs = []
    for id in ids:
        pairs += get_pairs(id, 5)

    print('')
    print('')

    with open('out.jsonl', 'w') as f:
        for pair in pairs:
            print('==>', pair['id'], pair['score'])
            f.write(json.dumps(pair) + '\n')

main()
