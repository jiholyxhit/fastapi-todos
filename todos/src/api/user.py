from fastapi import APIRouter, Depends, HTTPException

from schema.request import SignUpRequest, LogInRequest
from schema.response import UserSchema, JWTResponse

from service.user import UserService

from database.orm import User

from database.repository import UserRepository


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


@router.post("/log-in")
def user_log_in_handler(
        request: LogInRequest,
        user_service: UserService = Depends(),
        user_repo: UserRepository = Depends(),

):
    #1. request body(username, password)

    #2. db read user
    user: User | None = user_repo.get_user_by_username(
        username=request.username
    )
    if not user:
        raise HTTPException(status_code=404, detail="User Not Found")

    #3. user.password, request.password -> bcrpyt.checkpw
    verified: bool = user_service.verify_password(
        plain_password = request.password,
        hashed_password = user.password,
    )
    if not verified:
        raise HTTPException(status_code=401, detail="Not Authorized")

    #4. create jwt (User Service)
    access_token: str = user_service.create_jwt(username = user.username)

    #5. return jwt
    return JWTResponse(access_token=access_token)