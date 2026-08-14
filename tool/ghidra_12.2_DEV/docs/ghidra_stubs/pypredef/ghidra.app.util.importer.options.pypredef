from __future__ import annotations
import collections.abc
import datetime
import typing
from warnings import deprecated # type: ignore

import jpype # type: ignore
import jpype.protocol # type: ignore

import ghidra.app.util
import ghidra.program.model.address
import java.lang # type: ignore


T = typing.TypeVar("T")


class AbstractOption(ghidra.app.util.Option, typing.Generic[T]):
    """
    An :obj:`Option` that is specific to a value type
    """

    class_: typing.ClassVar[java.lang.Class]


class AddressOption(AbstractOption[ghidra.program.model.address.Address]):
    """
    An :obj:`Option` used to specify an :obj:`Address`
    """

    class Builder(ghidra.app.util.AbstractOptionBuilder[ghidra.program.model.address.Address, AddressOption]):
        """
        Builds a :obj:`AddressOption`
        """

        class_: typing.ClassVar[java.lang.Class]

        def __init__(self, name: typing.Union[java.lang.String, str]) -> None:
            """
            Creates a new :obj:`Builder`
            
            :param java.lang.String or str name: The name of the :obj:`AddressOption` to be built
            """


    class_: typing.ClassVar[java.lang.Class]

    def __init__(self, name: typing.Union[java.lang.String, str], value: ghidra.program.model.address.Address, arg: typing.Union[java.lang.String, str], group: typing.Union[java.lang.String, str], stateKey: typing.Union[java.lang.String, str], hidden: typing.Union[jpype.JBoolean, bool], description: typing.Union[java.lang.String, str]) -> None:
        """
        Creates a new :obj:`AddressOption`
        
        :param java.lang.String or str name: the name of the option
        :param ghidra.program.model.address.Address value: the value of the option
        :param java.lang.String or str arg: the option's command line argument
        :param java.lang.String or str group: the name for group of options
        :param java.lang.String or str stateKey: the state key name
        :param jpype.JBoolean or bool hidden: true if this option should be hidden from the user; otherwise, false
        :param java.lang.String or str description: a description of the option
        """


class AddressSpaceOption(AbstractOption[ghidra.program.model.address.AddressSpace]):
    """
    An :obj:`Option` used to specify an :obj:`AddressSpace`
    """

    class Builder(ghidra.app.util.AbstractOptionBuilder[ghidra.program.model.address.AddressSpace, AddressSpaceOption]):
        """
        Builds an :obj:`AddressSpaceOption`
        """

        class_: typing.ClassVar[java.lang.Class]

        def __init__(self, name: typing.Union[java.lang.String, str]) -> None:
            """
            Creates a new :obj:`Builder`
            
            :param java.lang.String or str name: The name of the :obj:`AddressSpaceOption` to be built
            """


    class_: typing.ClassVar[java.lang.Class]

    def __init__(self, name: typing.Union[java.lang.String, str], value: ghidra.program.model.address.AddressSpace, arg: typing.Union[java.lang.String, str], group: typing.Union[java.lang.String, str], stateKey: typing.Union[java.lang.String, str], hidden: typing.Union[jpype.JBoolean, bool], description: typing.Union[java.lang.String, str]) -> None:
        """
        Creates a new :obj:`AddressSpaceOption`
        
        :param java.lang.String or str name: the name of the option
        :param ghidra.program.model.address.AddressSpace value: the value of the option
        :param java.lang.String or str arg: the option's command line argument
        :param java.lang.String or str group: the name for group of options
        :param java.lang.String or str stateKey: the state key name
        :param jpype.JBoolean or bool hidden: true if this option should be hidden from the user; otherwise, false
        :param java.lang.String or str description: a description of the option
        """


