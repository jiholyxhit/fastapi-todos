from fastapi import APIRouter, Depends

from schema.request import SignUpRequest
from schema.response import UserSchema

from service.user import UserService

from database.orm import User

from database.repository import UserRepository

from

router = APIRouter(prefix = "/users")


@router.post("/sign-up", status_code=201)
def user_sign_up_handler(
        request: SignUpRequest,
        user_service: UserService = Depends(),
        user_repo: UserRepository = Depends(),
    ):
    #1. request(schema) body(username, password)
    #2. password -> hashing -> hashed_password (UserService Dependency)
    hashed_password: str = user_service.hash_password(
        plain_password = request.password
    )
    #3. ORM User(username, hashed_password)
    # user ORM obj
    user: User = User.create(
        username=request.username,
        hashed_password=hashed_password
    )
    #4. user -> db save (repository)
    #DB save + id generate
    user: User = user_repo.save_user(user=user) #id = int

    #5. return user(id, username)
    #Response Schema
    return UserSchema.model_validate(user)