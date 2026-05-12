from unittest import TestCase

from sg_image_builder.types.safe_str.Safe_Str__Image_Repository import Safe_Str__Image_Repository


class test_Safe_Str__Image_Repository(TestCase):
    def test__init__accepts_empty_as_sentinel(self):  # allow_empty=True so Type_Safe auto-init works
        assert str(Safe_Str__Image_Repository()) == ''
        assert str(Safe_Str__Image_Repository('')) == ''

    def test__accepts_single_component(self):  # OCI grammar: bare name (e.g. `ubuntu`)
        for ok in ('ubuntu', 'app1', 'a_b', 'app.v2', 'app-v2', 'app__v2'):
            with self.subTest(ok=ok):
                assert str(Safe_Str__Image_Repository(ok)) == ok

    def test__accepts_path_components(self):  # OCI grammar: `org/sub/app`
        for ok in ('library/ubuntu', 'org/app', 'org/sub/app', 'org/sub/sub2/app'):
            with self.subTest(ok=ok):
                assert str(Safe_Str__Image_Repository(ok)) == ok

    def test__preserves_slashes(self):  # Regression: Safe_Str__Text silently strips `/` to `_`
        s = Safe_Str__Image_Repository('library/ubuntu')
        assert '/' in str(s)
        assert '_' not in str(s)

    def test__rejects_uppercase(self):  # OCI repository names are lowercase-only
        for bad in ('Ubuntu', 'Library/ubuntu', 'org/App'):
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    Safe_Str__Image_Repository(bad)

    def test__rejects_leading_or_trailing_slash(self):  # Each component must start/end with [a-z0-9]
        for bad in ('/leading', 'trailing/', '/both/'):
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    Safe_Str__Image_Repository(bad)

    def test__rejects_disallowed_chars(self):  # Plus, at, colon etc. not allowed
        for bad in ('a+b', 'a@b', 'a:b', 'a b', 'a..b'):  # `..` would mean empty component
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    Safe_Str__Image_Repository(bad)

    def test__rejects_over_max_length(self):  # 256 chars is one over
        with self.assertRaises(ValueError):
            Safe_Str__Image_Repository('a' * 256)
