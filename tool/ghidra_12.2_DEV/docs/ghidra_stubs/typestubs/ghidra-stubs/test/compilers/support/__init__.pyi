from __future__ import annotations
import collections.abc
import datetime
import typing
from warnings import deprecated # type: ignore

import jpype # type: ignore
import jpype.protocol # type: ignore

import ghidra.pcode.emu
import ghidra.program.model.address
import ghidra.program.model.data
import ghidra.program.model.lang
import ghidra.program.model.listing
import ghidra.program.model.pcode
import ghidra.test
import ghidra.util
import java.lang # type: ignore
import java.util # type: ignore
import java.util.function # type: ignore


class CSpecPrototypeTest(ghidra.test.AbstractGhidraHeadlessIntegrationTest):
    """
    ``CSpecPrototypeTest`` provides an abstract JUnit test implementation
    for processor-specific and compiler-specific calling convention test cases.
     
    Tests which extend this class must implement abstract functions to specify LANGUAGE_ID,
    COMPILER_SPEC_ID, and CALLING_CONVENTION.
     
    An optional list of function names that contain errors can be passed to the constructor to
    designate those errors as expected. The test will pass as long as only expected errors are found.
     
    Source and binary files have a naming scheme.
    (LANGUAGE_ID)_(COMPILER_SPEC_ID)_(CALLING_CONVENTION)
     
    Trace logging is disabled by default. Specific traceLevel and traceLog disabled controlled via 
    environment properties CSpecTestTraceLevel and EmuTestTraceDisable.
     
    To create a new CSpecPrototypeTest for a given Module (e.g. Processors x86) complete the 
    following steps:
     
    1. Generate source code using Ghidra and the Ghidra script "GeneratePrototypeTestFileScript".
    NOTE: Do not rename the generated file; the filename is required for the test suit.
    2. Compile the source code using the following recommended GCC flags:
    gcc -O1 -c -fno-inline -fno-leading-underscore -o filename_without_extension filename.c
    3. Place the source code and compiled binary in the module's "data/cspectests" directory or the 
    ghidra.bin repository in the directory: "Ghidra/Test/TestResources/data/cspectests"
    4. Add a new package named "ghidra.test.processors.cspec" to the module if it does not exist and 
    place all new CSpecTest's in this package.
    5. New CSpecTests should extend this class and have a class name which ends in 'CSpecTest' and 
    starts with processor details that indicate what cspec prototype is being tested.
    - Implement abstract methods for Language ID, Compiler Spec ID, and Calling Convention.
    6. Use Ghidra and the Ghidra script "TestPrototypeScript" to debug errors. 
    - Click function links in the Script Console to jump to the Listing View.
    - To isolate a single function, highlight it in the Listing and re-run the script 
    for detailed debug output.
    """

    class_: typing.ClassVar[java.lang.Class]

    def getCallingConvention(self) -> str:
        """
        
        
        :return: String Calling Convention
        :rtype: str
        """

    def getCompilerSpecID(self) -> str:
        """
        
        
        :return: String Compiler Spec ID
        :rtype: str
        """

    def getLanguageID(self) -> str:
        """
        
        
        :return: String Language ID
        :rtype: str
        """

    def prototypeTest(self) -> None:
        """
        Tests that for a given binary and source code all functions in the binary are
        interpreted correctly by Ghidra using cspec files for the given calling convention.
        
        :raises java.lang.Exception: when the Prototype cannot be established, the source code could not be 
        parsed correctly, or the test could not be completed.
        """

    def setUp(self) -> None:
        """
        Ran before every test to prepare Ghidra for testing.
        
        :raises java.lang.Exception: when the test environment fails to be created or the emulator fails to
        load the program.
        """

    def tearDown(self) -> None:
        ...

    @property
    def callingConvention(self) -> java.lang.String:
        ...

    @property
    def languageID(self) -> java.lang.String:
        ...

    @property
    def compilerSpecID(self) -> java.lang.String:
        ...


