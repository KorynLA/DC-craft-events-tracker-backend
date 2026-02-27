import pytest
from validators import (
    is_valid_date,
    is_valid_time,
    is_valid_url,
    is_valid_int,
    is_valid_bool,
    is_valid_str,
    is_valid_email,
    validate_user_input,
    validate_required_user_input_exists
)

class TestValidateDate:
    
    def test_valid_dates(self):
        valid_dates = [
            '2026-05-12',
            '2100-01-01',
            '2026-12-31',
            '2028-02-29'
        ]
        for date in valid_dates:
            assert is_valid_date(date), f"Expected {date} to be valid"


    def test_invalid_years(self):
        invalid_dates = [
            '2000-05-12',
            '2023-12-31',
            '1999-06-15',
            '2025-09-30'
        ]
        for date in invalid_dates:
            assert not is_valid_date(date), f"Expected {date} to be invalid"


    def test_invalid_month(self):
        invalid_dates = [
            '2026-00-12',
            '2026-13-12'
        ]
        for date in invalid_dates:
            assert not is_valid_date(date), f"Expected {date} to be invalid"


    def test_invalid_day(self):
        invalid_dates = [
            '2026-05-00',
            '2026-05-32',
            '2027-02-30',
            '2027-02-29',
            '2027-04-31',
            '2027-11-31'
        ]
        for date in invalid_dates:
            assert not is_valid_date(date), f"Expected {date} to be invalid"
    
    def test_leap_year_validation(self):
        assert not is_valid_date('02-29-2026')
    
    def test_invalid_format(self):
        """Test dates with invalid format."""
        invalid_formats = [
            '5-12-2026',
            '2026/05/12',
            '2026-5-12',
            '26-05-12',
            '202-05-12',
            '20260512',
            '05-12',
            'invalid',
            ''
        ]
        for date in invalid_formats:
            assert not is_valid_date(date), f"Expected {date} to be invalid format"
    
    def test_edge_cases(self):
        assert is_valid_date('2026-01-01')
        assert is_valid_date('2900-01-01')
        assert is_valid_date('2026-01-31')
        assert is_valid_date('2026-03-31')
        assert is_valid_date('2026-04-30')
        assert not is_valid_date('2026-04-31')


class TestValidateTime:
    """Test cases for the validate_time function."""
    def test_valid_times(self):
        valid_times = [
            '00:00',
            '00:00:00',
            '09:00',
            '09:00:00',
            '12:30',
            '12:30:00',
            '16:30',
            '16:30:00',
            '23:59',
            '23:59:59'
        ]
        for time in valid_times:
            assert is_valid_time(time), f"Expected {time} to be valid"

    def test_invalid_hour(self):
        """Test times with invalid hours."""
        invalid_times = [
            '24:00',
            '24:00:00',
            '25:30',
            '-1:00',
            '99:00'
        ]
        for time in invalid_times:
            assert not is_valid_time(time), f"Expected {time} to be invalid"

    def test_invalid_minute(self):
        """Test times with invalid minutes."""
        invalid_times = [
            '10:60',
            '10:99',
            '10:-1',
            '10:5'
        ]
        for time in invalid_times:
            assert not is_valid_time(time), f"Expected {time} to be invalid"

    def test_invalid_second(self):
        """Test times with invalid seconds."""
        invalid_times = [
            '10:30:60',
            '10:30:99',
            '10:30:-1',
            '10:30:5'
        ]
        for time in invalid_times:
            assert not is_valid_time(time), f"Expected {time} to be invalid"

    def test_invalid_format(self):
        """Test times with invalid formats."""
        invalid_formats = [
            '9:00',        # hour must be two digits
            '9:00:00',
            '09:0',
            '09:00 AM',    # AM/PM not allowed
            '09-00',
            '09.00',
            '0900',
            'invalid',
            ''
        ]
        for time in invalid_formats:
            assert not is_valid_time(time), f"Expected {time} to be invalid"

    def test_all_24_hours(self):
        """Test that all 24 hours of the day are valid."""
        for hour in range(0, 24):
            hh = f"{hour:02d}"
            assert is_valid_time(f"{hh}:00")
            assert is_valid_time(f"{hh}:30")
            assert is_valid_time(f"{hh}:00:00")
            assert is_valid_time(f"{hh}:30:00")


