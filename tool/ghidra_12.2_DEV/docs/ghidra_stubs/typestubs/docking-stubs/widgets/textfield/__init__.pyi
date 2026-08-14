from __future__ import annotations
import collections.abc
import datetime
import typing
from warnings import deprecated # type: ignore

import jpype # type: ignore
import jpype.protocol # type: ignore

import docking.widgets.textfield.integer
import java.awt # type: ignore
import java.awt.event # type: ignore
import java.lang # type: ignore
import java.math # type: ignore
import java.text # type: ignore
import java.time # type: ignore
import java.util # type: ignore
import java.util.regex # type: ignore
import javax.swing # type: ignore
import javax.swing.event # type: ignore
import javax.swing.text # type: ignore


class DecimalFormatterFactory(javax.swing.JFormattedTextField.AbstractFormatterFactory):

    class_: typing.ClassVar[java.lang.Class]

    @typing.overload
    def __init__(self) -> None:
        ...

    @typing.overload
    def __init__(self, formatPattern: typing.Union[java.lang.String, str]) -> None:
        ...

    def getDecimalFormat(self) -> java.text.DecimalFormat:
        ...

    @property
    def decimalFormat(self) -> java.text.DecimalFormat:
        ...


class ElidingFilePathTextField(PreviewTextField):
    """
    :obj:`PreviewTextField` (JTextField) that has a preview that compresses / shortens the
    text in the field using rules that are tuned to preserve human readability of filename path info.
     
    
    Longer directory names are truncated and modified to have a "..." suffix.  When adjacent 
    directory names have been reduced to just "...", they are combined into a single "...." (4-dot).
     
    
    The first and last directory elements in the path are given preference and will be subject to
    shortening after interior directory name elements.
     
    
    The final element in the path (filename) is always preserved.
     
    
    If the preview of the path needs truncation, the full path will be temporarily appended to the
    the field's tool tip.
    """

    @typing.type_check_only
    class PathPartInfo(java.lang.Record):

        class_: typing.ClassVar[java.lang.Class]

        def equals(self, o: java.lang.Object) -> bool:
            ...

        def hashCode(self) -> int:
            ...

        def origIndex(self) -> int:
            ...

        def s(self) -> str:
            ...

        def toString(self) -> str:
            ...


    class_: typing.ClassVar[java.lang.Class]

    @typing.overload
    def __init__(self) -> None:
        """
        Creates a new :obj:`ElidingFilePathTextField` instance with no text.
        """

    @typing.overload
    def __init__(self, text: typing.Union[java.lang.String, str]) -> None:
        """
        Creates a new :obj:`ElidingFilePathTextField` instance with specified text value.
        
        :param java.lang.String or str text: string to assign as initial value of text field
        """

    @typing.overload
    def __init__(self, text: typing.Union[java.lang.String, str], hint: typing.Union[java.lang.String, str]) -> None:
        """
        Creates a new :obj:`ElidingFilePathTextField` instance with specified text and hint values.
        
        :param java.lang.String or str text: string to assign as initial value of text field
        :param java.lang.String or str hint: string to assign as the hint value that is shown when the field is blank
        """


class FixedSizeIntegerTextField(docking.widgets.textfield.integer.AbstractIntegerTextField):
    """
    TextField for entering numbers where the values are restricted to those that can be represented
    by a specific number of bits. For example, if the bit size is eight, signed values
    must be between -128 and 127 and unsigned values must be between 0 and 255. By
    default, this class uses all the formats from the :obj:`IntegerFormat` enum class except for
    signed octal and signed binary. 
    
     
    
    This field does continuous checking, so you can't enter a bad value.
    
    
    The bitSize can be changed on this field which will cause its min and max values to change to
    the appropriate values for that bit size and signedness of the current :obj:`IntegerFormat`.
    Also, if the current value doesn't fit in the new bit size, it will be reset to having no
    value (textfield is blank).
     
    
    Internally, values are maintained using BigIntegers so this class can accommodate any bit size
    desired. There are convenience methods for getting the value as either an int or long. You 
    should only use these convenience methods if you know the current bit size fits in either a 
    int or long respectively.
    
     
    
    There are several configuration options as follows:
     
    * Bit Size - This value must be 1 or greater and determines the minimum and maximum allowed
    input values when combined with the current format signedness.
    * Use number prefix - If this mode is on, then non-decimal values must be typed with its 
    prefix(i.e., 0x for hex). When requiring non-decimal prefix, the field is permitted to auto
    switch formats based on the prefix (or lack thereof). When the "use prefix" option is off, the
    only way to switch formats is to use the built-in ctrl-M action.
    * Show the number mode as hint text - If showing number mode is on, the format short name
    is displayed lightly in the bottom right portion of the text field.
    See:meth:`setShowNumberMode(boolean) <.setShowNumberMode>`
    """

    class_: typing.ClassVar[java.lang.Class]

    @typing.overload
    def __init__(self, columns: typing.Union[jpype.JInt, int], bitSize: typing.Union[jpype.JInt, int]) -> None:
        """
        Constructor
        
        :param jpype.JInt or int columns: the number of character positions for the preferred size of the text field
        :param jpype.JInt or int bitSize: the initial bit size
        """

    @typing.overload
    def __init__(self, columns: typing.Union[jpype.JInt, int], bitSize: typing.Union[jpype.JInt, int], initialValue: typing.Union[jpype.JLong, int]) -> None:
        """
        Constructor
        
        :param jpype.JInt or int columns: the number of character positions for the preferred size of the text field
        :param jpype.JInt or int bitSize: the initial bit size
        :param jpype.JLong or int initialValue: the value to initialize the field to
        """

    @typing.overload
    def __init__(self, columns: typing.Union[jpype.JInt, int], bitSize: typing.Union[jpype.JInt, int], initialValue: java.math.BigInteger) -> None:
        """
        Constructor
        
        :param jpype.JInt or int columns: the number of character positions for the preferred size of the text field
        :param jpype.JInt or int bitSize: the initial bit size
        :param java.math.BigInteger initialValue: the value to initialize the field to
        """

    def getBitSize(self) -> int:
        """
        :return: the current bit size for this field
        :rtype: int
        """

    def setBitSize(self, bitSize: typing.Union[jpype.JInt, int]) -> None:
        """
        Sets the bit size for this field, which effectively sets the min and max values for this 
        field when combined with the signedness of the currently selected :obj:`IntegerFormat`.
        
        :param jpype.JInt or int bitSize: the number of bits that will be used to store this value, effectively
        determining its min and max value
        """

    @property
    def bitSize(self) -> jpype.JInt:
        ...

    @bitSize.setter
    def bitSize(self, value: jpype.JInt):
        ...


