from __future__ import annotations
import collections.abc
import datetime
import typing
from warnings import deprecated # type: ignore

import jpype # type: ignore
import jpype.protocol # type: ignore

import java.awt.event # type: ignore
import java.lang # type: ignore
import java.math # type: ignore
import java.util # type: ignore
import java.util.function # type: ignore
import javax.swing # type: ignore
import javax.swing.event # type: ignore
import javax.swing.text # type: ignore
import utility.function


class AbstractIntegerTextField(java.lang.Object):
    """
    Base class for IntegerTextFields that allow entering integer values based on some 
    integer format (i.e., hex, decimal, unsigned hex, binary, etc.). This field does input
    validation, so only valid text for the current format can be typed.
    """

    @typing.type_check_only
    class HexDecimalDocumentFilter(javax.swing.text.DocumentFilter):
        """
        DocumentFilter that prevents users from entering invalid data into the field.
        """

        class_: typing.ClassVar[java.lang.Class]


    class_: typing.ClassVar[java.lang.Class]

    def __init__(self, columns: typing.Union[jpype.JInt, int], initialValue: java.math.BigInteger, *formats: IntegerFormat) -> None:
        """
        Creates a new IntegerTextField with the specified number of columns and initial value
        
        :param jpype.JInt or int columns: the number of columns
        :param java.math.BigInteger initialValue: the initial value
        :param jpype.JArray[IntegerFormat] formats: the supported InputNumberModes
        """

    def addActionListener(self, listener: java.awt.event.ActionListener) -> None:
        """
        Adds an ActionListener to the TextField.
        
        :param java.awt.event.ActionListener listener: the ActionListener to add.
        """

    def addChangeListener(self, listener: javax.swing.event.ChangeListener) -> None:
        """
        Adds a change listener that will be notified whenever the value changes.
        
        :param javax.swing.event.ChangeListener listener: the change listener to add.
        """

    def getAllFormats(self) -> java.util.List[IntegerFormat]:
        """
        Returns a list of all support :obj:`IntegerFormat`s supported by this field.
        
        :return: a list of all support number formats for this field.
        :rtype: java.util.List[IntegerFormat]
        """

    def getComponent(self) -> javax.swing.JComponent:
        """
        Returns the JTextField component that this class manages.
        
        :return: the JTextField component that this class manages.
        :rtype: javax.swing.JComponent
        """

    def getFormat(self) -> IntegerFormat:
        """
        :return: the current format for entering numbers into this field
        :rtype: IntegerFormat
        """

    def getIntValue(self) -> int:
        """
        Returns the current value as an int.
        
         
        
        If the field has no current value, 0 will be returned. If the value is bigger (or smaller)
        than an int, it will be cast to an int.
        
         
        
        If using this method, it is highly recommended that you set the max value to
        :obj:`Integer.MAX_VALUE` or lower.
        
        :return: the current value as an int. Or 0 if there is no value
        :rtype: int
        :raises ArithmeticException: if the value in this field will not fit into an int
        """

    def getLongValue(self) -> int:
        """
        Returns the current value as a long.
        
         
        
        If the field has no current value, 0 will be returned. If the value is bigger (or smaller)
        than an long, it will be cast to a long.
        
         
        
        If using this method, it is highly recommended that you set the max value to
        :obj:`Long.MAX_VALUE` or lower.
        
        :return: the current value as a long. Or 0 if there is no value
        :rtype: int
        :raises ArithmeticException: if the value in this field will not fit into a long
        """

    def getMaxValue(self) -> java.math.BigInteger:
        """
        Returns the current maximum allowed value. Null indicates that there is no maximum value.
        
        :return: the current maximum value allowed.
        :rtype: java.math.BigInteger
        """

    def getMinValue(self) -> java.math.BigInteger:
        """
        Returns the current minimum allowed value. Null indicates that there is no minimum value.
        
        :return: the current maximum value allowed.
        :rtype: java.math.BigInteger
        """

    def getText(self) -> str:
        """
        Returns the current text displayed in the field.
        
        :return: the current text displayed in the field.
        :rtype: str
        """

    def getValue(self) -> java.math.BigInteger:
        """
        Returns the current value of the field or null if the field has no current value.
        
        :return: the current value of the field or null if the field has no current value.
        :rtype: java.math.BigInteger
        """

    def removeActionListener(self, listener: java.awt.event.ActionListener) -> None:
        """
        Removes an ActionListener from the TextField.
        
        :param java.awt.event.ActionListener listener: the ActionListener to remove.
        """

    def removeChangeListener(self, listener: javax.swing.event.ChangeListener) -> None:
        """
        Removes the changes listener.
        
        :param javax.swing.event.ChangeListener listener: the listener to be removed.
        """

    def requestFocus(self) -> None:
        """
        Requests focus to the JTextField
        """

    def selectAll(self) -> None:
        """
        Selects the text in the JTextField
        """

    def setAccessibleName(self, name: typing.Union[java.lang.String, str]) -> None:
        """
        Sets the accessible name for the component of this input field.
        
        :param java.lang.String or str name: the accessible name for this field
        """

    def setEditable(self, editable: typing.Union[jpype.JBoolean, bool]) -> None:
        """
        Sets the editable mode for the JTextField component
        
        :param jpype.JBoolean or bool editable: boolean flag, if true component is editable
        """

    def setEnabled(self, enabled: typing.Union[jpype.JBoolean, bool]) -> None:
        """
        Sets the enablement on the JTextField component;
        
        :param jpype.JBoolean or bool enabled: true for enabled, false for disabled.
        """

    def setFormat(self, format: IntegerFormat) -> None:
        """
        Sets the format for entering an integer into this field. The current text in the field
        will change to keep the same numeric value, but in the new input format.
        
        :param IntegerFormat format: the format for entering an integer into the field.
        """

    def setHorizontalAlignment(self, alignment: typing.Union[jpype.JInt, int]) -> None:
        """
        Sets the horizontal alignment of the JTextField
        
        :param jpype.JInt or int alignment: the alignment as in :meth:`JTextField.setHorizontalAlignment(int) <JTextField.setHorizontalAlignment>`
        """

    def setShowNumberMode(self, show: typing.Union[jpype.JBoolean, bool]) -> None:
        """
        Turns on or off the faded text that displays the field's radix mode (hex or decimal).
        
        :param jpype.JBoolean or bool show: true to show the radix mode.
        """

    def setText(self, text: typing.Union[java.lang.String, str]) -> bool:
        """
        Sets the field to the given text. The text must be a properly formated string that is a valid
        value for this field. If the field is set to not allow "0x" prefixes, then the input
        string cannot start with 0x and furthermore, if the field is in decimal mode, then input
        string cannot take in hex digits a-f. On the other hand, if "0x" prefixes are allowed, then
        the input string can be either a decimal number or a hex number depending on if the input
        string starts with "0x". In this case, the field's hex mode will be set to match the input
        text. If the text is not valid, the field will not change.
        
        :param java.lang.String or str text: the value as text to set on this field
        :return: true if the set was successful
        :rtype: bool
        """

    def setUseNumberPrefix(self, usePrefix: typing.Union[jpype.JBoolean, bool]) -> None:
        """
        Sets whether or not that non-decimal formats require using a prefix (i.e., "0x" for hex).
        Generally, using a prefix is preferred as it allows the mode to auto-switch as the user
        types (or not types) a prefix. If the prefix is not used, the only way to change input
        formats is to use the built-in cntr-M action.
        
        :param jpype.JBoolean or bool usePrefix: true to require a prefix, false to not require a prefix
        """

    @typing.overload
    def setValue(self, newValue: typing.Union[jpype.JLong, int]) -> None:
        """
        Convenience method for setting the value to a long value;
        
        :param jpype.JLong or int newValue: the new value for the field.
        """

    @typing.overload
    def setValue(self, newValue: typing.Union[jpype.JInt, int]) -> None:
        """
        Convenience method for setting the value to an int value;
        
        :param jpype.JInt or int newValue: the new value for the field.
        """

    @typing.overload
    def setValue(self, newValue: java.math.BigInteger) -> None:
        """
        Sets the value of the field to the given value. A null value will clear the field.
        
        :param java.math.BigInteger newValue: the new value or null.
        """

    @property
    def maxValue(self) -> java.math.BigInteger:
        ...

    @property
    def intValue(self) -> jpype.JInt:
        ...

    @property
    def format(self) -> IntegerFormat:
        ...

    @format.setter
    def format(self, value: IntegerFormat):
        ...

    @property
    def longValue(self) -> jpype.JLong:
        ...

    @property
    def minValue(self) -> java.math.BigInteger:
        ...

    @property
    def component(self) -> javax.swing.JComponent:
        ...

    @property
    def allFormats(self) -> java.util.List[IntegerFormat]:
        ...

    @property
    def text(self) -> java.lang.String:
        ...

    @property
    def value(self) -> java.math.BigInteger:
        ...

    @value.setter
    def value(self, value: java.math.BigInteger):
        ...