class TestValidateURL:
    """Test cases for the validate_url function."""
    
    def test_valid_urls(self):
        """Test various valid URL formats."""
        valid_urls = [
            'http://example.com',
            'https://example.com',
            'https://www.example.com',
            'https://subdomain.example.com',
            'https://example.co.uk',
            'https://example.com/path',
            'https://example.com/path/to/page',
            'https://example.com/path?query=value',
            'https://example.com/path?query=value&another=param',
            'https://example.com:8080',
            'https://example.com:8080/path',
            'https://example.com/path#fragment',
            'https://example.com/path?query=value#fragment',
            'ftp://files.example.com',
            'https://my-site.example.com',
            'https://example123.com'
        ]
        for url in valid_urls:
            assert is_valid_url(url), f"Expected {url} to be valid"
    
    def test_invalid_protocol(self):
        """Test URLs with invalid or missing protocols."""
        invalid_urls = [
            'example.com',              # No protocol
            'www.example.com',          # No protocol
            'htp://example.com',        # Typo in protocol
            'file://example.com',       # Unsupported protocol
            '://example.com'
        ]
        for url in invalid_urls:
            assert not is_valid_url(url), f"Expected {url} to be invalid"
    
    def test_invalid_domain(self):
        """Test URLs with invalid domains."""
        invalid_urls = [
            'https://',                 # Missing domain
            'https://.',                # Just a dot
            'https://.com',             # Missing domain name
            'https://example',          # Missing TLD
            'https://example.',         # Incomplete TLD
            'https://-example.com',     # Domain starts with hyphen
            'https://example-.com'
        ]
        for url in invalid_urls:
            assert not is_valid_url(url), f"Expected {url} to be invalid"
    
    def test_valid_ports(self):
        """Test URLs with various port numbers."""
        valid_urls = [
            'https://example.com:80',
            'https://example.com:443',
            'https://example.com:8080',
            'https://example.com:3000',
            'https://example.com:65535'
        ]
        for url in valid_urls:
            assert is_valid_url(url), f"Expected {url} to be valid"
    
    def test_complex_paths_and_queries(self):
        """Test URLs with complex paths and query parameters."""
        valid_urls = [
            'https://example.com/api/v1/users',
            'https://example.com/search?q=test&page=1',
            'https://example.com/path/to/resource.html',
            'https://example.com/file.pdf',
            'https://example.com/path_with_underscore',
            'https://example.com/path-with-hyphen',
            'https://example.com/(parentheses)',
            "https://example.com/path'with'quotes"
        ]
        for url in valid_urls:
            assert is_valid_url(url), f"Expected {url} to be valid"
    
    def test_edge_cases(self):
        """Test edge cases for URL validation."""
        # Valid edge cases
        assert is_valid_url('https://a.b.c.d.example.com'), "Multiple subdomains"
        assert is_valid_url('https://example.museum'), "Long TLD"
        
        # Invalid edge cases
        assert not is_valid_url(''), "Empty string"
        assert not is_valid_url('not a url'), "Random text"
        assert not is_valid_url('https://'), "Incomplete URL"

class TestValidateBoolean:
    """Test cases for the validate_url function."""
    
    def test_valid_boleans(self):
        """Test various valid URL formats."""
        valid_booleans = [
            0,
            1,
            True,
            False
        ]
        for boolean in valid_booleans:
            assert is_valid_bool(boolean), f"Expected {boolean} to be valid"
    
    def test_invalid_booleans(self):
        invalid_booleans = [
            "true",
            "false",
            "hi",
            ".;/true",
            "    True"
        ]
        for boolean in invalid_booleans:
            assert not is_valid_bool(boolean), f"Expected {boolean} to be invalid"

