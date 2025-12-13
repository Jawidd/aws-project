import './PrivacyPage.css';
import DesktopNavigation from '../components/DesktopNavigation';
import DesktopSidebar from '../components/DesktopSidebar';
import { checkAuth } from '../lib/CheckAuth';
import { useEffect, useState } from 'react';

export default function PrivacyPage() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    const loadData = async () => {
      try {
        await checkAuth(setUser);
      } catch (err) {
        console.log(err);
      }
    };
    loadData();
  }, []);

  return (
    <article>
      <DesktopNavigation user={user} active={'privacy'} setPopped={null} />
      <div className='content'>
        <div className="privacy-page">
          <div className="privacy-header">
            <h1>Privacy Policy</h1>
            <p className="last-updated">Last updated: {new Date().toLocaleDateString()}</p>
          </div>
          
          <div className="privacy-content">
            <section className="privacy-section">
              <h2>1. Information We Collect</h2>
              <p>
                We collect information you provide directly to us, such as when you create an account, 
                post content, or contact us for support.
              </p>
              <h3>Personal Information</h3>
              <ul>
                <li>Name and email address</li>
                <li>Profile information (bio, profile picture)</li>
                <li>Account credentials</li>
                <li>Communication preferences</li>
              </ul>
              <h3>Usage Information</h3>
              <ul>
                <li>Posts, messages, and other content you create</li>
                <li>Interactions with other users' content</li>
                <li>Device information and IP address</li>
                <li>Usage patterns and preferences</li>
              </ul>
            </section>

            <section className="privacy-section">
              <h2>2. How We Use Your Information</h2>
              <p>We use the information we collect to:</p>
              <ul>
                <li>Provide, maintain, and improve our services</li>
                <li>Process transactions and send related information</li>
                <li>Send technical notices and support messages</li>
                <li>Respond to your comments and questions</li>
                <li>Prevent fraud and enhance security</li>
                <li>Analyze usage patterns to improve user experience</li>
              </ul>
            </section>

            <section className="privacy-section">
              <h2>3. Information Sharing</h2>
              <p>
                We do not sell, trade, or otherwise transfer your personal information to third parties 
                without your consent, except in the following circumstances:
              </p>
              <ul>
                <li>With your explicit consent</li>
                <li>To comply with legal obligations</li>
                <li>To protect our rights and safety</li>
                <li>With service providers who assist in our operations</li>
                <li>In connection with a business transfer or merger</li>
              </ul>
            </section>

            <section className="privacy-section">
              <h2>4. Data Security</h2>
              <p>
                We implement appropriate technical and organizational measures to protect your personal 
                information against unauthorized access, alteration, disclosure, or destruction. Our 
                security measures include:
              </p>
              <ul>
                <li>Encryption of data in transit and at rest</li>
                <li>Regular security assessments and updates</li>
                <li>Access controls and authentication systems</li>
                <li>Secure cloud infrastructure (AWS)</li>
                <li>Regular backups and disaster recovery procedures</li>
              </ul>
            </section>

            <section className="privacy-section">
              <h2>5. Data Retention</h2>
              <p>
                We retain your personal information for as long as necessary to provide our services 
                and fulfill the purposes outlined in this Privacy Policy. We may retain certain 
                information for longer periods as required by law or for legitimate business purposes.
              </p>
            </section>

            <section className="privacy-section">
              <h2>6. Your Rights and Choices</h2>
              <p>You have the following rights regarding your personal information:</p>
              <ul>
                <li><strong>Access:</strong> Request a copy of your personal information</li>
                <li><strong>Correction:</strong> Update or correct inaccurate information</li>
                <li><strong>Deletion:</strong> Request deletion of your personal information</li>
                <li><strong>Portability:</strong> Request transfer of your data</li>
                <li><strong>Opt-out:</strong> Unsubscribe from marketing communications</li>
              </ul>
              <p>
                To exercise these rights, please contact us using the information provided below.
              </p>
            </section>

            <section className="privacy-section">
              <h2>7. Cookies and Tracking</h2>
              <p>
                We use cookies and similar tracking technologies to enhance your experience on our 
                platform. These technologies help us:
              </p>
              <ul>
                <li>Remember your preferences and settings</li>
                <li>Analyze site traffic and usage patterns</li>
                <li>Provide personalized content and features</li>
                <li>Improve security and prevent fraud</li>
              </ul>
              <p>
                You can control cookie settings through your browser preferences.
              </p>
            </section>

            <section className="privacy-section">
              <h2>8. Third-Party Services</h2>
              <p>
                Our service may contain links to third-party websites or integrate with third-party 
                services. We are not responsible for the privacy practices of these third parties. 
                We encourage you to review their privacy policies before providing any information.
              </p>
            </section>

            <section className="privacy-section">
              <h2>9. Children's Privacy</h2>
              <p>
                Our service is not intended for children under 13 years of age. We do not knowingly 
                collect personal information from children under 13. If we become aware that we have 
                collected such information, we will take steps to delete it promptly.
              </p>
            </section>

            <section className="privacy-section">
              <h2>10. International Data Transfers</h2>
              <p>
                Your information may be transferred to and processed in countries other than your own. 
                We ensure appropriate safeguards are in place to protect your information in accordance 
                with applicable data protection laws.
              </p>
            </section>

            <section className="privacy-section">
              <h2>11. Changes to This Policy</h2>
              <p>
                We may update this Privacy Policy from time to time. We will notify you of any material 
                changes by posting the new Privacy Policy on this page and updating the "Last updated" date. 
                Your continued use of the service after such changes constitutes acceptance of the new policy.
              </p>
            </section>

            <section className="privacy-section">
              <h2>12. Contact Us</h2>
              <p>
                If you have any questions about this Privacy Policy or our privacy practices, please contact us:
              </p>
              <div className="contact-info">
                <p>Email: privacy@cruddur.com</p>
                <p>Address: Cruddur Privacy Team</p>
                <p>Data Protection Officer: dpo@cruddur.com</p>
              </div>
            </section>
          </div>
        </div>
      </div>
      <DesktopSidebar user={user} />
    </article>
  );
}