export async function uploadVideo(file) {
  const formData = new FormData();
  formData.append("file", file);

  try {
    const response = await fetch("http://localhost:8000/upload/video", {
      method: "POST",
      credentials: "include",
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

export async function isCookieValid() {

  try {
    const response = await fetch("http://localhost:8000/user/token", {
      method: "GET",
      credentials: "include",
    });

    if (!response.ok) {
      const errorData = await response.json();
      console.log(errorData)
      const err = new Error(errorData?.detail || "Erro ao atualizar dados");
      err.status = response.status;
      throw err;
    }

    return response.json();
  } catch (error) {
    throw error
  }
}


export async function getQuantityVideos() {
  try {
    const response = await fetch("http://localhost:8000/user/videos/quantity", {
      method: "POST",
      credentials: "include",
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

  formData.append("offset", offset);

  try {
    const response = await fetch("http://localhost:8000/user/videos", {
      method: "POST",
      credentials: "include",
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

  formData.append("videoId", videoId);

  try {
    const response = await fetch(`http://localhost:8000/user/video?videoId=${videoId}`, {
      method: "DELETE",
      credentials: "include",
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

  try {
    const response = await fetch(`http://localhost:8000/videos?offset=${offset}`, {
      method: "GET",
      credentials: "include",
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
  try {
    const response = await fetch(`http://localhost:8000/videos/query/?param=${query}`, {
      method: "GET",
      //credentials: "include",
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
    const response = await fetch(`http://localhost:8000/streaming/video?videoId=${videoId}`, {
      method: "GET",
      credentials: "include",
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
  try {
    const response = await fetch(`http://localhost:8000/videos/history/?offset=${offset}`, {
      method: "GET",
      credentials: "include",
    });

    if (!response.ok) {
      const errorData = await response.json();

      let message = "Erro ao buscar histórico";
      if (Array.isArray(errorData?.detail)) {
        message = errorData.detail.map(d => `${d.loc?.join('.')}: ${d.msg}`).join(' | ');
      } else if (typeof errorData?.detail === 'string') {
        message = errorData.detail;
      }

      const err = new Error(message);
      err.status = response.status;
      throw err;
    }

    return response.json();
  } catch (error) {
    if (!error.status) {
      error.status = 0;
    }
    console.log(error);
    throw error;
  }
}


export async function addLike(videoId) {
  const formData = new FormData();
  formData.append("videoId", videoId);

  const response = await fetch("http://localhost:8000/video/like", {
    method: "POST",
    credentials: "include",
    body: formData,
  });

  if (!response.ok) {
    const errorData = await response.json();
    const error = new Error(errorData?.detail || "Erro ao realizar o like em um vídeo");
    error.status = response.status;
    throw error;
  }

  return response.json();
}


export async function addDisLike(videoId) {
  const formData = new FormData();
  formData.append("videoId", videoId);

  try {
    const response = await fetch("http://localhost:8000/video/dislike", {
      method: "POST",
      credentials: "include",
      body: formData,
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw { status: response.status, message: errorData?.detail || "Erro ao realizar dislike no vídeo" };
    }

    return response.json();
  } catch (error) {
    if (error.status) throw error;
    throw { status: 0, message: error.message || "Erro desconhecido ao enviar dislike" };
  }
}






