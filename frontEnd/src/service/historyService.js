export async function insertVideoOnHistory(videoId) {
  
  const formData = new FormData();
  const TOKEN_USER = "token"

  formData.append("tokenUser", TOKEN_USER);
  formData.append("videoId", videoId);

  try {
    const response = await fetch("http://localhost:8000/video/history", {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData?.detail || "Erro ao inserir video no histórico"); 
    }

    return response.json();
  } catch (error) {
    throw new Error(error.message || "Erro ao inserir video no histórico");
  }
}


export async function addTimeWatched(videoId,timeAt) {
  console.log(videoId)
  console.log(timeAt)
  timeAt = parseInt(timeAt, 10);
  const formData = new FormData();
  const TOKEN_USER = "token"

  formData.append("tokenUser", TOKEN_USER);
  formData.append("videoId", videoId);
  formData.append("timeWatched", timeAt);

  try {
    const response = await fetch("http://localhost:8000/video/time", {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData?.detail || "Erro ao adicionar tempo asistido"); 
    }

    return response.json();
  } catch (error) {
    throw new Error(error.message || "Erro ao adicionar tempo asistido");
  }
}