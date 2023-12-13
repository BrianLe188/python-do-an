import bcrypt

def hash_password(password):
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    return hashed

def verify_password(raw, hash):
    if bcrypt.checkpw(raw, hash):
      return True
    return False