class BooleanOption(AbstractOption[java.lang.Boolean]):
    """
    An :obj:`Option` used to specify a :obj:`Boolean`
    """

    class Builder(ghidra.app.util.AbstractOptionBuilder[java.lang.Boolean, BooleanOption]):
        """
        Builds a :obj:`BooleanOption`
        """

        class_: typing.ClassVar[java.lang.Class]

        def __init__(self, name: typing.Union[java.lang.String, str]) -> None:
            """
            Creates a new :obj:`Builder`
            
            :param java.lang.String or str name: The name of the :obj:`BooleanOption` to be built
            """


    class_: typing.ClassVar[java.lang.Class]

    def __init__(self, name: typing.Union[java.lang.String, str], value: typing.Union[jpype.JBoolean, bool], arg: typing.Union[java.lang.String, str], group: typing.Union[java.lang.String, str], stateKey: typing.Union[java.lang.String, str], hidden: typing.Union[jpype.JBoolean, bool], description: typing.Union[java.lang.String, str]) -> None:
        """
        Creates a new :obj:`BooleanOption`
        
        :param java.lang.String or str name: the name of the option
        :param jpype.JBoolean or bool value: the value of the option
        :param java.lang.String or str arg: the option's command line argument
        :param java.lang.String or str group: the name for group of options
        :param java.lang.String or str stateKey: the state key name
        :param jpype.JBoolean or bool hidden: true if this option should be hidden from the user; otherwise, false
        :param java.lang.String or str description: a description of the option
        """


class DomainFileOption(StringOption):
    """
    An :obj:`Option` used to specify a :obj:`DomainFile`
    """

    class Builder(StringOption.Builder):
        """
        Builds a :obj:`DomainFileOption`
        """

        class_: typing.ClassVar[java.lang.Class]

        def __init__(self, name: typing.Union[java.lang.String, str]) -> None:
            """
            Creates a new :obj:`Builder`
            
            :param java.lang.String or str name: The name of the :obj:`DomainFileOption` to be built
            """


    class_: typing.ClassVar[java.lang.Class]

    def __init__(self, name: typing.Union[java.lang.String, str], value: typing.Union[java.lang.String, str], arg: typing.Union[java.lang.String, str], group: typing.Union[java.lang.String, str], stateKey: typing.Union[java.lang.String, str], hidden: typing.Union[jpype.JBoolean, bool], description: typing.Union[java.lang.String, str]) -> None:
        """
        Creates a new :obj:`DomainFileOption`
        
        :param java.lang.String or str name: the name of the option
        :param java.lang.String or str value: the value of the option
        :param java.lang.String or str arg: the option's command line argument
        :param java.lang.String or str group: the name for group of options
        :param java.lang.String or str stateKey: the state key name
        :param jpype.JBoolean or bool hidden: true if this option should be hidden from the user; otherwise, false
        :param java.lang.String or str description: a description of the option
        """


class DomainFolderOption(StringOption):
    """
    An :obj:`Option` used to specify a :obj:`DomainFolder`
    """

    class Builder(StringOption.Builder):
        """
        Builds a :obj:`DomainFolderOption`
        """

        class_: typing.ClassVar[java.lang.Class]

        def __init__(self, name: typing.Union[java.lang.String, str]) -> None:
            """
            Creates a new :obj:`Builder`
            
            :param java.lang.String or str name: The name of the :obj:`DomainFolderOption` to be built
            """


    class_: typing.ClassVar[java.lang.Class]

    def __init__(self, name: typing.Union[java.lang.String, str], value: typing.Union[java.lang.String, str], arg: typing.Union[java.lang.String, str], group: typing.Union[java.lang.String, str], stateKey: typing.Union[java.lang.String, str], hidden: typing.Union[jpype.JBoolean, bool], description: typing.Union[java.lang.String, str]) -> None:
        """
        Creates a new :obj:`DomainFolderOption`
        
        :param java.lang.String or str name: the name of the option
        :param java.lang.String or str value: the value of the option
        :param java.lang.String or str arg: the option's command line argument
        :param java.lang.String or str group: the name for group of options
        :param java.lang.String or str stateKey: the state key name
        :param jpype.JBoolean or bool hidden: true if this option should be hidden from the user; otherwise, false
        :param java.lang.String or str description: a description of the option
        """


