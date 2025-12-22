import bcrypt, random, time
from datetime import datetime, timedelta
from jose import jwt


class UserService:
    encoding: str = "UTF-8"
    secret_key: str = "d0c41af11e7ea13922c4be551b9e96991314c8dff147299da0fceb0493f4cc5b"
    jwt_algorithm: str = "HS256"

    def hash_password(self, plain_password: str) -> str:
        hashed_password: bytes = bcrypt.hashpw(
            plain_password.encode(self.encoding), #str => bytes (arg format of bcrpyt)
            salt = bcrypt.gensalt(),
        )
        return hashed_password.decode(self.encoding) #bytes => str (return format of bcrypt => return forma of hash_password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(
            plain_password.encode(self.encoding),
            hashed_password.encode(self.encoding),
        )

    def create_jwt(self, username: str ) -> str: #payload: dict
        return jwt.encode(
    {
                "sub": username,
                "exp": datetime.now() + timedelta(days=1),
            },
            self.secret_key,
            algorithm = self.jwt_algorithm,
        )

    def decode_jwt(self, access_token: str) -> str:
        payload: dict = jwt.decode(
            access_token, self.secret_key, algorithms=[self.jwt_algorithm]
        )
        #expiration check
        return payload["sub"] #username

    @staticmethod
    def create_otp():
        return random.randint(1000, 9999)

    @staticmethod
    def send_email_to_user(email: str) -> None:
        time.sleep(10)
        print(f"Sending email to {email}")
