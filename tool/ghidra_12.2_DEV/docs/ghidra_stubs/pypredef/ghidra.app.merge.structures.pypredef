from __future__ import annotations
import collections.abc
import datetime
import typing
from warnings import deprecated # type: ignore

import jpype # type: ignore
import jpype.protocol # type: ignore

import docking
import ghidra.program.model.data
import java.awt # type: ignore
import java.lang # type: ignore
import java.util # type: ignore
import java.util.function # type: ignore
import javax.swing # type: ignore
import javax.swing.event # type: ignore
import utility.function


class ComparisonItem(java.lang.Comparable[ComparisonItem]):
    """
    Base class for items that can be displayed in a :obj:`CoordinatedStructureDisplay`. These are
    basically different views from a :obj:`CoordinatedStructureLine` where each coordinated line
    has three comparison items, one for the left side structure, one for the right side structure,
    and for the merged structure.
    """

    @typing.type_check_only
    class ItemApplyState(java.lang.Enum[ComparisonItem.ItemApplyState]):

        class_: typing.ClassVar[java.lang.Class]
        NON_APPLIALBLE: typing.Final[ComparisonItem.ItemApplyState]
        APPLIED: typing.Final[ComparisonItem.ItemApplyState]
        NOT_APPLIED: typing.Final[ComparisonItem.ItemApplyState]

        @staticmethod
        def valueOf(name: typing.Union[java.lang.String, str]) -> ComparisonItem.ItemApplyState:
            ...

        @staticmethod
        def values() -> jpype.JArray[ComparisonItem.ItemApplyState]:
            ...


    class_: typing.ClassVar[java.lang.Class]
    MAX_COLS: typing.ClassVar[jpype.JInt]

    def applyAll(self) -> None:
        """
        Applies all the information in this item to the merged structure.
        """

    def canApplyAny(self) -> bool:
        """
        Returns true if any information in this item is not currently applied to the merged item.
        if true, the button should be displayed as unselected, indicating to the user that this
        item has information that can be applied.
        
        :return: true if any information in this item can be applied.
        :rtype: bool
        """

    def canClear(self) -> bool:
        """
        Returns true if the information from this item can be cleared. Currently only items
        from component lines can be cleared. Items such as the structure name can never be cleared
        and can only change by selecting the other side value.
        If true, the button will be allowed to become unselected without the other side being
        selected.
        
        :return: true if the information from this item can be cleared
        :rtype: bool
        """

    def clear(self) -> None:
        """
        Clears this item from the merged structure. Normally items from one side or the other
        are cleared when the corresponding item for the other side is applied. This allows the
        state where neither side is applied.
        """

    def getColumnText(self, column: typing.Union[jpype.JInt, int]) -> str:
        """
        Returns the text to be display for the given column index.
        
        :param jpype.JInt or int column: the index of the column to get text for
        :return: the text to be display for the given column index.
        :rtype: str
        """

    def getLine(self) -> int:
        """
        Return the line number for this item in the coordinated display. Note that this may
        be different from its index in its list model. The merged display removes blank lines, but
        maintains the line number where it matches in the left/right displays. This is uses to
        coordinated the left/right/merged views.
        
        :return: the line number for this item
        :rtype: int
        """

    def getMinWidth(self, column: typing.Union[jpype.JInt, int]) -> int:
        """
        Returns the minimum width of this column. Used to reserve space for a column even when
        there is no text to display in the column. The column may be wider if its text is wider
        than the minimum width. Used to help the renderer allocate available extra space when
        the view is resized.
        
        :param jpype.JInt or int column: the column to get the min width for
        :return: the minimum width of this column
        :rtype: int
        """

    @typing.overload
    def isAppliable(self) -> bool:
        """
        Returns true if this items represents something that can be applied or not applied. Used
        to determine if a button should be created for this item.  For
        example, a structure name can applied from either side, but the simple syntax line "{"
        is the same for all sides, so it is never appliable and should not have a corresponding
        button.
        
        :return: true if this item can potentially be applied.
        :rtype: bool
        """

    @typing.overload
    def isAppliable(self, column: typing.Union[jpype.JInt, int]) -> bool:
        """
        Returns true if the specific information represented by the given column index is something
        can be applied whether or not it is currently applied. This is used by the renderer to
        render this columns test normally (not faded or bold)
        
        :param jpype.JInt or int column: the column index to check if it is appliable
        :return: true if this columns information is changeable
        :rtype: bool
        """

    def isApplied(self, column: typing.Union[jpype.JInt, int]) -> bool:
        """
        Returns true if the specific information represented by the given column index is applied.
        This is used by the renderer to bold information that is applied and fade information
        that is not applied.
        
        :param jpype.JInt or int column: the column index to check if it is applied
        :return: true if this column information is currently applied
        :rtype: bool
        """

    def isBlank(self) -> bool:
        """
        Returns if this item represent a blank line. Useful for removing blank lines from the
        merge structure view.
        
        :return: true if this item represents a blank line
        :rtype: bool
        """

    def isLeftJustified(self, column: typing.Union[jpype.JInt, int]) -> bool:
        """
        Specifies if the column text should be left or right justified within it column.
        
        :param jpype.JInt or int column: the column index
        :return: true if the column text should be justified to the left side of the column
        :rtype: bool
        """

    @property
    def leftJustified(self) -> jpype.JBoolean:
        ...

    @property
    def blank(self) -> jpype.JBoolean:
        ...

    @property
    def columnText(self) -> java.lang.String:
        ...

    @property
    def appliable(self) -> jpype.JBoolean:
        ...

    @property
    def applied(self) -> jpype.JBoolean:
        ...

    @property
    def line(self) -> jpype.JInt:
        ...

    @property
    def minWidth(self) -> jpype.JInt:
        ...


