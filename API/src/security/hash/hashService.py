import bcrypt

def createHashForPassword(password:str) -> str:
    if password is None:
        raise ValueError(f"A senha não foi informada")
    
    passwordBytes = password.encode("utf-8")

    try:
        passwordHash = bcrypt.hashpw(passwordBytes, bcrypt.gensalt())
        return passwordHash
    except Exception as e:
        raise ValueError(f"Não foi possível gerar o hash da senha informada, tente novamente {e} [DEV]")

def isPasswordEqualDB(hashDataBase:bytes, password:str) -> bool:
    if hashDataBase is None or password is None:
        raise ValueError(f"Senha ou hashing não informado")
    
    passwordBytes = password.encode("utf-8")
    
    try:
        if bcrypt.checkpw(passwordBytes, hashDataBase):
            return True
        else:
            return False
    except Exception as e:
        raise ValueError(f"Ocorreu um erro ao verificar senha, erro: {e} [DEV]")
