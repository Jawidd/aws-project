import './AboutPage.css';

export default function AboutPage() {
  return (
    <article className="about-page">
      <div className="about-card">
        <h1>About Cruddur</h1>
        <p>
          This project was built for the AWS Cloud Project Bootcamp using the open source Cruddur reference app. It’s a practical sandbox for learning AWS, serverless, containers, and CI/CD.
        </p>
        <p>
          Explore the source on the <a href="https://github.com/omenking/aws-bootcamp-cruddur-2023" target="_blank" rel="noreferrer">Cruddur repository</a>.
        </p>
      </div>
    </article>
  );
}
