// Headless command bridge for AI-driven Ghidra usage.
//@category AI

import java.io.File;
import java.io.FileWriter;
import java.io.PrintWriter;
import java.io.StringWriter;
import java.nio.charset.StandardCharsets;
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Base64;
import java.util.HashSet;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;

import ghidra.app.cmd.function.ApplyFunctionSignatureCmd;
import ghidra.app.cmd.function.FunctionRenameOption;
import ghidra.app.decompiler.DecompInterface;
import ghidra.app.decompiler.DecompileOptions;
import ghidra.app.decompiler.DecompileResults;
import ghidra.app.plugin.assembler.Assembler;
import ghidra.app.plugin.assembler.Assemblers;
import ghidra.app.script.GhidraScript;
import ghidra.app.util.parser.FunctionSignatureParser;
import ghidra.program.model.address.Address;
import ghidra.program.model.address.AddressSet;
import ghidra.program.model.data.CategoryPath;
import ghidra.program.model.data.DataType;
import ghidra.program.model.data.DataTypeComponent;
import ghidra.program.model.data.DataTypeConflictHandler;
import ghidra.program.model.data.DataTypeManager;
import ghidra.program.model.data.DataUtilities;
import ghidra.program.model.data.FunctionDefinitionDataType;
import ghidra.program.model.data.Structure;
import ghidra.program.model.data.StructureDataType;
import ghidra.program.model.listing.CodeUnit;
import ghidra.program.model.listing.CommentType;
import ghidra.program.model.listing.Data;
import ghidra.program.model.listing.DataIterator;
import ghidra.program.model.listing.Function;
import ghidra.program.model.listing.FunctionIterator;
import ghidra.program.model.listing.Instruction;
import ghidra.program.model.listing.InstructionIterator;
import ghidra.program.model.listing.Parameter;
import ghidra.program.model.listing.Variable;
import ghidra.program.model.mem.Memory;
import ghidra.program.model.mem.MemoryBlock;
import ghidra.program.model.symbol.Reference;
import ghidra.program.model.symbol.ReferenceIterator;
import ghidra.program.model.symbol.SourceType;
import ghidra.program.model.symbol.Symbol;
import ghidra.program.model.symbol.SymbolIterator;
import ghidra.program.model.symbol.SymbolTable;
import ghidra.util.data.DataTypeParser;
import ghidra.util.data.DataTypeParser.AllowedDataTypes;

public class AiCommandScript extends GhidraScript {

	private static final int DEFAULT_LIMIT = 100;
	private static final String ENCODED_ARG_PREFIX = "__b64_";

	private interface TxAction {
		Object run() throws Exception;
	}

	@Override
	protected void run() throws Exception {
		Map<String, String> opts = parseArgs(getScriptArgs());
		Map<String, Object> root = new LinkedHashMap<>();
		String command = normalizeCommand(option(opts, "cmd", "summary"));
		root.put("command", command);

		try {
			if (currentProgram == null) {
				throw new IllegalStateException("No current program is open");
			}
			root.put("ok", true);
			root.put("program", programInfo(false));
			root.put("data", dispatch(command, opts));
		}
		catch (Throwable t) {
			root.put("ok", false);
			root.put("error", t.toString());
			root.put("stack", stackTrace(t));
		}

		writeResult(opts, root);
	}

	private Object dispatch(String command, Map<String, String> opts) throws Exception {
		switch (command) {
			case "summary":
			case "info":
				return programInfo(true);
			case "list_functions":
			case "functions":
				return listFunctions(opts);
			case "function_info":
				return functionInfo(resolveFunction(opts), true);
			case "list_variables":
			case "variables":
				return listVariables(opts);
			case "decompile":
				return decompile(opts);
			case "disassemble":
			case "disasm":
				return disassemble(opts);
			case "xrefs_to":
				return xrefsTo(opts);
			case "xrefs_from":
				return xrefsFrom(opts);
			case "function_refs":
				return functionRefs(opts);
			case "callers":
				return callers(opts);
			case "callees":
				return callees(opts);
			case "call_graph":
				return callGraph(opts);
			case "strings":
				return strings(opts);
			case "symbols":
				return symbols(opts, false);
			case "imports":
			case "externals":
				return symbols(opts, true);
			case "search_bytes":
			case "find_bytes":
				return searchBytes(opts);
			case "read_memory":
			case "bytes":
				return readMemory(opts);
			case "rename_function":
				return inTransaction("rename function", () -> renameFunction(opts));
			case "rename_symbol":
				return inTransaction("rename symbol", () -> renameSymbol(opts));
			case "create_label":
				return inTransaction("create label", () -> createLabel(opts));
			case "delete_symbol":
				return inTransaction("delete symbol", () -> deleteSymbol(opts));
			case "set_comment":
				return inTransaction("set comment", () -> setComment(opts));
			case "set_function_signature":
			case "apply_signature":
				return inTransaction("set function signature", () -> setFunctionSignature(opts));
			case "set_return_type":
				return inTransaction("set return type", () -> setReturnType(opts));
			case "set_calling_convention":
				return inTransaction("set calling convention", () -> setCallingConvention(opts));
			case "set_function_flag":
				return inTransaction("set function flag", () -> setFunctionFlag(opts));
			case "set_variable_type":
				return inTransaction("set variable type", () -> setVariableType(opts));
			case "rename_variable":
				return inTransaction("rename variable", () -> renameVariable(opts));
			case "set_variable_comment":
				return inTransaction("set variable comment", () -> setVariableComment(opts));
			case "create_struct":
				return inTransaction("create struct", () -> createStruct(opts));
			case "apply_type":
			case "create_data":
				return inTransaction("apply type", () -> applyType(opts));
			case "patch_bytes":
				return inTransaction("patch bytes", () -> patchBytes(opts));
			case "assemble":
				return inTransaction("assemble", () -> assemble(opts));
			case "create_function":
				return inTransaction("create function", () -> createFunctionCommand(opts));
			case "remove_function":
			case "delete_function":
				return inTransaction("remove function", () -> removeFunctionCommand(opts));
			case "clear_listing":
			case "clear_code_units":
				return inTransaction("clear listing", () -> clearListingCommand(opts));
			case "disassemble_at":
				return inTransaction("disassemble at", () -> disassembleAt(opts));
			case "analysis_options":
			case "list_analysis_options":
				return analysisOptions(opts);
			case "set_analysis_option":
			case "set_analysis_options":
				return inTransaction("set analysis option", () -> setAnalysisOptionsCommand(opts));
			case "run_analysis":
			case "analyze":
				return runAnalysis(opts);
			case "save":
				return saveProgram(opts);
			case "export_c":
				return exportC(opts);
			case "export_functions_json":
				return listFunctions(opts);
			case "export_strings_json":
				return strings(opts);
			case "export_report":
				return exportReport(opts);
			default:
				throw new IllegalArgumentException("Unsupported command: " + command);
		}
	}

	private Object inTransaction(String description, TxAction action) throws Exception {
		int tx = currentProgram.startTransaction(description);
		boolean commit = false;
		try {
			Object result = action.run();
			commit = true;
			return result;
		}
		finally {
			currentProgram.endTransaction(tx, commit);
		}
	}

