import './TermsPage.css';

export default function TermsPage() {
  return (
    <article className="terms-page">
      <div className="terms-content">
        <div className="header-section">
          <h1>Terms of Service</h1>
          <p className="last-updated">Last updated: {new Date().toLocaleDateString()}</p>
          <p className="intro">Please read these Terms of Service carefully before using Cruddur. By accessing or using our service, you agree to be bound by these terms.</p>
        </div>
        
        <section>
          <h2>1. Acceptance of Terms</h2>
          <p>By accessing and using Cruddur ("the Service"), you accept and agree to be bound by the terms and provisions of this agreement. If you do not agree to abide by the above, please do not use this service.</p>
        </section>
        
        <section>
          <h2>2. User Accounts</h2>
          <p>When you create an account with us, you must provide information that is accurate, complete, and current at all times. You are responsible for safeguarding the password and for all activities that occur under your account.</p>
          <ul>
            <li>You must be at least 13 years old to use this service</li>
            <li>You are responsible for maintaining account security</li>
            <li>You must notify us immediately of any unauthorized use</li>
          </ul>
        </section>
        
        <section>
          <h2>3. User Content and Conduct</h2>
          <p>You retain ownership of content you post on Cruddur. However, by posting content, you grant us a worldwide, non-exclusive, royalty-free license to use, modify, publicly perform, publicly display, reproduce, and distribute such content.</p>
          <h3>Prohibited Content:</h3>
          <ul>
            <li>Harassment, bullying, or threatening behavior</li>
            <li>Spam or unsolicited commercial content</li>
            <li>Illegal activities or content</li>
            <li>Hate speech or discriminatory content</li>
            <li>False or misleading information</li>
          </ul>
        </section>
        
        <section>
          <h2>4. Privacy and Data Protection</h2>
          <p>Your privacy is important to us. Please review our Privacy Policy, which also governs your use of the Service, to understand our practices.</p>
        </section>
        
        <section>
          <h2>5. Intellectual Property</h2>
          <p>The Service and its original content, features, and functionality are and will remain the exclusive property of Cruddur and its licensors. The Service is protected by copyright, trademark, and other laws.</p>
        </section>
        
        <section>
          <h2>6. Termination</h2>
          <p>We may terminate or suspend your account and bar access to the Service immediately, without prior notice or liability, under our sole discretion, for any reason whatsoever, including without limitation if you breach the Terms.</p>
        </section>
        
        <section>
          <h2>7. Disclaimer</h2>
          <p>The information on this service is provided on an "as is" basis. To the fullest extent permitted by law, this Company excludes all representations, warranties, conditions and terms.</p>
        </section>
        
        <section>
          <h2>8. Changes to Terms</h2>
          <p>We reserve the right to modify or replace these Terms at any time. If a revision is material, we will provide at least 30 days notice prior to any new terms taking effect.</p>
        </section>
        
        <section>
          <h2>9. Contact Information</h2>
          <p>If you have any questions about these Terms of Service, please contact us at:</p>
          <div className="contact-info">
            <p>Email: <a href="mailto:legal@cruddur.com">legal@cruddur.com</a></p>
            <p>Address: Cruddur Legal Department</p>
          </div>
        </section>
      </div>
    </article>
  );
}