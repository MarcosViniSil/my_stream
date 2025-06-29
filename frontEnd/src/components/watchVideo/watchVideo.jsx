import React, { useEffect, useState, useRef } from 'react'
import { useLocation, useNavigate } from "react-router-dom";
import { getDatasVideoToStream } from '../../service/videoService.js'
import { insertVideoOnHistory, addTimeWatched } from '../../service/historyService.js'
import VideoPlayer from '../playVideo/playVideo'
import './watchVideo.css'

export default function WatchVideo() {
    const [video, setVideo] = useState("");
    const [timeStopped, setTimeStopped] = useState(0);
    const [count, setCount] = useState(0);
    const [dataVideo, setdataVideo] = useState(null)
    const [isFinished, setIsFinished] = useState(false)
    const intervalRef = useRef(null);
    const isFinishedRef = useRef(false);

    const location = useLocation();
    const navigate = useNavigate();

    useEffect(() => {
        const fetchData = async () => {
            const videoId = getVideoId()
            if (!videoId?.trim()) {
                navigate("/");
                return;
            }


            const timeStopped = getTimeSttoped()
            const videoData = await getDatasVideo(videoId)
            if (videoData == null) {
                navigate("/");
                return
            }

            if (timeStopped || timeStopped != null && isNaN(timeStopped) && timeStopped > 0) {
                console.log("complete")
                setTimeStopped(timeStopped)
                //make request with time stopped
            } else {
                setTimeStopped(0)
                console.log("without time stopped")
                //make request without time stopped
            }


            setVideo(videoData);

            await saveVideoOnHistory(videoId)

        }
        fetchData()
    }, []);

    useEffect(() => {
        if (dataVideo !== null) {
            const timeoutId = setTimeout(startCount, 10000);

            return () => {
                clearTimeout(timeoutId);
                if (intervalRef.current) {
                    clearInterval(intervalRef.current);
                }
            };
        }
    }, [dataVideo]);

    const getDatasVideo = async (videoId) => {
        if (!videoId || videoId == null || videoId == undefined || videoId.length == 0) {
            navigate("/");
        }

        try {
            const response = await getDatasVideoToStream(videoId)
            return response
        } catch (error) {
            console.log(error)
            return null
        }

    }

    const startCount = async () => {
        await sendTimeWatched()
        setCount(prevcount => prevcount + 1);
        intervalRef.current = setInterval(() => {
            setCount(async prevcount => {
                await sendTimeWatched()
                return prevcount + 1;
            });
        }, 10000);
    };

const sendTimeWatched = async () => {
    if (!dataVideo) return;

    const N = 10;

    if (isFinishedRef.current) {
        console.log("Já terminou, saindo...");
        return;
    }

    const willFinish = dataVideo.currentTime + N >= dataVideo.duration;

    if (willFinish || (!dataVideo.paused && Math.floor(dataVideo.currentTime) > 0 && dataVideo.currentTime <= dataVideo.duration)) {
        try {
            const videoId = getVideoId();
            if (!videoId?.trim()) {
                navigate("/");
                return;
            }

            await addTimeWatched(videoId, Math.floor(dataVideo.currentTime));
            console.log("Tempo enviado");

            if (willFinish) {
                setIsFinished(true);
                isFinishedRef.current = true; 
            }
        } catch (error) {
            console.error(error);
        }
    }
};

    const manageVideo = (video) => {

        if (!video) {
            return;
        }
        setdataVideo(video)
    }

    const saveVideoOnHistory = async (videoId) => {
        if (!videoId || videoId == null || videoId == undefined || videoId.length == 0) {
            navigate("/");
        }

        try {
            const response = await insertVideoOnHistory(videoId)
            return response
        } catch (error) {
            console.log(error)
            return null
        }

    }

    const getVideoId = () => {
        const search = location.search;
        const id = new URLSearchParams(search).get("v");
        return id;
    }

    const getTimeSttoped = () => {
        const search = location.search;
        const time = new URLSearchParams(search).get("t");
        return time;
    }

    return (
        <>
            {video &&
                (<VideoPlayer videoDatas={video} timeAt={timeStopped} onTimeUpdate={manageVideo} />

                )}
        </>
    )
}