class ComparisonItemLayout(java.awt.LayoutManager):
    """
    LayoutManager for arranging the labels for each column in a :obj:`ComparisonItem`.
    The main idea here is that each type of item has a set of min/max widths associated with
    each column that is used to align like types of items so that their fields line up.
     
    The tricky part is how to handle sizing them as the view is expanded or contracted.
    Initially, all columns are given their minimum width and if the total is greater then the 
    available width, the last columns are clipped. If the available width is greater than the
    sum of the minimum widths, the extra width (10 at a time) is given to each column that still has
    text wider than its current width. This is repeated until the extra width is used up or all 
    columns have all the width they need to display their text.
    """

    @typing.type_check_only
    class ColumnWidths(java.lang.Object):
        ...
        class_: typing.ClassVar[java.lang.Class]


    class_: typing.ClassVar[java.lang.Class]

    def __init__(self) -> None:
        ...

    def setColumnWidths(self, widths: ComparisonItemLayout.ColumnWidths) -> None:
        ...


class ComparisonItemRenderer(javax.swing.ListCellRenderer[ComparisonItem], javax.swing.event.ListDataListener):
    """
    ListCellRenderer for rendering structure lines in :obj:`CoordinatedStructureDisplay`. It 
    consists of a label for each possible column. The labels are arranged by a 
    :obj:`ComparisonItemLayout` which is fed column widths for each type of line item. The 
    columns widths for each type are computed when the renderer is constructed by examining all
    the lines in the model and computing the min/max column widths for that type.
    """

    class_: typing.ClassVar[java.lang.Class]

    def getFontMetrics(self) -> java.awt.FontMetrics:
        ...

    def getPreferredHeight(self) -> int:
        ...

    @property
    def fontMetrics(self) -> java.awt.FontMetrics:
        ...

    @property
    def preferredHeight(self) -> jpype.JInt:
        ...


class CoordinatedStructureDisplay(javax.swing.JPanel):
    """
    Class for displaying a view into a :obj:`CoordinatedStructureModel`, showing either the
    left structure, the right structure, or the merged structure. It consists of a JList in
    a JScrollpane where the list model is extracted from the :obj:`CoordinatedStructureModel` for
    either the left,right, or merged view. These views track together for both view scrolling and
    list selection. They all share a :obj:`DisplayCoordinator` that assists with coordinating the
    views.
    """

    class_: typing.ClassVar[java.lang.Class]
    MARGIN: typing.Final = 10

    def __init__(self, title: typing.Union[java.lang.String, str], listModel: StructDisplayModel, coordinator: DisplayCoordinator) -> None:
        ...


