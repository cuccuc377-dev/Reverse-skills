from __future__ import annotations
import collections.abc
import datetime
import typing
from warnings import deprecated # type: ignore

import jpype # type: ignore
import jpype.protocol # type: ignore

import ghidra.app.util.bin
import ghidra.app.util.bin.format.pe
import java.lang # type: ignore
import java.util # type: ignore


class ChpeRangeType(java.lang.Enum[ChpeRangeType]):
    """
    CHPE range types
    """

    class_: typing.ClassVar[java.lang.Class]
    ARM64: typing.Final[ChpeRangeType]
    ARM64EC: typing.Final[ChpeRangeType]
    X86_64: typing.Final[ChpeRangeType]
    UNKNOWN: typing.Final[ChpeRangeType]

    def getValue(self) -> int:
        """
        :return: the type's defined value
        :rtype: int
        """

    @staticmethod
    def type(value: typing.Union[jpype.JInt, int]) -> ChpeRangeType:
        """
        Reads a :obj:`ChpeRangeType`
        
        :param jpype.JInt or int value: The defined value of the type
        :return: The type of the given value, or :obj:`.UNKNOWN` if the value does not correspond to 
        a known type
        :rtype: ChpeRangeType
        :raises IOException: if there was an IO-related error
        """

    @staticmethod
    def valueOf(name: typing.Union[java.lang.String, str]) -> ChpeRangeType:
        ...

    @staticmethod
    def values() -> jpype.JArray[ChpeRangeType]:
        ...

    @property
    def value(self) -> jpype.JLong:
        ...


class ImageArm64ecCodeRangeEntryPoint(ghidra.app.util.bin.StructConverter, ghidra.app.util.bin.format.pe.PeMarkupable):
    """
    Represents a ``IMAGE_ARM64EC_CODE_RANGE_ENTRY_POINT`` structure
    """

    class_: typing.ClassVar[java.lang.Class]

    def __init__(self, reader: ghidra.app.util.bin.BinaryReader, rva: typing.Union[jpype.JLong, int]) -> None:
        """
        Creates a new :obj:`ImageArm64ecCodeRangeEntryPoint`
        
        :param ghidra.app.util.bin.BinaryReader reader: A :obj:`BinaryReader` that points to the start of the structure
        :param jpype.JLong or int rva: The relative virtual address of the structure
        :raises IOException: if there was an IO-related error
        """

    def getEndRva(self) -> int:
        """
        :return: the end RVA
        :rtype: int
        """

    def getEntryPoint(self) -> int:
        """
        :return: the entry point RVA
        :rtype: int
        """

    def getStartRva(self) -> int:
        """
        :return: the start RVA
        :rtype: int
        """

    @property
    def endRva(self) -> jpype.JInt:
        ...

    @property
    def startRva(self) -> jpype.JInt:
        ...

    @property
    def entryPoint(self) -> jpype.JInt:
        ...


class ImageArm64ecMetadata(ghidra.app.util.bin.StructConverter, ghidra.app.util.bin.format.pe.PeMarkupable):
    """
    Represents a ``IMAGE_ARM64EC_METADATA`` structure
    """

    class_: typing.ClassVar[java.lang.Class]

    def __init__(self, reader: ghidra.app.util.bin.BinaryReader, nt: ghidra.app.util.bin.format.pe.NTHeader, va: typing.Union[jpype.JLong, int]) -> None:
        """
        Creates a new :obj:`ImageArm64ecMetadata`
        
        :param ghidra.app.util.bin.BinaryReader reader: A :obj:`BinaryReader` that points to the start of the structure
        :param ghidra.app.util.bin.format.pe.NTHeader nt: The :obj:`NTHeader`
        :param jpype.JLong or int va: The virtual address of the structure
        :raises IOException: if there was an IO-related error
        """

    def getCodeMapEntries(self) -> java.util.List[ImageChpeRangeEntry]:
        """
        :return: the :obj:`List` of :obj:`code map entries <ImageChpeRangeEntry>`
        :rtype: java.util.List[ImageChpeRangeEntry]
        """

    def getCodeRangeEntryPoints(self) -> java.util.List[ImageArm64ecCodeRangeEntryPoint]:
        """
        :return: the :obj:`List` of :obj:`code range entry points <ImageArm64ecCodeRangeEntryPoint>`
        :rtype: java.util.List[ImageArm64ecCodeRangeEntryPoint]
        """

    def getRedirectionEntries(self) -> java.util.List[ImageArm64ecRedirectionEntry]:
        """
        :return: the :obj:`List` of :obj:`redirection entries <ImageArm64ecRedirectionEntry>`
        :rtype: java.util.List[ImageArm64ecRedirectionEntry]
        """

    def getVersion(self) -> int:
        """
        :return: the metadata version
        :rtype: int
        """

    @property
    def redirectionEntries(self) -> java.util.List[ImageArm64ecRedirectionEntry]:
        ...

    @property
    def codeMapEntries(self) -> java.util.List[ImageChpeRangeEntry]:
        ...

    @property
    def codeRangeEntryPoints(self) -> java.util.List[ImageArm64ecCodeRangeEntryPoint]:
        ...

    @property
    def version(self) -> jpype.JInt:
        ...


