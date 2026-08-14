from __future__ import annotations
import collections.abc
import datetime
import typing
from warnings import deprecated # type: ignore

import jpype # type: ignore
import jpype.protocol # type: ignore

import docking
import docking.action.builder
import docking.actions
import docking.widgets.table
import docking.widgets.table.threaded
import ghidra.app.plugin.core.debug
import ghidra.app.plugin.core.debug.gui
import ghidra.base.widgets.table
import ghidra.debug.api.tracemgr
import ghidra.docking.settings
import ghidra.framework.plugintool
import ghidra.program.model.address
import ghidra.program.model.lang
import ghidra.program.model.listing
import ghidra.program.model.pcode
import ghidra.trace.model
import ghidra.trace.model.memory
import java.lang # type: ignore
import java.util # type: ignore
import java.util.function # type: ignore
import javax.swing # type: ignore
import javax.swing.table # type: ignore


T = typing.TypeVar("T")
V = typing.TypeVar("V")


class AbstractDebuggerVariableViewerVarValue(java.lang.Object):

    class_: typing.ClassVar[java.lang.Class]

    def canEdit(self) -> bool:
        ...

    def getAddress(self) -> ghidra.program.model.address.Address:
        ...

    def getError(self) -> str:
        ...

    def getLanguage(self) -> ghidra.program.model.lang.Language:
        ...

    def getRepr(self) -> str:
        ...

    def getValue(self) -> str:
        ...

    def isChanged(self) -> bool:
        ...

    def isKnown(self) -> bool:
        ...

    def setOldValue(self, oldValue: jpype.JArray[jpype.JByte]) -> None:
        ...

    def setRepr(self, reprValue: typing.Union[java.lang.String, str]) -> None:
        ...

    def setValue(self, valueString: typing.Union[java.lang.String, str]) -> None:
        ...

    @property
    def repr(self) -> java.lang.String:
        ...

    @repr.setter
    def repr(self, value: java.lang.String):
        ...

    @property
    def address(self) -> ghidra.program.model.address.Address:
        ...

    @property
    def known(self) -> jpype.JBoolean:
        ...

    @property
    def language(self) -> ghidra.program.model.lang.Language:
        ...

    @property
    def error(self) -> java.lang.String:
        ...

    @property
    def value(self) -> java.lang.String:
        ...

    @value.setter
    def value(self, value: java.lang.String):
        ...

    @property
    def changed(self) -> jpype.JBoolean:
        ...


class DebuggerVariableViewerHighVarValue(AbstractDebuggerVariableViewerVarValue):

    class_: typing.ClassVar[java.lang.Class]

    def __init__(self, variable: ghidra.program.model.pcode.HighSymbol, value: jpype.JArray[jpype.JByte], address: ghidra.program.model.address.Address, repr: typing.Union[java.lang.String, str], provider: DebuggerVariableViewerProvider, error: typing.Union[java.lang.String, str], state: ghidra.trace.model.memory.TraceMemoryState) -> None:
        ...


class DebuggerVariableViewerModel(docking.widgets.table.threaded.ThreadedTableModelStub[AbstractDebuggerVariableViewerVarValue]):

    @typing.type_check_only
    class DataTypeEditor(ghidra.base.widgets.table.AbstractDataTypeTableCellEditor):
        ...
        class_: typing.ClassVar[java.lang.Class]


    @typing.type_check_only
    class VariableValueOrReprCellEditor(javax.swing.AbstractCellEditor, javax.swing.table.TableCellEditor, typing.Generic[T]):

        class_: typing.ClassVar[java.lang.Class]

        def __init__(self, getter: java.util.function.Function[AbstractDebuggerVariableViewerVarValue, T]) -> None:
            ...


    @typing.type_check_only
    class VariableMemoryStateCellRenderer(docking.widgets.table.CustomToStringCellRenderer[AbstractDebuggerVariableViewerVarValue]):

        class_: typing.ClassVar[java.lang.Class]

        def __init__(self, toString: java.util.function.BiFunction[AbstractDebuggerVariableViewerVarValue, ghidra.docking.settings.Settings, java.lang.String]) -> None:
            ...


    @typing.type_check_only
    class AbstractDebuggerVariableColumn(docking.widgets.table.AbstractDynamicTableColumn[AbstractDebuggerVariableViewerVarValue, T, java.lang.Object], typing.Generic[T, V]):

        class_: typing.ClassVar[java.lang.Class]

        def isEditable(self) -> bool:
            ...

        def setValue(self, rowObject: AbstractDebuggerVariableViewerVarValue, data: java.lang.Object) -> None:
            ...

        @property
        def editable(self) -> jpype.JBoolean:
            ...


    @typing.type_check_only
    class AbstractDebuggerVariableColumnNoSetter(DebuggerVariableViewerModel.AbstractDebuggerVariableColumn[T, java.lang.Void], typing.Generic[T]):
        ...
        class_: typing.ClassVar[java.lang.Class]


    @typing.type_check_only
    class VariableValueOrReprColumn(DebuggerVariableViewerModel.AbstractDebuggerVariableColumn[AbstractDebuggerVariableViewerVarValue, java.lang.String]):
        ...
        class_: typing.ClassVar[java.lang.Class]


    @typing.type_check_only
    class SourceColumn(DebuggerVariableViewerModel.AbstractDebuggerVariableColumnNoSetter[java.lang.String]):
        ...
        class_: typing.ClassVar[java.lang.Class]


    @typing.type_check_only
    class StorageColumn(DebuggerVariableViewerModel.AbstractDebuggerVariableColumnNoSetter[AbstractDebuggerVariableViewerVarValue]):
        ...
        class_: typing.ClassVar[java.lang.Class]


    @typing.type_check_only
    class ReprColumn(DebuggerVariableViewerModel.VariableValueOrReprColumn):
        ...
        class_: typing.ClassVar[java.lang.Class]


    @typing.type_check_only
    class SymbolColumn(DebuggerVariableViewerModel.AbstractDebuggerVariableColumn[java.lang.String, java.lang.String]):
        ...
        class_: typing.ClassVar[java.lang.Class]


    @typing.type_check_only
    class TypeColumn(DebuggerVariableViewerModel.AbstractDebuggerVariableColumn[ghidra.program.model.data.DataType, ghidra.program.model.data.DataType]):
        ...
        class_: typing.ClassVar[java.lang.Class]


    @typing.type_check_only
    class ValueColumn(DebuggerVariableViewerModel.VariableValueOrReprColumn):
        ...
        class_: typing.ClassVar[java.lang.Class]


    @typing.type_check_only
    class ErrorColumn(DebuggerVariableViewerModel.AbstractDebuggerVariableColumnNoSetter[java.lang.String]):
        ...
        class_: typing.ClassVar[java.lang.Class]


    class_: typing.ClassVar[java.lang.Class]

    def __init__(self, tool: docking.Tool, provider: DebuggerVariableViewerProvider) -> None:
        ...

    def setModelData(self, result: java.util.List[AbstractDebuggerVariableViewerVarValue]) -> None:
        ...

    def setTrace(self, trace: ghidra.trace.model.Trace) -> None:
        ...