class IntegerFormat(java.lang.Enum[IntegerFormat]):
    """
    Input formats for entering integers into a text field such as the :obj:`IntegerTextField` or
    :obj:`FixedSizeIntegerTextField`
    """

    class_: typing.ClassVar[java.lang.Class]
    DEC: typing.Final[IntegerFormat]
    HEX: typing.Final[IntegerFormat]
    OCT: typing.Final[IntegerFormat]
    BIN: typing.Final[IntegerFormat]
    U_DEC: typing.Final[IntegerFormat]
    U_HEX: typing.Final[IntegerFormat]
    U_OCT: typing.Final[IntegerFormat]
    U_BIN: typing.Final[IntegerFormat]

    def format(self, value: java.math.BigInteger) -> str:
        """
        Converts the given value into a string representation corresponding to this number format.
        
        :param java.math.BigInteger value: the value to format into a string
        :return: A string representation of the given value.
        :rtype: str
        """

    def getDescription(self) -> str:
        """
        :return: a descriptive name of this number format
        :rtype: str
        """

    def getName(self) -> str:
        """
        :return: the short name of this number format
        :rtype: str
        """

    def getPrefix(self) -> str:
        """
        :return: the prefix associated with this format
        :rtype: str
        """

    def isUnsigned(self) -> bool:
        """
        Return true if this format is intended only for non-negative values. This is more of a hint
        to the client text field to determine if "-" characters are allowed to be entered.
        
        :return: true if this format is for unsigned numbers
        :rtype: bool
        """

    def parse(self, text: typing.Union[java.lang.String, str]) -> java.math.BigInteger:
        """
        Parses the given string into a BigInteger or null if the string is not properly structured
        for this number format.
        
        :param java.lang.String or str text: the text to parse into a BigInteger
        :return: the BigInteger interpretation of the given string for this number format.
        :rtype: java.math.BigInteger
        """

    @staticmethod
    def valueOf(name: typing.Union[java.lang.String, str]) -> IntegerFormat:
        ...

    @staticmethod
    def values() -> jpype.JArray[IntegerFormat]:
        ...

    @property
    def prefix(self) -> java.lang.String:
        ...

    @property
    def name(self) -> java.lang.String:
        ...

    @property
    def unsigned(self) -> jpype.JBoolean:
        ...

    @property
    def description(self) -> java.lang.String:
        ...


