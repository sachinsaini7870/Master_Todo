import { NavLink, useNavigate } from 'react-router-dom';
import TodoForm from '../components/TodoForm';


const CreateTodo = () => {

    const navigate = useNavigate();

    return (
        <>
            <div className="Login-Container">
                <div className="Login">
                    <h1>Create New Todo</h1>
                    <div className='Login-Form'>

                        <TodoForm />


                        <div className='Login-Links'>
                            <ul >
                                <li>
                                    <NavLink to={"/todos/list"}>All Todos</NavLink>
                                </li>
                                <li>
                                    <p onClick={() => navigate(-1)}>Go Back</p>
                                </li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </>
    )
}

export default CreateTodo