import React, { useState, useEffect } from 'react';
import VideoCard from '../../components/videoCard/videoCard'
import { getVideosUserQuery } from '../../service/videoService.js'
import { Spinner } from '@chakra-ui/react';
import { useLocation, useNavigate } from "react-router-dom";
import SearchBar from '../../components/searchBar/SearchBar'

export default function ListSearch() {
    const [loading, setLoading] = useState(false);
    const [videos, setVideos] = useState([])
    const location = useLocation();

    const navigate = useNavigate();


    const handleSearch = (searchTerm) => {
        if (!searchTerm || searchTerm.length == 0) return
        setTermToSearch(searchTerm)
    }

    const getTermToSearch = () => {
        const search = location.search;
        const term = new URLSearchParams(search).get("q");
        return term;
    }

    const setTermToSearch = (newTerm) => {
        const params = new URLSearchParams(location.search);
        if (newTerm) {
            params.set("q", newTerm);
        } else {
            params.delete("q");
        }
        navigate({ search: params.toString() });
    }

    const getDatasByTerm = async () => {
        let term = getTermToSearch()
        if (!term) return

        setLoading(true)
        try {
            let videos = await getVideosUserQuery(term)
            console.log(videos)
            if (videos && videos.length > 0) {
                setVideos(videos)
            } else {
                setVideos([])
            }
        } catch (err) {
            console.error("Erro ao buscar vídeos:", err)
            setVideos([])
        } finally {
            setLoading(false)
        }
    }

    useEffect(() => {
        getDatasByTerm()
    }, [location.search])

    const convertVideoDuration = (duration) => {
        if (duration >= 3600) {
            let hours = Math.floor(duration / 3600);
            duration %= 3600;
            let minutes = Math.floor(duration / 60);
            minutes = String(minutes).padStart(2, "0");
            let seconds = duration % 60;
            seconds = String(seconds).padStart(2, "0");
            return `${hours}:${minutes}:${seconds}`
        } else if (duration > 60 && duration < 3600) {
            let minutes = Math.floor(duration / 60);
            let seconds = duration % 60;
            seconds = String(seconds).padStart(2, "0");
            return `${minutes}:${seconds}`
        } else {
            let seconds = duration % 60;
            seconds = String(seconds).padStart(2, "0");
            return `0:${seconds}`
        }

    }
        const formatTimeWatched = (currentTime, totalTime) => {
        if (currentTime >= totalTime) {
            return 100;
        }

        const positionBar = Math.floor((currentTime * 100) / totalTime)

        if (positionBar < 0) {
            return 0;
        }

        if (positionBar > 100) {
            return 100;
        }

        return positionBar
    }
    
    return (
        <>
            {loading ? (
                <div style={{ display: 'flex', justifyContent: 'center', marginTop: '20px' }}>
                    <Spinner
                        thickness="4px"
                        speed="0.65s"
                        emptyColor="gray.200"
                        color="#419181"
                        size="xl"
                    />
                </div>
            ) : videos.length === 0 ? (
                <div>
                    <div className='search'>
                        <SearchBar onSearch={handleSearch} />
                    </div>
                    <p style={{ color: 'white', textAlign: 'center' }}>Nenhum vídeo encontrado.</p>
                </div>

            ) : (
                <div>
                    <div className='search'>
                        <SearchBar onSearch={handleSearch} />
                    </div>
                    <div className="video-grid">

                        {videos.map((video, index) => (
                            <VideoCard key={index} video={video} videoDuration={convertVideoDuration(video.videoDuration)} videoAt={video.timeWatched} progress={formatTimeWatched(video.timeWatched,video.videoDuration)} />
                        ))}
                    </div>

                </div>
            )}
        </>
    )
}