	private Map<String, Object> programInfo(boolean includeBlocks) {
		Map<String, Object> data = new LinkedHashMap<>();
		data.put("name", currentProgram.getName());
		data.put("executable_path", currentProgram.getExecutablePath());
		data.put("executable_format", currentProgram.getExecutableFormat());
		data.put("language", currentProgram.getLanguageID().toString());
		data.put("compiler", currentProgram.getCompilerSpec().getCompilerSpecID().toString());
		data.put("image_base", addr(currentProgram.getImageBase()));
		data.put("min_address", addr(currentProgram.getMinAddress()));
		data.put("max_address", addr(currentProgram.getMaxAddress()));
		data.put("function_count", currentProgram.getFunctionManager().getFunctionCount());
		data.put("symbol_count", currentProgram.getSymbolTable().getNumSymbols());
		if (includeBlocks) {
			List<Object> blocks = new ArrayList<>();
			for (MemoryBlock block : currentProgram.getMemory().getBlocks()) {
				Map<String, Object> b = new LinkedHashMap<>();
				b.put("name", block.getName());
				b.put("start", addr(block.getStart()));
				b.put("end", addr(block.getEnd()));
				b.put("size", block.getSize());
				b.put("read", block.isRead());
				b.put("write", block.isWrite());
				b.put("execute", block.isExecute());
				blocks.add(b);
			}
			data.put("memory_blocks", blocks);
		}
		return data;
	}

	private Map<String, Object> listFunctions(Map<String, String> opts) {
		int limit = intOption(opts, "limit", DEFAULT_LIMIT);
		int offset = intOption(opts, "offset", 0);
		String filter = option(opts, "filter", "").toLowerCase();
		List<Object> rows = new ArrayList<>();
		int matched = 0;
		int returned = 0;
		FunctionIterator it = currentProgram.getFunctionManager().getFunctions(true);
		while (it.hasNext() && returned < limit) {
			Function f = it.next();
			if (!filter.isEmpty() && !f.getName().toLowerCase().contains(filter) &&
				!addr(f.getEntryPoint()).toLowerCase().contains(filter)) {
				continue;
			}
			if (matched++ < offset) {
				continue;
			}
			rows.add(functionInfo(f, false));
			returned++;
		}
		Map<String, Object> data = new LinkedHashMap<>();
		data.put("offset", offset);
		data.put("limit", limit);
		data.put("matched_before_limit", matched);
		data.put("functions", rows);
		return data;
	}

	private Map<String, Object> listVariables(Map<String, String> opts) throws Exception {
		Function f = resolveFunctionForVariable(opts);
		List<Object> rows = new ArrayList<>();
		String kind = optionAny(opts, "all", "var_kind", "kind").toLowerCase();
		if ("return".equals(kind) || "all".equals(kind)) {
			rows.add(variableInfo(f.getReturn(), "return"));
		}
		if ("param".equals(kind) || "parameter".equals(kind) || "all".equals(kind)) {
			for (Parameter p : f.getParameters()) {
				rows.add(variableInfo(p, "param"));
			}
		}
		if ("local".equals(kind) || "all".equals(kind)) {
			for (Variable v : f.getLocalVariables()) {
				rows.add(variableInfo(v, "local"));
			}
		}
		Map<String, Object> data = new LinkedHashMap<>();
		data.put("function", functionInfo(f, true));
		data.put("variables", rows);
		return data;
	}

	private Map<String, Object> decompile(Map<String, String> opts) throws Exception {
		Function f = resolveFunction(opts);
		int timeout = intOption(opts, "timeout", 30);
		Map<String, Object> data = functionInfo(f, true);
		Map<String, Object> dec = decompileFunction(f, timeout);
		data.putAll(dec);
		return data;
	}

	private Map<String, Object> decompileFunction(Function f, int timeout) throws Exception {
		DecompInterface decompiler = new DecompInterface();
		try {
			decompiler.setOptions(new DecompileOptions());
			if (!decompiler.openProgram(currentProgram)) {
				throw new IllegalStateException(decompiler.getLastMessage());
			}
			DecompileResults res = decompiler.decompileFunction(f, timeout, monitor);
			Map<String, Object> data = new LinkedHashMap<>();
			data.put("completed", res.decompileCompleted());
			data.put("message", res.getErrorMessage());
			data.put("c", res.getDecompiledFunction() == null ? "" : res.getDecompiledFunction().getC());
			return data;
		}
		finally {
			decompiler.closeProgram();
			decompiler.dispose();
		}
	}

	private Map<String, Object> disassemble(Map<String, String> opts) throws Exception {
		int limit = intOption(opts, "limit", DEFAULT_LIMIT);
		List<Object> rows = new ArrayList<>();
		InstructionIterator it;
		Function f = null;
		if (opts.containsKey("name") || opts.containsKey("address")) {
			f = resolveFunction(opts);
		}
		if (f != null && !opts.containsKey("address_only")) {
			it = currentProgram.getListing().getInstructions(f.getBody(), true);
		}
		else {
			Address a = parseAddr(required(opts, "address"));
			it = currentProgram.getListing().getInstructions(a, true);
		}
		while (it.hasNext() && rows.size() < limit) {
			rows.add(instructionInfo(it.next()));
		}
		Map<String, Object> data = new LinkedHashMap<>();
		if (f != null) {
			data.put("function", functionInfo(f, false));
		}
		data.put("instructions", rows);
		return data;
	}

	private Map<String, Object> xrefsTo(Map<String, String> opts) throws Exception {
		Address a = parseAddr(required(opts, "address"));
		int limit = intOption(opts, "limit", DEFAULT_LIMIT);
		List<Object> rows = new ArrayList<>();
		ReferenceIterator it = currentProgram.getReferenceManager().getReferencesTo(a);
		while (it.hasNext() && rows.size() < limit) {
			rows.add(referenceInfo(it.next()));
		}
		Map<String, Object> data = new LinkedHashMap<>();
		data.put("address", addr(a));
		data.put("references", rows);
		return data;
	}

	private Map<String, Object> xrefsFrom(Map<String, String> opts) throws Exception {
		Address a = parseAddr(required(opts, "address"));
		int limit = intOption(opts, "limit", DEFAULT_LIMIT);
		List<Object> rows = new ArrayList<>();
		for (Reference ref : currentProgram.getReferenceManager().getReferencesFrom(a)) {
			if (rows.size() >= limit) {
				break;
			}
			rows.add(referenceInfo(ref));
		}
		Map<String, Object> data = new LinkedHashMap<>();
		data.put("address", addr(a));
		data.put("references", rows);
		return data;
	}

