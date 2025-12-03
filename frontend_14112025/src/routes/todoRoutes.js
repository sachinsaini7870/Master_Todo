import { CreateTodo, EditTodo, ListTodo, ShowTodo, } from "../Modules/todo/";
import RootError from "../Modules/components/RootError";
import TodoLayouts from "../Modules/layouts/TodoLayout";
import { protectedLoader } from "./loaders/protectedLoader";
import { redirect } from "react-router-dom";
import { showTodoLoader, fetchTodosLoader } from "./loaders/todoLoaders";
import { createTodoAction, deleteTodoAction, toggleTodoAction, updateTodoAction } from "./actions/todoActions";
import ChangePassword from "../Modules/auth/ChangePassword";
import { changePasswordAction } from "./actions/authActions";


export const TodosRoutes = [
    {
        index: true,
        loader: () => redirect("todos")
    },
    {
        path: "todos",
        Component: TodoLayouts,
        loader: protectedLoader,
        ErrorBoundary: RootError,
        children: [
            { index: true, loader: () => redirect("list") },
            { path: "list", loader: fetchTodosLoader, Component: ListTodo },
            { path: "create", action: createTodoAction, Component: CreateTodo },
            { path: ":id", loader: showTodoLoader, Component: ShowTodo },
            { path: ":id/edit", loader: showTodoLoader, action: updateTodoAction, Component: EditTodo },
            { path: ":id/delete", action: deleteTodoAction },
            { path: ":id/toggle", action: toggleTodoAction },
            { path: "change-password",  Component: ChangePassword, action: changePasswordAction },
        ]
    }
]