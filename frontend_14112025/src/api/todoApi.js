import api from "./api";

const todos = "/api/todos"

// export const fetchTodos = async (params = null) => {
//     const res = await api.get(todos + "/", { params: { params } });
//     return res.data;
// };

export const fetchTodos = async (completed = null) => {
    const params = {};

    if (completed !== null) {
        params.completed = completed; // backend expects ?completed=true/false
    }

    const res = await api.get(todos + "/", { params });
    return res.data;
};


export const createTodo = async (payload) => {
    const res = await api.post(todos + "/", payload);
    return res.data;
};

export const updateTodo = async (id, payload) => {
    const res = await api.put(todos + `/${id}`, payload);
    return res.data;
};

export const deleteTodo = async (id) => {
    const res = await api.delete(todos + `/${id}`);
    return res.data;
};

export const toggleTodo = async (id, payload) => {
    const res = await api.put(todos + `/${id}`, payload);
    return res.data;
};

export const getTodoById = async (id) => {
    const res = await api.get(todos + `/${id}`);
    return res.data;
};
