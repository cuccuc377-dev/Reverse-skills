from __future__ import annotations
import collections.abc
import datetime
import typing
from warnings import deprecated # type: ignore

import jpype # type: ignore
import jpype.protocol # type: ignore

import docking
import docking.action
import docking.action.builder
import docking.actions
import docking.widgets.gtreetable
import docking.widgets.table
import docking.widgets.table.threaded
import ghidra.app.plugin.core.debug
import ghidra.app.plugin.core.debug.gui
import ghidra.debug.api.tracemgr
import ghidra.framework.plugintool
import ghidra.program.model.address
import ghidra.program.model.listing
import ghidra.trace.model
import ghidra.trace.model.thread
import ghidra.trace.model.time
import java.lang # type: ignore
import java.util # type: ignore


class AbstractTraceCallTreeNode(docking.widgets.gtreetable.GTreeTableNode):

    class ParamNameToBytes(java.lang.Record):

        class_: typing.ClassVar[java.lang.Class]

        def __init__(self, name: typing.Union[java.lang.String, str], bytes: jpype.JArray[jpype.JByte]) -> None:
            ...

        def bytes(self) -> jpype.JArray[jpype.JByte]:
            ...

        def equals(self, o: java.lang.Object) -> bool:
            ...

        def hashCode(self) -> int:
            ...

        def name(self) -> str:
            ...

        def toString(self) -> str:
            ...


    class_: typing.ClassVar[java.lang.Class]

    def __init__(self, name: typing.Union[java.lang.String, str], module: typing.Union[java.lang.String, str], snap: ghidra.trace.model.time.TraceSnapshot, parameters: java.util.List[AbstractTraceCallTreeNode.ParamNameToBytes], returnVal: jpype.JArray[jpype.JByte]) -> None:
        ...

    def getLargestParamSize(self) -> int:
        ...

    def getModule(self) -> str:
        ...

    def getParameter(self, i: typing.Union[jpype.JInt, int]) -> AbstractTraceCallTreeNode.ParamNameToBytes:
        ...

    def getParameterNumber(self) -> int:
        ...

    def getParameterString(self, i: typing.Union[jpype.JInt, int]) -> str:
        ...

    def getParameters(self) -> java.util.List[AbstractTraceCallTreeNode.ParamNameToBytes]:
        ...

    def getReturnVal(self) -> jpype.JArray[jpype.JByte]:
        ...

    def getReturnValString(self) -> str:
        ...

    def getSnapshotKey(self) -> int:
        ...

    def setLargestParamSize(self, largestParamSize: typing.Union[jpype.JInt, int]) -> None:
        ...

    @property
    def returnVal(self) -> jpype.JArray[jpype.JByte]:
        ...

    @property
    def returnValString(self) -> java.lang.String:
        ...

    @property
    def parameterNumber(self) -> jpype.JInt:
        ...

    @property
    def parameter(self) -> AbstractTraceCallTreeNode.ParamNameToBytes:
        ...

    @property
    def module(self) -> java.lang.String:
        ...

    @property
    def snapshotKey(self) -> jpype.JLong:
        ...

    @property
    def largestParamSize(self) -> jpype.JInt:
        ...

    @largestParamSize.setter
    def largestParamSize(self, value: jpype.JInt):
        ...

    @property
    def parameterString(self) -> java.lang.String:
        ...

    @property
    def parameters(self) -> java.util.List[AbstractTraceCallTreeNode.ParamNameToBytes]:
        ...


class TraceCallTreeActionContext(docking.DefaultActionContext):

    class_: typing.ClassVar[java.lang.Class]

    def __init__(self, provider: TraceCallTreeProvider, selected: java.util.List[AbstractTraceCallTreeNode], source: docking.widgets.table.GTable) -> None:
        ...

    def getSelected(self) -> java.util.List[AbstractTraceCallTreeNode]:
        ...

    @property
    def selected(self) -> java.util.List[AbstractTraceCallTreeNode]:
        ...


