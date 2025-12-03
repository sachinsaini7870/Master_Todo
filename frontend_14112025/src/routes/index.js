// import { RouterProvider, createBrowserRouter } from "react-router-dom";
import { RootLayout } from "../Modules/layouts";
import RootError from "../Modules/components/RootError";
import { TodosRoutes } from "./todoRoutes";
import { AuthRoutes } from "./authRoutes";


const routes = [
    {
        path: "/",
        Component: RootLayout,
        ErrorBoundary: RootError,
        children: [
            ...TodosRoutes,
            ...AuthRoutes,
        ]
    }
];

export default routes