# Projeto stream de vídeos
![Fase 3](assets/images/tela-inicial.PNG)
### O projeto tem como objetivo realizar o stream de um vídeo em mp4 enviado por um usuário

## Como funciona?
### Fase 1
![Fase 1](assets/images/fase-1.PNG)
### Fase 2
![Fase 2](assets/images/fase2.PNG)
### Fase 3
![Fase 3](assets/images/fase3.PNG)

## Tecnologias utilizadas

- FastApi(Python)
- Minio(bucket local)
- RabbitMQ
- MySql
- React(javaScript)
- Api Gemini
- ffmpeg

## Imagens da aplicação

### Tela inicial
![Fase 3](assets/images/pagina-inicial.PNG)

### Tela videos cadastrados
![Fase 3](assets/images/tela-envio.PNG)


## Geração de legendas
### A api go google gemini foi utilizada para geração de legendas de um vídeo, o áudio é extraido utilizando o `ffmpeg` e enviado para o google gemini para geração da legenda em formato `.vtt`, posteriormente utilizando a url da legenda no atributo `src` da tag `track` para exibição.
![Fase 3](assets/images/geracao-legenda.PNG)