class TestValidateBoolean:
    """Test cases for the validate_url function."""
    
    def test_valid_int(self):
        """Test various valid URL formats."""
        valid_ints = [
            0,
            1,
            "1",
            "200",
            1.0,
            "1.0"
        ]
        for int_val in valid_ints:
            assert is_valid_int(int_val), f"Expected {int_val} to be valid"
    
    def test_invalid_int(self):
        invalid_ints = [
            "a",
            "./",
            "a9",
            " ",
            "",
            "z<10",
            -1
        ]
        for int_val in invalid_ints:
            assert not is_valid_int(int_val), f"Expected {int_val} to be invalid"

class TestValidateEmail:
    """Test cases for email validation function."""
    
    def test_valid_email(self):
        """Test various valid email formats."""
        valid_emails = [
            "user@example.com",
            "john.doe@example.com",
            "jane_doe@example.co.uk",
            "user+tag@example.com",
            "user123@test-domain.com",
            "first.last@subdomain.example.com",
            "a@example.com",
            "test@example.io",
            "user@localhost.localdomain",
            "user_name@example-domain.com",
            "UPPERCASE@EXAMPLE.COM",
            "MixedCase@Example.Com",
            "user@example.museum",
            "user@example.travel",
            "1234567890@example.com",
            "user@example-hyphen.com",
            "user.name+tag@example.com",
            "x@example.com",
            "user@sub.domain.example.com"
        ]
        for email in valid_emails:
            assert is_valid_email(email), f"Expected '{email}' to be valid"
    
    def test_invalid_email(self):
        """Test various invalid email formats."""
        invalid_emails = [
            "",  # Empty string
            " ",  # Whitespace only
            "plaintext",  # No @ symbol
            "@example.com",  # Missing local part
            "user@",  # Missing domain
            "user @example.com",  # Space in local part
            "user@exam ple.com",  # Space in domain
            "user..name@example.com",  # Consecutive dots
            ".user@example.com",  # Leading dot
            "user.@example.com",  # Trailing dot in local part
            "user@.example.com",  # Leading dot in domain
            "user@example..com",  # Consecutive dots in domain
            "user@example.com.",  # Trailing dot in domain
            "user@@example.com",  # Double @
            "user@example@com",  # Multiple @ symbols
            "user name@example.com",  # Space in local part
            "user@",  # No domain after @
            "@",  # Just @ symbol
            "user@example",  # Missing TLD
            "user@.com",  # Missing domain name
            "user#example.com",  # # instead of @
            "user@exam!ple.com",  # Invalid character in domain
            "user@-example.com",  # Domain starts with hyphen
            "user@example-.com",  # Domain ends with hyphen
            "user@example.c",  # TLD too short (single character)
            None,  # None value
            123,  # Integer
            "user@",  # Incomplete
            "user@example.",  # Incomplete domain
            "a@b@c@example.com",  # Multiple @ symbols
            "user()@example.com",  # Invalid characters in local part
            "user@exam ple.com",  # Space in domain
            "user\n@example.com",  # Newline character
            "user@example..com",  # Double dot in domain
            "<user@example.com>",  # Angle brackets
            "user@example,com",  # Comma instead of dot
            "user;@example.com",  # Semicolon in local part
            "user@[example.com",  # Unclosed bracket
            "user@example].com",  # Unmatched bracket
            "user@",  # Missing everything after @
            "user",  # No @ or domain
            "user@domain@example.com",  # Multiple @ symbols
            "user..email@example.com",  # Consecutive dots in local
            "user@-domain.com"  # Hyphen at start of domain
        ]
        for email in invalid_emails:
            assert not is_valid_email(email), f"Expected '{email}' to be invalid"
    
    def test_edge_cases(self):
        """Test edge cases for email validation."""
        edge_cases = [
            ("a@b.co", True),  # Minimum valid email
            ("user+filter@example.com", True),  # Plus sign (common for filters)
            ("user@subdomain.example.com", True),  # Subdomain
            ("user@example.co.uk", True),  # Multi-part TLD
            ("user_name@example.com", True),  # Underscore in local
            ("user-name@example.com", True),  # Hyphen in local
            ("user.name@example.com", True),  # Dot in local
            ("123@example.com", True),  # Numbers only in local
            ("user@123.com", True),  # Numbers in domain
            ("user@example.com.", False),  # Trailing dot
            (".user@example.com", False),  # Leading dot
            ("user.@example.com", False),  # Trailing dot in local
            ("user..name@example.com", False),  # Consecutive dots
            ("user@example", False),  # No TLD
            ("@example.com", False),  # No local part
            ("user@", False),  # No domain
            ("", False),  # Empty string
            ("  ", False)  # Whitespace
        ]
        for email, expected in edge_cases:
            result = is_valid_email(email)
            assert result == expected, f"Expected '{email}' to be {'valid' if expected else 'invalid'}, got {'valid' if result else 'invalid'}"
    
    def test_whitespace_handling(self):
        """Test handling of whitespace in emails."""
        whitespace_cases = [
            " user@example.com",
            "user@example.com ",
            " user@example.com ",
            "user @example.com",
            "user@ example.com",
            "user@exam ple.com",
            "\tuser@example.com"
        ]
        for email in whitespace_cases:
            assert not is_valid_email(email), f"Expected '{repr(email)}' to be invalid"
    
    def test_special_characters(self):
        """Test special characters in email addresses."""
        # Valid special characters
        valid_special = [
            "user+tag@example.com",
            "user_name@example.com",
            "user-name@example.com",
            "user.name@example.com",
            "first.last+tag@example.com"
        ]
        for email in valid_special:
            assert is_valid_email(email), f"Expected '{email}' to be valid"
        
        # Invalid special characters
        invalid_special = [
            "user!name@example.com",
            "user#name@example.com",
            "user$name@example.com",
            "user%name@example.com",
            "user&name@example.com",
            "user*name@example.com",
            "user=name@example.com",
            "user?name@example.com",
            "user^name@example.com",
            "user`name@example.com",
            "user{name@example.com",
            "user}name@example.com",
            "user|name@example.com",
            "user~name@example.com"
        ]
        for email in invalid_special:
            assert not is_valid_email(email), f"Expected '{email}' to be invalid"
    
    def test_case_sensitivity(self):
        """Test that email validation is case-insensitive (as per RFC)."""
        emails = [
            "User@Example.Com",
            "USER@EXAMPLE.COM",
            "user@example.com",
            "UsEr@ExAmPlE.cOm"
        ]
        for email in emails:
            assert is_valid_email(email), f"Expected '{email}' to be valid (case-insensitive)"
