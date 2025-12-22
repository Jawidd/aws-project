import './AboutPage.css';

export default function AboutPage() {
  return (
    <article className="about-page">
      <div className="about-content">
        <div className="hero-section">
          <h1>About Cruddur</h1>
          <p className="hero-text">
            This project was built as part of the AWS Cloud Project Bootcamp and follows the open source Cruddur reference implementation.
          </p>
        </div>
        
        <section className="mission">
          <h2>What is Cruddur?</h2>
          <p>
            Cruddur is a hands-on AWS cloud native social feed used to practice serverless, containers, and CI/CD. The frontend you are using mirrors the patterns and services showcased in the bootcamp and the <a href="https://github.com/omenking/aws-bootcamp-cruddur-2023" target="_blank" rel="noreferrer">Cruddur repository</a>.
          </p>
        </section>
        
        <section className="features">
          <h2>What We Offer</h2>
          <div className="features-grid">
            <div className="feature-card">
              <h3>Real-time Messaging</h3>
              <p>Connect instantly with friends and communities through our fast, reliable messaging system.</p>
            </div>
            <div className="feature-card">
              <h3>Privacy & Security</h3>
              <p>Your data is protected with industry-standard security measures and comprehensive privacy controls.</p>
            </div>
            <div className="feature-card">
              <h3>Responsive Design</h3>
              <p>Enjoy a seamless experience across all your devices with our modern, intuitive interface.</p>
            </div>
            <div className="feature-card">
              <h3>Community Focus</h3>
              <p>Build meaningful connections and engage in conversations that matter to you.</p>
            </div>
          </div>
        </section>
        
        <section className="values">
          <h2>Our Values</h2>
          <ul className="values-list">
            <li><strong>Authenticity:</strong> We encourage genuine interactions and real connections.</li>
            <li><strong>Privacy:</strong> Your personal information and conversations are protected.</li>
            <li><strong>Inclusivity:</strong> Everyone is welcome in our diverse community.</li>
            <li><strong>Innovation:</strong> We continuously improve to serve you better.</li>
          </ul>
        </section>
        
        <section className="contact">
          <h2>Get in Touch</h2>
          <p>Have questions or feedback? We'd love to hear from you. Contact us at <a href="mailto:hello@cruddur.com">hello@cruddur.com</a></p>
        </section>
      </div>
    </article>
  );
}
