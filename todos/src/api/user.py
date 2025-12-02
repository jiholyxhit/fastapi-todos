from fastapi import APIRouter


router = APIRouter(prefix = "/users")


@router.post("/sign-up", status_code=201)
def user_sign_up_handler():
    return True