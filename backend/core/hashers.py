from django.contrib.auth.hashers import PBKDF2PasswordHasher


class FastPBKDF2PasswordHasher(PBKDF2PasswordHasher):
    algorithm = "pbkdf2_sha256"
    iterations = 240000
