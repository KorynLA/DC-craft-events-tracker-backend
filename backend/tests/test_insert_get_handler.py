import pytest
import html
from handlers.insert_event_handler import sanitize_input


class TestSanitizeInput:

    def test_none_input_returns_none(self):
        assert sanitize_input(None) is None

    def test_empty_string_returns_none(self):
        assert sanitize_input("") is None

    def test_script_tags_are_removed(self):
        input_str = "<script>alert('xss')</script>Hello"
        result = sanitize_input(input_str)

        assert "<script>" not in result.lower()
        assert "</script>" not in result.lower()
        assert "alert" not in result.lower()
        assert "Hello" in result

    def test_script_with_attributes_removed(self):
        input_str = '<script type="text/javascript">malicious()</script>'
        result = sanitize_input(input_str)

        assert "<script>" not in result.lower()
        assert "malicious" not in result.lower()

    def test_sql_injection_like_input_is_escaped(self):
        input_str = "Robert'); DROP TABLE users;--"
        result = sanitize_input(input_str)

        # Ensure raw SQL special chars are escaped
        assert "DROP TABLE" in result
        assert "'" not in result
        assert html.escape(input_str) == result

    def test_common_sql_injection_patterns(self):
        input_str = "' OR '1'='1"
        result = sanitize_input(input_str)

        assert "'" not in result
        assert "&apos;" in result or "&#x27;" in result

    def test_emojis_are_removed(self):
        input_str = "Hello 👋🌍"
        result = sanitize_input(input_str)

        assert "👋" not in result
        assert "🌍" not in result
        assert result == "Hello "

    def test_mixed_text_html_and_emoji(self):
        input_str = "<b>Hello</b> 😊"
        result = sanitize_input(input_str)

        assert "😊" not in result
        assert "&lt;b&gt;" in result
        assert "&lt;/b&gt;" in result

    def test_combined_xss_sql_and_emoji(self):
        input_str = "<script>alert('x')</script> OR 1=1 😊"
        result = sanitize_input(input_str)

        assert "<script>" not in result.lower()
        assert "alert" not in result.lower()
        assert "😊" not in result
        assert "'" not in result
        assert "OR 1=1" in result

    def test_html_is_escaped(self):
        input_str = "<div>Hello</div>"
        result = sanitize_input(input_str)

        assert result == "&lt;div&gt;Hello&lt;/div&gt;"

    def test_safe_text_unchanged_except_escaping(self):
        input_str = "Just normal text"
        result = sanitize_input(input_str)

        assert result == input_str
