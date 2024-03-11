import pytest

from src.app import name_format, add_sudo_user, drop_sudo

# Probar nombres
@pytest.mark.parametrize(
    "name, expected",
    [
        ("", ""),                                         # Cadena vacía
        ("John-Doe", "john-doe"),                         # Nombre normal con guion
        ("J0hnD03", "jhnd"),                              # Nombre con números
        ("Léopoldo Álvarez", "lopoldo-lvarez"),           # Nombre con caracteres especiales y acentos
        ("Mr. T", "mr-t"),                                # Nombre con punto
        ("The Quick Brown Fox", "the-quick-brown-fox"),   # Nombre con mayúsculas
        ("Çağatay Ünlüoğlu", "aatay-nlolu"),              # Nombre con caracteres Unicode
        ("Isaac Newton", "isaac-newton"),                 # Nombre con espacio
        ("Captain Jack Sparrow", "captain-jack-sparrow"), # Nombre con título y espacio
    ]
)

def test_name_format(name, expected):
    assert name_format(name) == expected