class FloatingPointTextField(javax.swing.JTextField):
    """
    A simple text field for inputting floating point numbers. The field is continuously validated so 
    that only valid characters and values can be entered. If the text is blank or contains only "-",
    ".", or "-.", the value is considered to be 0. You can optionally set a min and max value. In 
    order for the continuous validation to work, the max must be a non-negative number and the min 
    must be a non-positive number.
    """

    @typing.type_check_only
    class FloatingPointDocumentFilter(javax.swing.text.DocumentFilter):
        ...
        class_: typing.ClassVar[java.lang.Class]


    class_: typing.ClassVar[java.lang.Class]

    @typing.overload
    def __init__(self, columns: typing.Union[jpype.JInt, int]) -> None:
        """
        Constructs a new empty FloatingPointTextField.
        
        :param jpype.JInt or int columns: the number of columns for determining the preferred width
        """

    @typing.overload
    def __init__(self, columns: typing.Union[jpype.JInt, int], initialValue: typing.Union[jpype.JDouble, float]) -> None:
        """
        Constructs a new FloatingPointTextField initialized with the given value.
        
        :param jpype.JInt or int columns: the number of columns for determining the preferred width
        :param jpype.JDouble or float initialValue: the initial value
        """

    def getValue(self) -> float:
        """
        Returns the value represented by the text in the field. If the field only contains "-",".",
        or "-.", the value returned will be 0.
        
        :return: the value represented by the text in the field
        :rtype: float
        """

    def setMaxValue(self, max: typing.Union[jpype.JDouble, float]) -> None:
        """
        Sets the maximum allowed value. The max must be 0 or positive so that continuous validation
        can work.
        
        :param jpype.JDouble or float max: the maximum allowed value.
        """

    def setMinValue(self, min: typing.Union[jpype.JDouble, float]) -> None:
        """
        Sets the minimum allowed value. The min must be 0 or negative so that continuous validation
        can work.
        
        :param jpype.JDouble or float min: the minimum allowed value.
        """

    def setValue(self, value: typing.Union[jpype.JDouble, float]) -> None:
        """
        Sets the text in the field to the given value.
        
        :param jpype.JDouble or float value: the value to display in the text field
        """

    @property
    def value(self) -> jpype.JDouble:
        ...

    @value.setter
    def value(self, value: jpype.JDouble):
        ...


