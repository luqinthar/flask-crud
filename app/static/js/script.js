async function fetchTodos() {
    const res = await fetch('/todos');
    const todos = await res.json();
    const list = document.getElementById('todoList');
    list.innerHTML = '';
    todos.forEach(todo => {
        const li = document.createElement('li');
        li.textContent = todo.task;
        const del = document.createElement('button');
        del.textContent = 'Delete';
        del.onclick = () => deleteTodo(todo.id);
        li.appendChild(del);
        list.appendChild(li);
    });
}

async function addTodo() {
    const task = document.getElementById('taskInput').value;
    if (!task) return;
    await fetch('/todos', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ task })
    });
    document.getElementById('taskInput').value = '';
    fetchTodos();
}

async function deleteTodo(id) {
    await fetch('/todos/' + id, { method: 'DELETE' });
    fetchTodos();
}

window.onload = fetchTodos;
