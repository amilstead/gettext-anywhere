import gettext
import unittest


class TestMonkeyPatch(unittest.TestCase):

    def test_patch(self):
        import gettext_anywhere
        from gettext_anywhere import monkey
        self.assertTrue(monkey._patched)
        self.assertEqual(gettext.translation, monkey._translation)

    def test_unpatch(self):
        self.test_patch()
        from gettext_anywhere import monkey
        monkey.unpatch()
        self.assertFalse(monkey._patched)
        self.assertNotEqual(gettext.translation, monkey._translation)


if __name__ == "__main__":
    unittest.main()
