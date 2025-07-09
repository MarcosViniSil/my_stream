from fastapi import APIRouter, Depends
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
async def createUser(
    user: Userlogin,
    userService: UserService = Depends(getUserService)
):
    return userService.logInUser(user)

