import unittest
from service import subscribe, subscribers


class SubscribeTest(unittest.TestCase):
    def setUp(self):
        subscribers.clear()

    def test_subscribe(self):
        self.assertEqual(subscribe("Ann"), {"subscribed": True})
        self.assertEqual(subscribers, {"Ann"})

    def test_empty(self):
        with self.assertRaises(ValueError):
            subscribe(" ")

    def test_duplicate(self):
        subscribe("Ann")
        subscribe("Ann")
        self.assertEqual(len(subscribers), 1)

    def test_large_name_rejected(self):
        # Feature A: reject overly long names as invalid input
        long_name = "A" * 256
        with self.assertRaises(ValueError):
            subscribe(long_name)

    def test_dependency_error_handled(self):
        # Feature B: simulate dependency failure and expect explicit error
        # We monkey-patch an imaginary dependency flag for this demo
        import service
        service.fail_dependency = True
        try:
            with self.assertRaises(RuntimeError):
                subscribe("Bob")
        finally:
            # cleanup
            if hasattr(service, 'fail_dependency'):
                delattr(service, 'fail_dependency')

    def test_capacity_limit(self):
        # Feature B: capacity limit of unique subscribers
        # Fill up to capacity with unique names
        for i in range(100):
            subscribe(f"user{i}")
        self.assertEqual(len(subscribers), 100)

        # Duplicates should not consume capacity
        subscribe("user0")
        self.assertEqual(len(subscribers), 100)

        # Adding a 101st unique subscriber should fail with a clear error
        with self.assertRaises(RuntimeError) as ctx:
            subscribe("extra")
        self.assertEqual(str(ctx.exception), "capacity exceeded")
        # Ensure not added
        self.assertEqual(len(subscribers), 100)


if __name__ == "__main__":
    unittest.main()
