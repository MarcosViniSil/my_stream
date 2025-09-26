export async function createUser(user) {

    let userBody = {
        "name": user.name,
        "email": user.email,
        "password": user.password
    }


    try {
        const response = await fetch("http://172.26.100.134:8000/sign/up", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(userBody),
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData?.detail || "Erro ao criar usuário");
        }

        return response.json();
    } catch (error) {
        throw new Error(error.message || "Erro ao criar usuário");
    }
}

export async function loginUser(user) {

    let userBody = {
        "email": user.email,
        "password": user.password
    }


    try {
        const response = await fetch("http://172.26.100.134:8000/sign/in", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            credentials: "include",
            body: JSON.stringify(userBody),
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData?.detail || "Erro ao criar usuário");
        }

        return response.json();
    } catch (error) {
        throw new Error(error.message || "Erro ao criar usuário");
    }
}

export async function getUserDatasAPI() {

    try {
        const response = await fetch("http://172.26.100.134:8000/user/datas", {
            method: "GET",
            //credentials: "include",
        });

        if (!response.ok) {
            const errorData = await response.json();
            const err = new Error(errorData?.detail || "Erro ao atualizar dados");
            err.status = response.status;
            throw err;
        }

        return response.json();
    } catch (error) {
        throw error;
    }
}

export async function updateUserDatas(user) {

    let userBody = {
        "userName": user.userName,
        "userEmail": user.userEmail
    }


    try {
        const response = await fetch("http://172.26.100.134:8000/user/datas", {
            method: "PUT",
            headers: {
                "Content-Type": "application/json"
            },
            //credentials: "include",
            body: JSON.stringify(userBody),
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw { status: response.status, message: errorData?.detail || "Erro ao realizar dislike no vídeo" };
        }

        return response.json();
    } catch (error) {
        throw new Error(error.message || "Erro ao obter dados do perfil");
    }
}

export async function sendCodeService(email) {
    try {
        const response = await fetch(`http://172.26.100.134:8000/user/code?email=${email}`, {
            method: "GET",
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData?.detail || "Erro ao criar usuário");
        }

        return response.json();
    } catch (error) {
        throw new Error(error.message || "Erro ao criar usuário");
    }
}

export async function verifyCodeService(email, code) {
    try {
        const response = await fetch(`http://172.26.100.134:8000/user/verify/code?email=${email}&code=${code}`, {
            method: "GET",
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData?.detail || "Erro ao criar usuário");
        }

        return response.json();
    } catch (error) {
        throw new Error(error.message || "Erro ao criar usuário");
    }
}

export async function updatePassword(email, code, password) {
    const body = {
        "email": email,
        "code": code,
        "password": password
    }
    try {
        const response = await fetch(`http://172.26.100.134:8000/user/password`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(body)
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData?.detail || "Erro ao atualziar senha");
        }

        return response.json();
    } catch (error) {
        throw new Error(error.message || "Erro ao atualziar senha");
    }
}