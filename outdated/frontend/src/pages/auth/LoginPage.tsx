import { useState, useRef } from 'react'; // Added useRef
import { useNavigate, useLocation, Link } from 'react-router-dom';
import { Turnstile, type TurnstileInstance } from '@marsidev/react-turnstile';
import './auth.scss';

const Login = () => {
  // 1. Properly type the ref for Turnstile
  const turnstileRef = useRef<TurnstileInstance>(null);
  const [error, setError] = useState('');
  const [token, setToken] = useState<string | null>(null);

  const navigate = useNavigate();
  const location = useLocation();

  const params = new URLSearchParams(location.search);
  const dest = params.get('dest') || '';

  // 2. The 'action' function receives formData automatically
  async function handleSubmit(formData: FormData) {
    setError(''); // Clear previous errors

    if (!token) {
      setError("Please complete the CAPTCHA!");
      return;
    }

    // Extract values using the 'name' attributes of your inputs
    const payload = {
      username: formData.get("username"),
      password: formData.get("password"),
      'cf-turnstile-response': token,
    };

    try {
      const response = await fetch(`/api/auth/login?dest=${encodeURIComponent(dest)}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      if (response.status == 500) {

      }

      const contentType = response.headers.get("content-type");
      if (contentType && contentType.includes("application/json")) {
        const data = await response.json();
        if (data.error) {
          setError(data.error);
          // 3. Reset CAPTCHA on error so user can try again
          turnstileRef.current?.reset();
          setToken(null); 
        } else if (data.redirredirectedect) {
          navigate(data.url);
        }
      } 
    } catch (err) {
      console.error("Submission failed", err);
      setError("A network error occurred.");
      turnstileRef.current?.reset();
    }
  }

  return (
    <div className="center">
      <div className="container-auth">
        <h2>Login</h2>
        {/* React 19+ form action */}
        <form className="auth" action={handleSubmit}>
          <div className="field">
            <label htmlFor="username">Username</label>
            <input
              type="text"
              name="username" /* Vital for formData.get() */
              required
              autoComplete="username"
            />
          </div>

          <div className="field">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              name="password" /* Vital for formData.get() */
              required
              autoComplete="current-password"
            />
          </div>

          {/* 4. Attached the ref here */}
          <Turnstile 
            ref={turnstileRef}
            siteKey="0x4AAAAAACWaR0VsAZrgSwiA" 
            onSuccess={(token) => setToken(token)} 
            onExpire={() => setToken(null)}
          />

          <div className="field">
            {error && <p style={{ color: 'red', fontSize: '14px' }}>{error}</p>}
            <button type="submit">Login</button>
          </div>
        </form>

        <Link to="/register">
          <button className="register" type="button">Register</button>
        </Link>
      </div>
    </div>
  );
};

export default Login;