class GFormattedTextField(javax.swing.JFormattedTextField):
    """
    :obj:`GFormattedTextField` provides an implementation of :obj:`JFormattedTextField` 
    which facilitates entry validation with an indication of its current status.
     
    
    When modified from its default value the field background will reflect its 
    current status.
    """

    class Status(java.lang.Enum[GFormattedTextField.Status]):

        class_: typing.ClassVar[java.lang.Class]
        UNCHANGED: typing.Final[GFormattedTextField.Status]
        CHANGED: typing.Final[GFormattedTextField.Status]
        INVALID: typing.Final[GFormattedTextField.Status]

        @staticmethod
        def valueOf(name: typing.Union[java.lang.String, str]) -> GFormattedTextField.Status:
            ...

        @staticmethod
        def values() -> jpype.JArray[GFormattedTextField.Status]:
            ...


    class_: typing.ClassVar[java.lang.Class]

    def __init__(self, factory: javax.swing.JFormattedTextField.AbstractFormatterFactory, defaultValue: java.lang.Object) -> None:
        ...

    def addTextEntryStatusListener(self, listener: TextEntryStatusListener) -> None:
        ...

    def disableFocusEventProcessing(self) -> None:
        ...

    def editingFinished(self) -> None:
        ...

    def getDefaultText(self) -> str:
        """
        Returns the default text.  This is useful to know what the original text is after the user
        has edited the text.
        
        :return: the default text
        :rtype: str
        """

    def getTextEntryStatus(self) -> GFormattedTextField.Status:
        ...

    def isChanged(self) -> bool:
        """
        Returns true if the contents of this field do not match the default.
        
        :return: true if the contents of this field do not match the default.
        :rtype: bool
        """

    def isInvalid(self) -> bool:
        """
        Returns true if the contents of this field are invalid, as determined by the InputValidator.
        
        :return: true if the contents of this field are invalid, as determined by the InputValidator.
        :rtype: bool
        """

    def reset(self) -> None:
        """
        Restores this field to its default text.
        """

    def setDefaultValue(self, defaultValue: java.lang.Object) -> None:
        """
        Establish default value.  Text field value should be set before invoking this method.
        
        :param java.lang.Object defaultValue: default value
        """

    def setIsError(self, isError: typing.Union[jpype.JBoolean, bool]) -> None:
        ...

    @property
    def textEntryStatus(self) -> GFormattedTextField.Status:
        ...

    @property
    def invalid(self) -> jpype.JBoolean:
        ...

    @property
    def defaultText(self) -> java.lang.String:
        ...

    @property
    def changed(self) -> jpype.JBoolean:
        ...


class GValidatedTextField(javax.swing.JTextField):

    class ValidatedDocument(javax.swing.text.PlainDocument):

        class_: typing.ClassVar[java.lang.Class]

        @typing.overload
        def __init__(self, validators: java.util.List[GValidatedTextField.TextValidator]) -> None:
            ...

        @typing.overload
        def __init__(self) -> None:
            ...

        def addValidationMessageListener(self, listener: GValidatedTextField.ValidationMessageListener) -> None:
            ...

        def addValidator(self, validator: GValidatedTextField.TextValidator) -> None:
            ...

        def removeValidationMessageListener(self, listener: GValidatedTextField.ValidationMessageListener) -> None:
            ...

        def removeValidator(self, validator: GValidatedTextField.TextValidator) -> None:
            ...


    class TextValidator(java.lang.Object):

        class_: typing.ClassVar[java.lang.Class]

        def validate(self, oldText: typing.Union[java.lang.String, str], newText: typing.Union[java.lang.String, str]) -> None:
            ...


    class ValidationMessageListener(java.lang.Object):

        class_: typing.ClassVar[java.lang.Class]

        def message(self, msg: typing.Union[java.lang.String, str]) -> None:
            ...


    class ValidationFailedException(java.lang.Exception):

        class_: typing.ClassVar[java.lang.Class]

        @typing.overload
        def __init__(self, msg: typing.Union[java.lang.String, str]) -> None:
            ...

        @typing.overload
        def __init__(self, cause: java.lang.Throwable) -> None:
            ...

        @typing.overload
        def __init__(self, msg: typing.Union[java.lang.String, str], cause: java.lang.Throwable) -> None:
            ...


    class LongField(GValidatedTextField):

        class LongValidator(GValidatedTextField.TextValidator):

            class_: typing.ClassVar[java.lang.Class]

            def __init__(self) -> None:
                ...

            def validateLong(self, oldLong: typing.Union[jpype.JLong, int], newLong: typing.Union[jpype.JLong, int]) -> None:
                ...


        class_: typing.ClassVar[java.lang.Class]

        @typing.overload
        def __init__(self, validators: java.util.List[GValidatedTextField.TextValidator], value: typing.Union[java.lang.String, str], columns: typing.Union[jpype.JInt, int]) -> None:
            ...

        @typing.overload
        def __init__(self, value: typing.Union[java.lang.String, str], columns: typing.Union[jpype.JInt, int]) -> None:
            ...

        @typing.overload
        def __init__(self, value: typing.Union[java.lang.String, str]) -> None:
            ...

        @typing.overload
        def __init__(self, columns: typing.Union[jpype.JInt, int]) -> None:
            ...

        def getValue(self) -> int:
            ...

        @property
        def value(self) -> jpype.JLong:
            ...


    class MaxLengthField(GValidatedTextField):

        @typing.type_check_only
        class MaxLengthDocument(GValidatedTextField.ValidatedDocument):

            class_: typing.ClassVar[java.lang.Class]

            def __init__(self, validators: java.util.List[GValidatedTextField.TextValidator]) -> None:
                ...


        class_: typing.ClassVar[java.lang.Class]

        @typing.overload
        def __init__(self, validators: java.util.List[GValidatedTextField.TextValidator], value: typing.Union[java.lang.String, str], columns: typing.Union[jpype.JInt, int]) -> None:
            ...

        @typing.overload
        def __init__(self, value: typing.Union[java.lang.String, str], columns: typing.Union[jpype.JInt, int]) -> None:
            ...

        @typing.overload
        def __init__(self, columns: typing.Union[jpype.JInt, int]) -> None:
            ...


    class_: typing.ClassVar[java.lang.Class]

    @typing.overload
    def __init__(self, validators: java.util.List[GValidatedTextField.TextValidator], value: typing.Union[java.lang.String, str], columns: typing.Union[jpype.JInt, int]) -> None:
        ...

    @typing.overload
    def __init__(self, value: typing.Union[java.lang.String, str], columns: typing.Union[jpype.JInt, int]) -> None:
        ...

    def addValidationMessageListener(self, listener: GValidatedTextField.ValidationMessageListener) -> None:
        ...

    def addValidator(self, validator: GValidatedTextField.TextValidator) -> None:
        ...

    def removeValidationMessageListener(self, listener: GValidatedTextField.ValidationMessageListener) -> None:
        ...

    def removeValidator(self, validator: GValidatedTextField.TextValidator) -> None:
        ...


