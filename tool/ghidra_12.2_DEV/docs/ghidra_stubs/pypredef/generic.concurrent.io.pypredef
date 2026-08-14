from __future__ import annotations
import collections.abc
import datetime
import typing
from warnings import deprecated # type: ignore

import jpype # type: ignore
import jpype.protocol # type: ignore

import java.io # type: ignore
import java.lang # type: ignore
import java.util # type: ignore
import java.util.concurrent # type: ignore
import java.util.function # type: ignore


class IOResult(java.lang.Runnable):
    """
    :obj:`Runnable` that will consume all text output from an :obj:`InputStream` tied to an 
    external processes (stdout / stderr).
     
    
    The output can be inspected line-by-line by providing a string :obj:`Consumer`, or the entire
    output of the process can be inspected by calling :meth:`getOutput() <.getOutput>` or 
    :meth:`getOutputAsString() <.getOutputAsString>`.
    """

    class_: typing.ClassVar[java.lang.Class]
    THREAD_POOL_NAME: typing.Final = "I/O Thread Pool"

    @typing.overload
    def __init__(self, input: java.io.InputStream) -> None:
        """
        Creates a :obj:`IOResult` that consumes the specified :obj:`InputStream`, saving it
        as text lines.
        
        :param java.io.InputStream input: :obj:`InputStream`
        """

    @typing.overload
    def __init__(self, input: java.io.InputStream, inception: java.lang.Throwable) -> None:
        """
        Creates a :obj:`IOResult` that consumes the specified :obj:`InputStream`, saving it
        as text lines.
        
        :param java.io.InputStream input: :obj:`InputStream`
        :param java.lang.Throwable inception: information about where this object was created
        """

    @typing.overload
    def __init__(self, input: java.io.InputStream, lineConsumer: java.util.function.Consumer[java.lang.String], inception: java.lang.Throwable) -> None:
        """
        Creates a :obj:`IOResult` that consumes the specified :obj:`InputStream`, handing each
        line to the :obj:`Consumer`.
         
        
        Example: ``new IOResult(process.getInputStream(), s -> System.out.println(s), null);``
        
        :param java.io.InputStream input: :obj:`InputStream`
        :param java.util.function.Consumer[java.lang.String] lineConsumer: :obj:`string consumer <Consumer>`
        :param java.lang.Throwable inception: information about where this object was created
        """

    @typing.overload
    def __init__(self, input: java.io.InputStream, lineConsumer: java.util.function.Consumer[java.lang.String], retainLines: typing.Union[jpype.JBoolean, bool], inception: java.lang.Throwable) -> None:
        """
        Creates a :obj:`IOResult` that consumes the specified :obj:`InputStream`, handing each
        line to the :obj:`Consumer` and optionally storing each line for later retrieval.
        
        :param java.io.InputStream input: :obj:`InputStream`
        :param java.util.function.Consumer[java.lang.String] lineConsumer: :obj:`string consumer <Consumer>`, optional
        :param jpype.JBoolean or bool retainLines: boolean flag, if true, the contents read from the InputStream will be
        available via :meth:`getOutput() <.getOutput>` and :meth:`getOutputAsString() <.getOutputAsString>`
        :param java.lang.Throwable inception: information about where this object was created
        """

    def getOutput(self) -> java.util.List[java.lang.String]:
        ...

    def getOutputAsString(self) -> str:
        ...

    @property
    def output(self) -> java.util.List[java.lang.String]:
        ...

    @property
    def outputAsString(self) -> java.lang.String:
        ...


class ProcessConsumer(java.lang.Object):
    """
    A class that allows clients to **asynchronously** consume the output of a :obj:`Process`s
    input and error streams.  The task is asynchronous to avoid deadlocks when both streams need
    to be read in order for the process to proceed.
    """

    class_: typing.ClassVar[java.lang.Class]

    def __init__(self) -> None:
        ...

    @staticmethod
    @typing.overload
    def consume(is_: java.io.InputStream) -> java.util.concurrent.Future[IOResult]:
        """
        Read the given input stream line-by-line. 
         
         
        To get all output after all reading is done you can call the blocking operation 
        :meth:`Future.get() <Future.get>`.
        
        :param java.io.InputStream is: the input stream
        :return: the future that will be complete when all lines are read
        :rtype: java.util.concurrent.Future[IOResult]
        """

    @staticmethod
    @typing.overload
    def consume(is_: java.io.InputStream, lineConsumer: java.util.function.Consumer[java.lang.String]) -> java.util.concurrent.Future[IOResult]:
        """
        Read the given input stream line-by-line.
         
         
        If you wish to get all output after all reading is done you can call the blocking 
        operation :meth:`Future.get() <Future.get>`.
        
        :param java.io.InputStream is: the input stream
        :param java.util.function.Consumer[java.lang.String] lineConsumer: the line consumer; may be null
        :return: the future that will be complete when all lines are read
        :rtype: java.util.concurrent.Future[IOResult]
        """

    @staticmethod
    def monitorAndSignalEof(is_: java.io.InputStream, lineConsumer: java.util.function.Consumer[java.lang.String], processName: typing.Union[java.lang.String, str]) -> None:
        """
        Reads the given input stream line-by-line, calling the given consumer.  When the
        InputStream reaches EOF, a final ``null`` will be sent to the line consumer.
         
        
        The Inputstream is consumed via a Thread created just for this setup.
        
        :param java.io.InputStream is: the input stream
        :param java.util.function.Consumer[java.lang.String] lineConsumer: the line consumer; may be null
        :param java.lang.String or str processName: descriptive name of process being monitored
        """



__all__ = ["IOResult", "ProcessConsumer"]