	private Map<String, Object> functionRefs(Map<String, String> opts) throws Exception {
		Function f = resolveFunction(opts);
		int limit = intOption(opts, "limit", DEFAULT_LIMIT);
		List<Object> outgoing = new ArrayList<>();
		InstructionIterator it = currentProgram.getListing().getInstructions(f.getBody(), true);
		while (it.hasNext() && outgoing.size() < limit) {
			Instruction ins = it.next();
			for (Reference ref : currentProgram.getReferenceManager().getReferencesFrom(ins.getAddress())) {
				if (outgoing.size() >= limit) {
					break;
				}
				outgoing.add(referenceInfo(ref));
			}
		}
		List<Object> incoming = new ArrayList<>();
		ReferenceIterator refs = currentProgram.getReferenceManager().getReferencesTo(f.getEntryPoint());
		while (refs.hasNext() && incoming.size() < limit) {
			incoming.add(referenceInfo(refs.next()));
		}
		Map<String, Object> data = new LinkedHashMap<>();
		data.put("function", functionInfo(f, false));
		data.put("incoming", incoming);
		data.put("outgoing", outgoing);
		return data;
	}

	private Map<String, Object> callers(Map<String, String> opts) throws Exception {
		Function f = resolveFunction(opts);
		List<Object> rows = new ArrayList<>();
		for (Function caller : f.getCallingFunctions(monitor)) {
			rows.add(functionInfo(caller, false));
		}
		Map<String, Object> data = new LinkedHashMap<>();
		data.put("function", functionInfo(f, false));
		data.put("callers", rows);
		return data;
	}

	private Map<String, Object> callees(Map<String, String> opts) throws Exception {
		Function f = resolveFunction(opts);
		List<Object> rows = new ArrayList<>();
		for (Function callee : f.getCalledFunctions(monitor)) {
			rows.add(functionInfo(callee, false));
		}
		Map<String, Object> data = new LinkedHashMap<>();
		data.put("function", functionInfo(f, false));
		data.put("callees", rows);
		return data;
	}

	private Map<String, Object> callGraph(Map<String, String> opts) throws Exception {
		Function start = resolveFunction(opts);
		int depth = intOption(opts, "depth", 2);
		int limit = intOption(opts, "limit", 500);
		Map<String, Object> nodes = new LinkedHashMap<>();
		List<Object> edges = new ArrayList<>();
		Set<String> seen = new HashSet<>();
		ArrayDeque<Object[]> queue = new ArrayDeque<>();
		queue.add(new Object[] { start, Integer.valueOf(0) });
		while (!queue.isEmpty() && nodes.size() < limit) {
			Object[] item = queue.removeFirst();
			Function f = (Function) item[0];
			int d = ((Integer) item[1]).intValue();
			String id = addr(f.getEntryPoint());
			if (seen.add(id)) {
				nodes.put(id, functionInfo(f, false));
			}
			if (d >= depth) {
				continue;
			}
			for (Function callee : f.getCalledFunctions(monitor)) {
				Map<String, Object> edge = new LinkedHashMap<>();
				edge.put("from", id);
				edge.put("to", addr(callee.getEntryPoint()));
				edges.add(edge);
				if (!seen.contains(addr(callee.getEntryPoint()))) {
					queue.addLast(new Object[] { callee, Integer.valueOf(d + 1) });
				}
				if (nodes.size() + queue.size() >= limit) {
					break;
				}
			}
		}
		Map<String, Object> data = new LinkedHashMap<>();
		data.put("start", functionInfo(start, false));
		data.put("depth", depth);
		data.put("nodes", new ArrayList<Object>(nodes.values()));
		data.put("edges", edges);
		return data;
	}

	private Map<String, Object> strings(Map<String, String> opts) {
		int limit = intOption(opts, "limit", DEFAULT_LIMIT);
		int minLen = intOption(opts, "min", 1);
		String filter = option(opts, "filter", "");
		List<Object> rows = new ArrayList<>();
		DataIterator it = currentProgram.getListing().getDefinedData(true);
		while (it.hasNext() && rows.size() < limit) {
			Data d = it.next();
			if (!d.hasStringValue()) {
				continue;
			}
			Object value = d.getValue();
			String s = value == null ? "" : value.toString();
			if (s.length() < minLen || (!filter.isEmpty() && !s.contains(filter))) {
				continue;
			}
			Map<String, Object> row = new LinkedHashMap<>();
			row.put("address", addr(d.getAddress()));
			row.put("length", s.length());
			row.put("value", s);
			row.put("datatype", d.getDataType().getName());
			rows.add(row);
		}
		Map<String, Object> data = new LinkedHashMap<>();
		data.put("strings", rows);
		return data;
	}

	private Map<String, Object> symbols(Map<String, String> opts, boolean externalOnly) {
		int limit = intOption(opts, "limit", DEFAULT_LIMIT);
		int offset = intOption(opts, "offset", 0);
		String filter = option(opts, "filter", "").toLowerCase();
		List<Object> rows = new ArrayList<>();
		int matched = 0;
		SymbolIterator it = externalOnly ? currentProgram.getSymbolTable().getExternalSymbols()
				: currentProgram.getSymbolTable().getAllSymbols(true);
		while (it.hasNext() && rows.size() < limit) {
			Symbol s = it.next();
			String fullName = s.getName(true);
			if (!filter.isEmpty() && !fullName.toLowerCase().contains(filter) &&
				!addr(s.getAddress()).toLowerCase().contains(filter)) {
				continue;
			}
			if (matched++ < offset) {
				continue;
			}
			rows.add(symbolInfo(s));
		}
		Map<String, Object> data = new LinkedHashMap<>();
		data.put("symbols", rows);
		return data;
	}

	private Map<String, Object> searchBytes(Map<String, String> opts) throws Exception {
		byte[] pattern = parseHex(required(opts, "hex"));
		int limit = intOption(opts, "limit", DEFAULT_LIMIT);
		List<Object> rows = new ArrayList<>();
		Memory memory = currentProgram.getMemory();
		Address pos = opts.containsKey("address") ? parseAddr(opts.get("address"))
				: currentProgram.getMinAddress();
		Address end = opts.containsKey("end") ? parseAddr(opts.get("end"))
				: currentProgram.getMaxAddress();
		while (pos != null && rows.size() < limit) {
			Address found = memory.findBytes(pos, end, pattern, null, true, monitor);
			if (found == null) {
				break;
			}
			rows.add(addr(found));
			pos = found.add(1);
		}
		Map<String, Object> data = new LinkedHashMap<>();
		data.put("hex", hex(pattern));
		data.put("matches", rows);
		return data;
	}

	private Map<String, Object> readMemory(Map<String, String> opts) throws Exception {
		Address a = parseAddr(required(opts, "address"));
		int length = intOption(opts, "length", intOption(opts, "count", 64));
		byte[] buf = new byte[length];
		currentProgram.getMemory().getBytes(a, buf);
		Map<String, Object> data = new LinkedHashMap<>();
		data.put("address", addr(a));
		data.put("length", length);
		data.put("hex", hex(buf));
		return data;
	}

	private Map<String, Object> renameFunction(Map<String, String> opts) throws Exception {
		Function f = resolveFunction(opts);
		String oldName = f.getName();
		String newName = requiredAny(opts, "new_name", "new-name", "to", "value");
		f.setName(newName, parseSourceType(opts));
		Map<String, Object> data = functionInfo(f, true);
		data.put("old_name", oldName);
		return data;
	}

