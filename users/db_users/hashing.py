from passlib.context import CryptContext


password_context = CryptContext(
    schemes=[
        "bcrypt",
    ],
    deprecated="auto",
)


class Hash:
    def bcrypt(self, password):
        return password_context.hash(password)

    def verify(self, hashed_password, given_password):
        return password_context.verify(given_password, hashed_password)
