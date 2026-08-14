from __future__ import annotations
import collections.abc
import datetime
import typing
from warnings import deprecated # type: ignore

import jpype # type: ignore
import jpype.protocol # type: ignore

import docking
import docking.action
import ghidra.app.plugin.core.debug
import ghidra.framework.plugintool
import ghidra.program.model.address
import ghidra.trace.model
import ghidra.trace.model.breakpoint
import ghidra.trace.model.target
import java.lang # type: ignore
import java.util # type: ignore
import javax.swing # type: ignore


class BreakpointTimelineActions(java.lang.Object):

    @typing.type_check_only
    class BreakType(java.lang.Enum[BreakpointTimelineActions.BreakType]):

        class_: typing.ClassVar[java.lang.Class]
        EXECUTE: typing.Final[BreakpointTimelineActions.BreakType]
        READ: typing.Final[BreakpointTimelineActions.BreakType]
        WRITE: typing.Final[BreakpointTimelineActions.BreakType]
        ACCESS: typing.Final[BreakpointTimelineActions.BreakType]

        @staticmethod
        def valueOf(name: typing.Union[java.lang.String, str]) -> BreakpointTimelineActions.BreakType:
            ...

        @staticmethod
        def values() -> jpype.JArray[BreakpointTimelineActions.BreakType]:
            ...


    @typing.type_check_only
    class SearchType(java.lang.Enum[BreakpointTimelineActions.SearchType]):

        class_: typing.ClassVar[java.lang.Class]
        FIRST: typing.Final[BreakpointTimelineActions.SearchType]
        PREVIOUS: typing.Final[BreakpointTimelineActions.SearchType]
        NEXT: typing.Final[BreakpointTimelineActions.SearchType]
        FINAL: typing.Final[BreakpointTimelineActions.SearchType]
        ALL: typing.Final[BreakpointTimelineActions.SearchType]

        @staticmethod
        def valueOf(name: typing.Union[java.lang.String, str]) -> BreakpointTimelineActions.SearchType:
            ...

        @staticmethod
        def values() -> jpype.JArray[BreakpointTimelineActions.SearchType]:
            ...


    @typing.type_check_only
    class AddressSnap(java.lang.Record):

        class_: typing.ClassVar[java.lang.Class]

        def address(self) -> ghidra.program.model.address.Address:
            ...

        def equals(self, o: java.lang.Object) -> bool:
            ...

        def hashCode(self) -> int:
            ...

        def snap(self) -> int:
            ...

        def toString(self) -> str:
            ...


    @typing.type_check_only
    class BreakpointTimelineActionProvider(docking.ComponentProvider):

        class_: typing.ClassVar[java.lang.Class]

        def __init__(self, tool: docking.Tool, title: typing.Union[java.lang.String, str], snapList: java.util.List[BreakpointTimelineActions.AddressSnap]) -> None:
            ...


    @typing.type_check_only
    class TimelineAction(docking.action.DockingAction):
        ...
        class_: typing.ClassVar[java.lang.Class]


    class_: typing.ClassVar[java.lang.Class]


@typing.type_check_only
class BreakpointTimelinePanel(javax.swing.JPanel):

    @typing.type_check_only
    class CachedIndex(java.lang.Object):
        ...
        class_: typing.ClassVar[java.lang.Class]


    class_: typing.ClassVar[java.lang.Class]


class BreakpointTimelinePlugin(ghidra.app.plugin.core.debug.AbstractDebuggerPlugin):

    class_: typing.ClassVar[java.lang.Class]

    def __init__(self, tool: ghidra.framework.plugintool.PluginTool) -> None:
        ...


class BreakpointTimelineProvider(docking.ComponentProvider):

    @typing.type_check_only
    class BreakpointHitEvent(java.lang.Record):

        class_: typing.ClassVar[java.lang.Class]

        def breakType(self) -> ghidra.trace.model.breakpoint.TraceBreakpointKind:
            ...

        def breakpointName(self) -> str:
            ...

        def equals(self, o: java.lang.Object) -> bool:
            ...

        def hashCode(self) -> int:
            ...

        def snap(self) -> int:
            ...

        def toString(self) -> str:
            ...


    @typing.type_check_only
    class BreakpointTimeOverviewEventListener(ghidra.trace.model.TraceDomainObjectListener):

        class_: typing.ClassVar[java.lang.Class]

        def __init__(self) -> None:
            ...


    @typing.type_check_only
    class CloseAllZoomWindowsAction(docking.action.DockingAction):
        ...
        class_: typing.ClassVar[java.lang.Class]


    @typing.type_check_only
    class SmallestCellSizeAction(docking.action.DockingAction):
        ...
        class_: typing.ClassVar[java.lang.Class]


    @typing.type_check_only
    class ToggleGridAction(docking.action.DockingAction):
        ...
        class_: typing.ClassVar[java.lang.Class]


    @typing.type_check_only
    class ToggleGridOrColumnAction(docking.action.DockingAction):
        ...
        class_: typing.ClassVar[java.lang.Class]


    @typing.type_check_only
    class ZoomInAction(docking.action.DockingAction):
        ...
        class_: typing.ClassVar[java.lang.Class]


    @typing.type_check_only
    class ZoomOutAction(docking.action.DockingAction):
        ...
        class_: typing.ClassVar[java.lang.Class]


    class_: typing.ClassVar[java.lang.Class]

    @staticmethod
    def getTraceObjectValuesWithPCsIntersectingRange(trace: ghidra.trace.model.Trace, range: ghidra.program.model.address.AddressRange) -> java.util.Iterator[ghidra.trace.model.target.TraceObjectValue]:
        ...



__all__ = ["BreakpointTimelineActions", "BreakpointTimelinePanel", "BreakpointTimelinePlugin", "BreakpointTimelineProvider"]
