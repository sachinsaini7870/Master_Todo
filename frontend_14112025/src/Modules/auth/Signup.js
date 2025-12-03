import React from 'react'
import { Form, NavLink, useActionData, useNavigation } from 'react-router-dom'

const Signup = () => {

    const actionData = useActionData();
    const navigation = useNavigation();

    const isSubmitting = navigation.state === "submitting";


    return (
        <div className="Login-Container">
            <div className="Login">
                <h1>Signup</h1>
                <div className="Login-Form">
                    <Form method="post" className="Todo-Form" >

                        <div>
                            <label>Username:</label>
                            <input name="username" type="text" required />
                        </div>
                        <div>
                            <label>Email:</label>
                            <input name="email" type="email" required />
                        </div>
                        <div>
                            <label>Password:</label>
                            <input name="password" type="password" required />
                        </div>

                        {/* backend action errors */}
                        {actionData?.error && <p className='Resend-Otp-Error'>{actionData.error}</p>}
                        {actionData?.success && <p className="Resend-Otp">{actionData.message}</p>}

                        <button type="submit" className="Button">
                            {isSubmitting ? "Sending..." : "Send OTP"}
                        </button>

                    </Form>

                    <div className="Login-Links">
                        <ul >
                            <li>
                                <NavLink to={"/auth/login"}>Login</NavLink>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>

    )
}

export default Signup