class CSpecPrototypeTestConstants(java.lang.Object):
    """
    Constants that are used by the CSpecPrototypeUtil to decode cspec test binary source code function
    names.
    """

    class_: typing.ClassVar[java.lang.Class]
    FIELD_NAME_PREFIX: typing.Final = "fld"
    STRUCT_CHAR_SINGLETON_NAME: typing.Final = "sc"
    STRUCT_SHORT_SINGLETON_NAME: typing.Final = "ss"
    STRUCT_INT_SINGLETON_NAME: typing.Final = "si"
    STRUCT_LONG_SINGLETON_NAME: typing.Final = "sl"
    STRUCT_LONG_LONG_SINGLETON_NAME: typing.Final = "sll"
    STRUCT_FLOAT_SINGLETON_NAME: typing.Final = "sf"
    STRUCT_DOUBLE_SINGLETON_NAME: typing.Final = "sd"
    STRUCT_CHAR_PAIR_NAME: typing.Final = "prc"
    STRUCT_SHORT_PAIR_NAME: typing.Final = "prs"
    STRUCT_INT_PAIR_NAME: typing.Final = "pri"
    STRUCT_LONG_PAIR_NAME: typing.Final = "prl"
    STRUCT_LONG_LONG_PAIR_NAME: typing.Final = "prll"
    STRUCT_FLOAT_PAIR_NAME: typing.Final = "prf"
    STRUCT_DOUBLE_PAIR_NAME: typing.Final = "prd"
    STRUCT_CHAR_TRIP_NAME: typing.Final = "trc"
    STRUCT_SHORT_TRIP_NAME: typing.Final = "trs"
    STRUCT_INT_TRIP_NAME: typing.Final = "tri"
    STRUCT_LONG_TRIP_NAME: typing.Final = "trl"
    STRUCT_LONG_LONG_TRIP_NAME: typing.Final = "trll"
    STRUCT_FLOAT_TRIP_NAME: typing.Final = "trf"
    STRUCT_DOUBLE_TRIP_NAME: typing.Final = "trd"
    STRUCT_CHAR_QUAD_NAME: typing.Final = "qc"
    STRUCT_SHORT_QUAD_NAME: typing.Final = "qs"
    STRUCT_INT_QUAD_NAME: typing.Final = "qi"
    STRUCT_LONG_QUAD_NAME: typing.Final = "ql"
    STRUCT_LONG_LONG_QUAD_NAME: typing.Final = "qll"
    STRUCT_FLOAT_QUAD_NAME: typing.Final = "qf"
    STRUCT_DOUBLE_QUAD_NAME: typing.Final = "qd"
    STRUCT_INT_LONG_INT: typing.Final = "stili"
    STRUCT_FLOAT_INT_FLOAT: typing.Final = "stfif"
    STRUCT_LONG_DOUBLE_LONG: typing.Final = "stldl"
    STRUCT_FLOAT_DOUBLE_FLOAT: typing.Final = "stfdf"
    UNION_CHAR: typing.Final = "unsc"
    UNION_SHORT: typing.Final = "unss"
    UNION_INT: typing.Final = "unsi"
    UNION_LONG: typing.Final = "unsl"
    UNION_FLOAT: typing.Final = "unsf"
    UNION_DOUBLE: typing.Final = "unsd"
    UNION_LONG_LONG: typing.Final = "unsll"
    UNION_INT_LONG: typing.Final = "unpil"
    UNION_FLOAT_DOUBLE: typing.Final = "unpfd"
    UNION_INT_FLOAT: typing.Final = "unpif"
    UNION_LONG_DOUBLE: typing.Final = "unpld"
    UNION_INT_DOUBLE: typing.Final = "unpid"
    UNION_LONG_FLOAT: typing.Final = "unplf"
    UNION_STRUCT_INT: typing.Final = "unsti"
    UNION_STRUCT_FLOAT: typing.Final = "unstf"
    UNION_MIXED_STRUCT_INTEGRAL: typing.Final = "unmsti"
    UNION_MIXED_STRUCT_FLOATING: typing.Final = "unmstf"
    UNION_MIXED_STRUCT_ALL_SMALL: typing.Final = "unmstas"
    UNION_MIXED_STRUCT_ALL_LARGE: typing.Final = "unmstal"
    UNION_STRUCT_TRIP_CHAR: typing.Final = "unsttc"
    UNION_STRUCT_TRIP_SHORT: typing.Final = "unstts"
    PARAMS_PRIMITIVE_IDENTICAL: typing.Final = "paramsPrimitiveIdentical"
    PARAMS_PRIMITIVE_ALTERNATE: typing.Final = "paramsPrimitiveAlternate"
    PARAMS_MISC: typing.Final = "paramsMisc"
    PARAMS_VARIADIC: typing.Final = "paramsVariadic"
    PARAMS_SINGLETON_STRUCT: typing.Final = "paramsSingletonStruct"
    PARAMS_PAIR_STRUCT: typing.Final = "paramsPairStruct"
    PARAMS_TRIP_STRUCT: typing.Final = "paramsTripStruct"
    PARAMS_QUAD_STRUCT: typing.Final = "paramsQuadStruct"
    PARAMS_MIXED_STRUCT: typing.Final = "paramsMixedStruct"
    PARAMS_UNION: typing.Final = "paramsUnion"
    PRODUCER: typing.Final = "producer"
    EXTERNAL: typing.Final = "external"
    RETURN_PRIMITIVE: typing.Final = "returnPrimitive"
    RETURN_SINGLETON: typing.Final = "returnSingleton"
    RETURN_PAIR: typing.Final = "returnPair"
    RETURN_TRIPLE: typing.Final = "returnTriple"
    RETURN_QUAD: typing.Final = "returnQuad"
    RETURN_MIXED: typing.Final = "returnMixed"
    RETURN_UNION: typing.Final = "returnUnion"

    def __init__(self) -> None:
        ...


