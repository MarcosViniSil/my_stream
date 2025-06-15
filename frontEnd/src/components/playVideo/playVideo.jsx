import React, { useEffect, useRef } from "react";
import Hls from "hls.js";

function VideoPlayer() {
  const videoRef = useRef();

  useEffect(() => {
    const video = videoRef.current;
    if (Hls.isSupported()) {
      const hls = new Hls();
      hls.loadSource("http://localhost:9000/python-test-bucket/35005a0c-5976-4572-834f-d6f21807e757/output.m3u8");
      hls.attachMedia(video);
      hls.on(Hls.Events.MANIFEST_PARSED, () => {
        video.play();
      });
    } else if (video.canPlayType("application/vnd.apple.mpegurl")) {
      video.src = "http://localhost:9000/python-test-bucket/35005a0c-5976-4572-834f-d6f21807e757/output.m3u8";
      video.addEventListener("loadedmetadata", () => {
        video.play();
      });
    }
  }, []);

  return <video ref={videoRef} controls style={{ width: "100%" }} />;
}

export default VideoPlayer;
