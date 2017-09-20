SALT_API = {"url": "https://172.16.234.105:8000",
            "user": "salt",
            "password": "salt"
}

SSH_LOCAL = {"username": "appuser",
             "password": "4rfv5tgb^YHN"
}

import string, random

def random_char(y):
    return ''.join(random.choice(string.ascii_letters) for x in range(y))
