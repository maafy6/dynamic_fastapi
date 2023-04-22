"""Window extensions."""
from abc import ABC, abstractmethod

from pydantic import constr
from pydantic.fields import FieldInfo


class Extension(ABC):
    """Window parameter extension marker.

    Task types can be declared with extensions that can add new fields and
    modify existing fields according to the parameters supplied to the
    extension.
    """

    __ext_name__: str
    """The name of the extension.
    
    Sub-classes must provide a value for this which will be used to identify
    the extension in configuration items.
    """

    __registry__: dict[str, type["Extension"]] = {}
    """Mapping of extension names to classes."""

    @classmethod
    def register(cls, ext_class: type["Extension"]) -> type["Extension"]:
        """Register an Extension class.

        :param ext_class: The class the register.

        :returns: The registered class.
        """
        cls.__registry__[ext_class.__ext_name__] = ext_class
        return ext_class

    @classmethod
    def extension(cls, ext_name, **kwargs) -> "Extension":
        """Return an extension instance.

        :param ext_name: The name of the extension.
        :param kwargs: Keyword arguments passed to the extension constructor.

        :returns: An instance of the extension.
        """
        return cls.__registry__[ext_name](**kwargs)

    @abstractmethod
    def field_definitions(self) -> dict[str, (type, FieldInfo)]:
        ...


extension = Extension.register


@extension
class KeyNonceExtension(Extension):
    """Add a key/nonce pair to the window parameters.

    Task types with the keynonce extension require two additional tasking
    parameters: `key` and `nonce`. Both are supplied as strings of hexadecimal
    digits, with a configurable length.
    """

    __ext_name__ = "keynonce"

    def __init__(self, key_len: int | None = None, nonce_len: int | None = None):
        """Create a KeyNonceExtenion.

        :param key_len: The required length of the key. If less than 1, any
            length is acceptable.
        :param nonce_len: The required length of the nonce. If less than 1,
            any length is acceptable.
        """
        if key_len is None:
            key_len = 16
        if nonce_len is None:
            nonce_len = 16

        self.key_len = key_len
        self.nonce_len = nonce_len

    def field_definitions(self) -> dict[str, (type, FieldInfo)]:
        """The field definitions.

        :returns: A dict with definitions for the "key" and "nonce" fields.
        """
        return {
            "key": (constr(regex=self.hex16_re(self.key_len)), FieldInfo(...)),
            "nonce": (constr(regex=self.hex16_re(self.nonce_len)), FieldInfo(...)),
        }

    def hex16_re(self, val: int) -> str:
        """Create a regex representing a length of {val} hex characters.

        :param val: The length of the regex.

        :returns: A regex matching {len} hex characters.
        """
        hex16 = "^[0-9a-fA-F]{len}$"
        if val > 0:
            key_regex = hex16.format(len=f"{{{val}}}")
        else:
            key_regex = hex16.format(len="*")

        return key_regex


@extension
class SymbolSetExtension(Extension):
    """Add a symbol_set field to the window parameters.

    Task types with the symbol_set extension require a symbol_set
    field, which is provided as an int.
    """

    __ext_name__ = "symbol_set"

    def field_definitions(self) -> dict[str, (type, FieldInfo)]:
        """The field defintions.

        :returns: A dict with the definitions for the "pncode" field.
        """
        return {"symbol_set": (int, FieldInfo(...))}
