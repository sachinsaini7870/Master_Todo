import React from 'react'
import { NavBar } from '../components'
import { Outlet } from 'react-router-dom'

const RootLayout = () => {
    return (
        <>
            <div className="Layout-Container">
                <NavBar />
                <Outlet />
            </div>
        </>
    )
}

export default RootLayout