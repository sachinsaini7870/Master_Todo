import React, { useState } from 'react'
import { Form, NavLink, useActionData, useNavigation } from 'react-router-dom'



const Login = () => {

    const actionData = useActionData();
    const navigation = useNavigation();

    const isSubmitting = navigation.state === "submitting";

    // local validation state
    const [error, setError] = useState("");



    function handleSubmit(e) {
        const form = e.target;
        const email = form.email.value.trim();
        const password = form.password.value.trim();

        if (!email) {
            e.preventDefault();
            setError("Email Required.");
            return;
        }

        if (!password) {
            e.preventDefault();
            setError("Passwords required.");
            return;
        }

        // clear UI error if validation passed
        setError("");
    }

    return (
        <>
            <div className="Login-Container">
                <div className="Login">
                    <h1>Login</h1>
                    <div className='Login-Form'>

                        <Form method="post" className="Todo-Form" onSubmit={handleSubmit}>

                            <div>
                                <label htmlFor='email'>Email:</label>
                                <input
                                    name="email"
                                    id='email'
                                    type='email'
                                    required
                                />
                            </div>

                            <div>
                                <label htmlFor='password'>Password:</label>
                                <input
                                    name="password"
                                    id='password'
                                    type='password'
                                    required
                                />
                            </div>

                            {/* frontend validation error */}
                            {error && <p className="Resend-Otp-Error">{error}</p>}

                            {/* backend action errors */}
                            {actionData?.error && <p className='Resend-Otp-Error'>{actionData.error}</p>}
                            {actionData?.success && <p className="Resend-Otp">{actionData.message}</p>}

                            <button type="submit" className="Button" disabled={isSubmitting}>
                                {isSubmitting ? "Loading..." : "Login"}
                            </button>
                        </Form>

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