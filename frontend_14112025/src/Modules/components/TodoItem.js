import React, { useEffect, useRef, useState } from 'react'
import { format } from 'date-fns'
import { useFetcher, useNavigate } from 'react-router-dom'

const TodoItem = ({ todo }) => {

    const [showDelete, setShowDelete] = useState(false);
    const popupRef = useRef(null);

    const date = format(todo.updated_at, "dd-MMM-yyyy hh:mm aa")
    const navigate = useNavigate();
    const fetcher = useFetcher();


    // ⭐ CLOSE POPUP ON OUTSIDE CLICK
    useEffect(() => {
        function handleClickOutside(e) {
            // if popup is open AND click is outside
            if (showDelete && popupRef.current && !popupRef.current.contains(e.target)) {
                setShowDelete(false);
            }
        }

        document.addEventListener("mousedown", handleClickOutside);
        return () => document.removeEventListener("mousedown", handleClickOutside);
    }, [showDelete]);

    function handleShowTodo(id, state) {
        navigate(`/todos/${id}`, { state: state })
    }

    function handleEditTodo(id) {
        navigate(`/todos/${id}/edit`)
    }

    function handleDelete() {
        fetcher.submit(null, {
            method: "post",
            action: `/todos/${todo.id}/delete`
        })
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
            <div className="Todo-Item">
                <div className="Todo-Item-Header">
                    <div className='Todo-Item-Title'>
                        <label className="checkbox-container" >
                            <input type="checkbox" defaultChecked={todo.completed} onChange={handleToggle} />
                            <span className="custom-checkbox"></span>
                        </label>
                        <h1 onClick={() => handleShowTodo(todo.id, todo)}>{todo.title}</h1>
                    </div>
                    <div className="Todo-Action">

                        <span className='Todo-Action-Items' onClick={() => handleEditTodo(todo.id)}><i className="fa-solid fa-pen-to-square"></i></span>

                        <span className='Todo-Action-Items Trash' >
                            <i className="fa-solid fa-trash" onClick={() => setShowDelete(true)}></i>

                            {showDelete && (
                                <div className="Confirm-Popup" ref={popupRef}>
                                    {fetcher.state === "submitting"? <p className="Delete-Popup">Deleting...  </p> : <p>Delete?</p> }

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
                <div className="Todo-Item-Body">
                    <p>{todo.description}</p>

                </div>
                <div className="Todo-Item-Footer">
                    <p><b><i>Last updated on {date}</i></b></p>
                </div>
            </div>

        </>
    )
}

export default TodoItem