class CSpecPrototypeTestUtil(java.lang.Object):
    """
    Utility for testing prototype models defined in cspec files.
    """

    class TestResult(java.lang.Record):

        class_: typing.ClassVar[java.lang.Class]

        def __init__(self, message: typing.Union[java.lang.String, str], hasError: typing.Union[jpype.JBoolean, bool]) -> None:
            ...

        def equals(self, o: java.lang.Object) -> bool:
            ...

        def hasError(self) -> bool:
            ...

        def hashCode(self) -> int:
            ...

        def message(self) -> str:
            ...

        def toString(self) -> str:
            ...


    class_: typing.ClassVar[java.lang.Class]

    def __init__(self) -> None:
        ...

    @staticmethod
    def applyInfoFromSourceIfNeeded(program: ghidra.program.model.listing.Program, model: ghidra.program.model.lang.PrototypeModel) -> None:
        """
        Parses function definitions and data types of global variables from the source code and 
        applies them to the binary. Also applies the correct signature overrides to calls of 
        variadic functions.
        
        :param ghidra.program.model.listing.Program program: Program produced from the source code being parsed.
        :param ghidra.program.model.lang.PrototypeModel model: The PrototypeModel of the program.
        :raises ParseException: when the c source code cannot be parsed.
        :raises IOException: when the c source code cannot be parsed.
        :raises ghidra.app.util.cparser.CPP.ParseException: when the c source code cannot be parsed.
        :raises CodeUnitInsertionException: When code units cannot be created at the given address.
        """

    @staticmethod
    def getAdjustedCalleeName(calleeName: typing.Union[java.lang.String, str]) -> str:
        """
        Adjusts the name of a function to remove characters prepended by compilers.
        
        :param java.lang.String or str calleeName: the name of the function
        :return: String the name of the function after it has been adjusted
        :rtype: str
        """

    @staticmethod
    def getExtendedValue(value: jpype.JArray[jpype.JByte], dt: ghidra.program.model.data.DataType, joinPiece: ghidra.program.model.pcode.Varnode, dataConverter: ghidra.util.DataConverter, logger: java.util.function.Consumer[java.lang.String]) -> jpype.JArray[jpype.JByte]:
        """
        Extends the byte representation of values from their original DataType to the DataType that 
        is indicated by the joinPiece Varnode's size.
        
        :param jpype.JArray[jpype.JByte] value: the raw byte array of the original value
        :param ghidra.program.model.data.DataType dt: the source data type (e.g., FloatDataType, DoubleDataType, or Structure)
        :param ghidra.program.model.pcode.Varnode joinPiece: representing the target storage, used to determine target size
        :param ghidra.util.DataConverter dataConverter: the converter used to determine endianness
        :param java.util.function.Consumer[java.lang.String] logger: ``Consumer<String>`` lambda function to print logging information
        :return: byte[] a byte array containing the extended value,
        :rtype: jpype.JArray[jpype.JByte]
        """

    @staticmethod
    def getFirstCall(function: ghidra.program.model.listing.Function) -> ghidra.program.model.listing.Function:
        """
        Returns the function that calls the given function first.
        
        :param ghidra.program.model.listing.Function function: the callee which is searched for
        :return: Function the caller which is first
        :rtype: ghidra.program.model.listing.Function
        """

    @staticmethod
    def getParameterPieces(caller: ghidra.program.model.listing.Function, callee: ghidra.program.model.listing.Function, model: ghidra.program.model.lang.PrototypeModel) -> java.util.ArrayList[ghidra.program.model.lang.ParameterPieces]:
        """
        Gets the parameters between a caller and callee and organizes them in a PrototypePieces 
        object by prototypeModel. ParameterPieces may be spread between them depending on the calling
        convention being used.
        
        :param ghidra.program.model.listing.Function caller: The function that calls the callee.
        :param ghidra.program.model.listing.Function callee: The function being called by the caller.
        :param ghidra.program.model.lang.PrototypeModel model: PrototypeModel corresponding to the calling convention.
        :return: ``ArrayList<ParameterPieces>``
        :rtype: java.util.ArrayList[ghidra.program.model.lang.ParameterPieces]
        """

    @staticmethod
    def getPassedValues(func: ghidra.program.model.listing.Function, pieces: java.util.List[ghidra.program.model.lang.ParameterPieces], dataConverter: ghidra.util.DataConverter, logger: java.util.function.Consumer[java.lang.String]) -> java.util.List[jpype.JArray[jpype.JByte]]:
        """
        For a given function, and list of parameter pieces, return a list of bytes representing the 
        values of the parameters. This data is produced from the source code of the binary which is 
        used in cspec tests to compare against the list of bytes representing parameter values from 
        the emulator.
        
        :param ghidra.program.model.listing.Function func: Function to get the parameter values of.
        :param java.util.List[ghidra.program.model.lang.ParameterPieces] pieces: ParameterPieces representing basic elements of the parameters of the function.
        :param ghidra.util.DataConverter dataConverter: used to convert data to bytes and vice versa.
        :param java.util.function.Consumer[java.lang.String] logger: ``Consumer<String>`` lambda function to print logging information
        :return: ``List<byte[]>`` byte representation of function parameter values
        :rtype: java.util.List[jpype.JArray[jpype.JByte]]
        :raises MemoryAccessException: if there is a problem accessing the function's program memory.
        """

    @staticmethod
    def getProtoModelToTest(program: ghidra.program.model.listing.Program, langComp: ghidra.program.model.lang.LanguageCompilerSpecPair) -> ghidra.program.model.lang.PrototypeModel:
        """
        Returns the PrototypeModel from the compiler spec of the given LanguageCompilerSpecPair and 
        calling convention specified in the program's name.
        
        :param ghidra.program.model.listing.Program program: Program whose name contains the desired calling convention
        :param ghidra.program.model.lang.LanguageCompilerSpecPair langComp: the language/compiler specification pair to query
        :return: PrototypeModel Model corresponding to the extracted calling convention
        :rtype: ghidra.program.model.lang.PrototypeModel
        :raises CompilerSpecNotFoundException: if the compiler specification cannot be found/loaded
        :raises LanguageNotFoundException: if the specified language is not available
        """

    @staticmethod
    def getTestResult(callee: ghidra.program.model.listing.Function, caller: ghidra.program.model.listing.Function, pieces: java.util.ArrayList[ghidra.program.model.lang.ParameterPieces], fromEmulator: java.util.List[jpype.JArray[jpype.JByte]], groundTruth: java.util.List[jpype.JArray[jpype.JByte]]) -> CSpecPrototypeTestUtil.TestResult:
        """
        Returns a TestResult record that includes a message detailing the differences between
        parameter data in the c source code, and parameter data in the Ghidra emulator between a
        specific caller function and callee function.
        
        :param ghidra.program.model.listing.Function caller: The function that calls the callee.
        :param ghidra.program.model.listing.Function callee: The function being called by the caller.
        :param java.util.ArrayList[ghidra.program.model.lang.ParameterPieces] pieces: ``ArrayList<ParameterPieces>`` representing basic elements of the parameters 
        between callers and callees.
        :param java.util.List[jpype.JArray[jpype.JByte]] fromEmulator: Byte list representing parameter values from the emulator.
        :param java.util.List[jpype.JArray[jpype.JByte]] groundTruth: Byte list representing parameter values from the c source code.
        :return: TestResult result record object that contains a message and a boolean hasError.
        :rtype: CSpecPrototypeTestUtil.TestResult
        """

    @staticmethod
    def getVarArgsParamTypes(func: ghidra.program.model.listing.Function) -> java.util.List[ghidra.program.model.data.DataType]:
        """
        All functions in the source code for these Cspec tests are named in such a way that the
        parameter types of the function are encoded in the name. This function decodes the
        function names to retrieve the function parameter types as a list.
        
        :param ghidra.program.model.listing.Function func: The function to decode into it's parameter's datatypes
        :return: ``List<DataType>`` the datatypes of the parameters of the function.
        :rtype: java.util.List[ghidra.program.model.data.DataType]
        """

    @staticmethod
    def readEmulatorMemory(emulatorThread: ghidra.pcode.emu.PcodeThread[jpype.JArray[jpype.JByte]], address: ghidra.program.model.address.Address, size: typing.Union[jpype.JInt, int]) -> jpype.JArray[jpype.JByte]:
        """
        Reads data from emulator's memory at the given Address and for the given size and returns as
        a byte array.
        
        :param ghidra.pcode.emu.PcodeThread[jpype.JArray[jpype.JByte]] emulatorThread: the active emulator thread to inspect
        :param ghidra.program.model.address.Address address: Address of memory to read
        :param jpype.JInt or int size: Size of memory chunk to read
        :return: byte[] containing the data read from the emulator's memory
        :rtype: jpype.JArray[jpype.JByte]
        """

    @staticmethod
    def readEmulatorStack(emulatorThread: ghidra.pcode.emu.PcodeThread[jpype.JArray[jpype.JByte]], stackReg: ghidra.program.model.lang.Register, addrSpace: ghidra.program.model.address.AddressSpace, offset: typing.Union[jpype.JInt, int], size: typing.Union[jpype.JInt, int], dataConverter: ghidra.util.DataConverter) -> jpype.JArray[jpype.JByte]:
        """
        Reads data from the emulator's stack memory by resolving the current stack pointer 
        and applying a specified offset.
        
        :param ghidra.pcode.emu.PcodeThread[jpype.JArray[jpype.JByte]] emulatorThread: the active emulator thread to inspect
        :param ghidra.program.model.lang.Register stackReg: the register acting as the stack pointer
        :param ghidra.program.model.address.AddressSpace addrSpace: the address space where the stack resides
        :param jpype.JInt or int offset: the byte offset from the stack pointer
        :param jpype.JInt or int size: the number of bytes to read from the stack
        :param ghidra.util.DataConverter dataConverter: the converter used to interpret the stack pointer's endianness
        :return: byte[] containing the data read from the emulator's memory
        :rtype: jpype.JArray[jpype.JByte]
        :raises java.lang.Exception: if the register cannot be read or the address is invalid within the state
        """

    @staticmethod
    def readParameterPieces(emulatorThread: ghidra.pcode.emu.PcodeThread[jpype.JArray[jpype.JByte]], piece: ghidra.program.model.lang.ParameterPieces, addrSpace: ghidra.program.model.address.AddressSpace, stackReg: ghidra.program.model.lang.Register, langCompPair: ghidra.program.model.lang.LanguageCompilerSpecPair, dataConverter: ghidra.util.DataConverter) -> jpype.JArray[jpype.JByte]:
        """
        Returns a byte array that represents parameters from the emulator.
        This data is used to compare against the representation of parameters constructed from
        the binary's source code.
        
        :param ghidra.pcode.emu.PcodeThread[jpype.JArray[jpype.JByte]] emulatorThread: the active emulator thread to inspect
        :param ghidra.program.model.lang.ParameterPieces piece: basic elements of a parameter
        :param ghidra.program.model.address.AddressSpace addrSpace: the address space where the stack resides
        :param ghidra.program.model.lang.Register stackReg: the register acting as the stack pointer
        :param ghidra.program.model.lang.LanguageCompilerSpecPair langCompPair: the language/compiler specification pair
        :param ghidra.util.DataConverter dataConverter: used to determine endianness and convert data to byte representation.
        :return: byte[] byte array representation of parameter pieces
        :rtype: jpype.JArray[jpype.JByte]
        :raises java.lang.Exception: if there is a problem reading the emulator stack or getting the correct
        language.
        """


