import './TrendingsSection.css';
import TrendingActivity from '../components/TrendingActivity';
import { useState, useEffect, useCallback } from 'react';

export default function TrendingsSection(props) {
  const [trendingActivities, setTrendingActivities] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const maxVisible = 3;
  const hasMore = trendingActivities.length > maxVisible;

  useEffect(() => {
    const fetchTrending = async () => {
      try {
        const backend_url = `${process.env.REACT_APP_BACKEND_URL}/api/activities/trending`;
        const res = await fetch(backend_url);
        if (res.ok) {
          const data = await res.json();
          setTrendingActivities(data);
        }
      } catch (err) {
        console.error('Error fetching trending activities:', err);
      }
    };

    fetchTrending();
  }, []);

  const nextSlide = useCallback(() => {
    if (currentIndex < trendingActivities.length - maxVisible) {
      setCurrentIndex(prev => prev + 1);
    }
  }, [currentIndex, trendingActivities.length, maxVisible]);
  
  const prevSlide = useCallback(() => {
    if (currentIndex > 0) {
      setCurrentIndex(prev => prev - 1);
    }
  }, [currentIndex]);

  const visibleActivities = trendingActivities.slice(currentIndex, currentIndex + maxVisible);

  return (
    <div className="trendings">
      <div className='trendings-header'>
        <div className='trendings-title'>Most Liked</div>
        {hasMore && (
          <div className='trending-controls'>
            <button 
              className={`trending-btn prev ${currentIndex === 0 ? 'disabled' : ''}`}
              onClick={prevSlide}
              disabled={currentIndex === 0}
            >
              ‹
            </button>
            <button 
              className={`trending-btn next ${currentIndex >= trendingActivities.length - maxVisible ? 'disabled' : ''}`}
              onClick={nextSlide}
              disabled={currentIndex >= trendingActivities.length - maxVisible}
            >
              ›
            </button>
          </div>
        )}
      </div>
      <div className='trending-collection'>
        {visibleActivities.map(activity => {
          return <TrendingActivity 
            key={activity.uuid} 
            message={activity.message}
            handle={activity.handle}
            likes_count={activity.likes_count}
          />;
        })}
      </div>
    </div>
  );
}