class CoordinatedStructureLine(java.lang.Object):
    """
    Base class for coordinating display lines of a left, right, and merged structure.
    """

    class CompareId(java.lang.Enum[CoordinatedStructureLine.CompareId]):

        class_: typing.ClassVar[java.lang.Class]
        LEFT: typing.Final[CoordinatedStructureLine.CompareId]
        RIGHT: typing.Final[CoordinatedStructureLine.CompareId]
        MERGED: typing.Final[CoordinatedStructureLine.CompareId]

        @staticmethod
        def valueOf(name: typing.Union[java.lang.String, str]) -> CoordinatedStructureLine.CompareId:
            ...

        @staticmethod
        def values() -> jpype.JArray[CoordinatedStructureLine.CompareId]:
            ...


    class_: typing.ClassVar[java.lang.Class]


class CoordinatedStructureModel(java.lang.Object):
    """
    Model for merging two structures in an interactive dialog. The first structure will be considered
    the left structure (it will be displayed on the left side) and the second structure will be
    considered the right structure. This class will internally generate a merged structure by 
    combining the two given structures. Initially, if there is a conflict, the first structure (left)
    will be given precedence.
    """

    @typing.type_check_only
    class LineBuilder(java.lang.Object):
        """
        Inner class to build the coordinated component lines (the hard part) of the three structures.
        """

        class_: typing.ClassVar[java.lang.Class]


    @typing.type_check_only
    class DefinedComponentQueue(java.lang.Object):

        class_: typing.ClassVar[java.lang.Class]

        def hasBitField(self, offset: typing.Union[jpype.JInt, int]) -> bool:
            ...

        def hasNext(self) -> bool:
            ...

        def hasZeroComp(self, offset: typing.Union[jpype.JInt, int]) -> bool:
            ...

        def next(self) -> ghidra.program.model.data.DataTypeComponent:
            ...

        def nextOffset(self) -> int:
            ...

        def peek(self) -> ghidra.program.model.data.DataTypeComponent:
            ...


    class_: typing.ClassVar[java.lang.Class]

    def __init__(self, struct1: ghidra.program.model.data.Structure, struct2: ghidra.program.model.data.Structure, errorHandler: java.util.function.Consumer[java.lang.String]) -> None:
        """
        Constructor
        
        :param ghidra.program.model.data.Structure struct1: the left structure (has initial precedence for conflicts)
        :param ghidra.program.model.data.Structure struct2: the right structure
        :param java.util.function.Consumer[java.lang.String] errorHandler: a consumer for reporting errors
        """

    def addChangeListener(self, callback: utility.function.Callback) -> None:
        ...

    def getData(self, compareId: CoordinatedStructureLine.CompareId) -> java.util.List[ComparisonItem]:
        ...

    def getLine(self, line: typing.Union[jpype.JInt, int]) -> CoordinatedStructureLine:
        ...

    def getLines(self) -> java.util.List[CoordinatedStructureLine]:
        ...

    def getMergedStructure(self) -> ghidra.program.model.data.Structure:
        ...

    def getSize(self) -> int:
        ...

    @property
    def size(self) -> jpype.JInt:
        ...

    @property
    def data(self) -> java.util.List[ComparisonItem]:
        ...

    @property
    def line(self) -> CoordinatedStructureLine:
        ...

    @property
    def lines(self) -> java.util.List[CoordinatedStructureLine]:
        ...

    @property
    def mergedStructure(self) -> ghidra.program.model.data.Structure:
        ...


@typing.type_check_only
class DisplayCoordinator(java.lang.Object):
    """
    Class for coordinating the scrolling and line selection of the three structure display.
    """

    class_: typing.ClassVar[java.lang.Class]


@typing.type_check_only
class StructDisplayModel(javax.swing.AbstractListModel[ComparisonItem]):
    """
    The :obj:`ListModel` model for one of the three structure displays.
    """

    class_: typing.ClassVar[java.lang.Class]


