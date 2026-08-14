from __future__ import annotations
import collections.abc
import datetime
import typing
from warnings import deprecated # type: ignore

import jpype # type: ignore
import jpype.protocol # type: ignore

import generic.jar
import ghidra.app.util.importer
import ghidra.program.model.listing
import ghidra.util.classfinder
import ghidra.util.task
import java.lang # type: ignore
import java.util # type: ignore


class DataArchiveUtils(java.lang.Object):

    @typing.type_check_only
    class JsonEntry(java.lang.Record):
        """
        An entry from a spec extension JSON configuration file
        """

        class_: typing.ClassVar[java.lang.Class]

        def endian(self) -> str:
            ...

        def equals(self, o: java.lang.Object) -> bool:
            ...

        def file(self) -> str:
            ...

        def formats(self) -> java.util.List[java.lang.String]:
            ...

        def hashCode(self) -> int:
            ...

        def processor(self) -> str:
            ...

        def size(self) -> str:
            ...

        def toString(self) -> str:
            ...

        def variant(self) -> str:
            ...


    class_: typing.ClassVar[java.lang.Class]

    def __init__(self) -> None:
        ...

    @staticmethod
    def readDataArchiveJsonConfig(jsonFile: generic.jar.ResourceFile, program: ghidra.program.model.listing.Program, log: ghidra.app.util.importer.MessageLog, monitor: ghidra.util.task.TaskMonitor) -> java.util.List[SourceLanguageDataArchive.DataArchiveRule]:
        """
        :return: a :obj:`List` of :obj:`SpecExtensionRule`s based on the given JSON configuration
        file
        :rtype: java.util.List[SourceLanguageDataArchive.DataArchiveRule]
        
        
        :param generic.jar.ResourceFile jsonFile: The JSON configuration file
        :param ghidra.program.model.listing.Program program: The :obj:`Program`
        :param ghidra.app.util.importer.MessageLog log: The error log
        :param ghidra.util.task.TaskMonitor monitor: The monitor
        :raises IOException: if there was a problem reading the JSON configuration file or the
        :obj:`SpecExtension` XML files it references
        """


class SourceLanguage(ghidra.util.classfinder.ExtensionPoint):
    """
    An :obj:`ExtensionPoint` to dynamically support source language-specific features
    """

    class_: typing.ClassVar[java.lang.Class]

    def existsIn(self, program: ghidra.program.model.listing.Program, monitor: ghidra.util.task.TaskMonitor) -> bool:
        """
        :return: true if the source language exists in the given :obj:`Program`; otherwise false
        :rtype: bool
        
        
        :param ghidra.program.model.listing.Program program: The :obj:`Program`
        :param ghidra.util.task.TaskMonitor monitor: The :obj:`TaskMonitor`
        :raises IOException: if an IO-related error occurred
        :raises CancelledException: if the user cancelled the operation
        """

    def getID(self) -> SourceLanguageID:
        """
        :return: the :obj:`ID <SourceLanguageID>` of the source language
        :rtype: SourceLanguageID
        """

    @property
    def iD(self) -> SourceLanguageID:
        ...


class SourceLanguageDataArchive(ghidra.util.classfinder.ExtensionPoint):
    """
    An :obj:`ExtensionPoint` to dynamically support source language-specific data archives
    """

    class DataArchiveRule(java.lang.Record):
        """
        Processor-related attributes that form conditions for applying the given data archive
        contents to a program
        """

        class_: typing.ClassVar[java.lang.Class]

        def __init__(self, processor: typing.Union[java.lang.String, str], endian: typing.Union[java.lang.String, str], size: typing.Union[java.lang.String, str], variant: typing.Union[java.lang.String, str], formats: java.util.List[java.lang.String], dataArchiveFile: generic.jar.ResourceFile) -> None:
            ...

        def dataArchiveFile(self) -> generic.jar.ResourceFile:
            ...

        def endian(self) -> str:
            ...

        def equals(self, o: java.lang.Object) -> bool:
            ...

        def formats(self) -> java.util.List[java.lang.String]:
            ...

        def hashCode(self) -> int:
            ...

        def processor(self) -> str:
            ...

        def size(self) -> str:
            ...

        def toString(self) -> str:
            ...

        def variant(self) -> str:
            ...


    class_: typing.ClassVar[java.lang.Class]

    def getCompatibleSourceLanguage(self) -> SourceLanguageID:
        """
        :return: the :obj:`SourceLanguageID` of the source language this 
        :obj:`SourceLanguageDataArchive` is compatible with
        :rtype: SourceLanguageID
        """

    def getDataArchiveRules(self, program: ghidra.program.model.listing.Program, log: ghidra.app.util.importer.MessageLog, monitor: ghidra.util.task.TaskMonitor) -> java.util.List[SourceLanguageDataArchive.DataArchiveRule]:
        """
        :return: the source language's :obj:`DataArchiveRule`s
        :rtype: java.util.List[SourceLanguageDataArchive.DataArchiveRule]
        
        
        :param ghidra.program.model.listing.Program program: The :obj:`Program`
        :param ghidra.app.util.importer.MessageLog log: The error log
        :param ghidra.util.task.TaskMonitor monitor: The :obj:`TaskMonitor`
        """

    @property
    def compatibleSourceLanguage(self) -> SourceLanguageID:
        ...


