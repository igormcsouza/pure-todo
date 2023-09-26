new Vue({
  el: "#app",
  data: {
    newTodo: "",
    todos: [],
    inputWarning: "",
  },
  methods: {
    addTodo: function () {
      if (this.newTodo.length > 12) {
        this.inputWarning = "Max input size is 12!";
        return;
      }

      if (this.newTodo.trim() !== "") {
        // Send a POST request to the backend to add the new todo
        fetch('/add-todo', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ todo: this.newTodo }),
        })
        .then(response => {
          if (response.ok) {
            // If the POST request is successful, reset the input field and fetch the updated todos
            this.newTodo = "";
            this.inputWarning = "";
            this.fetchTodos();
          } else {
            // Handle errors here
            console.error('Error adding todo:', response.status);
          }
        })
        .catch(error => {
          console.error('Error adding todo:', error);
        });
      }
    },
    removeTodo: function (index) {
      // Send a request to the backend to remove the todo at the specified index
      const todoToRemove = this.todos[index];
      fetch(`/remove-todo/${todoToRemove}`, {
        method: 'DELETE',
      })
      .then(response => {
        if (response.ok) {
          // If the DELETE request is successful, fetch the updated todos
          this.fetchTodos();
        } else {
          // Handle errors here
          console.error('Error removing todo:', response.status);
        }
      })
      .catch(error => {
        console.error('Error removing todo:', error);
      });
    },
    fetchTodos: function () {
      // Send a GET request to the backend to fetch the updated list of todos
      fetch('/get-todos')
      .then(response => response.json())
      .then(data => {
        if (data.todos) {
          this.todos = data.todos;
        }
      })
      .catch(error => {
        console.error('Error fetching todos:', error);
      });
    },
  },
  mounted() {
    // Fetch the initial list of todos when the component is mounted
    this.fetchTodos();
  },
});