class StructureComponentLine(CoordinatedStructureLine):
    """
    :obj:`CoordinatedStructureLine` for showing structure components.
    """

    @typing.type_check_only
    class StructureComponentItem(ComparisonItem):
        """
        Class for the individual :obj:`ComparisonItem`s for each of the structures.
        """

        class_: typing.ClassVar[java.lang.Class]


    class_: typing.ClassVar[java.lang.Class]
    COMPONENT_INDENT: typing.Final = 5
    OFFSET_SIZE: typing.Final = 10
    MIN_DT_SIZE: typing.Final = 100
    MIN_NAME_SIZE: typing.Final = 10
    MIN_COMMENT_SIZE: typing.Final = 10


class StructureDescriptionLine(CoordinatedStructureLine):
    """
    :obj:`CoordinatedStructureLine` for showing structure description (its comment).
    """

    @typing.type_check_only
    class DescriptionItem(ComparisonItem):
        """
        Class for the individual :obj:`ComparisonItem`s for each of the structures.
        """

        class_: typing.ClassVar[java.lang.Class]


    class_: typing.ClassVar[java.lang.Class]

    def __init__(self, model: CoordinatedStructureModel, leftStruct: ghidra.program.model.data.Structure, rightStruct: ghidra.program.model.data.Structure, mergedStruct: ghidra.program.model.data.Structure, line: typing.Union[jpype.JInt, int]) -> None:
        """
        Constructor
        
        :param CoordinatedStructureModel model: the :obj:`CoordinatedStructureModel`
        :param ghidra.program.model.data.Structure leftStruct: the left structure
        :param ghidra.program.model.data.Structure rightStruct: the right structure
        :param ghidra.program.model.data.Structure mergedStruct: the merged structure
        :param jpype.JInt or int line: the line number where this component will be shown in the overall list of 
        line items (including name, description, info, etc.)
        """


class StructureInfoLine(CoordinatedStructureLine):
    """
    :obj:`CoordinatedStructureLine` for showing invariant structure information. This includes
    syntax ("{" and "}") and structure details (size, alignment, packing).
    """

    @typing.type_check_only
    class InfoItem(ComparisonItem):
        """
        Class for the individual :obj:`ComparisonItem`s for each of the structures.
        """

        class_: typing.ClassVar[java.lang.Class]


    class_: typing.ClassVar[java.lang.Class]

    @typing.overload
    def __init__(self, model: CoordinatedStructureModel, left: typing.Union[java.lang.String, str], right: typing.Union[java.lang.String, str], merged: typing.Union[java.lang.String, str], line: typing.Union[jpype.JInt, int], type: typing.Union[java.lang.String, str]) -> None:
        """
        Constructor
        
        :param CoordinatedStructureModel model: the :obj:`CoordinatedStructureModel`
        :param java.lang.String or str left: the string to be displayed in the left display
        :param java.lang.String or str right: the string to be displayed in the right display
        :param java.lang.String or str merged: the string to be displayed in the merged display
        :param jpype.JInt or int line: the line number of this line in the overall display
        :param java.lang.String or str type: the type of info ("Syntax", or "Structure details")
        """

    @typing.overload
    def __init__(self, model: CoordinatedStructureModel, all: typing.Union[java.lang.String, str], line: typing.Union[jpype.JInt, int], type: typing.Union[java.lang.String, str]) -> None:
        """
        Constructor
        
        :param CoordinatedStructureModel model: the :obj:`CoordinatedStructureModel`
        :param java.lang.String or str all: the string to be displayed in all displays
        :param jpype.JInt or int line: the line number of this line in the overall display
        :param java.lang.String or str type: the type of info ("Syntax", or "Structure details")
        """


