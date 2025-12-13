import './ActivityFeed.css';
import ActivityItem from './ActivityItem';
import React from 'react';

export default function ActivityFeed(props) {
  const [currentIndex, setCurrentIndex] = React.useState(0);
  const maxVisible = 4;
  const activities = props.activities || [];
  const hasMore = activities.length > maxVisible;
  
  const nextSlide = React.useCallback(() => {
    if (currentIndex < activities.length - maxVisible) {
      setCurrentIndex(prev => prev + 1);
    }
  }, [currentIndex, activities.length, maxVisible]);
  
  const prevSlide = React.useCallback(() => {
    if (currentIndex > 0) {
      setCurrentIndex(prev => prev - 1);
    }
  }, [currentIndex]);
  
  // Keyboard navigation
  React.useEffect(() => {
    const handleKeyPress = (e) => {
      if (e.key === 'ArrowLeft') {
        prevSlide();
      } else if (e.key === 'ArrowRight') {
        nextSlide();
      }
    };
    
    if (hasMore) {
      window.addEventListener('keydown', handleKeyPress);
      return () => window.removeEventListener('keydown', handleKeyPress);
    }
  }, [hasMore, nextSlide, prevSlide]);
  
  // Reset to first page when activities change
  React.useEffect(() => {
    setCurrentIndex(0);
  }, [activities.length]);
  
  const visibleActivities = activities.slice(currentIndex, currentIndex + maxVisible);
  
  return (
    <div className='activity_feed'>
      <div className='activity_feed_heading'>
        <div className='title'>{props.title}</div>
        {hasMore && (
          <div className='activity_controls'>
            <button 
              className={`control_btn prev ${currentIndex === 0 ? 'disabled' : ''}`}
              onClick={prevSlide}
              disabled={currentIndex === 0}
              title="Previous (←)"
            >
              ‹
            </button>
            <span className='activity_counter'>
              {currentIndex + 1}-{Math.min(currentIndex + maxVisible, activities.length)} of {activities.length}
            </span>
            <button 
              className={`control_btn next ${currentIndex >= activities.length - maxVisible ? 'disabled' : ''}`}
              onClick={nextSlide}
              disabled={currentIndex >= activities.length - maxVisible}
              title="Next (→)"
            >
              ›
            </button>
          </div>
        )}
      </div>
      <div className='activity_feed_collection'>
        {visibleActivities.map((activity, index) => {
          return <ActivityItem 
            setReplyActivity={props.setReplyActivity} 
            setPopped={props.setPopped} 
            key={activity.uuid} 
            activity={activity} 
          />
        })}
        {visibleActivities.length === 0 && (
          <div className='no_activities'>
            <p>No activities to display</p>
          </div>
        )}
      </div>
    </div>
  );
}