class HexOrDecimalInput(javax.swing.JTextField):

    @typing.type_check_only
    class MyDocument(javax.swing.text.PlainDocument):
        ...
        class_: typing.ClassVar[java.lang.Class]


    class_: typing.ClassVar[java.lang.Class]

    @typing.overload
    def __init__(self) -> None:
        ...

    @typing.overload
    def __init__(self, columns: typing.Union[jpype.JInt, int]) -> None:
        ...

    @typing.overload
    def __init__(self, initialValue: typing.Union[java.lang.Long, int]) -> None:
        ...

    def getIntValue(self) -> int:
        ...

    def getValue(self) -> int:
        ...

    def setAllowNegative(self, b: typing.Union[jpype.JBoolean, bool]) -> None:
        ...

    def setDecimalMode(self) -> None:
        ...

    def setHexMode(self) -> None:
        ...

    @typing.overload
    def setValue(self, newValue: typing.Union[jpype.JInt, int]) -> None:
        ...

    @typing.overload
    def setValue(self, newValue: typing.Union[java.lang.Long, int]) -> None:
        ...

    @property
    def intValue(self) -> jpype.JInt:
        ...

    @property
    def value(self) -> jpype.JLong:
        ...

    @value.setter
    def value(self, value: jpype.JLong):
        ...


class HintTextField(javax.swing.JTextField):
    """
    Simple text field that shows a text hint when the field is empty.
    
     
    Hint text will be shown in light grey. Normal text will be plain black.
    """

    class_: typing.ClassVar[java.lang.Class]

    @typing.overload
    def __init__(self, hint: typing.Union[java.lang.String, str]) -> None:
        """
        Constructor
        
        :param java.lang.String or str hint: the hint text
        """

    @typing.overload
    def __init__(self, hint: typing.Union[java.lang.String, str], required: typing.Union[jpype.JBoolean, bool]) -> None:
        """
        Constructor
        
        :param java.lang.String or str hint: the hint text
        :param jpype.JBoolean or bool required: true if the field should be marked as required
        """

    @typing.overload
    def __init__(self, hint: typing.Union[java.lang.String, str], required: typing.Union[jpype.JBoolean, bool], verifier: javax.swing.InputVerifier) -> None:
        """
        Constructor
        
        :param java.lang.String or str hint: the hint text
        :param jpype.JBoolean or bool required: true, if the field should be marked as required
        :param javax.swing.InputVerifier verifier: input verifier, or null if none needed
        """

    @typing.overload
    def __init__(self, text: typing.Union[java.lang.String, str], hint: typing.Union[java.lang.String, str], required: typing.Union[jpype.JBoolean, bool], verifier: javax.swing.InputVerifier) -> None:
        ...

    def addListeners(self) -> None:
        """
        Key listener allows us to check field validity on every key typed
        """

    def isFieldValid(self) -> bool:
        """
        Returns true if the field contains valid input.
        
        :return: true if valid, false otherwise
        :rtype: bool
        """

    def paintComponent(self, g: java.awt.Graphics) -> None:
        """
        Overridden to paint the hint text over the field when it's empty
        """

    def setDefaultBackgroundColor(self, color: java.awt.Color) -> None:
        """
        Allows users to override the background color used by this field when the contents are
        valid.  The invalid color is currently set by this class.
        
        :param java.awt.Color color: the color
        """

    def setHint(self, hint: typing.Union[java.lang.String, str]) -> None:
        """
        Sets the hint for this text field
        
        :param java.lang.String or str hint: the hint text
        """

    def setRequired(self, required: typing.Union[jpype.JBoolean, bool]) -> None:
        """
        Sets whether the field is required or not. If so, it will be rendered
        differently to indicate that to the user.
        
        :param jpype.JBoolean or bool required: true if required, false otherwise
        """

    def setText(self, text: typing.Union[java.lang.String, str]) -> None:
        """
        Overridden to check the field validity when text changes
        
        :param java.lang.String or str text: the text to fill
        """

    @property
    def fieldValid(self) -> jpype.JBoolean:
        ...