class TraceCallTreeCallNode(AbstractTraceCallTreeNode):

    class_: typing.ClassVar[java.lang.Class]

    def __init__(self, name: typing.Union[java.lang.String, str], module: typing.Union[java.lang.String, str], snap: ghidra.trace.model.time.TraceSnapshot, parameters: java.util.List[AbstractTraceCallTreeNode.ParamNameToBytes], returnVal: jpype.JArray[jpype.JByte]) -> None:
        ...


class TraceCallTreeExternalNode(AbstractTraceCallTreeNode):

    class_: typing.ClassVar[java.lang.Class]

    def __init__(self, name: typing.Union[java.lang.String, str], module: typing.Union[java.lang.String, str], snap: ghidra.trace.model.time.TraceSnapshot, parameters: java.util.List[AbstractTraceCallTreeNode.ParamNameToBytes], returnVal: jpype.JArray[jpype.JByte]) -> None:
        ...


class TraceCallTreeLogContext(docking.DefaultActionContext):

    class_: typing.ClassVar[java.lang.Class]

    def __init__(self, provider: TraceCallTreeProvider, trace: ghidra.trace.model.Trace, dynamicPC: ghidra.program.model.address.Address) -> None:
        ...


class TraceCallTreeLogModel(docking.widgets.table.threaded.ThreadedTableModelStub[TraceCallTreeLogModel.TraceCallTreeLogObject]):

    @typing.type_check_only
    class DynamicAddressColumn(docking.widgets.table.AbstractDynamicTableColumn[TraceCallTreeLogModel.TraceCallTreeLogObject, ghidra.program.model.address.Address, java.lang.Object]):
        ...
        class_: typing.ClassVar[java.lang.Class]


    @typing.type_check_only
    class MessageColumn(docking.widgets.table.AbstractDynamicTableColumn[TraceCallTreeLogModel.TraceCallTreeLogObject, java.lang.String, java.lang.Object]):
        ...
        class_: typing.ClassVar[java.lang.Class]


    @typing.type_check_only
    class SnapColumn(docking.widgets.table.AbstractDynamicTableColumn[TraceCallTreeLogModel.TraceCallTreeLogObject, java.lang.Long, java.lang.Object]):
        ...
        class_: typing.ClassVar[java.lang.Class]


    @typing.type_check_only
    class StaticAddressColumn(docking.widgets.table.AbstractDynamicTableColumn[TraceCallTreeLogModel.TraceCallTreeLogObject, ghidra.program.model.address.Address, java.lang.Object]):
        ...
        class_: typing.ClassVar[java.lang.Class]


    class TraceCallTreeLogObject(java.lang.Record):

        class_: typing.ClassVar[java.lang.Class]

        def __init__(self, trace: ghidra.trace.model.Trace, log: typing.Union[java.lang.String, str], snap: typing.Union[jpype.JLong, int], dynamicAddress: ghidra.program.model.address.Address, staticAddress: ghidra.program.model.address.Address) -> None:
            ...

        def dynamicAddress(self) -> ghidra.program.model.address.Address:
            ...

        def equals(self, o: java.lang.Object) -> bool:
            ...

        def hashCode(self) -> int:
            ...

        def log(self) -> str:
            ...

        def snap(self) -> int:
            ...

        def staticAddress(self) -> ghidra.program.model.address.Address:
            ...

        def toString(self) -> str:
            ...

        def trace(self) -> ghidra.trace.model.Trace:
            ...


    @typing.type_check_only
    class TraceColumn(docking.widgets.table.AbstractDynamicTableColumn[TraceCallTreeLogModel.TraceCallTreeLogObject, java.lang.String, java.lang.Object]):
        ...
        class_: typing.ClassVar[java.lang.Class]


    @typing.type_check_only
    class LogKey(java.lang.Record):

        class_: typing.ClassVar[java.lang.Class]

        def dynamicAddress(self) -> ghidra.program.model.address.Address:
            ...

        def equals(self, o: java.lang.Object) -> bool:
            ...

        def hashCode(self) -> int:
            ...

        def snap(self) -> int:
            ...

        def toString(self) -> str:
            ...

        def traceName(self) -> str:
            ...


    class_: typing.ClassVar[java.lang.Class]


