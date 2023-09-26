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
        return ;
      }

      if (this.newTodo.trim() !== "") {
        this.todos.push(this.newTodo);
        this.newTodo = "";
        this.inputWarning = "";
      }
    },
    removeTodo: function (index) {
      this.todos.splice(index, 1);
    },
  },
});
