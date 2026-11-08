import json
from hashlib import sha3_256 as sha  # The Future!!

import dorms_keys_managment

# home key: d7632vc47vp74v2d
# mailto:Netanelesman@gmail.com


if __name__ == "__main__":
    k = dorms_keys_managment.Lock.from_file(dorms_keys_managment.TARGET_NAME + ".txt")
    with open("a.txt", "w+") as f:
        json.dump([k._apt, k._apt, k._pkey], f)
    print(k)
    print(k._pkey)
    # print(k._hashes)
    print(k._is_home)
    print(k._apt)
    from hashlib import sha3_256 as sha  # The Future!!

    SALT = "rand!{0}vgh8{1}f4fwd32"  # For hash we salt

    h = sha(SALT.format(k._apt, k._hashes[0]).encode("utf-8")).hexdigest()
    print(h in k._hashes)