@typing.type_check_only
class TraceCallTreeModel(docking.widgets.gtreetable.GTreeTableModel[AbstractTraceCallTreeNode]):

    @typing.type_check_only
    class ModuleColumn(docking.widgets.table.AbstractDynamicTableColumnStub[AbstractTraceCallTreeNode, java.lang.String]):
        ...
        class_: typing.ClassVar[java.lang.Class]


    @typing.type_check_only
    class ParameterColumn(docking.widgets.table.AbstractDynamicTableColumnStub[AbstractTraceCallTreeNode, java.lang.String]):
        ...
        class_: typing.ClassVar[java.lang.Class]


    @typing.type_check_only
    class ReturnColumn(docking.widgets.table.AbstractDynamicTableColumnStub[AbstractTraceCallTreeNode, java.lang.String]):
        ...
        class_: typing.ClassVar[java.lang.Class]


    @typing.type_check_only
    class SnapColumn(docking.widgets.table.AbstractDynamicTableColumnStub[AbstractTraceCallTreeNode, java.lang.Long]):
        ...
        class_: typing.ClassVar[java.lang.Class]


    class_: typing.ClassVar[java.lang.Class]

    def __init__(self, rootNode: AbstractTraceCallTreeNode) -> None:
        ...

    def setNumberOfParameterColumns(self, num: typing.Union[jpype.JInt, int]) -> None:
        ...


class TraceCallTreePlugin(ghidra.app.plugin.core.debug.AbstractDebuggerPlugin):

    class_: typing.ClassVar[java.lang.Class]

    def __init__(self, tool: ghidra.framework.plugintool.PluginTool) -> None:
        ...