	private Map<String, Object> renameSymbol(Map<String, String> opts) throws Exception {
		Symbol s = resolveSymbol(opts);
		String oldName = s.getName(true);
		String newName = requiredAny(opts, "new_name", "new-name", "to", "value");
		s.setName(newName, parseSourceType(opts));
		Map<String, Object> data = symbolInfo(s);
		data.put("old_name", oldName);
		return data;
	}

	private Map<String, Object> createLabel(Map<String, String> opts) throws Exception {
		Address a = parseAddr(required(opts, "address"));
		String label = requiredAny(opts, "label", "new_name", "name");
		Symbol s = currentProgram.getSymbolTable().createLabel(a, label, parseSourceType(opts));
		if (boolOption(opts, "primary", false)) {
			s.setPrimary();
		}
		return symbolInfo(s);
	}

	private Map<String, Object> deleteSymbol(Map<String, String> opts) throws Exception {
		Symbol s = resolveSymbol(opts);
		Map<String, Object> data = symbolInfo(s);
		data.put("deleted", s.delete());
		return data;
	}

	private Map<String, Object> setComment(Map<String, String> opts) throws Exception {
		String target = optionAny(opts, "code", "target", "kind").toLowerCase();
		String comment = boolOption(opts, "clear", false) ? null
				: optionAny(opts, null, "comment", "text", "value");
		if (comment == null && !boolOption(opts, "clear", false)) {
			throw new IllegalArgumentException("Missing required script argument: comment");
		}
		CommentType type = parseCommentType(optionAny(opts, "eol", "comment_type", "comment-type", "type"));
		Map<String, Object> data = new LinkedHashMap<>();
		if ("function".equals(target) || opts.containsKey("function") ||
			opts.containsKey("function_comment")) {
			Function f = resolveFunctionForVariable(opts);
			if (type == CommentType.REPEATABLE) {
				f.setRepeatableComment(comment);
			}
			else {
				f.setComment(comment);
			}
			data.put("function", functionInfo(f, true));
			data.put("comment_type", type.toString());
			return data;
		}
		Address a = parseAddr(required(opts, "address"));
		currentProgram.getListing().setComment(a, type, comment);
		data.put("address", addr(a));
		data.put("comment_type", type.toString());
		data.put("comment", comment);
		return data;
	}

	private Map<String, Object> setFunctionSignature(Map<String, String> opts) throws Exception {
		Function f = resolveFunction(opts);
		String signatureText = requiredAny(opts, "signature", "value");
		FunctionSignatureParser parser =
			new FunctionSignatureParser(currentProgram.getDataTypeManager(), null);
		FunctionDefinitionDataType signature = parser.parse(f.getSignature(), signatureText);
		FunctionRenameOption renameOption = boolOption(opts, "rename", true)
				? FunctionRenameOption.RENAME
				: FunctionRenameOption.NO_CHANGE;
		ApplyFunctionSignatureCmd cmd = new ApplyFunctionSignatureCmd(f.getEntryPoint(), signature,
			parseSourceType(opts), boolOption(opts, "preserve_calling_convention", false), false,
			DataTypeConflictHandler.DEFAULT_HANDLER, renameOption);
		if (!cmd.applyTo(currentProgram, monitor)) {
			throw new IllegalStateException("Failed to apply signature: " + cmd.getStatusMsg());
		}
		Function updated = currentProgram.getFunctionManager().getFunctionAt(f.getEntryPoint());
		return functionInfo(updated == null ? f : updated, true);
	}

	private Map<String, Object> setReturnType(Map<String, String> opts) throws Exception {
		Function f = resolveFunction(opts);
		DataType dt = parseDataType(requiredAny(opts, "type", "value"));
		f.setReturnType(dt, parseSourceType(opts));
		return functionInfo(f, true);
	}

	private Map<String, Object> setCallingConvention(Map<String, String> opts) throws Exception {
		Function f = resolveFunction(opts);
		String convention = requiredAny(opts, "calling_convention", "calling-convention", "value");
		f.setCallingConvention(convention);
		return functionInfo(f, true);
	}

	private Map<String, Object> setFunctionFlag(Map<String, String> opts) throws Exception {
		Function f = resolveFunction(opts);
		String flag = requiredAny(opts, "flag", "name").toLowerCase();
		boolean enabled = boolOption(opts, "enabled", boolOption(opts, "value", true));
		if ("noreturn".equals(flag) || "no_return".equals(flag)) {
			f.setNoReturn(enabled);
		}
		else if ("inline".equals(flag)) {
			f.setInline(enabled);
		}
		else if ("varargs".equals(flag) || "var_args".equals(flag)) {
			f.setVarArgs(enabled);
		}
		else if ("custom_storage".equals(flag)) {
			f.setCustomVariableStorage(enabled);
		}
		else {
			throw new IllegalArgumentException("Unsupported function flag: " + flag);
		}
		return functionInfo(f, true);
	}

	private Map<String, Object> setVariableType(Map<String, String> opts) throws Exception {
		Variable v = resolveVariable(opts);
		DataType dt = parseDataType(requiredAny(opts, "type", "value"));
		v.setDataType(dt, boolOption(opts, "align", true), boolOption(opts, "force", true),
			parseSourceType(opts));
		return variableInfo(v, optionAny(opts, "all", "var_kind", "kind"));
	}

	private Map<String, Object> renameVariable(Map<String, String> opts) throws Exception {
		Variable v = resolveVariable(opts);
		String oldName = v.getName();
		String newName = requiredAny(opts, "new_name", "new-name", "to", "value");
		v.setName(newName, parseSourceType(opts));
		Map<String, Object> data = variableInfo(v, optionAny(opts, "all", "var_kind", "kind"));
		data.put("old_name", oldName);
		return data;
	}

	private Map<String, Object> setVariableComment(Map<String, String> opts) throws Exception {
		Variable v = resolveVariable(opts);
		String comment = boolOption(opts, "clear", false) ? null : requiredAny(opts, "comment", "value");
		v.setComment(comment);
		return variableInfo(v, optionAny(opts, "all", "var_kind", "kind"));
	}

	private Map<String, Object> createStruct(Map<String, String> opts) throws Exception {
		String name = requiredAny(opts, "struct_name", "struct-name", "name");
		String categoryText = option(opts, "category", "/AI");
		int size = intOptionAny(opts, 0, "size", "length");
		CategoryPath category = new CategoryPath(categoryText);
		DataTypeManager dtm = currentProgram.getDataTypeManager();
		StructureDataType struct = new StructureDataType(category, name, size, dtm);
		String fields = option(opts, "fields", "");
		List<Object> fieldRows = new ArrayList<>();
		if (!fields.isEmpty()) {
			for (String fieldSpec : fields.split(";")) {
				fieldSpec = fieldSpec.trim();
				if (fieldSpec.isEmpty()) {
					continue;
				}
				fieldRows.add(addStructField(struct, fieldSpec));
			}
		}
		DataType resolved = dtm.addDataType(struct, conflictHandler(opts));
		Map<String, Object> data = dataTypeInfo(resolved);
		data.put("fields", fieldRows);
		return data;
	}