class IntegerTextField(docking.widgets.textfield.integer.AbstractIntegerTextField):
    """
    TextField for entering integer numbers in one of several number formats. By default, this class
    uses the :obj:`IntegerFormat.DEC` and the :obj:`IntegerFormat.HEX`, but it can be constructed
    with any of the formats defined in :obj:`IntegerFormat`.
    
     
    
    This field does continuous checking, so you can't enter a bad value.
    
     
    
    Internally, values are maintained using BigIntegers so this field can contain numbers as large as
    desired. There are convenience methods for getting the value as either an int or long. If using
    these convenience methods, you should also set the max allowed value so that users can't enter a
    value larger than can be represented by the :meth:`getIntValue() <.getIntValue>` or :meth:`getLongValue() <.getLongValue>`
    methods as appropriate.
    
     
    
    There are several configuration options as follows:
     
    * Max value - This value must be positive and will restrict the input to values less than or
    equal to this value.
    * Min value - This value must be generally be negative and will restrict the input to values
    greater than or equal to this value. As a special case, the min value can be set to 1.
    * Use number prefix - If this mode is on, then non-decimal values must be typed with its 
    prefix(i.e., 0x for hex). When requiring non-decimal prefix, the field is permitted to auto
    switch formats based on the prefix (or lack thereof). When the use prefix is off, the only way
    to switch formats is to use the ctrl-M action.
    * Show the number mode as hint text - If showing number mode is on, the format short name
    is displayed lightly in the bottom right portion of the text field.
    See:meth:`setShowNumberMode(boolean) <.setShowNumberMode>`
    """

    class_: typing.ClassVar[java.lang.Class]

    @typing.overload
    def __init__(self) -> None:
        ...

    @typing.overload
    def __init__(self, columns: typing.Union[jpype.JInt, int]) -> None:
        ...

    @typing.overload
    def __init__(self, columns: typing.Union[jpype.JInt, int], initialValue: typing.Union[jpype.JLong, int]) -> None:
        ...

    @typing.overload
    def __init__(self, columns: typing.Union[jpype.JInt, int], initialValue: java.math.BigInteger) -> None:
        ...

    @deprecated("use getFormat() instead")
    def isHexMode(self) -> bool:
        """
        Returns true if in hex mode, false if in another mode.
        
        :return: true if in hex mode, false if in decimal mode.
        :rtype: bool
        
        .. deprecated::
        
        use :meth:`getFormat() <.getFormat>` instead
        """

    @deprecated("use setMinValue(BigInteger) instead")
    def setAllowNegativeValues(self, b: typing.Union[jpype.JBoolean, bool]) -> None:
        """
        Sets whether or not negative numbers are accepted.
        
        :param jpype.JBoolean or bool b: if true, negative numbers are allowed.
        
        .. deprecated::
        
        use :meth:`setMinValue(BigInteger) <.setMinValue>` instead
        """

    @deprecated("use setUseNumberPrefix(boolean) instead")
    def setAllowsHexPrefix(self, usePrefix: typing.Union[jpype.JBoolean, bool]) -> None:
        """
        Sets whether on not the field supports the 0x prefix for hex numbers. This method is 
        deprecated since it now supports addition input modes other than hex or decimal. Turning
        the prefix on for hex will also turn it on for other non-decimal modes as well.
        
         
        
        If 0x is supported, hex numbers will be displayed with the 0x prefix. Also, when typing, you
        must type 0x first to enter a hex number, otherwise it will only allow digits 0-9. If the 0x
        prefix option is turned off, then hex numbers are displayed without the 0x prefix and you
        can't change the decimal/hex mode by typing 0x. The field will either be in decimal or hex
        mode and the typed text will be interpreted appropriately for the mode.
        
        :param jpype.JBoolean or bool usePrefix: true to use the 0x convention for hex.
        
        .. deprecated::
        
        use :meth:`setUseNumberPrefix(boolean) <.setUseNumberPrefix>` instead
        """

    @deprecated("use setFormat(IntegerFormat) instead")
    def setDecimalMode(self) -> None:
        """
        Sets the mode to Decimal.
        
         
        
        If the field is currently in hex mode, the current text will be change from displaying the
        current value from hex to decimal.
        
        
        .. deprecated::
        
        use :meth:`setFormat(IntegerFormat) <.setFormat>` instead
        """

    @deprecated("use setFormat(IntegerFormat) instead")
    def setHexMode(self) -> None:
        """
        Sets the radix mode to Hex.
        
         
        
        If the field is currently in decimal mode, the current text will be change from displaying
        the current value from decimal to hex.
        
        
        .. deprecated::
        
        use :meth:`setFormat(IntegerFormat) <.setFormat>` instead
        """

    @property
    def hexMode(self) -> jpype.JBoolean:
        ...