class SourceLanguageID(java.lang.Comparable[SourceLanguageID]):
    """
    Represents a :obj:`source language <SourceLanguage>`'s ID
    """

    class_: typing.ClassVar[java.lang.Class]

    def __init__(self, id: typing.Union[java.lang.String, str]) -> None:
        """
        Creates a new :obj:`SourceLanguageID`.
         
        
        An ID must not be blank or contain commas.
        
        :param java.lang.String or str id: The :obj:`SourceLanguage`'s ID
        :raises IllegalArgumentException: if the ID blank, null, or contains commas
        """

    def getIdAsString(self) -> str:
        """
        :return: the :obj:`SourceLanguage` ID as a string
        :rtype: str
        """

    @property
    def idAsString(self) -> java.lang.String:
        ...


class SourceLanguageService(java.lang.Object):
    """
    A service for applying source language-related :obj:`ExtensionPoint`s to a :obj:`Program`
    """

    class_: typing.ClassVar[java.lang.Class]

    def __init__(self) -> None:
        ...

    @staticmethod
    def addSpecExtensions(program: ghidra.program.model.listing.Program, sourceLanguageIDs: java.util.Set[SourceLanguageID], log: ghidra.app.util.importer.MessageLog, monitor: ghidra.util.task.TaskMonitor) -> None:
        """
        Adds any :obj:`SourceLanguageSpecExtension`s that are compatible with the given set of 
        :obj:`SourceLanguageID`s to the :obj:`Program`
        
        :param ghidra.program.model.listing.Program program: The :obj:`Program`
        :param java.util.Set[SourceLanguageID] sourceLanguageIDs: The :obj:`SourceLanguageID`s
        :param ghidra.app.util.importer.MessageLog log: The error log
        :param ghidra.util.task.TaskMonitor monitor: The :obj:`TaskMonitor`
        """

    @staticmethod
    def find(program: ghidra.program.model.listing.Program, log: ghidra.app.util.importer.MessageLog, monitor: ghidra.util.task.TaskMonitor) -> java.util.Set[SourceLanguageID]:
        """
        Finds any :obj:`SourceLanguage`s that 
        :meth:`exist in <SourceLanguage.existsIn>` the given program, and
        returns their :obj:`SourceLanguageID`s.
         
        
        NOTE: This method does a fresh scan using 
        :meth:`SourceLanguage.existsIn(Program, TaskMonitor) <SourceLanguage.existsIn>` and does not check 
        :meth:`Program.getSourceLanguageIDs() <Program.getSourceLanguageIDs>`, so it may be slow.
        
        :param ghidra.program.model.listing.Program program: The :obj:`Program`
        :param ghidra.app.util.importer.MessageLog log: The error log
        :param ghidra.util.task.TaskMonitor monitor: The :obj:`TaskMonitor`
        :return: The :obj:`SourceLanguageID`s of the found :obj:`SourceLanguage`s
        :rtype: java.util.Set[SourceLanguageID]
        :raises CancelledException: if the user cancelled the operation
        """

    @staticmethod
    def getDataArchives(program: ghidra.program.model.listing.Program, sourceLanguageIDs: java.util.Set[SourceLanguageID], log: ghidra.app.util.importer.MessageLog, monitor: ghidra.util.task.TaskMonitor) -> java.util.List[generic.jar.ResourceFile]:
        """
        Adds any :obj:`SourceLanguageDataArchive`s that are compatible with the given set of
        :obj:`SourceLanguageID`s to the :obj:`Program`
        
        :param ghidra.program.model.listing.Program program: The :obj:`Program`
        :param java.util.Set[SourceLanguageID] sourceLanguageIDs: The :obj:`SourceLanguage`
        :param ghidra.app.util.importer.MessageLog log: The error log
        :param ghidra.util.task.TaskMonitor monitor: The :obj:`TaskMonitor`
        :return: The number of data archives that were added to the :obj:`Program`
        :rtype: java.util.List[generic.jar.ResourceFile]
        """


