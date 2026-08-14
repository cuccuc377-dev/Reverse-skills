from __future__ import annotations
import collections.abc
import datetime
import typing
from warnings import deprecated # type: ignore

import jpype # type: ignore
import jpype.protocol # type: ignore

import docking
import ghidra.app.plugin
import ghidra.framework.plugintool
import java.lang # type: ignore


class RestoreSelectionPlugin(ghidra.app.plugin.ProgramPlugin):

    @typing.type_check_only
    class SelectionState(java.lang.Object):
        """
        A state class to keep track of past and current selections and to determine when we can
        restore an old selection.
        """

        class_: typing.ClassVar[java.lang.Class]


    class_: typing.ClassVar[java.lang.Class]

    def __init__(self, tool: ghidra.framework.plugintool.PluginTool) -> None:
        ...


@typing.type_check_only
class SelectBytesDialog(docking.ReusableDialogComponentProvider):
    """
    Dialog for making program selections
    """

    class_: typing.ClassVar[java.lang.Class]


class SelectBytesPlugin(ghidra.framework.plugintool.Plugin):
    """
    This plugin allows users to select bytes anywhere inside of the Code Browser and Byte Viewer.
    """

    class_: typing.ClassVar[java.lang.Class]

    def __init__(self, tool: ghidra.framework.plugintool.PluginTool) -> None:
        ...



__all__ = ["RestoreSelectionPlugin", "SelectBytesDialog", "SelectBytesPlugin"]
