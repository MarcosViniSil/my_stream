from fastapi import APIRouter, Depends,Response,Cookie
from src.models.dependencies import getUserService
from src.models.user import UpdatePassword, User, UserDatas,Userlogin
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
    return {"message": token}

@userRouter.get("/user/datas")
async def loginUser(
    access_token: str = Cookie(...),
    userService: UserService = Depends(getUserService)
):
    
    return userService.getUserDatas(access_token)

@userRouter.put("/user/datas")
async def updateUserDatas(
    user: UserDatas,
    access_token: str = Cookie(...),
    userService: UserService = Depends(getUserService)
):
    
    return userService.updateUserDatas(user,access_token)

@userRouter.get("/user/code")
async def sendCodeToUser(
    email: str,
    userService: UserService = Depends(getUserService)
):
    
    return userService.sendCodeToUser(email)


@userRouter.get("/user/verify/code")
async def verifyToken(
    email: str,
    code:int,
    userService: UserService = Depends(getUserService)
):
    
    return userService.validateCode(email,code)

@userRouter.put("/user/password")
async def updatePassword(
    userPassword : UpdatePassword,
    userService: UserService = Depends(getUserService)
):
    
    return userService.updatePassword(userPassword)

@userRouter.get("/user/token")
async def updatePassword(
    access_token: str = Cookie(...),
    userService: UserService = Depends(getUserService)
):
    
    return userService.isTokenValid(access_token)
