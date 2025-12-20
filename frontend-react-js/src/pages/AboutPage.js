import './AboutPage.css';

export default function AboutPage() {
  return (
    <article className="about-page">
      <div className="about-content">
        <div className="hero-section">
          <h1>About Cruddur</h1>
          <p className="hero-text">A modern social platform designed to connect people through meaningful conversations and shared experiences. version 1.0</p>
        </div>
        
        <section className="mission">
          <h2>Our Mission</h2>
          <p>At Cruddur, we believe in fostering authentic connections and enabling users to share their thoughts, ideas, and moments in a safe and engaging environment. We're committed to building a platform that prioritizes user privacy, meaningful interactions, and community building.</p>
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