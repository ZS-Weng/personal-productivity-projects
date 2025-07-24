<script>
  import { onMount } from 'svelte';
  import { taskStore } from '../stores/taskStore';
  
  let task = {
    title: '',
    description: ''
  };

  let isEditing = false;

  onMount(() => {
    if (taskStore.selectedTask) {
      task = { ...taskStore.selectedTask };
      isEditing = true;
    }
  });

  function handleSubmit() {
    if (isEditing) {
      taskStore.updateTask(task);
    } else {
      taskStore.addTask(task);
    }
    resetForm();
  }

  function resetForm() {
    task = { title: '', description: '' };
    isEditing = false;
    taskStore.selectedTask = null;
  }
</script>

<form on:submit|preventDefault={handleSubmit}>
  <label>
    Title:
    <input type="text" bind:value={task.title} required />
  </label>
  <label>
    Description:
    <textarea bind:value={task.description} required></textarea>
  </label>
  <button type="submit">{isEditing ? 'Update Task' : 'Add Task'}</button>
  <button type="button" on:click={resetForm}>Cancel</button>
</form>

<style>
  form {
    display: flex;
    flex-direction: column;
  }
  label {
    margin-bottom: 1em;
  }
  button {
    margin-top: 1em;
  }
</style>