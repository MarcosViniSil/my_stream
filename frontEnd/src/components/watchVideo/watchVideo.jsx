import React, { useEffect } from 'react'
import { useLocation } from "react-router-dom";
import VideoPlayer from '../playVideo/playVideo'
import './watchVideo.css'

export default function WatchVideo(){
    
    const location = useLocation();
    
    useEffect(() => {
        console.log(getVideoId())
        console.log(getTimeSttoped())
    }, []);

    const getVideoId = () => {
        const search = location.search;
        const id = new URLSearchParams(search).get("v");
        return id;
    }

    const getTimeSttoped = () =>{
        const search = location.search;
        const time = new URLSearchParams(search).get("t");
        return time;
    }

    return (
        <>
            <VideoPlayer />
        </>
    )
}