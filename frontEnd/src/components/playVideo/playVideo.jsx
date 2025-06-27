import React, { useEffect, useRef, useState } from "react";
import Hls from "hls.js";
import { FaPlay } from "react-icons/fa";
import { FaPause } from "react-icons/fa";
import { MdFullscreen } from "react-icons/md";
import { IoVolumeMedium } from "react-icons/io5";
import { FaVolumeXmark } from "react-icons/fa6";//mutado
import { IoIosVolumeHigh } from "react-icons/io";//maximo





import "./playVideo.css";

function VideoPlayer() {
  const videoRef = useRef(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [progress, setProgress] = useState(0);
  const [volume, setVolume] = useState(0.4);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);

  useEffect(() => {
    const video = videoRef.current;
    if (Hls.isSupported()) {
      const hls = new Hls();
      hls.loadSource("http://localhost:9000/python-test-bucket/a2ef4a28-7a94-4156-b33c-384dc2cecce6/output.m3u8");
      hls.attachMedia(video);
      hls.on(Hls.Events.MANIFEST_PARSED, () => {
        video.play();
        setIsPlaying(true);
      });
    } else if (video.canPlayType("application/vnd.apple.mpegurl")) {
      video.src = "http://localhost:9000/python-test-bucket/a2ef4a28-7a94-4156-b33c-384dc2cecce6/output.m3u8";
      video.addEventListener("loadedmetadata", () => {
        video.play();
        setIsPlaying(true);
      });
    }

    const handleTimeUpdate = () => {
      const progress = (video.currentTime / video.duration) * 100;
      setProgress(progress);
    };

    const updateTime = () => {
      setCurrentTime(video.currentTime);
    };

    const setMetaData = () => {
      setDuration(video.duration);
    }

    video.addEventListener("timeupdate", updateTime);
    video.addEventListener("loadedmetadata", setMetaData);

    video.addEventListener("timeupdate", handleTimeUpdate);

    return () => {
      video.removeEventListener("timeupdate", handleTimeUpdate);
    };

  }, []);

  const formatTime = (duration) => {
    if (isNaN(duration)) return "0:00";
    if (duration >= 3600) {
      let hours = Math.floor(duration / 3600);
      duration %= 3600;
      let minutes = Math.floor(duration / 60);
      minutes = String(minutes).padStart(2, "0");
      let seconds = Math.floor(duration % 60);
      seconds = String(seconds).padStart(2, "0");
      return `${hours}:${minutes}:${seconds}`
    } else if (duration > 60 && duration < 3600) {
      let minutes = Math.floor(duration / 60);
      let seconds = Math.floor(duration % 60);
      seconds = String(seconds).padStart(2, "0");
      return `${minutes}:${seconds}`
    } else {
      let seconds = Math.floor(duration % 60);
      seconds = String(seconds).padStart(2, "0");
      return `0:${seconds}`
    }

  }

  const togglePlay = () => {
    const video = videoRef.current;
    if (video.paused) {
      video.play();
      setIsPlaying(true);
    } else {
      video.pause();
      setIsPlaying(false);
    }
  };

  const handleProgressChange = (e) => {
    const video = videoRef.current;
    const newTime = (e.target.value / 100) * video.duration;
    video.currentTime = newTime;
    setProgress(e.target.value);

  };

  const handleVolumeChange = (e) => {
    const video = videoRef.current;
    const newVolume = e.target.value;
    video.volume = newVolume;
    setVolume(newVolume);
    if(e.target.value == 0){
      //mutado
    }else if(e.target.value == 1){
      //maximo
    }else{
      //medio
    }
  };

  const handleFullscreen = () => {
    const video = videoRef.current;

    if (!document.fullscreenElement) {
      video.requestFullscreen();
    } else {
      document.exitFullscreen();
    }
  }

  return (
    <div className="videoContainer">
      <div className="wrapVideo">
        <video ref={videoRef} className="videoPlayer" />
        <div className="controls">

          <div className="wrapProgress">
            <input id="progress" type="range" min="0" max="100" value={progress} onChange={handleProgressChange} style={{
              '--progress': `${progress}%`
            }} />
          </div>

          <div className="wrapControls">
            <div className="volumeTimeAndPlay">
              
              <button onClick={togglePlay}> {isPlaying ? <FaPause/> : <FaPlay />} </button>
              
              <div className="wrapVolume">
                <label htmlFor="volume"> {volume == 0 ? <FaVolumeXmark className="volumeIconMuted"/>:volume == 1 ? <IoIosVolumeHigh className="volumeIconMax"/>:<IoVolumeMedium className="volumeIcon" />}</label>
                <input id="volume" type="range" min="0" max="1" step="0.01" value={volume} onChange={handleVolumeChange} style={{
                  '--progress': `${volume * 100}%`
                }} />
              </div>

              <div className="timeDisplay">
                {<p className="wrapTimeVideo"><p className="wrapTimeVideoCurrent">{formatTime(currentTime)}</p> <p className="separator"> / </p> <p className="wrapTimeVideoTotal">{formatTime(duration)}</p></p>}
              </div>

            </div>


            <MdFullscreen className="fullScreen" onClick={handleFullscreen} />
          
          </div>
        </div>
      </div>
    </div>
  );
}

export default VideoPlayer;
