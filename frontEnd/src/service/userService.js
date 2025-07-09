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