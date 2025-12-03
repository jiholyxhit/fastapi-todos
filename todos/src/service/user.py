import bcrypt

class UserService:
    encoding: str = "UTF-8"

    def hash_password(self, plain_password: str) -> str:
        hashed_password: bytes = bcrypt.hashpw(
            plain_password.encode(self.encoding), #str => bytes (arg format of bcrpyt)
            salt = bcrypt.gensalt(),
        )
        return hashed_password.decode(self.encoding) #bytes => str (return format of bcrypt => return forma of hash_password)

