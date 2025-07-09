from fastapi import APIRouter, Depends,Response
from src.models.dependencies import getUserService
from src.models.user import User,Userlogin
from src.service.userService import UserService

userRouter = APIRouter()

@userRouter.post("/sign/up")
async def createUser(
    user: User,
    userService: UserService = Depends(getUserService)
):
    return userService.createUser(user)


@userRouter.post("/sign/in")
async def loginUser(
    user: Userlogin,
    response: Response,
    userService: UserService = Depends(getUserService)
):
    token = userService.logInUser(user)
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=True,
        samesite="Strict"
    )
    return {"message": "logado"}

