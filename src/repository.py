todo: list[str] = []


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
        return todo
    
    @staticmethod
    def get_one(todo_name: str) -> bool:
        return todo_name in todo
    
    @classmethod
    def create(cls, todo_name: str):
        cls._check_instance(todo_name)
        todo.append(todo_name)

    @classmethod
    def delete(cls, todo_name: str):
        cls._check_instance(todo_name)
        todo.remove(todo_name)