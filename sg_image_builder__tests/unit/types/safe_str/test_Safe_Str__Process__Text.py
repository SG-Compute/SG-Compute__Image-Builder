from unittest import TestCase

from sg_image_builder.types.safe_str.Safe_Str__Process__Text import Safe_Str__Process__Text


class test_Safe_Str__Process__Text(TestCase):
    def test__init__accepts_empty(self):  # Empty default is the Type_Safe auto-init state
        assert str(Safe_Str__Process__Text()) == ''
        assert str(Safe_Str__Process__Text('')) == ''

    def test__preserves_trailing_newline(self):  # Regression: Safe_Str__Http__Text trims trailing whitespace
        s = Safe_Str__Process__Text('Linux ...\n')
        assert str(s) == 'Linux ...\n'

    def test__preserves_leading_whitespace(self):  # And leading - same trim_whitespace=False reason
        s = Safe_Str__Process__Text('   indented line')
        assert str(s) == '   indented line'

    def test__preserves_shell_chars(self):  # Regression: Safe_Str__Text strips slashes / quotes / pipes
        s = Safe_Str__Process__Text('/usr/bin/ls -la "with quotes" | grep foo')
        assert str(s) == '/usr/bin/ls -la "with quotes" | grep foo'

    def test__preserves_multiline_output(self):  # Real-world build output is multi-line
        body = 'line one\nline two\nline three\n'
        s = Safe_Str__Process__Text(body)
        assert str(s) == body

    def test__strips_control_chars(self):  # Inherited from Safe_Str__Http__Text: null and friends are stripped
        s = Safe_Str__Process__Text('hello\x00world\x07')
        body = str(s)
        assert '\x00' not in body
        assert '\x07' not in body

    def test__preserves_tab_and_lf(self):  # Tab + LF kept verbatim - they carry meaning in CLI output
        body = 'col1\tcol2\nrow2\nrow3'
        s = Safe_Str__Process__Text(body)
        assert str(s) == body

    def test__normalises_crlf_to_lf(self):  # Inherited from Safe_Str__Http__Text: CR becomes LF.
        # Acceptable for captured stdout where consumers expect LF.
        s = Safe_Str__Process__Text('row1\r\nrow2')
        assert str(s) == 'row1\nrow2'

    def test__max_length_is_ten_megabytes(self):  # Sanity check of the class-level constant
        assert Safe_Str__Process__Text.max_length == 10 * 1024 * 1024
