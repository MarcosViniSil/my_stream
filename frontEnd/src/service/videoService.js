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
      throw new Error(errorData?.detail || "Erro ao enviar o vídeo"); 
    }

    return response.json();
  } catch (error) {
    throw new Error(error.message || "Erro ao enviar o vídeo");
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
      throw new Error(errorData?.detail || "Erro ao enviar o vídeo"); 
    }

    return response.json();
  } catch (error) {
    throw new Error(error.message || "Erro ao enviar o vídeo");
  }
}

export async function deleteVideo(videoId) {
  const formData = new FormData();
  
  const token = "";
  formData.append("tokenUser", token);
  formData.append("videoId", videoId);

  try {
    const response = await fetch("http://localhost:8000/user/video", {
      method: "DELETE",
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
