import { fetchTodos, getTodoById } from "../../api/todoApi"; // your API call


// export async function fetchTodosLoader() {

//     const res = await fetchTodos();

//     if (!res) throw new Error("Failed to load todos");
    
//     return res;
// }

export async function fetchTodosLoader({ request }) {
    const url = new URL(request.url);
    const completed = url.searchParams.get("completed"); // "true" | "false" | null

    const todos = await fetchTodos(completed);

    return {
        todos,
        completedFilter: completed || "all"
    };
}



export async function showTodoLoader({ params }) {
    
    const res = await getTodoById(params.id)
    if (!res) throw new Error("Failed to load todo by id");    
    
    return res;
}
