import { Link } from 'react-router-dom';

export default function LessonsPage() {
    return (
    <nav>
    {/* This changes the URL instantly without a page flicker */}
    <p>
        Userpage
    </p>
    
    <Link to="/">Home</Link>
    </nav>
    );
}