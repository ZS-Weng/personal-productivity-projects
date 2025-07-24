<script>
  import TaskForm from './components/TaskForm.svelte';
  import TaskItem from './components/TaskItem.svelte';
  import { taskStore } from './stores/taskStore.js';

  let tasks = taskStore.tasks;

  function addTask(task) {
    taskStore.addTask(task);
  }

  function removeTask(taskId) {
    taskStore.removeTask(taskId);
  }
</script>

<main>
  <h1>Task Manager</h1>
  <TaskForm on:addTask={addTask} />
  <ul>
    {#each tasks as task (task.id)}
      <TaskItem {task} on:removeTask={removeTask} />
    {/each}
  </ul>
</main>

<style>
  main {
    padding: 1em;
    max-width: 600px;
    margin: 0 auto;
    font-family: Arial, sans-serif;
  }

  h1 {
    text-align: center;
  }

  ul {
    list-style-type: none;
    padding: 0;
  }
</style>