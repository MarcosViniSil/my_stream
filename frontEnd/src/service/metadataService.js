export async function UploadMetaDatas(id,title,photo) {
  const formData = new FormData();
  formData.append("id", id);
  formData.append("videoTitle", title);
  formData.append("thumbnailImage", photo);

  try {
    const response = await fetch("http://172.26.100.134:8000/upload/metadata", {
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
