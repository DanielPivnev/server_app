import unittest

from cIient import create_presence, process_answer, main


class TestClient(unittest.TestCase):

    def test_create_presence_presence(self):
        self.assertEqual(create_presence()['action'], 'presence')

    def test_create_presence_time(self):
        self.assertEqual(type(create_presence()['time']), float)

    def test_create_presence_account_name(self):
        self.assertEqual(create_presence()['user']['account_name'], 'Guest')

    def test_create_presence_account_name_attr(self):
        self.assertEqual(create_presence('test')['user']['account_name'], 'test')

    def test_process_answer_HTTP_200_OK(self):
        self.assertEqual(process_answer({'response': 200, 'alert': 'OK'}), '200 OK')

    def test_process_answer_HTTP_400_bad_request(self):
        self.assertEqual(process_answer({'response': 400, 'error': 'Bad Request'}), '400 Bad Request')

    def test_process_answer_raise_value_error(self):
        self.assertRaises(ValueError, process_answer, 'test')

    def test_main(self):
        self.assertEqual(main(), None)


if __name__ == "__main__":
    unittest.main()