class DebuggerVariableViewerPlugin(ghidra.app.plugin.core.debug.AbstractDebuggerPlugin):

    class_: typing.ClassVar[java.lang.Class]

    def __init__(self, tool: ghidra.framework.plugintool.PluginTool) -> None:
        ...


class DebuggerVariableViewerProvider(ghidra.framework.plugintool.ComponentProviderAdapter, ghidra.app.plugin.core.debug.gui.DebuggerProvider, docking.actions.PopupActionProvider):

    @typing.type_check_only
    class VariableViewerStates(java.lang.Enum[DebuggerVariableViewerProvider.VariableViewerStates]):

        class_: typing.ClassVar[java.lang.Class]
        LISTING: typing.Final[DebuggerVariableViewerProvider.VariableViewerStates]
        DECOMPILER: typing.Final[DebuggerVariableViewerProvider.VariableViewerStates]
        BOTH: typing.Final[DebuggerVariableViewerProvider.VariableViewerStates]

        @staticmethod
        def valueOf(name: typing.Union[java.lang.String, str]) -> DebuggerVariableViewerProvider.VariableViewerStates:
            ...

        @staticmethod
        def values() -> jpype.JArray[DebuggerVariableViewerProvider.VariableViewerStates]:
            ...


    @typing.type_check_only
    class DebuggerVariableViewerPopupAction(java.lang.Object):

        class_: typing.ClassVar[java.lang.Class]
        NAME: typing.Final = "Debugger variable viewer Popup Actions"
        DESCRIPTION: typing.Final = "Popup actions for debugger variable viewer"
        HELP_ANCHOR: typing.Final = ""
        GROUP1: typing.Final = "z"
        GROUP2: typing.Final = "zz"

        @staticmethod
        def builder(owner: docking.ComponentProvider, subgroup: typing.Union[java.lang.String, str], *path: typing.Union[java.lang.String, str]) -> docking.action.builder.ActionBuilder:
            ...


    @typing.type_check_only
    class DebuggerVariableActionContext(docking.DefaultActionContext):

        class_: typing.ClassVar[java.lang.Class]

        def __init__(self, provider: DebuggerVariableViewerProvider, selected: java.util.List[AbstractDebuggerVariableViewerVarValue], source: docking.widgets.table.GTable) -> None:
            ...

        def getSelected(self) -> java.util.List[AbstractDebuggerVariableViewerVarValue]:
            ...

        @property
        def selected(self) -> java.util.List[AbstractDebuggerVariableViewerVarValue]:
            ...


    class_: typing.ClassVar[java.lang.Class]

    def __init__(self, plugin: DebuggerVariableViewerPlugin) -> None:
        ...

    def rebuildTable(self) -> None:
        ...

    def setCoordinates(self, coordinates: ghidra.debug.api.tracemgr.DebuggerCoordinates) -> None:
        ...


class DebuggerVariableViewerVarValue(AbstractDebuggerVariableViewerVarValue):

    class_: typing.ClassVar[java.lang.Class]

    def __init__(self, variable: ghidra.program.model.listing.Variable, value: jpype.JArray[jpype.JByte], address: ghidra.program.model.address.Address, repr: typing.Union[java.lang.String, str], provider: DebuggerVariableViewerProvider, error: typing.Union[java.lang.String, str], state: ghidra.trace.model.memory.TraceMemoryState) -> None:
        ...



__all__ = ["AbstractDebuggerVariableViewerVarValue", "DebuggerVariableViewerHighVarValue", "DebuggerVariableViewerModel", "DebuggerVariableViewerPlugin", "DebuggerVariableViewerProvider", "DebuggerVariableViewerVarValue"]
