import re
from typing import Optional
from urllib.parse import urlparse
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

NAME_SIZE=500
DESCRIPTION_SIZE=500
ORGRANIZATION_SIZE=250
LOCATION_SIZE=250

def is_valid_date(date_string: str) -> bool:
    # YYYY-MM-DD (any 4-digit year)
    pattern = r'^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$'

    if not re.match(pattern, date_string):
        return False

    year, month, day = map(int, date_string.split('-'))

    if year <= 2025:
        return False

    # Leap year check
    is_leap = (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

    days_in_month = [
        31,
        29 if is_leap else 28,
        31, 30, 31, 30,
        31, 31, 30, 31, 30, 31
    ]

    return day <= days_in_month[month - 1]


def is_valid_time(time_string: str) -> bool:
    # Strict 24-hour format:
    # HH:MM or HH:MM:SS
    pattern = r'^([01][0-9]|2[0-3]):[0-5][0-9](:[0-5][0-9])?$'
    return bool(re.match(pattern, time_string))

def is_valid_bool(user_input):
    return type(user_input) == bool

def is_valid_int(user_input):
    if isinstance(user_input, bool):
        return False
    if isinstance(user_input, int):
        return user_input >= 0
    if isinstance(user_input, float):
        return user_input >= 0
    if isinstance(user_input, str):
        if user_input.isdigit() and user_input.isdigit() >= 0:
            return True
        else:
            try:
                user_input = user_input.strip()
                val = float(user_input)
                return val.is_integer() and val >= 0
            except ValueError:
                return False
    return False

def is_valid_url(user_input):
    if not isinstance(user_input, str):
        return False
    try:
        result = urlparse(user_input)
    except Exception:
        return False

    if result.scheme.lower() not in ["http", "https", "ftp"]:
        return False

    netloc = result.netloc
    if not netloc or netloc.strip(".") == "":
        return False
    host, port = netloc.split(":") if ":" in netloc else (netloc, None)
    if port:
        if not port.isdigit() or not (0 < int(port) <= 65535):
            return False

    domain_parts = host.split(".")
    if len(domain_parts) < 2:
        return False

    for part in domain_parts:
        if not part or part.startswith("-") or part.endswith("-"):
            return False
        if not re.match(r"^[A-Za-z0-9-]+$", part):
            return False
    return True

def is_valid_str(user_input, max_chars):
    if len(user_input.strip()) < 1:
        return False
    if len(user_input) > max_chars:
        return False
    return True

def is_valid_email(email):
    if not email or not isinstance(email, str):
        return False
    
    # Basic email regex pattern
    # Local part: alphanumeric, dots, hyphens, underscores, plus signs
    # Domain part: alphanumeric, dots, hyphens (no underscores per RFC)
    pattern = r'^[a-zA-Z0-9][a-zA-Z0-9._+-]*[a-zA-Z0-9]@[a-zA-Z0-9][a-zA-Z0-9.-]*\.[a-zA-Z]{2,}$|^[a-zA-Z0-9]@[a-zA-Z0-9][a-zA-Z0-9.-]*\.[a-zA-Z]{2,}$'
    
    # Check basic pattern match
    if not re.match(pattern, email):
        return False
    
    # Additional validation rules
    if '..' in email:  # No consecutive dots
        return False
    
    if email.startswith('.') or email.endswith('.'):  # No leading/trailing dots
        return False
    
    if '@.' in email or '.@' in email:  # No dots immediately adjacent to @
        return False
    
    if email.count('@') != 1:  # Exactly one @ symbol
        return False
    
    local, domain = email.split('@')
    
    # Local part shouldn't start or end with dot
    if local.startswith('.') or local.endswith('.'):
        return False
    
    # Domain shouldn't start or end with hyphen or dot
    if domain.startswith('-') or domain.startswith('.'):
        return False
    
    if domain.endswith('-') or domain.endswith('.'):
        return False
    
    # Check for hyphen immediately before TLD (e.g., example-.com)
    if '.-' in domain or '-.' in domain:
        return False
    
    # Domain names shouldn't contain underscores (per RFC standards)
    if '_' in domain:
        return False
    return True

def validate_required_user_input_exists(user_input):
    if not user_input.get("name"):
        logger.info("No name in JSON")
        return False
    if not user_input.get("time"):
        logger.info("No time in JSON")
        return False
    if not user_input.get("date"):
        logger.info("No date in JSON")
        return False
    if not user_input.get("location"):
        logger.info("No location in JSON")
        return False
    if not user_input.get("link"):
        logger.info("No link in JSON")
        return False
    if not user_input.get("email"):
        logger.info("No email in JSON")
        return False
    if not user_input.get("organization"):
        logger.info("No organization in JSON")
        return False
    return True

def validate_user_input(user_input, name, description, organization, location):
    if user_input.get("time") and not is_valid_time(user_input.get("time")):
        logger.info("Invalid time")
        return False
    if user_input.get("date") and not is_valid_date(user_input.get("date")):
        logger.info("Invalid date")
        return False
    if user_input.get("price") and not is_valid_int(user_input.get("price")):
        logger.info("Invalid price")
        return False
    if user_input.get("link") and not is_valid_url(user_input.get("link")):
        logger.info("Invalid link")
        return False
    if user_input.get("kids") and not is_valid_bool(user_input.get("kids")):
        logger.info("Invalid kids")
        return False
    if user_input.get("email") and not is_valid_email(user_input.get("email")):
        logger.info("Invalid email")
        return False
    if name and not is_valid_str(name, NAME_SIZE):
        logger.info("Invalid name length")
        return False
    if description and not is_valid_str(description, DESCRIPTION_SIZE):
        logger.info("Invalid description length")
        return False
    if organization and not is_valid_str(organization, ORGRANIZATION_SIZE):
        logger.info("Invalid organization length")
        return False
    if location and not is_valid_str(location, LOCATION_SIZE):
        logger.info("Invalid location length")
        return False
    return True