	private Map<String, Object> addStructField(Structure struct, String fieldSpec) throws Exception {
		String[] parts = fieldSpec.split(":", 5);
		Integer offset = null;
		String typeText;
		String name = null;
		String comment = null;
		int length = -1;
		if (parts.length >= 3 && looksInteger(parts[0])) {
			offset = Integer.valueOf(parseIntFlex(parts[0]));
			typeText = parts[1].trim();
			name = emptyToNull(parts[2].trim());
			if (parts.length >= 4 && !parts[3].trim().isEmpty()) {
				length = parseIntFlex(parts[3].trim());
			}
			if (parts.length >= 5) {
				comment = emptyToNull(parts[4].trim());
			}
		}
		else if (parts.length >= 2) {
			typeText = parts[0].trim();
			name = emptyToNull(parts[1].trim());
			if (parts.length >= 3 && !parts[2].trim().isEmpty()) {
				length = parseIntFlex(parts[2].trim());
			}
			if (parts.length >= 4) {
				comment = emptyToNull(parts[3].trim());
			}
		}
		else {
			int lastSpace = fieldSpec.trim().lastIndexOf(' ');
			if (lastSpace <= 0) {
				throw new IllegalArgumentException("Invalid field spec: " + fieldSpec);
			}
			typeText = fieldSpec.substring(0, lastSpace).trim();
			name = fieldSpec.substring(lastSpace + 1).trim();
		}
		DataType dt = parseDataType(typeText);
		int actualLength = length > 0 ? length : dt.getLength();
		if (offset != null) {
			int need = offset.intValue() + Math.max(actualLength, 1);
			if (need > struct.getLength()) {
				struct.growStructure(need - struct.getLength());
			}
			struct.replaceAtOffset(offset.intValue(), dt, length, name, comment);
		}
		else {
			struct.add(dt, length, name, comment);
		}
		Map<String, Object> row = new LinkedHashMap<>();
		row.put("offset", offset);
		row.put("name", name);
		row.put("type", dt.getDisplayName());
		row.put("length", length);
		row.put("comment", comment);
		return row;
	}

	private Map<String, Object> applyType(Map<String, String> opts) throws Exception {
		Address a = parseAddr(required(opts, "address"));
		DataType dt = parseDataType(requiredAny(opts, "type", "datatype", "value"));
		int length = intOption(opts, "length", -1);
		Data data = DataUtilities.createData(currentProgram, a, dt, length, parseClearDataMode(opts));
		return dataInfo(data);
	}

	private Map<String, Object> patchBytes(Map<String, String> opts) throws Exception {
		Address a = parseAddr(required(opts, "address"));
		byte[] bytes = parseHex(requiredAny(opts, "bytes", "hex", "value"));
		byte[] before = new byte[bytes.length];
		currentProgram.getMemory().getBytes(a, before);
		currentProgram.getMemory().setBytes(a, bytes);
		Map<String, Object> data = new LinkedHashMap<>();
		data.put("address", addr(a));
		data.put("length", bytes.length);
		data.put("before", hex(before));
		data.put("after", hex(bytes));
		return data;
	}

	private Map<String, Object> assemble(Map<String, String> opts) throws Exception {
		Address a = parseAddr(required(opts, "address"));
		String text = requiredAny(opts, "assembly", "asm", "value");
		String[] lines = splitAssembly(text);
		Assembler assembler = Assemblers.getAssembler(currentProgram);
		InstructionIterator it = assembler.assemble(a, lines);
		List<Object> rows = new ArrayList<>();
		while (it.hasNext()) {
			rows.add(instructionInfo(it.next()));
		}
		Map<String, Object> data = new LinkedHashMap<>();
		data.put("address", addr(a));
		data.put("assembly", text);
		data.put("instructions", rows);
		return data;
	}

	private Map<String, Object> createFunctionCommand(Map<String, String> opts) throws Exception {
		Address entry = parseAddr(requiredAny(opts, "entry", "address"));
		String name = optionAny(opts, null, "new_name", "name");
		Function f;
		if (opts.containsKey("body_start") || opts.containsKey("body_end")) {
			Address start = parseAddr(optionAny(opts, addr(entry), "body_start", "start"));
			Address end = parseAddr(requiredAny(opts, "body_end", "end", "end_address"));
			f = currentProgram.getFunctionManager().createFunction(name, entry, new AddressSet(start, end),
				name == null ? SourceType.DEFAULT : parseSourceType(opts));
		}
		else {
			f = createFunction(entry, name);
		}
		if (f == null) {
			throw new IllegalStateException("Function was not created at " + entry);
		}
		return functionInfo(f, true);
	}

	private Map<String, Object> removeFunctionCommand(Map<String, String> opts) throws Exception {
		Function f = resolveFunction(opts);
		Map<String, Object> data = functionInfo(f, false);
		data.put("removed", currentProgram.getFunctionManager().removeFunction(f.getEntryPoint()));
		return data;
	}

	private Map<String, Object> clearListingCommand(Map<String, String> opts) throws Exception {
		Address start = parseAddr(required(opts, "address"));
		Address end = opts.containsKey("end") ? parseAddr(opts.get("end"))
				: opts.containsKey("end_address") ? parseAddr(opts.get("end_address")) : start;
		boolean clearContext = boolOption(opts, "clear_context", true);
		currentProgram.getListing().clearCodeUnits(start, end, clearContext);
		Map<String, Object> data = new LinkedHashMap<>();
		data.put("start", addr(start));
		data.put("end", addr(end));
		data.put("clear_context", clearContext);
		return data;
	}

	private Map<String, Object> disassembleAt(Map<String, String> opts) throws Exception {
		Address a = parseAddr(required(opts, "address"));
		boolean ok = disassemble(a);
		Map<String, Object> data = new LinkedHashMap<>();
		data.put("address", addr(a));
		data.put("disassembled", ok);
		Instruction ins = currentProgram.getListing().getInstructionAt(a);
		if (ins != null) {
			data.put("instruction", instructionInfo(ins));
		}
		return data;
	}

	private Map<String, Object> analysisOptions(Map<String, String> opts) {
		Map<String, String> all = getCurrentAnalysisOptionsAndValues(currentProgram);
		String filter = option(opts, "filter", "").toLowerCase();
		Map<String, Object> rows = new LinkedHashMap<>();
		for (Map.Entry<String, String> e : all.entrySet()) {
			if (filter.isEmpty() || e.getKey().toLowerCase().contains(filter)) {
				rows.put(e.getKey(), e.getValue());
			}
		}
		Map<String, Object> data = new LinkedHashMap<>();
		data.put("analysis_options", rows);
		return data;
	}

	private Map<String, Object> setAnalysisOptionsCommand(Map<String, String> opts) {
		String name = requiredAny(opts, "analysis_option", "option", "name");
		String value = requiredAny(opts, "analysis_value", "value", "enabled");
		setAnalysisOption(currentProgram, name, value);
		Map<String, Object> data = new LinkedHashMap<>();
		data.put("option", name);
		data.put("value", value);
		return data;
	}

