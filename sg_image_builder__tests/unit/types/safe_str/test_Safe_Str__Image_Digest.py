from unittest import TestCase

from sg_image_builder.types.safe_str.Safe_Str__Image_Digest import Safe_Str__Image_Digest


class test_Safe_Str__Image_Digest(TestCase):
    SHA256 = 'sha256:' + 'a' * 64
    SHA512 = 'sha512:' + 'f' * 128

    def test__init__rejects_empty(self):  # allow_empty=False; an empty digest is never valid
        with self.assertRaises(ValueError):
            Safe_Str__Image_Digest('')

    def test__accepts_sha256(self):  # 64 lowercase hex chars
        assert str(Safe_Str__Image_Digest(self.SHA256)) == self.SHA256

    def test__accepts_sha512(self):  # 128 lowercase hex chars
        assert str(Safe_Str__Image_Digest(self.SHA512)) == self.SHA512

    def test__rejects_wrong_sha256_length(self):  # 63 chars is one short
        with self.assertRaises(ValueError):
            Safe_Str__Image_Digest('sha256:' + 'a' * 63)

    def test__rejects_wrong_sha512_length(self):  # 127 chars is one short
        with self.assertRaises(ValueError):
            Safe_Str__Image_Digest('sha512:' + 'a' * 127)

    def test__rejects_uppercase_hex(self):  # OCI digests are lowercase
        with self.assertRaises(ValueError):
            Safe_Str__Image_Digest('sha256:' + 'A' * 64)

    def test__rejects_unsupported_algorithm(self):  # md5, sha1, sha384 not in OCI distribution-spec
        for bad in ('md5:' + 'a' * 32, 'sha1:' + 'a' * 40, 'sha384:' + 'a' * 96):
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    Safe_Str__Image_Digest(bad)

    def test__rejects_missing_prefix(self):  # bare hex without algorithm prefix
        with self.assertRaises(ValueError):
            Safe_Str__Image_Digest('a' * 64)

    def test__rejects_non_hex_chars(self):  # `g` is not in [0-9a-f]
        with self.assertRaises(ValueError):
            Safe_Str__Image_Digest('sha256:' + 'g' * 64)