class SourceLanguageSpecExtension(ghidra.util.classfinder.ExtensionPoint):
    """
    An :obj:`ExtensionPoint` to dynamically support source language-specific 
    :obj:`spec extensions <SpecExtension>`
    """

    class SpecExtensionRule(java.lang.Record):
        """
        Processor-related attributes that form conditions for applying the given spec extension
        contents to a program
        """

        class_: typing.ClassVar[java.lang.Class]

        def __init__(self, processor: typing.Union[java.lang.String, str], endian: typing.Union[java.lang.String, str], size: typing.Union[java.lang.String, str], variant: typing.Union[java.lang.String, str], formats: java.util.List[java.lang.String], contents: typing.Union[java.lang.String, str]) -> None:
            ...

        def contents(self) -> str:
            ...

        def endian(self) -> str:
            ...

        def equals(self, o: java.lang.Object) -> bool:
            ...

        def formats(self) -> java.util.List[java.lang.String]:
            ...

        def hashCode(self) -> int:
            ...

        def processor(self) -> str:
            ...

        def size(self) -> str:
            ...

        def toString(self) -> str:
            ...

        def variant(self) -> str:
            ...


    class_: typing.ClassVar[java.lang.Class]

    def getCompatibleSourceLanguage(self) -> SourceLanguageID:
        """
        :return: the :obj:`SourceLanguageID` of the source language this 
        :obj:`SourceLanguageSpecExtension` is compatible with
        :rtype: SourceLanguageID
        """

    def getSpecExtensionRules(self, program: ghidra.program.model.listing.Program, log: ghidra.app.util.importer.MessageLog, monitor: ghidra.util.task.TaskMonitor) -> java.util.List[SourceLanguageSpecExtension.SpecExtensionRule]:
        """
        :return: the source language's :obj:`SpecExtensionRule`s
        :rtype: java.util.List[SourceLanguageSpecExtension.SpecExtensionRule]
        
        
        :param ghidra.program.model.listing.Program program: The :obj:`Program`
        :param ghidra.app.util.importer.MessageLog log: The error log
        :param ghidra.util.task.TaskMonitor monitor: The :obj:`TaskMonitor`
        """

    @property
    def compatibleSourceLanguage(self) -> SourceLanguageID:
        ...


class SpecExtensionUtils(java.lang.Object):

    @typing.type_check_only
    class JsonEntry(java.lang.Record):
        """
        An entry from a spec extension JSON configuration file
        """

        class_: typing.ClassVar[java.lang.Class]

        def directory(self) -> str:
            ...

        def endian(self) -> str:
            ...

        def equals(self, o: java.lang.Object) -> bool:
            ...

        def formats(self) -> java.util.List[java.lang.String]:
            ...

        def hashCode(self) -> int:
            ...

        def processor(self) -> str:
            ...

        def size(self) -> str:
            ...

        def toString(self) -> str:
            ...

        def variant(self) -> str:
            ...


    class_: typing.ClassVar[java.lang.Class]

    def __init__(self) -> None:
        ...

    @staticmethod
    def readSpecExtensionDir(dir: generic.jar.ResourceFile) -> java.util.List[java.lang.String]:
        """
        :return: a :obj:`List` of :obj:`SpecExtension` XML file contents found in the given 
        directory
        :rtype: java.util.List[java.lang.String]
        
        
        :param generic.jar.ResourceFile dir: A directory containing :obj:`SpecExtension` XML files
        :raises IOException: if there was a problem reading the XML files
        """

    @staticmethod
    def readSpecExtensionJsonConfig(jsonFile: generic.jar.ResourceFile, program: ghidra.program.model.listing.Program, log: ghidra.app.util.importer.MessageLog, monitor: ghidra.util.task.TaskMonitor) -> java.util.List[SourceLanguageSpecExtension.SpecExtensionRule]:
        """
        :return: a :obj:`List` of :obj:`SpecExtensionRule`s based on the given JSON configuration
        file
        :rtype: java.util.List[SourceLanguageSpecExtension.SpecExtensionRule]
        
        
        :param generic.jar.ResourceFile jsonFile: The JSON configuration file
        :param ghidra.program.model.listing.Program program: The :obj:`Program`
        :param ghidra.app.util.importer.MessageLog log: The error log
        :param ghidra.util.task.TaskMonitor monitor: The monitor
        :raises IOException: if there was a problem reading the JSON configuration file or the
        :obj:`SpecExtension` XML files it references
        """

    @staticmethod
    def readSpecExtensionXmlFile(xmlFile: generic.jar.ResourceFile) -> str:
        """
        :return: the given :obj:`SpecExtension` XML file's contents
        :rtype: str
        
        
        :param generic.jar.ResourceFile xmlFile: A :obj:`SpecExtension` XML file
        :raises IOException: if there was a problem reading the XML file
        """



__all__ = ["DataArchiveUtils", "SourceLanguage", "SourceLanguageDataArchive", "SourceLanguageID", "SourceLanguageService", "SourceLanguageSpecExtension", "SpecExtensionUtils"]
