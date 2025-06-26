import React, { useEffect } from 'react';
import { getVideosInitialPage } from "../../service/videoService";
import { useLocation, useNavigate } from "react-router-dom";
import VideoCard from '../../components/videoCard/videoCard'
import SearchBar from '../../components/searchBar/SearchBar'
import './videosInitialPage.css'
import { useState } from 'react';
import { Spinner } from '@chakra-ui/react';

export default function VideosInitialPage() {
    const [offSet, setOffSet] = useState(0)
    const [videos, setVideos] = useState([])
    const [isFetching, setIsFetching] = useState(false);
    const [hasMore, setHasMore] = useState(true);
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();
    
    const handleSearch = (searchTerm) => {
        if(!searchTerm || searchTerm.length == 0) return 
        console.log(videos)
        console.log("Termo pesquisado:", searchTerm);

        navigate(`busca?q=${searchTerm}`);
        
    }

    useEffect(() => {
        const handleScroll = () => {
            const scrollTop = window.scrollY;
            const windowHeight = window.innerHeight;
            const fullHeight = document.documentElement.scrollHeight;

            if (!isFetching && hasMore && scrollTop + windowHeight >= fullHeight - 200) {
                setIsFetching(true);
            }
        };

        window.addEventListener("scroll", handleScroll);
        return () => window.removeEventListener("scroll", handleScroll);
    }, [isFetching, hasMore]);

    useEffect(() => {
        const fetchMoreVideos = async () => {
            try {
                const moreVideos = await getVideosInitialPage(offSet);
                if (moreVideos && moreVideos.length > 0) {
                    setVideos(prev => [...prev, ...moreVideos]);
                    setOffSet(prev => prev + 1);
                } else {
                    setHasMore(false);
                }
            } catch (err) {
                console.error("Erro ao carregar mais vídeos:", err);
            } finally {
                setIsFetching(false);
            }
        };

        if (isFetching && hasMore) {
            fetchMoreVideos();
        }
    }, [isFetching, hasMore]);

    useEffect(() => {
        const loadInitialVideos = async () => {
            try {
                const videos = await getVideosInitialPage(0);
                setVideos(videos);
                setLoading(false)
                setOffSet(1);
            } catch (err) {
                console.error("Erro ao buscar vídeos iniciais:", err);
            }
        };

        loadInitialVideos();
    }, []);


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
                <p style={{ color: 'white', textAlign: 'center' }}>Nenhum vídeo disponível.</p>
            ) : (
                <div>
                    <div className='search'>
                        <SearchBar onSearch={handleSearch} />
                    </div>
                    <div className="video-grid">
                        {videos.map((video, index) => (
                            <VideoCard key={index} video={video} videoDuration={convertVideoDuration(video.videoDuration)} />
                        ))}
                    </div>
                </div>
            )}
        </>

    )
}