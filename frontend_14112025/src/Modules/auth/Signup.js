import React, { useState } from 'react'
import { Form, NavLink } from 'react-router-dom'

const Signup = () => {

    const [isSubmitting, setIsSubmitting] = useState(false)

    function handleSubmit() {
        setIsSubmitting(true)
    }

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
                        <button type="submit" className="Button"
                            onClick={handleSubmit}
                        >
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