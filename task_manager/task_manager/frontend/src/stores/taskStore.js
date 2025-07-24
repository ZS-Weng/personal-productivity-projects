import { writable } from 'svelte/store';

const createTaskStore = () => {
    const { subscribe, set, update } = writable([]);

    return {
        subscribe,
        addTask: (task) => update(tasks => [...tasks, task]),
        removeTask: (taskId) => update(tasks => tasks.filter(task => task.id !== taskId)),
        setTasks: (tasks) => set(tasks),
        clearTasks: () => set([])
    };
};

export const taskStore = createTaskStore();