	private Map<String, Object> runAnalysis(Map<String, String> opts) {
		boolean changesOnly = boolOption(opts, "changes_only", false);
		if (changesOnly) {
			analyzeChanges(currentProgram);
		}
		else {
			analyzeAll(currentProgram);
		}
		Map<String, Object> data = new LinkedHashMap<>();
		data.put("changes_only", changesOnly);
		data.put("function_count", currentProgram.getFunctionManager().getFunctionCount());
		return data;
	}

	private Map<String, Object> saveProgram(Map<String, String> opts) throws Exception {
		String comment = option(opts, "comment", "Saved by Ghidra AI CLI");
		Map<String, Object> data = new LinkedHashMap<>();
		data.put("saved", true);
		data.put("save_mode", "headless_post_script");
		data.put("comment", comment);
		return data;
	}

	private Map<String, Object> exportC(Map<String, String> opts) throws Exception {
		int limit = intOption(opts, "limit", 20);
		int timeout = intOption(opts, "timeout", 30);
		String filter = option(opts, "filter", "").toLowerCase();
		List<Object> rows = new ArrayList<>();
		FunctionIterator it = currentProgram.getFunctionManager().getFunctions(true);
		while (it.hasNext() && rows.size() < limit) {
			Function f = it.next();
			if (!filter.isEmpty() && !f.getName().toLowerCase().contains(filter) &&
				!addr(f.getEntryPoint()).toLowerCase().contains(filter)) {
				continue;
			}
			Map<String, Object> row = functionInfo(f, true);
			row.putAll(decompileFunction(f, timeout));
			rows.add(row);
		}
		Map<String, Object> data = new LinkedHashMap<>();
		data.put("functions", rows);
		return data;
	}

	private Map<String, Object> exportReport(Map<String, String> opts) throws Exception {
		Map<String, Object> data = new LinkedHashMap<>();
		data.put("summary", programInfo(true));
		data.put("functions", listFunctions(opts).get("functions"));
		data.put("imports", symbols(opts, true).get("symbols"));
		data.put("strings", strings(opts).get("strings"));
		return data;
	}

	private Map<String, Object> functionInfo(Function f, boolean signature) {
		Map<String, Object> data = new LinkedHashMap<>();
		data.put("name", f.getName());
		data.put("entry", addr(f.getEntryPoint()));
		data.put("body_size", f.getBody().getNumAddresses());
		data.put("thunk", f.isThunk());
		data.put("external", f.isExternal());
		data.put("calling_convention", f.getCallingConventionName());
		data.put("noreturn", f.hasNoReturn());
		data.put("inline", f.isInline());
		data.put("varargs", f.hasVarArgs());
		if (signature) {
			data.put("signature", f.getSignature().toString());
			data.put("prototype", f.getPrototypeString(false, true));
			data.put("comment", f.getComment());
			data.put("repeatable_comment", f.getRepeatableComment());
		}
		return data;
	}

	private Map<String, Object> variableInfo(Variable v, String kind) {
		Map<String, Object> data = new LinkedHashMap<>();
		data.put("kind", kind);
		data.put("name", v.getName());
		data.put("type", v.getDataType().getDisplayName());
		data.put("length", v.getLength());
		data.put("storage", String.valueOf(v.getVariableStorage()));
		data.put("source", v.getSource().toString());
		data.put("comment", v.getComment());
		data.put("first_use_offset", v.getFirstUseOffset());
		data.put("stack", v.isStackVariable());
		data.put("register", v.isRegisterVariable());
		data.put("memory", v.isMemoryVariable());
		if (v.isStackVariable()) {
			data.put("stack_offset", v.getStackOffset());
		}
		if (v.getMinAddress() != null) {
			data.put("min_address", addr(v.getMinAddress()));
		}
		return data;
	}

	private Map<String, Object> symbolInfo(Symbol s) {
		Map<String, Object> row = new LinkedHashMap<>();
		row.put("id", s.getID());
		row.put("name", s.getName());
		row.put("full_name", s.getName(true));
		row.put("address", addr(s.getAddress()));
		row.put("type", s.getSymbolType().toString());
		row.put("source", s.getSource().toString());
		row.put("references", s.getReferenceCount());
		row.put("primary", s.isPrimary());
		row.put("dynamic", s.isDynamic());
		row.put("external", s.isExternal());
		return row;
	}

	private Map<String, Object> instructionInfo(Instruction ins) throws Exception {
		Map<String, Object> row = new LinkedHashMap<>();
		row.put("address", addr(ins.getAddress()));
		row.put("text", ins.toString());
		row.put("bytes", hex(ins.getBytes()));
		return row;
	}

	private Map<String, Object> referenceInfo(Reference ref) {
		Map<String, Object> row = new LinkedHashMap<>();
		row.put("from", addr(ref.getFromAddress()));
		row.put("to", addr(ref.getToAddress()));
		row.put("type", ref.getReferenceType().toString());
		row.put("operand_index", ref.getOperandIndex());
		row.put("primary", ref.isPrimary());
		return row;
	}

	private Map<String, Object> dataInfo(Data d) {
		Map<String, Object> data = new LinkedHashMap<>();
		data.put("address", addr(d.getAddress()));
		data.put("length", d.getLength());
		data.put("type", d.getDataType().getDisplayName());
		Object value = d.getValue();
		data.put("value", value == null ? null : value.toString());
		return data;
	}

	private Map<String, Object> dataTypeInfo(DataType dt) {
		Map<String, Object> data = new LinkedHashMap<>();
		data.put("name", dt.getName());
		data.put("display_name", dt.getDisplayName());
		data.put("path", dt.getPathName());
		data.put("length", dt.getLength());
		if (dt instanceof Structure) {
			List<Object> comps = new ArrayList<>();
			Structure s = (Structure) dt;
			for (DataTypeComponent c : s.getDefinedComponents()) {
				Map<String, Object> row = new LinkedHashMap<>();
				row.put("ordinal", c.getOrdinal());
				row.put("offset", c.getOffset());
				row.put("length", c.getLength());
				row.put("name", c.getFieldName());
				row.put("type", c.getDataType().getDisplayName());
				row.put("comment", c.getComment());
				comps.add(row);
			}
			data.put("components", comps);
		}
		return data;
	}

	private Function resolveFunctionForVariable(Map<String, String> opts) throws Exception {
		String fText = optionAny(opts, null, "function", "func");
		if (fText == null) {
			return resolveFunction(opts);
		}
		if (looksAddress(fText)) {
			Map<String, String> copy = new LinkedHashMap<>(opts);
			copy.put("address", fText);
			return resolveFunction(copy);
		}
		Map<String, String> copy = new LinkedHashMap<>(opts);
		copy.remove("address");
		copy.put("name", fText);
		return resolveFunction(copy);
	}

