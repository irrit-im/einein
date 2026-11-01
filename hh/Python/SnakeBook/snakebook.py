import csv
import os
from dataclasses import dataclass, fields
from datetime import datetime, timedelta
from enum import Enum

# accounts reserved for administration - users cant use them
RESTRICTED_ACCOUNTS = ["Winner", "Instruction"]

FILE_DIR = os.path.abspath(os.path.dirname(__file__))
POSTS_CSV = os.path.join(FILE_DIR, "posts.csv") # path of the posts database

class PostType(Enum):
    """
        All possible post types
    """
    ANNOUNCEMENT = "Announcement"   # a restricted format for public announcements on the platform
    PRIVATE = "Private"             # private posts are saved in the database but are not shown
    PUBLIC = "Public"               # public posts are shown publicly and are always visible
    DISAPPEARING = "Disappearing"   # disappearing posts are shown only for a limited time from posting
    UNKNOWN = None  # not an actual type, but reserved for post types not in this list.

# restricted post types which users can't use
RESTRICTED_TYPES = [PostType.ANNOUNCEMENT.value, PostType.UNKNOWN.value]

TIME_TO_DISAPPEAR = timedelta(minutes=5) # the time until a disappearing message disappears

@dataclass
class Post:
    """
        A single post on snakebook.
    """
    POST_COUNTER = 0
    account: str        # the account which posted the post
    type_str: str       # a string value of the type of this post
    timestamp: str      # time of posting, for sorting posts and disappearing posts
    message: str        # the actual post content

    @property
    def post_type(self):
        """
            Retrieves the type of this message as a PostType
        """
        try:
            return PostType(self.type_str)
        except ValueError: # post type is an invalid string
            return PostType.UNKNOWN

    def __str__(self) -> str:
        """
            String representation of the post for displaying it
        """
        if self.post_type == PostType.PUBLIC:
            return f"[*] {self.account} says: \"{self.message}\" [*]"
        elif self.post_type == PostType.PRIVATE:
            return "[*] Private Post [*]"
        elif self.post_type == PostType.ANNOUNCEMENT:
            return f"[!] {self.message} ~ announcement by {self.account} [!]"
        elif self.post_type == PostType.DISAPPEARING:
            post_time = datetime.fromisoformat(self.timestamp)
            if datetime.now() - post_time < TIME_TO_DISAPPEAR:
                return f"[{post_time}] \"{self.message}\" ~{self.account}"
            return "This post disappeared!"
        
        # unknown post type
        return f"Corrupted Post! Found Type: {self.type_str}"
        

def add_user_post(post_type=PostType.PRIVATE.value):
    """
        A function which queries the user for post values and adds a post to the database.
        The function enforces restrictions on making posts
    """
    sender = input("Account: ").strip().title()
    message = input("Message: ")

    if sender in RESTRICTED_ACCOUNTS:
        raise ValueError("Restricted Sender!")

    if post_type in RESTRICTED_TYPES:
        raise ValueError("Restricted Post Type!")

    csv_line = f"\"{sender}\",\"{post_type}\",\"{datetime.now().isoformat()}\",\"{message}\"\n"
    with open(POSTS_CSV, 'a') as csv_file:
        csv_file.write(csv_line)

def print_posts():
    """
        Prints all posts in the database
    """
    posts = []
    with open(POSTS_CSV, 'r') as csv_file:
        for row in csv.reader(csv_file, delimiter=','):
            if len(row) != len(fields(Post)):
                # skips empty lines in file
                continue
            posts.append(Post(*row))

    posts.sort(key=lambda post: post.timestamp)

    print("\n =-=-= Posts =-=-=")
    for post in posts:
        print(post)
    print("\n")


if __name__ == '__main__':
    try:
        while True:
            print_posts()

            post_type = input("What type of post would you like to make?\n")
            try:
                add_user_post(post_type.title())
            except ValueError as e:
                print(f"Bad Request: {e}")
            else:
                print("Added Post!")
    except KeyboardInterrupt:
        print("Goodbye!")
