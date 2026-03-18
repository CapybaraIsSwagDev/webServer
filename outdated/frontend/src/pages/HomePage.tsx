import { Link } from 'react-router-dom';

export default function LessonsPage() {
    return (
    <nav>
    {/* This changes the URL instantly without a page flicker */}
    <Link to="/lessons">
        <button>Lessons</button>
    </Link>
    
    <Link to="/">Home</Link>
    </nav>
    );
}