from __future__ import annotations
import collections.abc
import datetime
import typing
from warnings import deprecated # type: ignore

import jpype # type: ignore
import jpype.protocol # type: ignore

import docking.widgets.table
import docking.widgets.table.threaded
import ghidra.util.table.column
import java.io # type: ignore
import java.lang # type: ignore
import java.util # type: ignore
import java.util.function # type: ignore
import javax.swing # type: ignore
import javax.swing.border # type: ignore


T = typing.TypeVar("T")


class GTreeTable(javax.swing.JPanel, typing.Generic[T]):

    class_: typing.ClassVar[java.lang.Class]

    def __init__(self, model: GTreeTableModel[T]) -> None:
        ...

    def getFilterPanel(self) -> docking.widgets.table.GTableFilterPanel[T]:
        """
        Get the filter panel of this table
        
        :return: The filter panel
        :rtype: docking.widgets.table.GTableFilterPanel[T]
        """

    def getTable(self) -> docking.widgets.table.GTable:
        """
        Get the GTable of this GTreeTable
        
        :return: The table
        :rtype: docking.widgets.table.GTable
        """

    def getTableModel(self) -> GTreeTableModel[T]:
        """
        Get the model tied to this GTreeTable
        
        :return: The model
        :rtype: GTreeTableModel[T]
        """

    @property
    def filterPanel(self) -> docking.widgets.table.GTableFilterPanel[T]:
        ...

    @property
    def tableModel(self) -> GTreeTableModel[T]:
        ...

    @property
    def table(self) -> docking.widgets.table.GTable:
        ...


class GTreeTableCellRenderer(docking.widgets.table.GTableCellRenderer, ghidra.util.table.column.GColumnRenderer[T], typing.Generic[T]):

    @typing.type_check_only
    class ExpandCollapseBorder(javax.swing.border.Border):
        ...
        class_: typing.ClassVar[java.lang.Class]


    class_: typing.ClassVar[java.lang.Class]

    def __init__(self) -> None:
        ...

    def inExpandIcon(self, node: GTreeTableNode, x: typing.Union[jpype.JInt, int]) -> bool:
        """
        Check if x position is in the expand icon space
        
        :param GTreeTableNode node: Node to determine how indented the expand icon is
        :param jpype.JInt or int x: X coordinate to check against
        :return: true/false if X coordinate is in expand icon space
        :rtype: bool
        """


class GTreeTableModel(docking.widgets.table.threaded.ThreadedTableModelStub[T], typing.Generic[T]):

    @typing.type_check_only
    class TreeColumn(docking.widgets.table.AbstractDynamicTableColumnStub[T, GTreeTableNode]):

        class_: typing.ClassVar[java.lang.Class]

        def __init__(self, columnName: typing.Union[java.lang.String, str]) -> None:
            ...


    class_: typing.ClassVar[java.lang.Class]

    def __init__(self, rootNode: GTreeTableNode) -> None:
        ...

    def setRootNode(self, node: GTreeTableNode) -> None:
        """
        Set the root node of this model
        
        :param GTreeTableNode node: Root node to set
        """


