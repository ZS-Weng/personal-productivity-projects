<script>
  export let task;
</script>

<div class="task-item">
  <h3>{task.title}</h3>
  <p>{task.description}</p>
  <span>Status: {task.completed ? 'Completed' : 'Pending'}</span>
</div>

<style>
  .task-item {
    border: 1px solid #ccc;
    padding: 10px;
    margin: 10px 0;
    border-radius: 5px;
  }
  .task-item h3 {
    margin: 0;
  }
  .task-item p {
    margin: 5px 0;
  }
  .task-item span {
    font-weight: bold;
  }
</style>