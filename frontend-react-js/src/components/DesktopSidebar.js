import './DesktopSidebar.css';
import Search from '../components/Search';
import TrendingSection from '../components/TrendingsSection'
import JoinSection from '../components/JoinSection'
import { Link } from 'react-router-dom';

export default function DesktopSidebar(props) {
  let trending;
  if (props.user) {
    trending = <TrendingSection />
  }

  let join;
  if (!props.user) {
    join = <JoinSection />
  }

  return (
    <section>
      <Search />
      {trending}
      {join}
      <footer>
        <Link to="/about">About</Link>
        <Link to="/terms">Terms</Link>
        <Link to="/privacy">Privacy</Link>
      </footer>
    </section>
  );
}