	private Function resolveFunction(Map<String, String> opts) throws Exception {
		if (opts.containsKey("address") || opts.containsKey("entry")) {
			Address a = parseAddr(optionAny(opts, null, "entry", "address"));
			Function f = currentProgram.getFunctionManager().getFunctionAt(a);
			if (f == null) {
				f = currentProgram.getFunctionManager().getFunctionContaining(a);
			}
			if (f == null) {
				throw new IllegalArgumentException("No function at or containing " + a);
			}
			return f;
		}
		String name = required(opts, "name");
		FunctionIterator it = currentProgram.getFunctionManager().getFunctions(true);
		while (it.hasNext()) {
			Function f = it.next();
			if (f.getName().equals(name) || f.getName().contains(name)) {
				return f;
			}
		}
		throw new IllegalArgumentException("No function matched name: " + name);
	}

	private Variable resolveVariable(Map<String, String> opts) throws Exception {
		Function f = resolveFunctionForVariable(opts);
		String kind = optionAny(opts, "all", "var_kind", "kind").toLowerCase();
		if ("return".equals(kind)) {
			return f.getReturn();
		}
		Variable[] vars;
		if ("param".equals(kind) || "parameter".equals(kind)) {
			vars = f.getParameters();
		}
		else if ("local".equals(kind)) {
			vars = f.getLocalVariables();
		}
		else {
			vars = f.getAllVariables();
		}
		if (opts.containsKey("index")) {
			int idx = parseIntFlex(opts.get("index"));
			if (idx < 0 || idx >= vars.length) {
				throw new IllegalArgumentException("Variable index out of range: " + idx);
			}
			return vars[idx];
		}
		String varName = requiredAny(opts, "var", "variable", "old_name");
		for (Variable v : vars) {
			if (v.getName().equals(varName)) {
				return v;
			}
		}
		for (Variable v : vars) {
			if (v.getName().contains(varName)) {
				return v;
			}
		}
		throw new IllegalArgumentException("No variable matched: " + varName);
	}

	private Symbol resolveSymbol(Map<String, String> opts) throws Exception {
		SymbolTable table = currentProgram.getSymbolTable();
		if (opts.containsKey("symbol_id") || opts.containsKey("id")) {
			long id = Long.parseLong(optionAny(opts, null, "symbol_id", "id"));
			Symbol s = table.getSymbol(id);
			if (s == null) {
				throw new IllegalArgumentException("No symbol id: " + id);
			}
			return s;
		}
		if (opts.containsKey("address")) {
			Address a = parseAddr(opts.get("address"));
			if (opts.containsKey("name")) {
				Symbol s = table.getGlobalSymbol(opts.get("name"), a);
				if (s != null) {
					return s;
				}
			}
			Symbol primary = table.getPrimarySymbol(a);
			if (primary != null) {
				return primary;
			}
			Symbol[] symbols = table.getSymbols(a);
			if (symbols.length > 0) {
				return symbols[0];
			}
			throw new IllegalArgumentException("No symbol at address: " + a);
		}
		String name = required(opts, "name");
		SymbolIterator it = table.getAllSymbols(true);
		while (it.hasNext()) {
			Symbol s = it.next();
			if (s.getName(true).equals(name) || s.getName().equals(name)) {
				return s;
			}
		}
		it = table.getAllSymbols(true);
		while (it.hasNext()) {
			Symbol s = it.next();
			if (s.getName(true).contains(name) || s.getName().contains(name)) {
				return s;
			}
		}
		throw new IllegalArgumentException("No symbol matched name: " + name);
	}

	private DataType parseDataType(String text) throws Exception {
		DataTypeManager dtm = currentProgram.getDataTypeManager();
		DataTypeParser parser = new DataTypeParser(dtm, dtm, null, AllowedDataTypes.ALL);
		return parser.parse(text);
	}

	private DataUtilities.ClearDataMode parseClearDataMode(Map<String, String> opts) {
		String text = optionAny(opts, "clear_all_conflict_data", "clear_mode", "clear-mode").toUpperCase();
		if ("CHECK".equals(text) || "CHECK_FOR_SPACE".equals(text)) {
			return DataUtilities.ClearDataMode.CHECK_FOR_SPACE;
		}
		if ("SINGLE".equals(text) || "CLEAR_SINGLE_DATA".equals(text)) {
			return DataUtilities.ClearDataMode.CLEAR_SINGLE_DATA;
		}
		if ("UNDEFINED".equals(text) || "CLEAR_ALL_UNDEFINED_CONFLICT_DATA".equals(text)) {
			return DataUtilities.ClearDataMode.CLEAR_ALL_UNDEFINED_CONFLICT_DATA;
		}
		if ("DEFAULT".equals(text) || "CLEAR_ALL_DEFAULT_CONFLICT_DATA".equals(text)) {
			return DataUtilities.ClearDataMode.CLEAR_ALL_DEFAULT_CONFLICT_DATA;
		}
		return DataUtilities.ClearDataMode.CLEAR_ALL_CONFLICT_DATA;
	}

	private DataTypeConflictHandler conflictHandler(Map<String, String> opts) {
		String text = option(opts, "conflict", "replace").toLowerCase();
		if ("keep".equals(text) || "use_existing".equals(text)) {
			return DataTypeConflictHandler.KEEP_HANDLER;
		}
		if ("rename".equals(text) || "add".equals(text)) {
			return DataTypeConflictHandler.DEFAULT_HANDLER;
		}
		return DataTypeConflictHandler.REPLACE_HANDLER;
	}

	private CommentType parseCommentType(String text) {
		String s = text.toUpperCase();
		if ("END_OF_LINE".equals(s)) {
			s = "EOL";
		}
		return CommentType.valueOf(s);
	}

	private SourceType parseSourceType(Map<String, String> opts) {
		String text = option(opts, "source", "USER_DEFINED").toUpperCase();
		if ("USER".equals(text)) {
			return SourceType.USER_DEFINED;
		}
		return SourceType.valueOf(text);
	}

	private String[] splitAssembly(String text) {
		List<String> lines = new ArrayList<>();
		for (String line : text.split("\\r?\\n|;")) {
			line = line.trim();
			if (!line.isEmpty()) {
				lines.add(line);
			}
		}
		return lines.toArray(new String[lines.size()]);
	}

