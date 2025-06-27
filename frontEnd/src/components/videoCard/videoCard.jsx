import React from 'react';

import './videoCard.css'

export default function VideoCard({video,videoDuration}) {

  return (
    <div className="video-card">
      <a href={`/watch?v=${video.videoId}`}>
        <div className='wrapThumbnailAndDuration'>
          <img
            src={video.thumbnailUrl}
            alt={video.videoTitle}
            className="thumbnail"
          />
          <p className='duration'>{videoDuration}</p>
      </div>

      <div className="video-info">
        <h3 className="video-title">{video.videoTitle}</h3>
        <p className="video-meta">
          Criado por <span className="video-user">{video.userName}</span> em <span className="video-date">{video.videoDate}</span>
        </p>
      </div>
      </a>
    </div>
  );
};