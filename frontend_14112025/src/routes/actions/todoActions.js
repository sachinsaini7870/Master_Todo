import { redirect } from "react-router-dom";
import { deleteTodo, updateTodo, createTodo, toggleTodo } from "../../api";


export async function deleteTodoAction({ params }) {
    await deleteTodo(params.id);
    return redirect("/todos/list");
}


export async function updateTodoAction({ params, request }) {
    const formData = await request.formData();

    const updatedTodo = {
        title: formData.get("title"),
        description: formData.get("description"),
    };

    await updateTodo(params.id, updatedTodo);

    return redirect(`/todos/list`);
}

export async function createTodoAction({ request }) {
    const formData = await request.formData();

    const Todo = {
        title: formData.get("title"),
        description: formData.get("description"),
    };

    await createTodo(Todo);

    return redirect(`/todos/list`)
}


export async function toggleTodoAction({ params, request }) {
    const id = params.id;
    const formData = await request.formData();

    const toggle = {
        completed: formData.get("completed")
    }

    await toggleTodo(id, toggle);
    return null;
}