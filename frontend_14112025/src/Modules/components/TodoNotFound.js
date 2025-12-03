import React from 'react'
import { NavLink } from 'react-router-dom'

const TodoNotFound = ({ completedFilter }) => {

    let createLink = false

    if (completedFilter === "all") {
        createLink = true
    }

    return (
        <>
            <div className="Login-Container">
                <div className="Login">
                    <h1>Todo Not Found ! </h1>


                    <div className='Login-Links'>
                        <ul >
                            {
                                createLink ?
                                    <li className='Todo-Nav-Links'>
                                        <NavLink to={"/todos/create"} >Create Todo</NavLink>
                                    </li>
                                    :
                                    <li className='Todo-Nav-Links'>
                                        <NavLink to={"/todos/list"} >All Todos</NavLink>
                                    </li>
                            }
                        </ul>
                    </div>
                </div>
            </div>
        </>
    )
}

export default TodoNotFound