class ImageArm64ecRedirectionEntry(ghidra.app.util.bin.StructConverter, ghidra.app.util.bin.format.pe.PeMarkupable):
    """
    Represents a ``IMAGE_ARM64EC_REDIRECTION_ENTRY`` structure
    """

    class_: typing.ClassVar[java.lang.Class]

    def __init__(self, reader: ghidra.app.util.bin.BinaryReader, rva: typing.Union[jpype.JLong, int]) -> None:
        """
        Creates a new :obj:`ImageArm64ecRedirectionEntry`
        
        :param ghidra.app.util.bin.BinaryReader reader: A :obj:`BinaryReader` that points to the start of the structure
        :param jpype.JLong or int rva: The relative virtual address of the structure
        :raises IOException: if there was an IO-related error
        """

    def getDesintation(self) -> int:
        """
        :return: the destination RVA
        :rtype: int
        """

    def getSource(self) -> int:
        """
        :return: the source RVA
        :rtype: int
        """

    @property
    def source(self) -> jpype.JInt:
        ...

    @property
    def desintation(self) -> jpype.JInt:
        ...


class ImageChpeMetadataX86(ghidra.app.util.bin.StructConverter, ghidra.app.util.bin.format.pe.PeMarkupable):
    """
    Represents a ``IMAGE_CHPE_METADATA_X86`` structure
    """

    class_: typing.ClassVar[java.lang.Class]

    def __init__(self, reader: ghidra.app.util.bin.BinaryReader, nt: ghidra.app.util.bin.format.pe.NTHeader, va: typing.Union[jpype.JLong, int]) -> None:
        """
        Creates a new :obj:`ImageChpeMetadataX86`
        
        :param ghidra.app.util.bin.BinaryReader reader: A :obj:`BinaryReader` that points to the start of the structure
        :param ghidra.app.util.bin.format.pe.NTHeader nt: The :obj:`NTHeader`
        :param jpype.JLong or int va: The virtual address of the structure
        :raises IOException: if there was an IO-related error
        """

    def getCodeMapEntries(self) -> java.util.List[ImageChpeRangeEntry]:
        """
        :return: the :obj:`List` of :obj:`code map entries <ImageChpeRangeEntry>`
        :rtype: java.util.List[ImageChpeRangeEntry]
        """

    def getVersion(self) -> int:
        """
        :return: the metadata version
        :rtype: int
        """

    @property
    def codeMapEntries(self) -> java.util.List[ImageChpeRangeEntry]:
        ...

    @property
    def version(self) -> jpype.JInt:
        ...


class ImageChpeRangeEntry(ghidra.app.util.bin.StructConverter, ghidra.app.util.bin.format.pe.PeMarkupable):
    """
    Represents a ``IMAGE_CHPE_RANGE_ENTRY`` structure
    """

    class_: typing.ClassVar[java.lang.Class]

    def __init__(self, reader: ghidra.app.util.bin.BinaryReader, rva: typing.Union[jpype.JLong, int]) -> None:
        """
        Creates a new :obj:`ImageChpeRangeEntry`
        
        :param ghidra.app.util.bin.BinaryReader reader: A :obj:`BinaryReader` that points to the start of the structure
        :param jpype.JLong or int rva: The relative virtual address of the structure
        :raises IOException: if there was an IO-related error
        """

    def getLength(self) -> int:
        """
        :return: the length of the range
        :rtype: int
        """

    def getRangeType(self) -> ChpeRangeType:
        """
        :return: the :obj:`type <ChpeRangeType>` of range
        :rtype: ChpeRangeType
        """

    def getStartOffset(self) -> int:
        """
        :return: the start offset of the range
        :rtype: int
        """

    @property
    def startOffset(self) -> jpype.JInt:
        ...

    @property
    def rangeType(self) -> ChpeRangeType:
        ...

    @property
    def length(self) -> jpype.JLong:
        ...



__all__ = ["ChpeRangeType", "ImageArm64ecCodeRangeEntryPoint", "ImageArm64ecMetadata", "ImageArm64ecRedirectionEntry", "ImageChpeMetadataX86", "ImageChpeRangeEntry"]
