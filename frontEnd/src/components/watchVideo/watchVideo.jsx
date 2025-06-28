import React, { useEffect, useState } from 'react'
import { useLocation, useNavigate } from "react-router-dom";
import { getDatasVideoToStream } from '../../service/videoService.js'
import VideoPlayer from '../playVideo/playVideo'
import './watchVideo.css'

export default function WatchVideo() {
    const [video, setVideo] = useState("");
    const [timeStopped, setTimeStopped] = useState(0);

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

            
        }
        fetchData()
    }, []);

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
                (<VideoPlayer videoDatas={video} timeAt={timeStopped} />

                )}
        </>
    )
}