class TestValidateRequiredUserInputExists:
    """Test suite for validate_required_user_input_exists function"""
    
    def test_all_required_fields_present_returns_true(self):
        user_input = {
            "name": "Community Yoga",
            "time": "09:00",
            "date": "2026-06-20",
            "location": "Riverside Park",
            "organization": "Community",
            "link": "https://example.com",
            "email": "test@example.com"
        }
        assert validate_required_user_input_exists(user_input) == True
    
    def test_missing_name_returns_false(self):
        user_input = {
            "time": "09:00",
            "date": "2026-06-20",
            "location": "Riverside Park",
            "link": "https://example.com",
            "email": "test@example.com"
        }
        assert validate_required_user_input_exists(user_input) == False
    
    def test_empty_name_returns_false(self):
        user_input = {
            "name": "",
            "time": "09:00",
            "date": "2026-06-20",
            "location": "Riverside Park",
            "link": "https://example.com",
            "email": "test@example.com"
        }
        assert validate_required_user_input_exists(user_input) == False
    
    def test_none_name_returns_false(self):
        user_input = {
            "name": None,
            "time": "09:00",
            "date": "2026-06-20",
            "location": "Riverside Park",
            "link": "https://example.com",
            "email": "test@example.com"
        }
        assert validate_required_user_input_exists(user_input) == False
    
    def test_missing_time_returns_false(self):
        user_input = {
            "name": "Community Yoga",
            "date": "2026-06-20",
            "location": "Riverside Park",
            "link": "https://example.com",
            "email": "test@example.com"
        }
        assert validate_required_user_input_exists(user_input) == False
    
    def test_missing_date_returns_false(self):
        user_input = {
            "name": "Community Yoga",
            "time": "09:00",
            "location": "Riverside Park",
            "link": "https://example.com",
            "email": "test@example.com"
        }
        assert validate_required_user_input_exists(user_input) == False
    
    def test_missing_location_returns_false(self):
        user_input = {
            "name": "Community Yoga",
            "time": "09:00",
            "date": "2026-06-20",
            "link": "https://example.com",
            "email": "test@example.com"
        }
        assert validate_required_user_input_exists(user_input) == False
    
    def test_missing_link_returns_false(self):
        user_input = {
            "name": "Community Yoga",
            "time": "09:00",
            "date": "2026-06-20",
            "location": "Riverside Park",
            "email": "test@example.com"
        }
        assert validate_required_user_input_exists(user_input) == False
    
    def test_missing_email_returns_false(self):
        user_input = {
            "name": "Community Yoga",
            "time": "09:00",
            "date": "2026-06-20",
            "location": "Riverside Park",
            "link": "https://example.com"
        }
        assert validate_required_user_input_exists(user_input) == False
    
    def test_empty_dict_returns_false(self):
        assert validate_required_user_input_exists({}) == False
    
    def test_extra_fields_dont_affect_validation(self):
        user_input = {
            "name": "Community Yoga",
            "time": "09:00",
            "date": "2026-06-20",
            "location": "Riverside Park",
            "link": "https://example.com",
            "email": "test@example.com",
            "description": "Extra field",
            "price": "10.00",
            "organization": "Extra org"
        }
        assert validate_required_user_input_exists(user_input) == True
    
    def test_all_fields_empty_strings_returns_false(self):
        user_input = {
            "name": "",
            "time": "",
            "date": "",
            "location": "",
            "link": "",
            "email": ""
        }
        assert validate_required_user_input_exists(user_input) == False
    
    def test_all_fields_none_returns_false(self):
        user_input = {
            "name": None,
            "time": None,
            "date": None,
            "location": None,
            "link": None,
            "email": None
        }
        assert validate_required_user_input_exists(user_input) == False