class LocalDateTextField(java.lang.Object):
    """
    Text field for entering dates. Optionally, a minimum and maximum date value can be set on this
    text field.
    """

    @typing.type_check_only
    class MyTextField(javax.swing.JTextField):
        ...
        class_: typing.ClassVar[java.lang.Class]


    class_: typing.ClassVar[java.lang.Class]

    def __init__(self, dateFormatPattern: typing.Union[java.lang.String, str]) -> None:
        ...

    def addActionListener(self, listener: java.awt.event.ActionListener) -> None:
        ...

    def addChangeListener(self, listener: javax.swing.event.ChangeListener) -> None:
        """
        Adds a change listener that will be notified whenever the value changes.
        
        :param javax.swing.event.ChangeListener listener: the change listener to add.
        """

    def getComponent(self) -> javax.swing.JComponent:
        ...

    def getMaximum(self) -> java.time.LocalDate:
        ...

    def getMinimum(self) -> java.time.LocalDate:
        ...

    def getTextField(self) -> javax.swing.JTextField:
        ...

    def getValue(self) -> java.time.LocalDate:
        ...

    def isShowingFieldMode(self) -> bool:
        ...

    def removeActionListener(self, listener: java.awt.event.ActionListener) -> None:
        ...

    def removeChangeListener(self, listener: javax.swing.event.ChangeListener) -> None:
        """
        Removes the changes listener.
        
        :param javax.swing.event.ChangeListener listener: the listener to be removed.
        """

    def requestFocus(self) -> None:
        ...

    def selectAll(self) -> None:
        ...

    def setDayMode(self) -> None:
        """
        Sets the mode to Day.
        """

    def setEnabled(self, enabled: typing.Union[jpype.JBoolean, bool]) -> None:
        ...

    def setMaximum(self, maximum: java.time.LocalDate) -> None:
        """
        Sets the maximum allowed date. Can be null.
        
        :param java.time.LocalDate maximum: the minimum allowed date.
        """

    def setMinimum(self, minimum: java.time.LocalDate) -> None:
        """
        Sets the minimum allowed date. Can be null.
        
        :param java.time.LocalDate minimum: the minimum allowed date.
        """

    def setMonthMode(self) -> None:
        """
        Sets the mode to Month.
        """

    def setShowFieldMode(self, show: typing.Union[jpype.JBoolean, bool]) -> None:
        """
        Turns on or off the faded text that indicates if the field is in month or day mode
        
        :param jpype.JBoolean or bool show: true to show the mode.
        """

    def setValue(self, newDate: java.time.LocalDate) -> None:
        ...

    @property
    def component(self) -> javax.swing.JComponent:
        ...

    @property
    def maximum(self) -> java.time.LocalDate:
        ...

    @maximum.setter
    def maximum(self, value: java.time.LocalDate):
        ...

    @property
    def showingFieldMode(self) -> jpype.JBoolean:
        ...

    @property
    def value(self) -> java.time.LocalDate:
        ...

    @value.setter
    def value(self, value: java.time.LocalDate):
        ...

    @property
    def minimum(self) -> java.time.LocalDate:
        ...

    @minimum.setter
    def minimum(self, value: java.time.LocalDate):
        ...

    @property
    def textField(self) -> javax.swing.JTextField:
        ...


class PreviewTextField(HintTextField):
    """
    Abstract base class for text fields that can show a preview of a modified version of their text
    when it does not have focus.
     
    
    The tool tip of the field is updated to include the full value of the field if the preview was
    truncated during painting.  Override :meth:`getPreviewToolTipAdditionalText() <.getPreviewToolTipAdditionalText>` to control
    what text is added to the tool tip in those cases.
     
    
    NOTE: using an ending </HTML> tag in a tool tip string is not recommended as it will
    defeat PreviewTextField's updated information from being displayed to the user.
    """

    class_: typing.ClassVar[java.lang.Class]


class TextEntryStatusListener(java.lang.Object):

    class_: typing.ClassVar[java.lang.Class]

    def statusChanged(self, textField: GFormattedTextField) -> None:
        ...


