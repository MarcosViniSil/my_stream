import React, { useState, useEffect } from 'react'
import HistoyVideosCard from '../historyVideosCard/historyVideosCard'
import { getHistory } from "../../service/videoService";
import './historyVideos.css'
import { Spinner } from '@chakra-ui/react';

export default function HistoryVideos() {
    const [offSet, setOffSet] = useState(0)
    const [metaDatas, setMetaDatas] = useState([])
    const [isFetching, setIsFetching] = useState(false);
    const [hasMore, setHasMore] = useState(true);
    const [loading, setLoading] = useState(true);

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
        const fetchMoreHistory = async () => {
            try {
                const metadatasRe = await getHistory(offSet);
                if (metadatasRe && metadatasRe.length > 0) {
                    setMetaDatas(prev => [...prev, ...metadatasRe]);
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
            fetchMoreHistory();
        }
    }, [isFetching, hasMore]);

    useEffect(() => {
        const loadInitialDatasHistory = async () => {
            try {
                const metadatasRe = await getHistory(offSet);
                setMetaDatas(metadatasRe);
                setLoading(false)
                setOffSet(1);
            } catch (err) {
                console.error("Erro ao buscar vídeos iniciais:", err);
            }
        };

        loadInitialDatasHistory();
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
            ) : metaDatas.length === 0 ? (
                <p style={{ color: 'white', textAlign: 'center' }}>Nenhum vídeo no histórico</p>
            ) : (
                <div>
                    {
                        metaDatas.map(datas => (
                            <div key={`${datas.date}-${Math.random() * ((Math.PI % Math.random()) + 1)}`}>
                                <h2 className='dateText'>{datas.dateText}</h2>
                                {datas['videos'].map((metadatas, idx) => (
                                    <HistoyVideosCard
                                        key={`${metadatas.videoId}-${datas.date}`}
                                        metaDatas={metadatas}
                                        Duration={formatTime(metadatas.videoDuration)}
                                        timeAt={formatTimeWatched(metadatas.lastTime, metadatas.videoDuration)}
                                    />
                                ))}
                            </div>
                        ))
                    }
                </div>
            )}
        </>
    )
}