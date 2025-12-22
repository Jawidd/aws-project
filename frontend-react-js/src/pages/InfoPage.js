import './InfoPage.css';
import { Link } from 'react-router-dom';

export default function InfoPage() {
  return (
    <article className="info-page">
      <div className="info-card">
        <h1>Info & Policies</h1>
        <p>
          This app is provided for learning and demo purposes. By using it you agree that content is offered as-is and you should avoid sharing sensitive data; we may adjust or remove data at any time.
        </p>
        <div className="info-actions">
          <Link className="home-button" to="/">← Back to Home</Link>
        </div>
      </div>
    </article>
  );
}
