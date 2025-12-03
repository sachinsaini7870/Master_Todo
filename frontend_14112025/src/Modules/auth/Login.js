import React, { useState } from 'react'
import { NavLink, useNavigate } from 'react-router-dom'
import { loginApi } from '../../api'
import { useAuth } from '../../hooks/useAuth'


const Login = () => {

    const { login } = useAuth();
    const navigate = useNavigate();

    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");


    async function handleSubmit({ email, password }) {
        try {
            setLoading(true);
            setError("");

            const { token, user } = await loginApi({ email, password });

            login(token, user);

            navigate("/");

        } catch (err) {
            setError(err.response?.data?.message || "Invalid credentials");
        } finally {
            setLoading(false);
        }
    }




    return (
        <>
            <div className="Login-Container">
                <div className="Login">
                    <h1>Login</h1>
                    <div className='Login-Form'>
                        <form action="" onSubmit={(e) => {
                            e.preventDefault();
                            handleSubmit({ email, password });
                        }}>
                            <input type="email"
                                placeholder='Email'
                                onChange={(e) => setEmail(e.target.value)}
                                value={email}
                                required
                                autoFocus
                            />

                            <input type="password"
                                placeholder='Password'
                                onChange={(e) => setPassword(e.target.value)}
                                value={password}
                                required
                            />

                            <button type="submit"
                                className='Button'
                                disabled={loading}
                            >
                                {loading ? "Loading..." : "Login"}
                            </button>

                        </form>
                        {error && <p style={{ color: "red" }}>{error}</p>}
                        <div className='Login-Links'>
                            <ul >
                                <li>
                                    <NavLink to={"/auth/signup"}>Signup</NavLink>
                                </li>
                                <li>
                                    <NavLink to={"/auth/forgot"}>Forgot</NavLink>
                                </li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </>
    )
}

export default Login