class TextFieldLinker(java.lang.Object):
    """
    A class that links text fields into a "formatted text field", separated by expressions.
     
     
    
    This fulfills a similar purpose to formatted text fields, except the individual parts may be
    placed independent of the other components. Granted, they ought to appear in an intuitive order.
    The input string is split among a collection of :obj:`JTextField`s each according to a given
    pattern -- excluding the final field. Cursor navigation, insertion, deletion, etc. are all
    applied as if the linked text fields were part of a single composite text field.
     
     
    
    The individual text fields must be constructed and added by the user, as in the example:
     
     
    Box hbox = Box.createHorizontalBox();
    TextFieldLinker linker = new TextFieldLinker();
     
    JTextField first = new JTextField();
    hbox.add(first);
    hbox.add(Box.createHorizontalStrut(10));
    linker.linkField(first, "\\s+", " ");
     
    JTextField second = new JTextField();
    hbox.add(second);
    hbox.add(new GLabel("-"));
    linker.linkField(second, "-", "-");
     
    JTextField third = new JTextField();
    hbox.add(third);
    linker.linkLastField(third);
     
    linker.setVisible(true);
    """

    @typing.type_check_only
    class LinkedField(java.lang.Object):
        """
        A field that has been added with its corresponding separator expression and replacement
        """

        class_: typing.ClassVar[java.lang.Class]

        def unregisterListener(self) -> None:
            ...


    @typing.type_check_only
    class FieldState(java.lang.Object):
        """
        The current state of a linked field, stored separately from the actual component
        """

        class_: typing.ClassVar[java.lang.Class]

        def clampedCaret(self) -> int:
            ...


    @typing.type_check_only
    class LinkerState(java.lang.Object):
        """
        A class to track the internal state gathered from the text fields
        """

        class_: typing.ClassVar[java.lang.Class]

        def copy(self) -> TextFieldLinker.LinkerState:
            """
            Copy the state
            
            :return: the copy
            :rtype: TextFieldLinker.LinkerState
            """

        @typing.overload
        def getGlobalCaret(self) -> int:
            """
            Get the composite caret location
            
            :return: the location (including separators)
            :rtype: int
            """

        @typing.overload
        def getGlobalCaret(self, omitSep: typing.Union[jpype.JInt, int]) -> int:
            """
            Get the composite caret location, omitting the given separator.
            
            :param jpype.JInt or int omitSep: the separator to omit, or -1 to omit nothing
            :return: the location
            :rtype: int
            """

        @typing.overload
        def getText(self) -> str:
            """
            Get the whole composite string
            
            :return: the text
            :rtype: str
            """

        @typing.overload
        def getText(self, omitSep: typing.Union[jpype.JInt, int]) -> str:
            """
            Get the composite string, omitting the given separator.
             
             
            
            This is used as a helper to delete the separator when backspace/delete is pressed at a
            boundary.
            
            :param jpype.JInt or int omitSep: the separator to omit, or -1 to omit nothing
            :return: the text
            :rtype: str
            """

        def getTextBeforeCursor(self, field: typing.Union[jpype.JInt, int]) -> str:
            """
            Get the composite text preceding the caret in the given field
            
            :param jpype.JInt or int field: the field whose caret to use
            :return: the text
            :rtype: str
            """

        def isAfterSep(self, field: typing.Union[jpype.JInt, int]) -> bool:
            """
            Figure out whether the caret in the given field immediately proceeds a separator.
             
             
            
            In other words, the caret must be to the far left (position 0), and the given field must
            not be the first field. If true, the caret immediately follows separator index
            ``field - 1``.
            
            :param jpype.JInt or int field: the field index to check
            :return: true if the caret immediately follows a separator.
            :rtype: bool
            """

        def isBeforeSep(self, field: typing.Union[jpype.JInt, int]) -> bool:
            """
            Figure out whether the caret in the given field immediately precedes a separator.
             
             
            
            In other words, the caret must be to the far right, and the given field must not be the
            last field. If true, the caret immediately precedes separator index ``field``.
            
            :param jpype.JInt or int field: the field index to check
            :return: true if the caret immediately precedes a separator.
            :rtype: bool
            """

        def navigateFieldLeft(self, field: typing.Union[jpype.JInt, int]) -> None:
            """
            Change focus to the given field as if navigating left.
             
             
            
            The caret will be moved to the rightmost position, because we're moving left from the
            leftmost position of the field to the right.
            
            :param jpype.JInt or int field: the field index to be given focus.
            """

        def navigateFieldRight(self, field: typing.Union[jpype.JInt, int]) -> None:
            """
            Change focus to the given field as if navigating right.
             
             
            
            The caret will be moved to the leftmost position, because we're moving right from the
            rightmost position of the field to the left.
            
            :param jpype.JInt or int field: the field index to be given focus.
            """

        def reformat(self) -> None:
            """
            Re-parse the composite string and place the components into their proper fields
            """

        def reset(self) -> None:
            """
            Erase the state
             
             
            
            Blank all the fields, and put the caret at the front of the first field.
            """

        def setGlobalCaret(self, caret: typing.Union[jpype.JInt, int]) -> None:
            """
            Set the composite caret location
            
            :param jpype.JInt or int caret: the new caret location
            :raises BadLocationException: if the location exceeds the text length
            """

        def setText(self, text: typing.Union[java.lang.String, str]) -> int:
            """
            Set the composite text
            
            :param java.lang.String or str text: the new text
            """

        @property
        def globalCaret(self) -> jpype.JInt:
            ...

        @globalCaret.setter
        def globalCaret(self, value: jpype.JInt):
            ...

        @property
        def afterSep(self) -> jpype.JBoolean:
            ...

        @property
        def textBeforeCursor(self) -> java.lang.String:
            ...

        @property
        def beforeSep(self) -> jpype.JBoolean:
            ...

        @property
        def text(self) -> java.lang.String:
            ...


    @typing.type_check_only
    class DualFieldListener(java.awt.event.KeyAdapter, javax.swing.event.CaretListener, java.awt.event.FocusListener, javax.swing.event.DocumentListener):
        """
        A listener for all my callbacks
         
         
        
        A separate listener is constructed and installed on each field so that we have a reference to
        the field in every callback.
        """

        class_: typing.ClassVar[java.lang.Class]

        def __init__(self, linked: TextFieldLinker.LinkedField) -> None:
            ...


    class_: typing.ClassVar[java.lang.Class]

    def __init__(self) -> None:
        ...

    def addFocusListener(self, listener: java.awt.event.FocusListener) -> None:
        """
        Add a focus listener
         
         
        
        The focus listener will receive a callback only when focus is passed completely outside the
        composite text field. No events are generated when focus passes from one field in the
        composite to another.
        
        :param java.awt.event.FocusListener listener: the focus listener to add
        """

    def clear(self) -> None:
        """
        Clear the composite field, i.e., clear all the linked fields
        """

    def getField(self, i: typing.Union[jpype.JInt, int]) -> javax.swing.JTextField:
        """
        Get an individual field in the composite
        
        :param jpype.JInt or int i: the index of the field
        :return: the field
        :rtype: javax.swing.JTextField
        """

    def getFocusedField(self) -> javax.swing.JTextField:
        """
        Get the individual field last having focus
         
         
        
        Effectively, this gives the field containing the composite caret
        
        :return: the last-focused field
        :rtype: javax.swing.JTextField
        """

    def getNumFields(self) -> int:
        """
        Get the number of fields in this composite
        
        :return: the field count
        :rtype: int
        """

    def getText(self) -> str:
        """
        Get the full composite text
        
        :return: the text, including separators
        :rtype: str
        """

    def getTextBeforeCursor(self, where: javax.swing.JTextField) -> str:
        """
        Get the text preceding the caret in the given field
        
        :param javax.swing.JTextField where: the field whose caret to consider
        :return: the text
        :rtype: str
        """

    def isVisible(self) -> bool:
        """
        Check if all component fields are visible
        
        :return: false if any component is not visible, true otherwise
        :rtype: bool
        """

    @typing.overload
    def linkField(self, field: javax.swing.JTextField, exp: typing.Union[java.lang.String, str], sep: typing.Union[java.lang.String, str]) -> None:
        """
        
        
        
        .. seealso::
        
            | :obj:`.linkField(JTextField, Pattern, String)`
        """

    @typing.overload
    def linkField(self, field: javax.swing.JTextField, pat: java.util.regex.Pattern, sep: typing.Union[java.lang.String, str]) -> None:
        """
        Add a new text field to this linker
         
         
        
        Links the given field with the others present in this linker, if any. ``pat`` is a
        regular expression that dictates where the given field ends, and the next field begins. When
        ``pat`` matches a part of the text in ``field``, the text is split and re-flowed so
        that the second part is moved into the next linked field. The separator is omitted from both
        fields. The fields should be positioned in order with labels between that display the
        expected separators, so that the user may understand what is happening. The
        :meth:`getText() <.getText>` and :meth:`getTextBeforeCursor(JTextField) <.getTextBeforeCursor>` methods will include
        ``sep`` between the fields.
         
         
        
        Any number of fields may be added in this fashion, but the last field -- having no associated
        pattern or separator -- must be added using :meth:`linkLastField(JTextField) <.linkLastField>`. Thus, before
        linking is actually activated, at least one field must be present. To be meaningful, at least
        two fields should be linked.
         
         
        
        **NOTE:** ``pat`` must accept ``sep``, otherwise calling :meth:`setText(String) <.setText>`
        with the results of :meth:`getText() <.getText>` will have unexpected effects.
        
        :param javax.swing.JTextField field: the field to link
        :param java.util.regex.Pattern pat: the regular expression to search for following the field
        :param java.lang.String or str sep: the separator that replaces ``pat`` when matched
        """

    def linkLastField(self, field: javax.swing.JTextField) -> None:
        """
        Add the final field, and actually link the fields
         
         
        
        The fields are not effectively linked until this method is called. Additionally, once this
        method is called, the linker cannot take any additional fields.
        
        :param javax.swing.JTextField field: the final field
        """

    def removeFocusListener(self, listener: java.awt.event.FocusListener) -> None:
        """
        Remove a focus listener
        
        :param java.awt.event.FocusListener listener: the focus listener to remove
        """

    def setCaretPosition(self, pos: typing.Union[jpype.JInt, int]) -> None:
        """
        Set the location of the caret among the composite text
        
        :param jpype.JInt or int pos: the position, including separators
        :raises BadLocationException: if the position is larger than the composite text
        """

    def setFont(self, font: java.awt.Font) -> None:
        """
        Set the font for all linked fields
        
        :param java.awt.Font font: the new font
        """

    def setText(self, text: typing.Union[java.lang.String, str]) -> None:
        """
        Set the full composite text
        
        :param java.lang.String or str text: the text, including separators
        """

    def setVisible(self, visible: typing.Union[jpype.JBoolean, bool]) -> None:
        """
        Set the visibility of all the component fields
        
        :param jpype.JBoolean or bool visible: true to show, false to hide
        """

    @staticmethod
    def twoSpacedFields() -> TextFieldLinker:
        """
        A convenient factory to build two fields separated by spaces
        
        :return: the linker containing two new linked :obj:`JTextField`s
        :rtype: TextFieldLinker
        """

    @property
    def visible(self) -> jpype.JBoolean:
        ...

    @visible.setter
    def visible(self, value: jpype.JBoolean):
        ...

    @property
    def field(self) -> javax.swing.JTextField:
        ...

    @property
    def focusedField(self) -> javax.swing.JTextField:
        ...

    @property
    def textBeforeCursor(self) -> java.lang.String:
        ...

    @property
    def text(self) -> java.lang.String:
        ...

    @text.setter
    def text(self, value: java.lang.String):
        ...

    @property
    def numFields(self) -> jpype.JInt:
        ...



__all__ = ["DecimalFormatterFactory", "ElidingFilePathTextField", "FixedSizeIntegerTextField", "FloatingPointTextField", "GFormattedTextField", "GValidatedTextField", "HexOrDecimalInput", "HintTextField", "IntegerTextField", "LocalDateTextField", "PreviewTextField", "TextEntryStatusListener", "TextFieldLinker"]
