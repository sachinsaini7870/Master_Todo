import React from 'react'
import { Form, NavLink, useActionData, useNavigation } from 'react-router-dom'

const Forgot = () => {

    const actionData = useActionData();
    const navigation = useNavigation();

    const isSubmitting = navigation.state === "submitting";

    return (
        <>
            <div className="Login-Container">
                <div className="Login">
                    <h1>Forgot Password</h1>
                    <div className='Login-Form'>

                        <Form method="post" className="Todo-Form">
                            <div>
                                <label htmlFor='email'>Email:</label>
                                <input name="email" id='email' type='email' required />
                            </div>

                            <button type="submit"
                                className="Button"
                            // onClick={handleSubmit}
                            >
                                {isSubmitting ? "Sending..." : "Send Rest Link"}

                            </button>

                        </Form>

                        <div className='Login-Links'>
                            {actionData?.error  && (
                                <p className='Resend-Otp-Error'>{actionData.error}</p>
                            )}
                            {actionData?.success && (
                                <p className="Resend-Otp">{actionData.message}</p>
                            )}
                            <ul >
                                <li>
                                    <NavLink to={"/auth/login"}>Login</NavLink>
                                </li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </>
    )
}

export default Forgot