	private Address parseAddr(String text) throws Exception {
		Address a = currentProgram.getAddressFactory().getAddress(text);
		if (a != null) {
			return a;
		}
		String s = text.toLowerCase();
		if (s.startsWith("0x")) {
			long v = Long.parseUnsignedLong(s.substring(2), 16);
			return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v);
		}
		long v = Long.parseUnsignedLong(s, 16);
		return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v);
	}

	private Map<String, String> parseArgs(String[] args) {
		Map<String, String> opts = new LinkedHashMap<>();
		for (int i = 0; i < args.length; i++) {
			String arg = args[i];
			int eq = arg.indexOf('=');
			if (eq > 0) {
				putArg(opts, arg.substring(0, eq), arg.substring(eq + 1));
				continue;
			}
			if (arg.startsWith("--")) {
				String key = arg.substring(2);
				String value = "true";
				if (i + 1 < args.length && !args[i + 1].startsWith("--")) {
					value = args[++i];
				}
				putArg(opts, key, value);
				continue;
			}
			if (i + 1 < args.length) {
				putArg(opts, arg, args[++i]);
			}
		}
		return opts;
	}

	private void putArg(Map<String, String> opts, String key, String value) {
		if (key.startsWith(ENCODED_ARG_PREFIX)) {
			opts.put(key.substring(ENCODED_ARG_PREFIX.length()), decodeArg(value));
			return;
		}
		opts.put(key, value);
	}

	private String decodeArg(String value) {
		String padded = value;
		int remainder = padded.length() % 4;
		if (remainder != 0) {
			padded += "====".substring(remainder);
		}
		byte[] bytes = Base64.getUrlDecoder().decode(padded);
		return new String(bytes, StandardCharsets.UTF_8);
	}

	private String normalizeCommand(String command) {
		return command.replace('-', '_').trim().toLowerCase();
	}

	private String required(Map<String, String> opts, String key) {
		String value = opts.get(key);
		if (value == null || value.isEmpty()) {
			throw new IllegalArgumentException("Missing required script argument: " + key);
		}
		return value;
	}

	private String requiredAny(Map<String, String> opts, String... keys) {
		for (String key : keys) {
			String value = opts.get(key);
			if (value != null && !value.isEmpty()) {
				return value;
			}
		}
		throw new IllegalArgumentException("Missing required script argument, one of: " + join(keys));
	}

	private String option(Map<String, String> opts, String key, String defaultValue) {
		String value = opts.get(key);
		return value == null ? defaultValue : value;
	}

	private String optionAny(Map<String, String> opts, String defaultValue, String... keys) {
		for (String key : keys) {
			String value = opts.get(key);
			if (value != null) {
				return value;
			}
		}
		return defaultValue;
	}

	private int intOption(Map<String, String> opts, String key, int defaultValue) {
		String value = opts.get(key);
		if (value == null || value.isEmpty()) {
			return defaultValue;
		}
		return parseIntFlex(value);
	}

	private int intOptionAny(Map<String, String> opts, int defaultValue, String... keys) {
		for (String key : keys) {
			String value = opts.get(key);
			if (value != null && !value.isEmpty()) {
				return parseIntFlex(value);
			}
		}
		return defaultValue;
	}

	private boolean boolOption(Map<String, String> opts, String key, boolean defaultValue) {
		String value = opts.get(key);
		if (value == null || value.isEmpty()) {
			return defaultValue;
		}
		String s = value.toLowerCase();
		return "1".equals(s) || "true".equals(s) || "yes".equals(s) || "on".equals(s);
	}

	private int parseIntFlex(String value) {
		String s = value.trim().toLowerCase();
		if (s.startsWith("0x")) {
			return Integer.parseUnsignedInt(s.substring(2), 16);
		}
		return Integer.parseInt(s);
	}

	private boolean looksInteger(String value) {
		try {
			parseIntFlex(value);
			return true;
		}
		catch (Exception e) {
			return false;
		}
	}

	private boolean looksAddress(String value) {
		return value != null && (value.startsWith("0x") || value.indexOf(':') >= 0 || value.matches("[0-9a-fA-F]{4,}"));
	}

	private String emptyToNull(String value) {
		return value == null || value.isEmpty() ? null : value;
	}

	private String join(String[] values) {
		StringBuilder sb = new StringBuilder();
		for (int i = 0; i < values.length; i++) {
			if (i > 0) {
				sb.append(", ");
			}
			sb.append(values[i]);
		}
		return sb.toString();
	}

	private void writeResult(Map<String, String> opts, Map<String, Object> root) throws Exception {
		String json = toJson(root);
		String output = opts.get("output");
		if (output != null && !output.isEmpty()) {
			try (FileWriter writer = new FileWriter(new File(output))) {
				writer.write(json);
				writer.write(System.lineSeparator());
			}
		}
		String out = opts.get("out");
		if (out == null || out.isEmpty()) {
			println(json);
			return;
		}
		try (FileWriter writer = new FileWriter(new File(out))) {
			writer.write(json);
			writer.write(System.lineSeparator());
		}
	}

	private String toJson(Object value) {
		if (value == null) {
			return "null";
		}
		if (value instanceof String) {
			return quote((String) value);
		}
		if (value instanceof Number || value instanceof Boolean) {
			return value.toString();
		}
		if (value instanceof Map) {
			StringBuilder sb = new StringBuilder();
			sb.append("{");
			boolean first = true;
			for (Object eObj : ((Map<?, ?>) value).entrySet()) {
				Map.Entry<?, ?> e = (Map.Entry<?, ?>) eObj;
				if (!first) {
					sb.append(",");
				}
				first = false;
				sb.append(quote(String.valueOf(e.getKey())));
				sb.append(":");
				sb.append(toJson(e.getValue()));
			}
			sb.append("}");
			return sb.toString();
		}
		if (value instanceof Iterable) {
			StringBuilder sb = new StringBuilder();
			sb.append("[");
			boolean first = true;
			for (Object item : (Iterable<?>) value) {
				if (!first) {
					sb.append(",");
				}
				first = false;
				sb.append(toJson(item));
			}
			sb.append("]");
			return sb.toString();
		}
		return quote(String.valueOf(value));
	}

	private String quote(String s) {
		StringBuilder sb = new StringBuilder();
		sb.append('"');
		for (int i = 0; i < s.length(); i++) {
			char c = s.charAt(i);
			switch (c) {
				case '"':
					sb.append("\\\"");
					break;
				case '\\':
					sb.append("\\\\");
					break;
				case '\b':
					sb.append("\\b");
					break;
				case '\f':
					sb.append("\\f");
					break;
				case '\n':
					sb.append("\\n");
					break;
				case '\r':
					sb.append("\\r");
					break;
				case '\t':
					sb.append("\\t");
					break;
				default:
					if (c < 0x20) {
						sb.append(String.format("\\u%04x", (int) c));
					}
					else {
						sb.append(c);
					}
			}
		}
		sb.append('"');
		return sb.toString();
	}

	private String addr(Address address) {
		return address == null ? null : address.toString();
	}

	private byte[] parseHex(String text) {
		String cleaned = text.replace("0x", "").replace("0X", "").replace("\\x", "")
				.replaceAll("[^0-9a-fA-F]", "");
		if ((cleaned.length() & 1) != 0) {
			throw new IllegalArgumentException("Hex string must have an even number of digits");
		}
		byte[] out = new byte[cleaned.length() / 2];
		for (int i = 0; i < out.length; i++) {
			out[i] = (byte) Integer.parseInt(cleaned.substring(i * 2, i * 2 + 2), 16);
		}
		return out;
	}

	private String hex(byte[] bytes) {
		StringBuilder sb = new StringBuilder();
		for (byte b : bytes) {
			sb.append(String.format("%02X", b & 0xff));
		}
		return sb.toString();
	}

	private String stackTrace(Throwable t) {
		StringWriter sw = new StringWriter();
		t.printStackTrace(new PrintWriter(sw));
		return sw.toString();
	}
}
