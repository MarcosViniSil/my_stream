import React from 'react'
import './historyVideosCard.css'

export default function HistoryVideosCard({ metaDatas,Duration,timeAt,progress }) {
    return (
        <>
            <div className="videoHistoryCard">
                <a href={ timeAt === 0 ? `/watch?v=${metaDatas.videoId}` : `/watch?v=${metaDatas.videoId}&t=${timeAt}`} >
                    <div className="videoCardContent">
                        <div className='thumbnailContainer'>
                            <img
                                src={metaDatas.thumbnailUrl}
                                alt={metaDatas.videoTitle}
                                className="thumbnail"
                            />
                            <div className={`progress-bar-container ${timeAt === 0 ? 'desactivate' : 'activate'}`}>
                                <div
                                    className="progress-bar"
                                    style={{ width: `${progress}%` }}
                                ></div>
                            </div>
                            <p className='duration'>{Duration}</p>
                        </div>

                        <div className="video-info">
                            <h1 className="video-title">{metaDatas.videoTitle}</h1>
                            <p className='author'>{metaDatas.userName}</p>
                        </div>
                    </div>
                </a>
            </div>
        </>
    )
}