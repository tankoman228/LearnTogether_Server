import hashlib
import password_hash

class Token:

    def __init__(self, text, is_admin, admin_level):
        self.hash = password_hash.hash_password(text)
        self.is_admin = is_admin
        self.admin_level = admin_level
