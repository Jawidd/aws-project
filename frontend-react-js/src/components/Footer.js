import './Footer.css';
import { Link } from 'react-router-dom';

export default function Footer() {
  return (
    <footer className="app-footer">
      <div className="footer-content">
        <div className="footer-section">
          <h3>Cruddur</h3>
          <p>Connect, Share, and Discover</p>
        </div>
        
        <div className="footer-section">
          <h4>Company</h4>
          <ul>
            <li><Link to="/about">About</Link></li>
            <li><a href="#careers">Careers</a></li>
            <li><a href="#blog">Blog</a></li>
            <li><a href="#help">Help Center</a></li>
          </ul>
        </div>
        
        <div className="footer-section">
          <h4>Legal</h4>
          <ul>
            <li><Link to="/info">Info & Policies</Link></li>
            <li><a href="#cookies">Cookie Policy</a></li>
            <li><a href="#community">Community Guidelines</a></li>
          </ul>
        </div>
        
        <div className="footer-section">
          <h4>Connect</h4>
          <ul>
            <li><a href="#twitter">Twitter</a></li>
            <li><a href="#github">GitHub</a></li>
            <li><a href="#linkedin">LinkedIn</a></li>
            <li><a href="#contact">Contact Us</a></li>
          </ul>
        </div>
      </div>
      
      <div className="footer-bottom">
        <p>&copy; {new Date().getFullYear()} Cruddur. All rights reserved.</p>
        <div className="footer-links">
          <Link to="/info">Info</Link>
          <Link to="/about">About</Link>
        </div>
      </div>
    </footer>
  );
}
