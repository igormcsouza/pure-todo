import unittest
from unittest import TestCase, mock

from .repository import TodoRepository, InsertionException, Singleton


class TodoRepositoryTestCase(TestCase):

    def setUp(self) -> None:
        Singleton.todos = ["this", "is", "a", "todo", "test"]

        return super().setUp()

    def test_get_all(self):
        todos = TodoRepository.get_all()
        self.assertListEqual(todos, ["this", "is", "a", "todo", "test"])

    def test_create(self):
        TodoRepository.create("one extra")
        self.assertIn("one extra", Singleton.todos)

    def test_delete(self):
        TodoRepository.delete("test")
        self.assertNotIn("test", Singleton.todos)

    def test_delete_no_int(self):
        try:
            TodoRepository.delete(1)
        except InsertionException as e:
            self.assertEqual(
                str(e), "The given todo is not a str, but <class 'int'>")

    @mock.patch("logging.warning")
    def test_delete_nothing(self, warning_patch):
        TodoRepository.delete("matheus")
        warning_patch.assert_called_once_with(
            "Could not remove 'matheus' because is not currently "
            "in the list."
        )
        self.assertListEqual(
            Singleton.todos, ["this", "is", "a", "todo", "test"])

    def test_get_one(self):
        is_there = TodoRepository.get_one("this")
        self.assertTrue(is_there)

    def test_get_one_false(self):
        is_there = TodoRepository.get_one("igor")
        self.assertFalse(is_there)

    def tearDown(self) -> None:
        Singleton.todos = []
        return super().tearDown()


if __name__ == '__main__':
    unittest.main()
