from __future__ import annotations
import collections.abc
import datetime
import typing
from warnings import deprecated # type: ignore

import jpype # type: ignore
import jpype.protocol # type: ignore

import docking.widgets.tree
import ghidra.framework.plugintool
import ghidra.trace.model
import ghidra.util.database.spatial
import java.awt # type: ignore
import java.lang # type: ignore


class RStarDiagnosticsPlugin(ghidra.framework.plugintool.Plugin):

    class_: typing.ClassVar[java.lang.Class]

    def __init__(self, tool: ghidra.framework.plugintool.PluginTool) -> None:
        ...


class RStarPlotProvider(ghidra.framework.plugintool.ComponentProviderAdapter):

    @typing.type_check_only
    class OffsetSnap(java.lang.Record):

        class_: typing.ClassVar[java.lang.Class]

        def equals(self, o: java.lang.Object) -> bool:
            ...

        def hashCode(self) -> int:
            ...

        def offset(self) -> int:
            ...

        def snap(self) -> int:
            ...


    @typing.type_check_only
    class MyPainter(ghidra.trace.database.map.DBTraceAddressSnapRangePropertyMapTree.Painter):

        class_: typing.ClassVar[java.lang.Class]

        def __init__(self, rect: java.awt.Rectangle, bounds: ghidra.trace.model.TraceAddressSnapRange) -> None:
            ...


    class_: typing.ClassVar[java.lang.Class]

    def __init__(self, plugin: RStarDiagnosticsPlugin) -> None:
        ...


class RStarTreeProvider(ghidra.framework.plugintool.ComponentProviderAdapter):

    @typing.type_check_only
    class HasShape(java.lang.Object):

        class_: typing.ClassVar[java.lang.Class]

        def getShape(self) -> ghidra.trace.model.TraceAddressSnapRange:
            ...

        @property
        def shape(self) -> ghidra.trace.model.TraceAddressSnapRange:
            ...


    @typing.type_check_only
    class RootRStarNode(docking.widgets.tree.GTreeLazyNode, RStarTreeProvider.HasShape):
        ...
        class_: typing.ClassVar[java.lang.Class]


    @typing.type_check_only
    class NodeRStarNode(docking.widgets.tree.GTreeLazyNode, RStarTreeProvider.HasShape):

        class_: typing.ClassVar[java.lang.Class]

        def __init__(self, rec: ghidra.util.database.spatial.DBTreeNodeRecord[typing.Any]) -> None:
            ...


    @typing.type_check_only
    class DataRStarNode(docking.widgets.tree.GTreeNode, RStarTreeProvider.HasShape):

        class_: typing.ClassVar[java.lang.Class]

        def __init__(self, rec: ghidra.util.database.spatial.DBTreeDataRecord[typing.Any, typing.Any, typing.Any]) -> None:
            ...


    class_: typing.ClassVar[java.lang.Class]

    def __init__(self, plugin: RStarDiagnosticsPlugin) -> None:
        ...

    def select(self, shape: ghidra.trace.model.TraceAddressSnapRange) -> None:
        ...



__all__ = ["RStarDiagnosticsPlugin", "RStarPlotProvider", "RStarTreeProvider"]
