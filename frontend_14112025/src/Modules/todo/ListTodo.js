import TodoItem from '../components/TodoItem'
import { NavLink, useLoaderData } from 'react-router-dom'
import TodoNotFound from '../components/TodoNotFound';
import { useAuth } from '../../hooks/useAuth';
import { useEffect } from 'react';

const ListTodo = () => {

    const { setToken, setUser } = useAuth();
    const { todos, completedFilter } = useLoaderData();

    useEffect(() => {
        const token = localStorage.getItem("token");
        if (token) {
            setToken(token)
        }
        let user = localStorage.getItem("user");
        user = user.replace(/"/g, "");
        if (token) {
            setUser(user)
        }
    }, []);



    return (
        <>
            <div className="Todo-Container">
                <div className="Todo">
                    <div className="Todo-Tab">
                        <div className="Tab-Menu">
                            <NavLink to="/todos/list" className={completedFilter === "all" ? "Active" : ""}>
                                All Todos
                            </NavLink>

                            <NavLink to="/todos/list?completed=false" className={completedFilter === "false" ? "Active" : ""}>
                                Pending Todos
                            </NavLink>

                            <NavLink to="/todos/list?completed=true" className={completedFilter === "true" ? "Active" : ""}>
                                Completed Todos
                            </NavLink>

                        </div>
                    </div>
                    <div className="Todo-Body">

                        {todos && todos.length >= 0 ? todos.map((todo) => (

                            <TodoItem todo={todo} key={todo.id} />

                        )) : <TodoNotFound completedFilter={completedFilter} />}

                    </div>
                </div>
            </div >
        </>
    )
}

export default ListTodo

