import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import styles from './Header.module.scss';

// Define what the User data looks like
interface UserData {
  username: string;
  xp: number;
}

export default function Header() {
  const [user, setUser] = useState<UserData | null>(null);
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);

  // 1. Load User Data from Flask on mount
  useEffect(() => {
    fetch("/api/user/header")
      .then(res => {
        if (res.ok) return res.json();
        throw new Error("Not logged in");
      })
      .then(data => setUser(data))
      .catch(() => setUser(null));
  }, []);

  // 2. Logic for XP Bar (Ported from your JS)
  const calculateXpPercentage = (xp: number) => {
    xp = 40
    const nextLevelXP = Math.ceil(Math.sqrt((xp + 1) / 50)) ** 2 * 50;
    return Math.round((xp / nextLevelXP) * 100);
  };

  const handleLogout = async () => {
    await fetch("/logout", { method: "POST" });
    window.location.href = "/";
  };

  return (
    <header>
      <h1 className={styles.logo}>
        <Link to="/">Capydev</Link>
      </h1>

      {user ? (
        /* LOGGED IN NAV */
        <nav id="nav-logged-in">
          <a href="/user/lessons"><button className={styles.navButton}>Lessons</button></a>
          
          <div className="account-container">
            <button 
              className={styles.navButton} 
              style={{ textAlign: 'left' }} 
              onClick={() => setIsDropdownOpen(!isDropdownOpen)}
            >
              <p className={styles.username}>{user.username}</p>
              <div className={styles.progress}>
                <div 
                  className={styles.progressFill}
                  style={{ width: `${calculateXpPercentage(user.xp)}%` }}
                ></div>
              </div>
            </button>

            {isDropdownOpen && (
              <div className={styles.dropdown}>
                <div><Link to="/user">Profile</Link></div>
                <div><Link to="/settings">Settings</Link></div>
                <div><a onClick={handleLogout} className="delete" style={{ cursor: 'pointer' }}>Logout</a></div>
              </div>
            )}
          </div>
        </nav>
      ) : (
        /* LOGGED OUT NAV */
        <nav id="nav-logged-out">
          <Link to="/login"><button className={styles.navButton}>Login</button></Link>
          <Link to="/register"><button className={styles.navButton}>Register</button></Link>
        </nav>
      )}
    </header>
  );
}