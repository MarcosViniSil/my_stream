export async function createUser(user) {

    let userBody = {
        "name": user.name,
        "email": user.email,
        "password": user.password
    }


    try {
        const response = await fetch("http://localhost:8000/sign/up", {
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
        const response = await fetch("http://localhost:8000/sign/in", {
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
        const response = await fetch("http://localhost:8000/user/datas", {
            method: "GET",
            credentials: "include",
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

export async function updateUserDatas(user) {

    let userBody = {
        "userName": user.userName,
        "userEmail": user.userEmail
    }


    try {
        const response = await fetch("http://localhost:8000/user/datas", {
            method: "PUT",
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