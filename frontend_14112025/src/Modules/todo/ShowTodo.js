import { format } from 'date-fns';
import React, { useState } from 'react'
import { NavLink, redirect, useFetcher, useLoaderData, useNavigate } from 'react-router-dom'

const ShowTodo = () => {

    const [showDelete, setShowDelete] = useState(false);


    const loaderTodo = useLoaderData();
    const navigate = useNavigate();
    const fetcher = useFetcher();

    const todo = loaderTodo
    const date = format(todo.updated_at, "dd-MMM-yyyy hh:mm aa")

    function handleEditTodo(id) {
        navigate(`/todos/${id}/edit`)
    }

    function handleDelete() {
        fetcher.submit(null, {
            method: "post",
            action: `/todos/${todo.id}/delete`
        })
        return redirect("/todos/list")
    }

    const handleToggle = () => {
        const fd = new FormData();
        fd.append("completed", String(!todo.completed)); // send the new value

        // Submit to the action route that will call PUT /todos/:id
        fetcher.submit(fd, {
            method: "put", // use put so action sees request.method === "PUT"
            action: `/todos/${todo.id}/toggle`,
        });
    };


    return (
        <>
            <div className="Show-Todo-Container">
                <div className="Show-Todo">
                    <div className="Show-Todo-Header">
                        <label className="checkbox-container">
                            <input type="checkbox" defaultChecked={todo.completed} onChange={handleToggle} />
                            <span className="custom-checkbox"></span>
                            <h1>{todo.title}</h1>
                        </label>
                        <div className="Todo-Action">
                            <span className='Todo-Action-Items' onClick={() => handleEditTodo(todo.id)}><i className="fa-solid fa-pen-to-square"></i></span>
                            <span className='Todo-Action-Items Trash'>

                                <i className="fa-solid fa-trash" onClick={() => setShowDelete(true)}></i>

                                {showDelete && (
                                    <div className="Confirm-Popup">
                                        <p>Delete?</p>

                                        <button className="btn-confirm" onClick={handleDelete}>
                                            Yes
                                        </button>

                                        <button className="btn-cancel" onClick={() => setShowDelete(false)}>
                                            No
                                        </button>
                                    </div>
                                )}


                            </span>
                        </div>

                    </div>
                    <div className="Show-Todo-Body">
                        <p>{todo.description}</p>

                    </div>
                    <div className="Show-Todo-Footer">
                        <p><b><i>Last updated on {date}</i></b></p>
                        <p><NavLink to={"/todos/list"}>All Todos</NavLink></p>

                    </div>
                </div>
            </div>
        </>
    )
}

export default ShowTodo