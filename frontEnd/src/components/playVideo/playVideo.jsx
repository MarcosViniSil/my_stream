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
import { MdSubtitles } from "react-icons/md";
import { MdSubtitlesOff } from "react-icons/md";
import { addDisLike, addLike } from '../../service/videoService.js'
import {
  Popover,
  PopoverTrigger,
  PopoverContent,
  Box,
  PopoverBody,
  Link,
} from "@chakra-ui/react";

import "./playVideo.css";
import { useNavigate } from "react-router-dom";

function VideoPlayer({ videoDatas, timeAt, onTimeUpdate }) {
  const videoRef = useRef(null);
  const navigate = useNavigate();
  const [isPlaying, setIsPlaying] = useState(false);
  const [progress, setProgress] = useState(0);
  const [volume, setVolume] = useState(0.4);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);
  const [showControls, setShowControls] = useState(true);
  const [showUnmuteButton, setShowUnmuteButton] = useState(true);
  const [isMobile, setIsMobile] = useState(false)
  const [isSubtitle, setIsSubtitle] = useState(false)
  const [like, setLike] = useState(0)
  const [dislike, setDislike] = useState(0)
  const [isFetching, setIsFetching] = useState(false)
  const [reaction, setReaction] = useState(0);
  const [showTooltip, setShowToolTip] = useState(false)
  const [showTooltip2, setShowToolTip2] = useState(false)
  const [messageLike, setMessageLike] = useState("Você precisa estar logado para curtir o vídeo.")
  const [messageDisLike, setMessageDisLike] = useState("Você precisa estar logado para reagir ao vídeo.")
  
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
      onTimeUpdate(video)
    };

    const setMetaData = () => {
      setDuration(video.duration);
    }
    console.log(videoDatas.videoSubtitles)
    setLike(formatReactionNumber(videoDatas.likes))
    setDislike(formatReactionNumber(videoDatas.dislikes))
    setReaction(videoDatas.reaction || 0);

    video.addEventListener("timeupdate", updateTime);
    video.addEventListener("loadedmetadata", setMetaData);

    video.addEventListener("timeupdate", handleTimeUpdate);

    return () => {
      video.removeEventListener("timeupdate", handleTimeUpdate);
    };



  }, []);


  useEffect(() => {
    const video = videoRef.current;
    if (!video) return;
    if (!video.textTracks || video.textTracks.length === 0) return;

    const track = video.textTracks[0];

    track.mode = isSubtitle ? "showing" : "disabled";
  }, [isSubtitle]);

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
      timeout = setTimeout(() => setShowControls(false), 800);
    };

    wrapper.addEventListener('mousemove', handleMouseMove);

    return () => {
      wrapper.removeEventListener('mousemove', handleMouseMove);
      clearTimeout(timeout);
    };
  }, []);

  const formatReactionNumber = (number) => {
    if (isNaN(number)) {
      return 0;
    }

    if (number < 1000) {
      return number
    }

    if (number >= 1000 && number <= 999999) {
      const res = Math.floor(number / 1000)
      return `${res} mil`
    }

    if (number >= 1000000 && number <= 999999999) {
      const res = Math.floor(number / 1000000)
      return `${res} mi`
    }

    if (number >= 1000000000 && number <= 99999999999) {
      const res = Math.floor(number / 1000000000)
      return `${res} bi`
    }

  }

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
    let isMobile = /Mobi|Android/i.test(navigator.userAgent);
    return isMobile
  }

  const changeSubtitles = () => {
    if (videoDatas.videoSubtitles == "") {
      return
    }
    setIsSubtitle(prev => !prev)
    const track = videoRef.current.textTracks[0];
    if (isSubtitle && track) {
      track.mode = "disabled";
    } else {
      track.mode = "showing";
    }

  }

  const sendLike = async () => {
    const videoId = videoDatas.videoId
    if (!videoId || isFetching) {
      return
    }
    setIsFetching(true)
    try {
      await addLike(videoId);

      if (reaction === 1) {
        setLike(prev => prev - 1);
        setReaction(0);
      } else {
        setLike(prev => prev + 1);
        if (reaction === -1) {
          setDislike(prev => prev - 1);
        }
        setReaction(1);
      }

    } catch (err) {
      if (err.status === 422) {
        setShowToolTip(true)
      } else if (err.status === 401) {
        console.log("erro 401")
         setMessageLike("O seu login expirou, realize novamente o login para poder curtir o vídeo")
          setShowToolTip(true);
         console.log(messageLike)
      } else {
        alert("Erro inesperado ao curtir o vídeo.");
      }
    } finally {
      setIsFetching(false);
    }
  }

  const sendDisLike = async () => {
    const videoId = videoDatas.videoId
    if (!videoId || isFetching) {
      return
    }
    setIsFetching(true);
    try {
      await addDisLike(videoDatas.videoId);

      if (reaction === -1) {
        setDislike(prev => prev - 1);
        setReaction(0);
      } else {
        setDislike(prev => prev + 1);
        if (reaction === 1) {
          setLike(prev => prev - 1);
        }
        setReaction(-1);
      }

    } catch (err) {
      console.log(err)
    if (err.status === 422) {
        setShowToolTip2(true)
      } else if (err.status === 401) {
        setMessageDisLike("O seu login expirou, realize o login novamente para poder reagir")
        setShowToolTip2(true)
      } else {
        alert("Erro inesperado ao curtir o vídeo.");
      }
  
    } finally {
      setIsFetching(false);
    }
  }

  const handleLoginClick = () => {
    navigate("/login")
  }

  return (
    <div className="wrapAll">
      <div className="videoContainer">
        <div className={`wrapVideo ${!showControls ? 'hideCursor' : ''}`}>

          <video crossOrigin="anonymous" onClick={togglePlay} muted autoPlay ref={videoRef} className="videoPlayer">
            {videoDatas.videoSubtitles != "" && (
              <track
                src={videoDatas.videoSubtitles}
                kind="subtitles"
                srcLang="pt"
                label="Português"
                default
              />
            )}


          </video>

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
              <div className="containerSubtitlesAndFullScreen">
                <div onClick={changeSubtitles}>
                  {isSubtitle ? (
                    <MdSubtitles className="subTitles" />
                  ) : (
                    <MdSubtitlesOff className="subTitles" />
                  )}
                </div>

                <MdFullscreen className="fullScreen" onClick={handleFullscreen} />
              </div>

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
            <p className="authorPlayVideo">criado por {videoDatas.userName} em {videoDatas.videoDate}</p>
          </div>
          <div className="likesAndDislikes">
            <Popover
              boxShadow="none"
              border="none"
              isOpen={showTooltip}
              onClose={() => setShowToolTip(false)}
            >
              <PopoverTrigger>
                <button
                  onClick={sendLike}
                  className={`likes ${reaction === 1 ? "activeLike" : ""}`}
                >
                  <AiFillLike className="iconLike" />
                  <span className="valueLD">{formatReactionNumber(like)}</span>
                </button>
              </PopoverTrigger>
              <PopoverContent
                bg="#212121"
                border="none"
                boxShadow="none"
                borderRadius="md"
              >
                <PopoverBody bg="#212121cb" p={4} borderRadius="md">
                  <Box textAlign="center" color="white">
                    { messageLike }
                    <br />
                    <Link
                      onClick={handleLoginClick}
                      display="block"
                      mt={2}
                      color="white"
                      cursor="pointer"
                      fontWeight="bold"
                      _hover={{ color: "#4caf50", textDecoration: "underline" }}
                    >
                      login
                    </Link>
                  </Box>
                </PopoverBody>
              </PopoverContent>
            </Popover>

            <Popover
              boxShadow="none"
              border="none"
              isOpen={showTooltip2}
              onClose={() => setShowToolTip2(false)}
            >
              <PopoverTrigger>
                <button
                  onClick={sendDisLike}
                  className={`dislikes ${reaction === -1 ? "activeDislike" : ""}`}
                >
                  <AiFillDislike className="iconDisLike" />
                  <span className="valueLD">{formatReactionNumber(dislike)}</span>
                </button>
              </PopoverTrigger>
              <PopoverContent
                bg="#212121"
                border="none"
                boxShadow="none"
                borderRadius="md"
              >
                <PopoverBody bg="#212121cb" p={4} borderRadius="md">
                  <Box textAlign="center" color="white">
                    {messageDisLike}
                    <br />
                    <Link
                      onClick={handleLoginClick}
                      display="block"
                      mt={2}
                      color="white"
                      cursor="pointer"
                      fontWeight="bold"
                      _hover={{ color: "#4caf50", textDecoration: "underline" }}
                    >
                      login
                    </Link>
                  </Box>
                </PopoverBody>
              </PopoverContent>
            </Popover>
          </div>

        </div>
      </div>
    </div>
  );
}

export default VideoPlayer;