// import React, { useEffect, useState } from "react";
import { useState } from "react";
import { Form } from "react-router-dom";


export default function TodoForm({
    initialTodo = { title: "", description: "" }
}) {
    const form = initialTodo;

    const [error, setError] = useState("");

    function handleSubmit(e) {
        const createForm = e.target;
        const title = createForm.title.value.trim();

        if (!title) {
            e.preventDefault();
            setError("Title cannot be empty");
            return;
        }

        // clear UI error if validation passed
        setError("");
    }


    return (
        <>
            <Form method="post" className="Todo-Form" onSubmit={handleSubmit}>
                <div>
                    <label htmlFor="title">Title:</label>
                    <input
                        name="title"
                        id="title"
                        type="text"
                        placeholder='Enter Todo Title'
                        defaultValue={form.title}
                        autoFocus
                        required
                    />
                </div>

                <div>
                    <label htmlFor="description">Description:</label>
                    <textarea
                        name="description"
                        id="description"
                        type="text"
                        placeholder='Enter Todo Description'
                        rows={5}
                        defaultValue={form.description}
                    />
                </div>


                {/* frontend validation error */}
                {error && <p className="Resend-Otp-Error">{error}</p>}


                <button
                    type="submit"
                    className='Button'
                >
                    Save Todo
                </button>
            </Form>
        </>
    );
}
