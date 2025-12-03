import React, { useEffect, useRef, useState } from 'react'
import { Form, useActionData, useFetcher, useNavigate } from 'react-router-dom'

const VerifySignUp = () => {

    const fetcher = useFetcher();
    const timeoutRef = useRef(null);
    const navigate = useNavigate();

    const [isSubmitting, setIsSubmitting] = useState(false)

    function handleSubmit() {
        setIsSubmitting(true)
        return null
    }

    function handleResend() {
        const fd = new FormData();
        const email = localStorage.getItem("email");
        if (email) {
            fd.append("email", String(email));

            fetcher.submit(fd, {
                method: "post",
                action: "/auth/resend-otp",
            });

            clearTimeout(timeoutRef.current);
            timeoutRef.current = setTimeout(() => {

            }, 5000);
            return null
        }
    }

    useEffect(() => {
        return () => clearTimeout(timeoutRef.current);
    }, []);


    return (
        <div className="Login-Container">
            <div className="Login">
                <h1>Signup verify</h1>
                <div className="Login-Form">

                    <Form method="post" className="Todo-Form">

                        <div>
                            <label htmlFor='otp'>OTP:</label>
                            <input name="otp" id='otp' maxLength={6} required />
                        </div>

                        <button type="submit"
                            className="Button"
                            onClick={handleSubmit}
                        >
                            {isSubmitting ? "Verifying..." : "Register"}

                        </button>

                    </Form>

                    <div className="Login-Links">
                        {fetcher.data?.error && (
                            <p className='Resend-Otp-Error'>{fetcher.data.error}</p>
                        )}
                        {fetcher.data?.success && (
                            <p className="Resend-Otp">{fetcher.data.message}</p>
                        )}
                        <ul >

                            <li>
                                <p onClick={() => navigate(-1)}>Go Back</p>
                            </li>
                            <li>
                                {fetcher.state === "submitting" ? <p>Sending...</p> : <p onClick={handleResend}>ReSend Otp</p>}
                            </li>

                        </ul>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default VerifySignUp