from snakebook import POSTS_CSV, Post, PostType
from dataclasses import asdict
import csv


INITIAL_POSTS = [
    Post("Winner", PostType.ANNOUNCEMENT.value, "2004-02-04T01:23:45.6789", "Can you make an announcement using this Winner account?"),
    Post("Instruction", PostType.PUBLIC.value, "2004-02-04T03:14:15.926535", f"Your solution cannot edit the file \"posts.csv\" directly!"),
    Post("Instruction", PostType.PUBLIC.value, "2004-02-22T22:22:22.222220", f"If you need to reset \"posts.csv\" you can run the \"reset_snakebook.py\" script.")
]

CSV_ORDER = ["account", "type_str", "timestamp", "message"]

if __name__ == '__main__':
    with open(POSTS_CSV, 'w') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')
        rows = []

        for post in INITIAL_POSTS:
            sorted_items = [(key, val) for key, val in asdict(post).items()]
            sorted_items.sort(key=lambda item: CSV_ORDER.index(item[0]))
            rows.append([val for _, val in sorted_items])

        csv_writer.writerows(rows)