class StructureMergeDialog(docking.DialogComponentProvider):
    """
    Dialog for merging structures. The dialog is constructed given two structures and it will 
    merge them, producing a third merged structure. The dialog will then display all three
    structures and provide controls for dealing with conflicts, allowing the user to choose
    components from the left or right side structures.
     
    
    The dialog itself doesn't do anything with the resulting merged structure. Clients need
    to provide an apply consumer that will be called when the user presses the dialog's apply
    button.
     
    
    The dialog also provides the following actions as keyboard only actions:
     
    1. Apply Item (<SPACE>): pressing the space bar key will apply the currently focussed and
    selected item from either the left side or right sided. (Assuming it is applicable).
    2. Focus Left Side (<LEFT ARROW>): pressing the left arrow will give focus to the left side
    display.
    3. Focus Right Side (<RIGHT ARROW>): pressing the right arrow will give focus to the right side
    display.
    """

    @typing.type_check_only
    class StructureMergeDialogFocusTraveralPolicy(java.awt.FocusTraversalPolicy):
        """
        Customized focus traversal policy to avoid traversing to any of the apply buttons. The
        focus will go as follows: left display, right display, merged display, apply button, and
        finally cancel button.
        """

        class_: typing.ClassVar[java.lang.Class]


    @typing.type_check_only
    class LeftRightButtonPanel(javax.swing.JPanel):

        class_: typing.ClassVar[java.lang.Class]

        def buildButtons(self, firstIndex: typing.Union[jpype.JInt, int], lastIndex: typing.Union[jpype.JInt, int]) -> None:
            ...


    @typing.type_check_only
    class StructureMergeDialogContext(docking.DefaultActionContext):

        class_: typing.ClassVar[java.lang.Class]

        def __init__(self, dialog: docking.DialogComponentProvider, source: java.awt.Component, display: CoordinatedStructureDisplay) -> None:
            ...

        def getComparisonItem(self) -> ComparisonItem:
            ...

        @property
        def comparisonItem(self) -> ComparisonItem:
            ...


    class_: typing.ClassVar[java.lang.Class]

    def __init__(self, title: typing.Union[java.lang.String, str], struct1: ghidra.program.model.data.Structure, struct2: ghidra.program.model.data.Structure, applyConsumer: utility.function.ExceptionalConsumer[ghidra.program.model.data.Structure, java.lang.Exception]) -> None:
        """
        Constructor
        
        :param java.lang.String or str title: the dialog title.
        :param ghidra.program.model.data.Structure struct1: the first structure (will receive precedence for any conflicting components
        :param ghidra.program.model.data.Structure struct2: the second structure
        :param utility.function.ExceptionalConsumer[ghidra.program.model.data.Structure, java.lang.Exception] applyConsumer: the consumer to call when the user presses the apply button. This
        consumer can throw an exception which will be displayed in the dialog and the dialog won't
        close. If the apply does not throw an exception, the dialog will be closed.
        """


class StructureNameLine(CoordinatedStructureLine):
    """
    :obj:`CoordinatedStructureLine` for showing the structure's name.
    """

    @typing.type_check_only
    class NameItem(ComparisonItem):
        """
        Class for the individual :obj:`ComparisonItem`s for each of the structures.
        """

        class_: typing.ClassVar[java.lang.Class]


    class_: typing.ClassVar[java.lang.Class]

    def __init__(self, model: CoordinatedStructureModel, leftStruct: ghidra.program.model.data.Structure, rightStruct: ghidra.program.model.data.Structure, mergedStruct: ghidra.program.model.data.Structure, line: typing.Union[jpype.JInt, int]) -> None:
        """
        Constructor
        
        :param CoordinatedStructureModel model: the :obj:`CoordinatedStructureModel`
        :param ghidra.program.model.data.Structure leftStruct: the left structure
        :param ghidra.program.model.data.Structure rightStruct: the right structure
        :param ghidra.program.model.data.Structure mergedStruct: the merged structure
        :param jpype.JInt or int line: the line number where this component will be shown in the overall list of 
        line items (including name, description, info, etc.)
        """



__all__ = ["ComparisonItem", "ComparisonItemLayout", "ComparisonItemRenderer", "CoordinatedStructureDisplay", "CoordinatedStructureLine", "CoordinatedStructureModel", "DisplayCoordinator", "StructDisplayModel", "StructureComponentLine", "StructureDescriptionLine", "StructureInfoLine", "StructureMergeDialog", "StructureNameLine"]