class TraceCallTreeProvider(ghidra.framework.plugintool.ComponentProviderAdapter, ghidra.app.plugin.core.debug.gui.DebuggerProvider, docking.actions.PopupActionProvider):

    @typing.type_check_only
    class ClearLogAction(docking.action.DockingAction):
        ...
        class_: typing.ClassVar[java.lang.Class]


    @typing.type_check_only
    class FoldRecursiveAction(docking.action.DockingAction):
        ...
        class_: typing.ClassVar[java.lang.Class]


    @typing.type_check_only
    class JumpToCurrentAction(docking.action.DockingAction):
        ...
        class_: typing.ClassVar[java.lang.Class]


    @typing.type_check_only
    class NodeFallthrough(java.lang.Record):

        class_: typing.ClassVar[java.lang.Class]

        def equals(self, o: java.lang.Object) -> bool:
            ...

        def fallthrough(self) -> ghidra.program.model.address.Address:
            ...

        def hashCode(self) -> int:
            ...

        def node(self) -> AbstractTraceCallTreeNode:
            ...

        def toString(self) -> str:
            ...


    @typing.type_check_only
    class RebuildCallTreeAction(docking.action.DockingAction):
        ...
        class_: typing.ClassVar[java.lang.Class]


    @typing.type_check_only
    class RootCache(java.lang.Record):

        class_: typing.ClassVar[java.lang.Class]

        def __init__(self) -> None:
            ...

        def equals(self, o: java.lang.Object) -> bool:
            ...

        def hashCode(self) -> int:
            ...

        def rootNodesPerThread(self) -> java.util.Map[ghidra.trace.model.thread.TraceThread, AbstractTraceCallTreeNode]:
            ...

        def toString(self) -> str:
            ...


    @typing.type_check_only
    class ShowLogWindowAction(docking.action.ToggleDockingAction):
        ...
        class_: typing.ClassVar[java.lang.Class]


    @typing.type_check_only
    class ShowReturnsToggleAction(docking.action.ToggleDockingAction):
        ...
        class_: typing.ClassVar[java.lang.Class]


    @typing.type_check_only
    class ShowTailCallsToggleAction(docking.action.ToggleDockingAction):
        ...
        class_: typing.ClassVar[java.lang.Class]


    @typing.type_check_only
    class TraceCallTreeEventListener(ghidra.trace.model.TraceDomainObjectListener):

        class_: typing.ClassVar[java.lang.Class]

        def __init__(self) -> None:
            ...


    @typing.type_check_only
    class TraceCallTreePopupAction(java.lang.Object):

        class_: typing.ClassVar[java.lang.Class]
        NAME: typing.Final = "Trace Call Tree Popup Actions"
        DESCRIPTION: typing.Final = "Popup actions for trace call tree"
        HELP_ANCHOR: typing.Final = ""
        GROUP1: typing.Final = "z"
        GROUP2: typing.Final = "zz"
        GROUP3: typing.Final = "zzz"
        GROUP4: typing.Final = "zzzz"

        @staticmethod
        def builder(owner: docking.ComponentProvider, group: typing.Union[java.lang.String, str], subgroup: typing.Union[java.lang.String, str], *path: typing.Union[java.lang.String, str]) -> docking.action.builder.ActionBuilder:
            ...


    @typing.type_check_only
    class UnfoldRecursiveAction(docking.action.DockingAction):
        ...
        class_: typing.ClassVar[java.lang.Class]


    class_: typing.ClassVar[java.lang.Class]

    def __init__(self, plugin: TraceCallTreePlugin) -> None:
        ...

    def dispose(self) -> None:
        ...

    def programClosed(self, program: ghidra.program.model.listing.Program) -> None:
        ...

    def programOpened(self, program: ghidra.program.model.listing.Program) -> None:
        ...

    def setCoordinates(self, coords: ghidra.debug.api.tracemgr.DebuggerCoordinates) -> None:
        ...

    def traceClosed(self, trace: ghidra.trace.model.Trace) -> None:
        ...


class TraceCallTreeReturnNode(AbstractTraceCallTreeNode):

    class_: typing.ClassVar[java.lang.Class]

    def __init__(self, name: typing.Union[java.lang.String, str], module: typing.Union[java.lang.String, str], snap: ghidra.trace.model.time.TraceSnapshot, parameters: java.util.List[AbstractTraceCallTreeNode.ParamNameToBytes], returnVal: jpype.JArray[jpype.JByte]) -> None:
        ...


class TraceCallTreeTable(docking.widgets.gtreetable.GTreeTable[AbstractTraceCallTreeNode]):

    class_: typing.ClassVar[java.lang.Class]

    def __init__(self, model: docking.widgets.gtreetable.GTreeTableModel[AbstractTraceCallTreeNode]) -> None:
        ...

    def setStatusMessage(self, msg: typing.Union[java.lang.String, str]) -> None:
        ...


class TraceCallTreeTailCallNode(AbstractTraceCallTreeNode):

    class_: typing.ClassVar[java.lang.Class]

    def __init__(self, name: typing.Union[java.lang.String, str], module: typing.Union[java.lang.String, str], snap: ghidra.trace.model.time.TraceSnapshot, parameters: java.util.List[AbstractTraceCallTreeNode.ParamNameToBytes], returnVal: jpype.JArray[jpype.JByte]) -> None:
        ...



__all__ = ["AbstractTraceCallTreeNode", "TraceCallTreeActionContext", "TraceCallTreeCallNode", "TraceCallTreeExternalNode", "TraceCallTreeLogContext", "TraceCallTreeLogModel", "TraceCallTreeModel", "TraceCallTreePlugin", "TraceCallTreeProvider", "TraceCallTreeReturnNode", "TraceCallTreeTable", "TraceCallTreeTailCallNode"]
