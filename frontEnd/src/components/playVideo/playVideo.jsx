import React, { useEffect, useRef, useState } from "react";
import Hls from "hls.js";
import { FaPlay } from "react-icons/fa";
import { FaPause } from "react-icons/fa";
import { MdFullscreen } from "react-icons/md";
import { IoIosVolumeLow } from "react-icons/io";
import { IoIosVolumeOff } from "react-icons/io";
import { IoIosVolumeHigh } from "react-icons/io";
import { FaVolumeXmark } from "react-icons/fa6";
import { AiFillLike } from "react-icons/ai";
import { AiFillDislike } from "react-icons/ai";

import "./playVideo.css";

function VideoPlayer({ videoDatas,timeAt }) {
  const videoRef = useRef(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [progress, setProgress] = useState(0);
  const [volume, setVolume] = useState(0.4);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);
  const [showControls, setShowControls] = useState(true);
  const [showUnmuteButton, setShowUnmuteButton] = useState(true);
  const [isMobile, setIsMobile] = useState(false)

  useEffect(() => {
    const video = videoRef.current;
    if (Hls.isSupported()) {
      const hls = new Hls();
      hls.loadSource(videoDatas.videoUrl);
      hls.attachMedia(video);
      hls.on(Hls.Events.MANIFEST_PARSED, () => {
         video.currentTime = timeAt;
        setIsPlaying(true);
        
      });
    } else if (video.canPlayType("application/vnd.apple.mpegurl")) {
      video.src = videoDatas.videoUrl;
      video.addEventListener("loadedmetadata", () => {
        video.currentTime = timeAt;
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

  useEffect(() => {
    const handleResize = () => {
      const width = window.innerWidth;

      if (width <= 700 && isUserOnMobile()) {
        setIsMobile(true)
      } else {
        setIsMobile(false)
      }
    };

    handleResize();

    window.addEventListener("resize", handleResize);

    return () => {
      window.removeEventListener("resize", handleResize);
    };
  }, []);

  useEffect(() => {
    let timeout;
    const wrapper = videoRef.current.parentElement;

    const handleMouseMove = () => {
      setShowControls(true);
      clearTimeout(timeout);
      timeout = setTimeout(() => setShowControls(false), 3000);
    };

    wrapper.addEventListener('mousemove', handleMouseMove);

    return () => {
      wrapper.removeEventListener('mousemove', handleMouseMove);
      clearTimeout(timeout);
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
      video.play().then(() => setIsPlaying(true));
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
  };

  const handleFullscreen = () => {
    const wrapper = videoRef.current.parentElement;
    if (!document.fullscreenElement) {
      wrapper.requestFullscreen();
    } else {
      document.exitFullscreen();
    }
  }

  const unmute = () => {
    const video = videoRef.current;
    video.muted = false;
    video.volume = 0.5;
    setShowUnmuteButton(false);
  };

  const isUserOnMobile = () => {
    let isMobile = window.navigator.userAgentData.mobile;
    return isMobile
  }

  return (
    <div className="wrapAll">
      <div className="videoContainer">
        <div className="wrapVideo">
          
          <video onClick={togglePlay} muted autoPlay ref={videoRef} className="videoPlayer" />
          
          <div className={`controls ${!showControls ? 'hideControls' : ''}`}>

            <div className="wrapProgress">
              <input id="progress" type="range" min="0" max="100" value={progress} onChange={handleProgressChange} style={{
                '--progress': `${progress}%`
              }} />
            </div>

            <div className="wrapControls">
              <div className="volumeTimeAndPlay">

                <button onClick={togglePlay}> {isPlaying ? <FaPause /> : <FaPlay />} </button>

                {!isMobile && (<div className="wrapVolume">
                  <label id="labelVolume" htmlFor="volume"> {volume == 0 ? <p className="volumeIcon"><IoIosVolumeOff /></p> : volume == 1 ? <p className="volumeIcon"> <IoIosVolumeHigh /> </p> : <p className="volumeIconLow"><IoIosVolumeLow /></p>}</label>
                  <input id="volume" type="range" min="0" max="1" step="0.01" value={volume} onChange={handleVolumeChange} style={{
                    '--progress': `${volume * 100}%`
                  }} />
                </div>)}

                <div className="timeDisplay">
                  {<div className="wrapTimeVideo">
                    <span className="wrapTimeVideoCurrent">{formatTime(currentTime)}</span>
                    <span className="separator"> / </span>
                    <span className="wrapTimeVideoTotal">{formatTime(duration)}</span>
                  </div>}
                </div>

              </div>
              <MdFullscreen className="fullScreen" onClick={handleFullscreen} />
            </div>

          </div>
          {showUnmuteButton && (
            <button id="buttonActivateSound" onClick={unmute}>
              <FaVolumeXmark />
              Clique para ativar o som
            </button>
          )}
        </div>
        <div className="wrapDatasVideo">
          <div className="wrapAuthorAndTitle">
            <h3>{videoDatas.videoTitle}</h3>
            <p>criado por {videoDatas.userName} em {videoDatas.videoDate}</p>
          </div>
          <div className="likesAndDislikes">
            <p className="likes"> <AiFillLike /> <span className="valueLD">{videoDatas.likes}</span>  </p>
            <p className="dislikes"> <AiFillDislike />  <span className="valueLD">{videoDatas.dislikes}</span> </p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default VideoPlayer;