class MultiFormatTextField(javax.swing.JTextField):
    """
    Overrides the JTextField mainly to allow hint painting for the current input format. It also
    handles processing control-M to switch modes.
    """

    class_: typing.ClassVar[java.lang.Class]

    def __init__(self, columns: typing.Union[jpype.JInt, int], formats: java.util.List[IntegerFormat], formatChangeConsumer: java.util.function.Consumer[IntegerFormat]) -> None:
        ...

    def addTextChangedCallback(self, c: utility.function.Callback) -> None:
        """
        Uses the given callback to notify the client when the text has changed in this text field.
        
        :param utility.function.Callback c: the callback to be notified when the text changes in this field
        """

    def setFormat(self, format: IntegerFormat) -> None:
        """
        Sets the :obj:`IntegerFormat` that will be used to format and parse the text in this
        field.
        
        :param IntegerFormat format: the number format that will be used to format and parse the text in this field
        """

    def setShowInputFormatHint(self, show: typing.Union[jpype.JBoolean, bool]) -> None:
        """
        Turns on or off the faded hint text that displays the field's current format (i.e., hex,
        decimal).
        
        :param jpype.JBoolean or bool show: true to show the input format.
        """



__all__ = ["AbstractIntegerTextField", "IntegerFormat", "MultiFormatTextField"]
