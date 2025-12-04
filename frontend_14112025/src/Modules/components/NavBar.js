import React from 'react'
import { NavLink, useLocation, useNavigate } from 'react-router-dom'
import { useAuth } from '../../hooks/useAuth'

const NavBar = () => {
    const { user, logout, isAuthenticated } = useAuth()
    const navigate = useNavigate();
    const location = useLocation();

    const hideCreateButton = location.pathname === "/todos/create";

    const onLogout = () => {
        logout()
        navigate("/auth/login")
    }

    return (
        <>
            <div className='Auth-Navbar'>
                <div className='Logo' onClick={() => navigate("/todos/list")}>Todo App</div>
                <div className='Nav-Menu'>
                    {isAuthenticated ?
                        <>
                            <ul className='Nav-List'>
                                {!hideCreateButton && (
                                    <li>
                                        <NavLink to={"/todos/create"}><i className="fa-solid fa-plus Todo-Icons"></i>Create</NavLink>
                                    </li>

                                )}
                                <div className="Profile">
                                    <i className="fa-regular fa-circle-user Profile-icon"></i>{user}
                                    <div className='Profile-Menu'>
                                        <p onClick={() => navigate("/todos/change-password")}>Change Password</p>
                                        <p onClick={onLogout}>Logout</p>
                                    </div>
                                </div>
                            </ul>
                        </>
                        :
                        <></>
                    }
                </div>
            </div>
        </>
    )
}

export default NavBar