import pytest

from src.app import name_format, add_sudo_user, drop_sudo

# Test name formatting
@pytest.mark.parametrize(
    "name, expected",
    [
        ("", ""),                                         # Empty string
        ("John-Doe", "john-doe"),                         # Normal name with hyphen
        ("J0hnD03", "jhnd"),                              # Name with numbers
        ("Léopoldo Álvarez", "lopoldo-lvarez"),           # Name with special characters and accents
        ("Mr. T", "mr-t"),                                # Name with period
        ("The Quick Brown Fox", "the-quick-brown-fox"),   # Name with uppercase
        ("Çağatay Ünlüoğlu", "aatay-nlolu"),              # Name with Unicode characters
        ("Isaac Newton", "isaac-newton"),                 # Name with space
        ("Captain Jack Sparrow", "captain-jack-sparrow"), # Title case name with space
    ]
)

def test_name_format(name, expected):
    assert name_format(name) == expected