class GTreeTableNode(java.io.Serializable):

    @typing.type_check_only
    class EachAncestorIterator(java.util.Iterator[GTreeTableNode]):
        ...
        class_: typing.ClassVar[java.lang.Class]


    @typing.type_check_only
    class EachDecendantIterator(java.util.Iterator[GTreeTableNode]):
        ...
        class_: typing.ClassVar[java.lang.Class]


    @typing.type_check_only
    class EachDecendantDFSIterator(java.util.Iterator[GTreeTableNode]):
        ...
        class_: typing.ClassVar[java.lang.Class]


    @typing.type_check_only
    class EachExpandedIterator(java.util.Iterator[GTreeTableNode]):
        ...
        class_: typing.ClassVar[java.lang.Class]


    class_: typing.ClassVar[java.lang.Class]

    def __init__(self, name: typing.Union[java.lang.String, str]) -> None:
        ...

    def add(self, newChild: GTreeTableNode) -> None:
        """
        Add new child to this node's children
        
        :param GTreeTableNode newChild: New child to add
        """

    def ancestors(self) -> java.lang.Iterable[GTreeTableNode]:
        """
        Get an iterable of all the ancestors of this node
        
        :return: An iterable of ancestors
        :rtype: java.lang.Iterable[GTreeTableNode]
        """

    def depthFirstSearchList(self) -> java.util.List[GTreeTableNode]:
        """
        Get a list of all descendants of this node in depth first search order
        
        :return: List of descendants in DFS order
        :rtype: java.util.List[GTreeTableNode]
        """

    def descendants(self) -> java.lang.Iterable[GTreeTableNode]:
        """
        Get an iterable of all the descendants of this node
        
        :return: An iterable of descendants
        :rtype: java.lang.Iterable[GTreeTableNode]
        """

    def descendantsDFS(self) -> java.lang.Iterable[GTreeTableNode]:
        """
        Get an iterable of all the descendants of this node in DFS order
        
        :return: An iterable of descendants
        :rtype: java.lang.Iterable[GTreeTableNode]
        """

    def expandedDescendants(self) -> java.lang.Iterable[GTreeTableNode]:
        """
        Get an iterable of all the expanded descendants of this node
        
        :return: An iterable of expanded descendants
        :rtype: java.lang.Iterable[GTreeTableNode]
        """

    def find(self, condition: java.util.function.Predicate[GTreeTableNode]) -> java.util.List[GTreeTableNode]:
        """
        Find nodes in descendants that match a certain condition
        
        :param java.util.function.Predicate[GTreeTableNode] condition: Predicate to match nodes on
        :return: List of nodes matching the condition
        :rtype: java.util.List[GTreeTableNode]
        """

    def forEachAncestor(self, action: java.util.function.Consumer[GTreeTableNode]) -> None:
        """
        Perform an action on each ancestor of this node
        
        :param java.util.function.Consumer[GTreeTableNode] action: To perform on each ancestor
        """

    def forEachDescendant(self, action: java.util.function.Consumer[GTreeTableNode]) -> None:
        """
        Perform an action on each descendant of this node
        
        :param java.util.function.Consumer[GTreeTableNode] action: To perform on each descendant
        """

    def forEachDescendantDFS(self, action: java.util.function.Consumer[GTreeTableNode]) -> None:
        """
        Perform an action on each descendant of this node in DFS order
        
        :param java.util.function.Consumer[GTreeTableNode] action: To perform on each descendant
        """

    def forEachExpanded(self, action: java.util.function.Consumer[GTreeTableNode]) -> None:
        """
        Perform an action on each expanded descendant of this node
        
        :param java.util.function.Consumer[GTreeTableNode] action: To perform on each expanded descendant
        """

    def getChildCount(self) -> int:
        """
        Get number of children
        
        :return: Number of children
        :rtype: int
        """

    def getChildren(self) -> java.util.List[GTreeTableNode]:
        """
        Get list of children
        
        :return: List of children
        :rtype: java.util.List[GTreeTableNode]
        """

    def getExpanded(self) -> java.util.List[GTreeTableNode]:
        """
        Get list of descendants who are expanded
        
        :return: List of expanded descendants
        :rtype: java.util.List[GTreeTableNode]
        """

    def getIcon(self) -> javax.swing.Icon:
        """
        Get icon
        
        :return: icon
        :rtype: javax.swing.Icon
        """

    def getLevel(self) -> int:
        """
        Get tree depth from the root node
        
        :return: Level from root node
        :rtype: int
        """

    def getName(self) -> str:
        """
        Get name of node
        
        :return: name
        :rtype: str
        """

    def getParent(self) -> GTreeTableNode:
        """
        Get parent of node
        
        :return: parent
        :rtype: GTreeTableNode
        """

    def getPath(self) -> java.util.List[GTreeTableNode]:
        """
        Get list of ancestors in order leading to this node
        
        :return: List of nodes leading to this one
        :rtype: java.util.List[GTreeTableNode]
        """

    def getRoot(self) -> GTreeTableNode:
        """
        Get root node
        
        :return: root node
        :rtype: GTreeTableNode
        """

    def getTreeData(self) -> str:
        """
        Get data associated with this node
        
        :return: data
        :rtype: str
        """

    def hasChildren(self) -> bool:
        """
        Check if node has children
        
        :return: true/false if node has children
        :rtype: bool
        """

    def hasNodeInItsAncestry(self, anotherNode: GTreeTableNode) -> bool:
        """
        Check if another node is in this node's ancestry, the current node will return true as
        being in its own ancestry
        
        :param GTreeTableNode anotherNode: Node to check for in the current nodes ancestry
        :return: true/false if other node is in the ancestry
        :rtype: bool
        """

    def hasVisibleChildren(self) -> bool:
        """
        Check if this node has any visible children
        
        :return: true/false if any children are visible
        :rtype: bool
        """

    def insert(self, newChild: GTreeTableNode, childIndex: typing.Union[jpype.JInt, int]) -> None:
        """
        Insert a new node into the children of this node
        
        :param GTreeTableNode newChild: New child to insert
        :param jpype.JInt or int childIndex: Index to insert child at
        """

    def isExpanded(self) -> bool:
        """
        Check if node is expanded
        
        :return: true/false if expanded
        :rtype: bool
        """

    def isLeaf(self) -> bool:
        """
        Check if node is leaf node
        
        :return: true/false if leaf
        :rtype: bool
        """

    def isRoot(self) -> bool:
        """
        Check if node is root node (i.e. it has no parent)
        
        :return: true/false if root
        :rtype: bool
        """

    def isVisible(self) -> bool:
        """
        
        
        :return: 
        :rtype: bool
        """

    @typing.overload
    def remove(self, aChild: GTreeTableNode) -> None:
        """
        Remove child from list of children
        
        :param GTreeTableNode aChild: Child to remove
        """

    @typing.overload
    def remove(self, childIndex: typing.Union[jpype.JInt, int]) -> None:
        """
        Remove child from list of children
        
        :param jpype.JInt or int childIndex: Index of child to remove
        """

    def setExpanded(self, expanded: typing.Union[jpype.JBoolean, bool]) -> None:
        """
        Change node expanded state
        
        :param jpype.JBoolean or bool expanded: Expanded state
        """

    def setParent(self, newParent: GTreeTableNode) -> None:
        """
        Set parent of node
        
        :param GTreeTableNode newParent: Parent to set
        """

    def setVisible(self, visible: typing.Union[jpype.JBoolean, bool]) -> None:
        """
        Change node visibility state
        
        :param jpype.JBoolean or bool visible: Node visibility
        """

    @property
    def path(self) -> java.util.List[GTreeTableNode]:
        ...

    @property
    def parent(self) -> GTreeTableNode:
        ...

    @parent.setter
    def parent(self, value: GTreeTableNode):
        ...

    @property
    def expanded(self) -> java.util.List[GTreeTableNode]:
        ...

    @property
    def visible(self) -> jpype.JBoolean:
        ...

    @visible.setter
    def visible(self, value: jpype.JBoolean):
        ...

    @property
    def level(self) -> jpype.JInt:
        ...

    @property
    def children(self) -> java.util.List[GTreeTableNode]:
        ...

    @property
    def root(self) -> GTreeTableNode:
        ...

    @property
    def name(self) -> java.lang.String:
        ...

    @property
    def icon(self) -> javax.swing.Icon:
        ...

    @property
    def childCount(self) -> jpype.JInt:
        ...

    @property
    def leaf(self) -> jpype.JBoolean:
        ...

    @property
    def treeData(self) -> java.lang.String:
        ...



__all__ = ["GTreeTable", "GTreeTableCellRenderer", "GTreeTableModel", "GTreeTableNode"]
