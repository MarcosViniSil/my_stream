export async function uploadVideo(file) {
  const formData = new FormData();
  formData.append("file", file);

  try {
    const response = await fetch("http://172.26.100.134:8000/upload/video", {
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
