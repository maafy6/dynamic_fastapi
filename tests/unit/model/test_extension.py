"""Tests for dynamic_fastapi.model.extension."""
import pytest
from pydantic import ConstrainedStr, StrRegexError
from pydantic.fields import FieldInfo

from dynamic_fastapi.model.extension import (
    Extension, KeyNonceExtension, SymbolSetExtension
)


class TestExtension:
    """Tests for dynamic_fastapi.model.extension.Extension."""

    def test_registered(self) -> None:
        """Validate that the expected extensions are registered."""
        assert Extension.__registry__.keys() == {"keynonce", "symbol_set"}

    def test_extension(self) -> None:
        """Test the creation of an extension."""
        kne = Extension.extension("keynonce", key_len=12)

        assert isinstance(kne, KeyNonceExtension)
        assert kne.key_len == 12
        assert kne.nonce_len == 16


class TestKeyNonceExtension:
    """Tests for dynamic_fastapi.model.extension.KeyNonceExtension."""

    @pytest.mark.parametrize(("key_len", "nonce_len"), [(None, None), (12, 8)])
    def test_field_definitions(self, key_len: int, nonce_len: int) -> None:
        """Validate that this produces the expected field definitions."""
        ext = KeyNonceExtension(key_len=key_len, nonce_len=nonce_len)
        field_defs = ext.field_definitions()

        assert set(field_defs.keys()) == {"key", "nonce"}

        key_def, nonce_def = field_defs["key"], field_defs["nonce"]
        self._validate_hex16(*key_def, key_len)
        self._validate_hex16(*nonce_def, nonce_len)

    def _validate_hex16(
        self, field_type: type, field_info: FieldInfo, length: int | None
    ) -> None:
        """Validate a field accepts no more than length characters.

        :param field_type: The field type.
        :param field_info: The field info.
        :param length: The max length of the field.
        """
        if length is None:
            length = 16

        assert issubclass(field_type, ConstrainedStr)
        assert field_type.validate("0" * length)
        with pytest.raises(StrRegexError):
            field_type.validate("0" * (length + 1))
        assert field_info.default == ...


class TestSymbolSetCodeExtension:
    """Tests for dynamic_fastapi.model.extension.SymbolSetExtension."""

    def test_field_definitions(self) -> None:
        """Validate that this produces the expected field definitions."""
        ext = SymbolSetExtension()
        field_defs = ext.field_definitions()

        assert set(field_defs.keys()) == {"symbol_set"}

        assert field_defs["symbol_set"][0] == int