class HexLongOption(AbstractOption[ghidra.app.util.HexLong]):
    """
    An :obj:`Option` used to specify a :obj:`HexLong`
    """

    class Builder(ghidra.app.util.AbstractOptionBuilder[ghidra.app.util.HexLong, HexLongOption]):
        """
        Builds a :obj:`HexLongOption`
        """

        class_: typing.ClassVar[java.lang.Class]

        def __init__(self, name: typing.Union[java.lang.String, str]) -> None:
            """
            Creates a new :obj:`Builder`
            
            :param java.lang.String or str name: The name of the :obj:`HexLongOption` to be built
            """


    class_: typing.ClassVar[java.lang.Class]

    def __init__(self, name: typing.Union[java.lang.String, str], value: ghidra.app.util.HexLong, arg: typing.Union[java.lang.String, str], group: typing.Union[java.lang.String, str], stateKey: typing.Union[java.lang.String, str], hidden: typing.Union[jpype.JBoolean, bool], description: typing.Union[java.lang.String, str]) -> None:
        """
        Creates a new :obj:`HexLongOption`
        
        :param java.lang.String or str name: the name of the option
        :param ghidra.app.util.HexLong value: the value of the option
        :param java.lang.String or str arg: the option's command line argument
        :param java.lang.String or str group: the name for group of options
        :param java.lang.String or str stateKey: the state key name
        :param jpype.JBoolean or bool hidden: true if this option should be hidden from the user; otherwise, false
        :param java.lang.String or str description: a description of the option
        """


class IntegerOption(AbstractOption[java.lang.Integer]):
    """
    An :obj:`Option` used to specify an :obj:`Integer`
    """

    class Builder(ghidra.app.util.AbstractOptionBuilder[java.lang.Integer, IntegerOption]):
        """
        Builds a :obj:`IntegerOption`
        """

        class_: typing.ClassVar[java.lang.Class]

        def __init__(self, name: typing.Union[java.lang.String, str]) -> None:
            """
            Creates a new :obj:`Builder`
            
            :param java.lang.String or str name: The name of the :obj:`IntegerOption` to be built
            """


    class_: typing.ClassVar[java.lang.Class]

    def __init__(self, name: typing.Union[java.lang.String, str], value: typing.Union[jpype.JInt, int], arg: typing.Union[java.lang.String, str], group: typing.Union[java.lang.String, str], stateKey: typing.Union[java.lang.String, str], hidden: typing.Union[jpype.JBoolean, bool], description: typing.Union[java.lang.String, str]) -> None:
        """
        Creates a new :obj:`IntegerOption`
        
        :param java.lang.String or str name: the name of the option
        :param jpype.JInt or int value: the value of the option
        :param java.lang.String or str arg: the option's command line argument
        :param java.lang.String or str group: the name for group of options
        :param java.lang.String or str stateKey: the state key name
        :param jpype.JBoolean or bool hidden: true if this option should be hidden from the user; otherwise, false
        :param java.lang.String or str description: a description of the option
        """


class StringOption(AbstractOption[java.lang.String]):
    """
    An :obj:`Option` used to specify a :obj:`String`
    """

    class Builder(ghidra.app.util.AbstractOptionBuilder[java.lang.String, StringOption]):
        """
        Builds a :obj:`StringOption`
        """

        class_: typing.ClassVar[java.lang.Class]

        def __init__(self, name: typing.Union[java.lang.String, str]) -> None:
            """
            Creates a new :obj:`Builder`
            
            :param java.lang.String or str name: The name of the :obj:`StringOption` to be built
            """


    class_: typing.ClassVar[java.lang.Class]

    def __init__(self, name: typing.Union[java.lang.String, str], value: typing.Union[java.lang.String, str], arg: typing.Union[java.lang.String, str], group: typing.Union[java.lang.String, str], stateKey: typing.Union[java.lang.String, str], hidden: typing.Union[jpype.JBoolean, bool], description: typing.Union[java.lang.String, str]) -> None:
        """
        Creates a new :obj:`IntegerOption`
        
        :param java.lang.String or str name: the name of the option
        :param java.lang.String or str value: the value of the option
        :param java.lang.String or str arg: the option's command line argument
        :param java.lang.String or str group: the name for group of options
        :param java.lang.String or str stateKey: the state key name
        :param jpype.JBoolean or bool hidden: true if this option should be hidden from the user; otherwise, false
        :param java.lang.String or str description: a description of the option
        """



__all__ = ["AbstractOption", "AddressOption", "AddressSpaceOption", "BooleanOption", "DomainFileOption", "DomainFolderOption", "HexLongOption", "IntegerOption", "StringOption"]
