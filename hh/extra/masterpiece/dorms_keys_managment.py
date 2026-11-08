import argparse
import json
import string
from hashlib import sha3_256 as sha  # The Future!!

DEBUG = False
# Ship with False

DEFAULT_KEY_SIZE = 16
ENCODING = "utf-8"
CORPUS = string.ascii_letters + string.digits + "./"  # The letters that can form a password
SALT = "rand!{0}vgh8{1}f4fwd32"  # For hash we salt
HOME_NAME = "G404-5(Home)"  # No place like home
TARGET_NAME = "G777(Target)"
FLASHING = "\033[6m{0}\033[0m"  # :)
MOTP = """
Hi There!
This is the dormitory guard service!
Today, as you may know, everything becomes digitalized.
So we provided you with a digital interface to open your apartment's lock.
Unfortunately, we have not yet manged to teleport objects from your apartment and back :(
But hey! enjoy seeing your door opened when you enter your room's key!
NOTE: in order to support legacy systems, we implemented the lock's mechanisms to match a normal, cylinder lock.
You can find a reference in the PDF attached (No PDF malware there, guaranteed), and (part of the code) here.
THIS IS THE ONLY SOURCE OF INFORMATION YOU HAVE.    
Note that each letter corresponds to a pin.
To further enhance security, we are using 16 pin keys with 64 options for each (2_LOOK_INSIDE^96 options for a key!).

You are provided with the private key to G404-5(Home).
The password to the next level is the private key to G777(Target) door.
Behatzlaha.
"""


class Lock(object):  # My implementation, enjoy.

    @staticmethod
    def hash(apartment, key):
        assert len(key) == 16
        assert all([c in CORPUS for c in key])
        return sha(SALT.format(apartment, key).encode(ENCODING)).hexdigest()

    @staticmethod
    def from_file(path):
        with open(path, "r+")as f:
            return Lock(*json.loads(f.read()))

    @staticmethod
    def from_raw_keys(apartment, private_key, master_key, is_home=False):
        from key_setup import get_hashes
        return Lock(apartment, get_hashes(apartment, private_key, master_key), private_key, is_home)

    def __init__(self, apartment, hashes, pkey=None, is_home=False):
        self._apt = apartment
        self._is_home = is_home
        self._pkey = pkey
        self._hashes = hashes
        

    def to_file(self, path):
        with open(path, "w+") as f:
            json.dump([self._apt, self._hashes, self._pkey if self._is_home else None], f)

    def success(self):
        print(FLASHING.format("Correct key! \nDoor of {0} opened!".format(self._apt)))

    def fail(self):
        print(("Wrong key! \nDoor of {0} \033[91mlocked!\033[0m \n\n" + FLASHING.format(
            "Remember!, your private key is {1}")).format(self._apt,
                                                          self._pkey if self._pkey is not None else "not here!"))

    def try_open(self, key):
        h = Lock.hash(self._apt, key)
        if h in self._hashes:
            return True
        else:
            return False


def main():
    if DEBUG:
        from key_setup import main as ksmain
        ksmain()

    else:
        parser = argparse.ArgumentParser(description=MOTP)
        parser.add_argument("-i", "--iknowthekey", help="Try a key on your target door", action="store_true")
        parser.add_argument("key", help="Your key, {0} chars from corpus".format(DEFAULT_KEY_SIZE))
        lhome = Lock.from_file(HOME_NAME + ".txt")
        ltarg = Lock.from_file(TARGET_NAME + ".txt")
        args = parser.parse_args()
        if args.iknowthekey:
            door = ltarg
        else:
            door = lhome

        if door.try_open(args.key):
            door.success()
            exit(0x31337)
        else:
            door.fail()
            exit(-1)


if __name__ == '__main__':
    main()
