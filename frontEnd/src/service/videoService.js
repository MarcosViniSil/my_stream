export async function uploadVideo(file) {
  const formData = new FormData();
  formData.append("file", file);

  try {
    const response = await fetch("http://localhost:8000/upload/video", {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData?.detail || "Erro ao enviar o vídeo"); 
    }

    return response.json();
  } catch (error) {
    throw new Error(error.message || "Erro ao enviar o vídeo");
  }
}

export async function getQuantityVideos() {
  const formData = new FormData();
  const token = "";
  formData.append("tokenUser", token);

  try {
    const response = await fetch("http://localhost:8000/user/videos/quantity", {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData?.detail || "Erro ao obter quantidade de vídeos"); 
    }

    return response.json();
  } catch (error) {
    throw new Error(error.message || "Erro ao obter quantidade de vídeos");
  }
}

export async function getVideosUser(offset) {
  const formData = new FormData();
  
  const token = "";
  formData.append("tokenUser", token);
  formData.append("offset", offset);

  try {
    const response = await fetch("http://localhost:8000/user/videos", {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData?.detail || "Erro ao obter detalhes de vídeos do usuário"); 
    }

    return response.json();
  } catch (error) {
    throw new Error(error.message || "Erro ao obter detalhes de vídeos do usuário");
  }
}

export async function deleteVideo(videoId) {
  const formData = new FormData();
  
  const token = "";
  formData.append("tokenUser", token);
  formData.append("videoId", videoId);

  try {
    const response = await fetch(`http://localhost:8000/user/video?tokenUser=${token}&videoId=${videoId}`, {
      method: "DELETE",
      body: formData,
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData?.detail || "Erro ao deletar vídeo"); 
    }

    return response.json();
  } catch (error) {
    throw new Error(error.message || "Erro ao deletar vídeo");
  }
}

export async function getVideosInitialPage(offset) {
  const TOKEN_USER = "token"
  //const TOKEN_USER = "None"
  try {
    const response = await fetch(`http://localhost:8000/videos?token=${TOKEN_USER}&offset=${offset}`, {
      method: "GET"
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData?.detail || "Erro ao obter vídeos da página inicial"); 
    }

    return response.json();
  } catch (error) {
    throw new Error(error.message || "Erro ao obter vídeos da página inicial");
  }
}

export async function getVideosUserQuery(query) {
  const TOKEN = "aa"
  try {
    const response = await fetch(`http://localhost:8000/videos/query/?token=${TOKEN}&param=${query}`, {
      method: "GET"
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData?.detail || "Erro ao obter vídeos da página inicial"); 
    }

    return response.json();
  } catch (error) {
    throw new Error(error.message || "Erro ao obter vídeos da página inicial");
  }
}

export async function getDatasVideoToStream(videoId) {
  try {
    const response = await fetch(`http://localhost:8000/streaming/video/${videoId}`, {
      method: "GET"
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData?.detail || "Erro ao obter vídeos da página inicial"); 
    }

    return response.json();
  } catch (error) {
    throw new Error(error.message || "Erro ao obter vídeos da página inicial");
  }
}

export async function getHistory(offset) {
  const TOKEN_USER = "get on local storage"
  try {
    const response = await fetch(`http://localhost:8000/videos/history/?token=${TOKEN_USER}&offset=${offset}`, {
      method: "GET"
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData?.detail || "Erro ao obter vídeos da página inicial"); 
    }

    return response.json();
  } catch (error) {
    throw new Error(error.message || "Erro ao obter vídeos da página inicial");
  }
}