class CSpecTestPCodeEmulator(ghidra.pcode.emu.PcodeEmulator):
    """
    An extension of :obj:`PcodeEmulator` that can load program memory and set up the emulator 
    to run at a specific function entry point.
    """

    class_: typing.ClassVar[java.lang.Class]

    @typing.overload
    def __init__(self, lang: ghidra.program.model.lang.Language) -> None:
        ...

    @typing.overload
    def __init__(self, lang: ghidra.program.model.lang.Language, traceDisabled: typing.Union[jpype.JBoolean, bool], traceLevel: typing.Union[jpype.JInt, int]) -> None:
        ...

    @typing.overload
    def __init__(self, lang: ghidra.program.model.lang.Language, traceDisabled: typing.Union[jpype.JBoolean, bool], traceLevel: typing.Union[jpype.JInt, int], logger: java.util.function.Consumer[java.lang.String]) -> None:
        ...

    def prepareFunction(self, func: ghidra.program.model.listing.Function) -> ghidra.pcode.emu.PcodeThread[jpype.JArray[jpype.JByte]]:
        """
        Load the function entry point context registers into emulator, create stack space,
        set program counter. Return a emulator thread ready for a run() call
        
        :param ghidra.program.model.listing.Function func: The function to prepare the emulator to run.
        :return: ``PcodeThread<byte[]>``
        :rtype: ghidra.pcode.emu.PcodeThread[jpype.JArray[jpype.JByte]]
        """



__all__ = ["CSpecPrototypeTest", "CSpecPrototypeTestConstants", "CSpecPrototypeTestUtil", "CSpecTestPCodeEmulator"]
