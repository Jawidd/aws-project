import './AboutPage.css';
import { Link } from 'react-router-dom';

export default function AboutPage() {
  return (
    <article className="about-page">
      <div className="about-card">
        <h1>About Cruddur</h1>

        <p>
          This is my deployed Cruddur application, available at{' '}
          <a href="https://cruddur.jawid.me" target="_blank" rel="noreferrer">
            cruddur.jawid.me
          </a>
          , built as a hands-on AWS learning project.
        </p>

        <p>
          The implementation and customizations for this project are maintained in my repository:{' '}
          <a href="https://github.com/Jawidd/aws-project" target="_blank" rel="noreferrer">
            github.com/Jawidd/aws-project
          </a>.
        </p>

        <p>
          This project was originally based on the open source Cruddur reference app created for the
          AWS Cloud Project Bootcamp, focusing on real-world AWS, serverless, containers, and CI/CD.
          You can explore the original source here:{' '}
          <a
            href="https://github.com/omenking/aws-bootcamp-cruddur-2023"
            target="_blank"
            rel="noreferrer"
          >
            Cruddur reference repository
          </a>.
        </p>

        <div className="about-actions">
          <Link className="home-button" to="/">← Back to Home</Link>
        </div>
      </div>
    </article>
  );
}
