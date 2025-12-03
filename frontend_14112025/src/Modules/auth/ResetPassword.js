import React, { useState } from 'react'
import { Form, useActionData, useNavigate, useNavigation } from 'react-router-dom';

const ResetPassword = () => {

    const actionData = useActionData();
    const navigation = useNavigation();
    const navigate = useNavigate();

    const isSubmitting = navigation.state === "submitting";

    // local validation state
    const [error, setError] = useState("");


    function handleSubmit(e) {
        const form = e.target;
        const password = form.password.value.trim();
        const confirm = form.confirm_password.value.trim();

        if (password.length < 6) {
            e.preventDefault();
            setError("Password must be at least 6 characters.");
            return;
        }

        if (password !== confirm) {
            e.preventDefault();
            setError("Passwords do not match.");
            return;
        }

        // clear UI error if validation passed
        setError("");
    }

    return (
        <div className="Login-Container">
            <div className="Login">
                <h1>Reset Password</h1>

                <div className='Login-Form'>

                    <Form method="post" className="Todo-Form" onSubmit={handleSubmit}>

                        <div>
                            <label htmlFor='password'>New Password:</label>
                            <input
                                name="password"
                                id='password'
                                type='password'
                                required
                            />
                        </div>

                        <div>
                            <label htmlFor='confirm_password'>Confirm Password:</label>
                            <input
                                name="confirm_password"
                                id='confirm_password'
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
                            {isSubmitting ? "Updating..." : "Reset Password"}
                        </button>
                    </Form>

                    <div className='Login-Links'>
                        <ul>
                            <li>
                                <p onClick={() => navigate(-1)}>Go Back</p>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default ResetPassword;
