import logging


class Singleton:
    todos: list[str] = []


class InsertionException(Exception):
    pass


class TodoRepository:

    @staticmethod
    def _check_instance(todo_name: str):
        if not isinstance(todo_name, str):
            raise InsertionException(
                f"The given todo is not a str, but {type(todo_name)}")

    @staticmethod
    def get_all() -> list[str]:
        return Singleton.todos

    @staticmethod
    def get_one(todo_name: str) -> bool:
        return todo_name in Singleton.todos

    @classmethod
    def create(cls, todo_name: str):
        cls._check_instance(todo_name)
        Singleton.todos.append(todo_name)

    @classmethod
    def delete(cls, todo_name: str):
        cls._check_instance(todo_name)
        try:
            Singleton.todos.remove(todo_name)
        except ValueError:
            logging.warning(f"Could not remove '{todo_name}' because is not "
                            "currently in the list.")
