import React, { useEffect, useRef } from "react";
import Hls from "hls.js";

function VideoPlayer() {
  const videoRef = useRef();

  useEffect(() => {
    const video = videoRef.current;
    if (Hls.isSupported()) {
      const hls = new Hls();
      hls.loadSource("http://localhost:9000/python-test-bucket/020f63a0-75f7-4601-a0d2-ce00f86d1bfa/output.m3u8"); // endpoint da API que entrega o m3u8 com URLs assinadas
      hls.attachMedia(video);
      hls.on(Hls.Events.MANIFEST_PARSED, () => {
        video.play();
      });
    } else if (video.canPlayType("application/vnd.apple.mpegurl")) {
      video.src = "http://localhost:9000/python-test-bucket/020f63a0-75f7-4601-a0d2-ce00f86d1bfa/output.m3u8";
      video.addEventListener("loadedmetadata", () => {
        video.play();
      });
    }
  }, []);

  return <video ref={videoRef} controls style={{ width: "100%" }} />;
}

export default VideoPlayer;