class TestValidateUserInput:
    
    @pytest.fixture
    def valid_user_input(self):
        return {
            "name": "Community Yoga",
            "time": "09:00:00",
            "date": "2026-06-20",
            "location": "Riverside Park",
            "link": "https://example.com",
            "email": "test@example.com",
            "price": "10",
            "kids": True,
            "description": "A relaxing yoga session",
            "organization": "Yoga Inc"
        }

    def test_name_exactly_140_characters_returns_true(self, valid_user_input):
        name_500 = "x" * 500
        valid_user_input["name"] = name_500
        assert validate_user_input(valid_user_input, name=name_500,
                                   description="Test", organization="Test", location="Test") == True
    
    def test_name_501_characters_returns_false(self, valid_user_input):
        name_501 = "x" * 501
        assert validate_user_input(valid_user_input, name=name_501,
                                   description="Test", organization="Test", location="Test") == False
    
    def test_name_empty_string_passes(self, valid_user_input):
        assert validate_user_input(valid_user_input, name="",
                                   description="Test", organization="Test", location="Test") == True
    
    def test_name_none_passes(self, valid_user_input):
        assert validate_user_input(valid_user_input, name=None,
                                   description="Test", organization="Test", location="Test") == True


class TestParametrizedValidation:
    
    @pytest.mark.parametrize("field_name,field_value", [
        ("name", ""), ("name", None), ("time", ""), ("time", None),
        ("date", ""), ("date", None), ("location", ""), ("location", None),
        ("link", ""), ("link", None), ("email", ""), ("email", None)
    ])
    def test_required_field_empty_or_none_returns_false(self, field_name, field_value):
        user_input = {
            "name": "Community Yoga",
            "time": "09:00",
            "date": "2026-06-20",
            "location": "Riverside Park",
            "link": "https://example.com",
            "email": "test@example.com"
        }
        user_input[field_name] = field_value
        assert validate_required_user_input_exists(user_input) == False
