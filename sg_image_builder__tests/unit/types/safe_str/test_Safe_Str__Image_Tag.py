from unittest import TestCase

from sg_image_builder.types.safe_str.Safe_Str__Image_Tag import Safe_Str__Image_Tag


class test_Safe_Str__Image_Tag(TestCase):
    def test__init__rejects_empty(self):  # allow_empty=False; empty tag is never valid
        with self.assertRaises(ValueError):
            Safe_Str__Image_Tag('')

    def test__accepts_common_tags(self):  # The canon - real-world tags from docker hub
        for tag in ('latest', '22.04', 'v1.2.3', 'v1.2.3-rc.1', 'alpine3.18', '1.0', '_alpha'):
            with self.subTest(tag=tag):
                assert str(Safe_Str__Image_Tag(tag)) == tag

    def test__accepts_max_length(self):  # 128 chars is the OCI ceiling
        tag = 'a' + 'b' * 127  # 128 chars total
        assert str(Safe_Str__Image_Tag(tag)) == tag

    def test__rejects_over_max_length(self):  # 129 chars is one over
        with self.assertRaises(ValueError):
            Safe_Str__Image_Tag('a' + 'b' * 128)

    def test__rejects_leading_period(self):  # OCI: must not start with `.`
        with self.assertRaises(ValueError):
            Safe_Str__Image_Tag('.hidden')

    def test__rejects_leading_dash(self):  # OCI: must not start with `-`
        with self.assertRaises(ValueError):
            Safe_Str__Image_Tag('-flag')

    def test__rejects_disallowed_chars(self):  # Spaces, plus, slashes etc. not allowed
        for bad in ('with space', 'with+plus', 'with/slash', 'with:colon', 'with@at'):
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    Safe_Str__Image_Tag(bad)
