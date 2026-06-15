// Minimal TypeScript navigation helper using the TS compiler API.
// Usage:
//   node ts_navigation.js <repoRoot> <filePath> <line0> <character0>
//
// Prints a single JSON object to stdout:
// {
//   ok: boolean,
//   usageKind: "call" | "declaration" | "other",
//   definitionPath: string | null,
//   definitionRange: { start: { line, character }, end: { line, character } } | null,
//   fullDefSource: string | null,
//   nodeKind: string | null,
//   error: string | null
// }

const fs = require("fs");
const path = require("path");
const ts = require("typescript");

function defaultCompilerOptions() {
  return {
    module: ts.ModuleKind.CommonJS,
    target: ts.ScriptTarget.ES2020,
    jsx: ts.JsxEmit.React,
    allowJs: true,
    checkJs: true,
    strict: false,
    moduleResolution: ts.ModuleResolutionKind.NodeJs,
    resolveJsonModule: true,
  };
}

function applyN8nWorkflowPathAlias(options, repoRootAbs, projectRoot) {
  const workflowSrc = path.join(repoRootAbs, "packages", "workflow", "src");
  if (!fs.existsSync(workflowSrc)) {
    return;
  }
  options.paths = options.paths || {};
  if (options.paths["n8n-workflow"]) {
    return;
  }
  const base =
    options.baseUrl != null ? path.resolve(projectRoot, options.baseUrl) : projectRoot;
  let rel;
  try {
    rel = path.relative(base, workflowSrc);
  } catch (_) {
    rel = path.relative(projectRoot, workflowSrc);
  }
  options.paths["n8n-workflow"] = [rel.split(path.sep).join("/")];
}

function getProjectConfig(repoRoot, absFile) {
  const repoRootAbs = path.resolve(repoRoot);
  const absFileResolved = path.resolve(absFile);
  const fileDir = path.dirname(absFileResolved);

  let configPath =
    ts.findConfigFile(fileDir, ts.sys.fileExists, "tsconfig.json") ||
    ts.findConfigFile(fileDir, ts.sys.fileExists, "jsconfig.json");

  const rootConfigPath = path.join(repoRootAbs, "tsconfig.json");
  if (!configPath && fs.existsSync(rootConfigPath)) {
    configPath = rootConfigPath;
  }

  if (!configPath) {
    return {
      projectRoot: repoRootAbs,
      options: defaultCompilerOptions(),
      fileNames: [absFileResolved],
    };
  }

  const projectRoot = path.dirname(configPath);
  const configFile = ts.readConfigFile(configPath, ts.sys.readFile);
  if (configFile.error) {
    return {
      projectRoot,
      options: defaultCompilerOptions(),
      fileNames: [absFileResolved],
    };
  }

  const parsed = ts.parseJsonConfigFileContent(
    configFile.config,
    ts.sys,
    projectRoot,
    undefined,
    configPath,
  );

  const options = { ...(parsed.options || {}) };
  applyN8nWorkflowPathAlias(options, repoRootAbs, projectRoot);

  const fileNames =
    parsed.fileNames && parsed.fileNames.length
      ? Array.from(new Set(parsed.fileNames.concat([absFileResolved])))
      : [absFileResolved];

  return { projectRoot, options, fileNames };
}

function findNodeAt(sourceFile, pos) {
  function visit(node) {
    if (pos >= node.getStart(sourceFile, true) && pos < node.getEnd()) {
      return ts.forEachChild(node, visit) || node;
    }
    return undefined;
  }
  return visit(sourceFile) || sourceFile;
}

function classifyUsage(node) {
  let cur = node;
  while (cur) {
    if (ts.isCallExpression(cur) || ts.isNewExpression(cur)) return "call";
    if (
      ts.isFunctionDeclaration(cur) ||
      ts.isMethodDeclaration(cur) ||
      ts.isFunctionExpression(cur) ||
      ts.isArrowFunction(cur)
    ) {
      return "declaration";
    }
    cur = cur.parent;
  }
  return "other";
}

/** True if go-to-definition at this node is meaningful (do not replace with outer callee). */
function isDirectNavigationTarget(node) {
  if (!node) return false;
  if (
    ts.isIdentifier(node) ||
    ts.isPropertyAccessExpression(node) ||
    ts.isElementAccessExpression(node) ||
    ts.isCallExpression(node) ||
    ts.isNewExpression(node)
  ) {
    return true;
  }
  // Optional TS API guards (names differ across typescript package versions).
  if (typeof ts.isSuperKeyword === "function" && ts.isSuperKeyword(node)) return true;
  if (typeof ts.isThisExpression === "function" && ts.isThisExpression(node)) return true;
  if (typeof ts.isMetaProperty === "function" && ts.isMetaProperty(node)) return true;
  return false;
}

function pickBestDefinition(defs, repoRoot) {
  if (!defs || !defs.length) return undefined;
  const repoAbs = path.resolve(repoRoot);
  const scored = defs.map((d) => {
    const file = d.fileName;
    const abs = path.resolve(file);
    const isDts = abs.endsWith(".d.ts");
    const inNodeModules = abs.includes("node_modules");
    const inRepo = abs.startsWith(repoAbs);
    let score = 0;
    if (!isDts) score += 10;
    if (inRepo) score += 5;
    if (!inNodeModules) score += 2;
    return { def: d, score };
  });
  scored.sort((a, b) => b.score - a.score);
  return scored[0].def;
}

function extractFullDefinitionSource(def) {
  const fileText = fs.readFileSync(def.fileName, "utf8");
  const sourceFile = ts.createSourceFile(
    def.fileName,
    fileText,
    ts.ScriptTarget.Latest,
    true,
  );

  const start = def.textSpan.start;
  const end = start + def.textSpan.length;

  function findNode(node) {
    if (start >= node.getStart(sourceFile, true) && end <= node.getEnd()) {
      return ts.forEachChild(node, findNode) || node;
    }
    return undefined;
  }

  let node = findNode(sourceFile) || sourceFile;

  const isExternalDts =
    def.fileName.endsWith(".d.ts") || def.fileName.includes("node_modules");

  function isDeclarationLike(n) {
    return !!n && (
      ts.isFunctionDeclaration(n) ||
      ts.isMethodDeclaration(n) ||
      ts.isMethodSignature(n) ||
      ts.isCallSignatureDeclaration(n) ||
      ts.isArrowFunction(n) ||
      ts.isFunctionExpression(n) ||
      ts.isVariableDeclaration(n) ||
      ts.isPropertyDeclaration(n) ||
      ts.isPropertySignature(n) ||
      ts.isInterfaceDeclaration(n) ||
      ts.isClassDeclaration(n) ||
      ts.isExportAssignment(n) ||
      ts.isExportDeclaration(n)
    );
  }

  function promoteNode(n) {
    if (!n) return n;

    // Always return the *nearest* declaration-like ancestor (function, method,
    // property, variable, class, interface, etc.) without promoting further
    // up the tree. This ensures we return the concrete method/function/field
    // definition itself instead of the outer class/interface, even for
    // external .d.ts / node_modules code.
    if (isDeclarationLike(n)) {
      return n;
    }
    let cur = n;
    while (cur && cur.parent) {
      if (isDeclarationLike(cur.parent)) {
        return cur.parent;
      }
      cur = cur.parent;
    }

    return n;
  }

  node = promoteNode(node);

  const fullStart = node.getFullStart();
  const fullEnd = node.getEnd();
  const text = fileText.slice(fullStart, fullEnd);

  const startLC = sourceFile.getLineAndCharacterOfPosition(fullStart);
  const endLC = sourceFile.getLineAndCharacterOfPosition(fullEnd);

  return {
    text,
    nodeKind: ts.SyntaxKind[node.kind],
    range: {
      start: { line: startLC.line, character: startLC.character },
      end: { line: endLC.line, character: endLC.character },
    },
  };
}

function main() {
  try {
    const [repoRoot, filePath, lineStr, charStr] = process.argv.slice(2);
    if (!repoRoot || !filePath || lineStr === undefined || charStr === undefined) {
      throw new Error(
        "Usage: node ts_navigation.js <repoRoot> <filePath> <line0> <character0>",
      );
    }

    const line0 = Number(lineStr);
    const col0 = Number(charStr);
    const absFile = path.resolve(repoRoot, filePath);
    const { projectRoot, options, fileNames } = getProjectConfig(
      repoRoot,
      absFile,
    );

    if (!fs.existsSync(absFile)) {
      throw new Error(`File not found: ${absFile}`);
    }

    const program = ts.createProgram({
      rootNames: fileNames,
      options,
    });
    const checker = program.getTypeChecker();

    const sourceFile = program.getSourceFile(absFile);
    if (!sourceFile) throw new Error(`SourceFile not found: ${absFile}`);

    // Track rough progress through navigation to pinpoint any internal
    // TypeScript failures when debugging.
    let debugStage = "pos";
    try {
      // Clamp the requested position to the valid range of the source file to
      // avoid triggering internal TypeScript debug assertions when the caller
      // passes slightly out-of-range line/column values.
      const lastLC = sourceFile.getLineAndCharacterOfPosition(sourceFile.getEnd());
      const maxLine = lastLC.line;
      const safeLine = Math.max(0, Math.min(line0, maxLine));
      const lineText =
        sourceFile.text.split(/\r?\n/)[safeLine] ?? "";
      const maxCol = lineText.length;
      const safeCol = Math.max(0, Math.min(col0, maxCol));
      const pos = sourceFile.getPositionOfLineAndCharacter(safeLine, safeCol);
      debugStage = "node";
      const node = findNodeAt(sourceFile, pos);
      debugStage = "classify";
      const usageKind = classifyUsage(node);

      // For calls: (1) If the cursor is on the invoked expression (including a
      // prefix chain like node.properties in node.properties.forEach(...)),
      // keep defPos so we resolve that segment, not the final .forEach.
      // (2) If the cursor is in the argument list, only snap to the callee when
      // the cursor is not already on a navigable subexpression (e.g. options in
      // Array.isArray(p.options) must resolve options, not isArray).
      debugStage = "defPos";
      let defPos = pos;
      {
        let cur = node;
        while (cur && !ts.isCallExpression(cur) && !ts.isNewExpression(cur)) {
          cur = cur.parent;
        }
        if (cur && (ts.isCallExpression(cur) || ts.isNewExpression(cur))) {
          const invoked = cur.expression;
          const invokedEnd = invoked.getEnd();
          if (pos < invokedEnd) {
            // still on callee chain
          } else {
            const inner = findNodeAt(sourceFile, pos);
            if (!isDirectNavigationTarget(inner)) {
              let callee = invoked;
              if (ts.isPropertyAccessExpression(invoked)) {
                callee = invoked.name;
              }
              defPos = callee.getStart(sourceFile, true);
            }
          }
        }
      }

      // Primary: use the TypeChecker to get symbol declarations, which are
      // usually better than LanguageService definition infos (which often point
      // at import sites). Guard this in try/catch because certain nodes can
      // trigger internal TypeScript debug assertions.
      debugStage = "nodeForDef";
      const nodeForDef = findNodeAt(sourceFile, defPos);
      let symbol = null;
      let defs = [];

      debugStage = "checker";
      symbol = checker.getSymbolAtLocation(nodeForDef);
      // If this is an alias (e.g. imported symbol), resolve to its target so we
      // can see the real declarations (e.g. from node_modules/.d.ts).
      if (symbol && (symbol.flags & ts.SymbolFlags.Alias)) {
        const aliased = checker.getAliasedSymbol(symbol);
        if (aliased) symbol = aliased;
      }

      // Fallback/improvement: for property accesses like "Foo.bar(...)" or
      // "Foo.bar", resolve the property symbol via the container's type. This
      // makes static-method calls like MemoryVectorStore.fromExistingIndex(...)
      // and enum-like objects such as NodeConnectionTypes.AiEmbedding and
      // repository methods like credentialsRepository.findOneBy(...) work more
      // reliably, even when the primary symbol is missing or points at a less
      // useful declaration.
      if (ts.isIdentifier(nodeForDef)) {
        const parent = nodeForDef.parent;
        if (ts.isPropertyAccessExpression(parent) && parent.name === nodeForDef) {
          const containerExpr = parent.expression;
          const containerSym = checker.getSymbolAtLocation(containerExpr);
          if (containerSym) {
            const containerType = checker.getTypeOfSymbolAtLocation(
              containerSym,
              containerExpr,
            );
            let propSym = null;
            if (containerType) {
              propSym = containerType.getProperty(nodeForDef.text);
            }
            // If we found a property symbol on the container type and it has
            // real declarations (e.g. from a repository or vector store type),
            // prefer it over whatever we had before.
            if (propSym && propSym.declarations && propSym.declarations.length) {
              symbol = propSym;
            }
          }
        }
      }

      if (symbol && symbol.declarations && symbol.declarations.length) {
        defs = symbol.declarations.map((decl) => {
          const sf = decl.getSourceFile();
          const start = decl.getStart(sf, true);
          const end = decl.getEnd();
          return {
            fileName: sf.fileName,
            textSpan: { start, length: end - start },
            name: symbol.getName(),
            containerName: "",
            kind: ts.ScriptElementKind.unknown,
            kindModifiers: "",
          };
        });
      }
      debugStage = "checkerDone";

      // Fallback: if the checker path failed or produced no definitions, ask
      // the LanguageService for definition infos at the same position.
      if (!defs.length) {
        debugStage = "languageService";
        const servicesHost = {
          getScriptFileNames: () => fileNames,
          getScriptVersion: () => "0",
          getScriptSnapshot: (fileName) => {
            if (!fs.existsSync(fileName)) return undefined;
            return ts.ScriptSnapshot.fromString(fs.readFileSync(fileName, "utf8"));
          },
          getCurrentDirectory: () => projectRoot,
          getCompilationSettings: () => options,
          getDefaultLibFileName: (opts) => ts.getDefaultLibFilePath(opts),
          fileExists: ts.sys.fileExists,
          readFile: ts.sys.readFile,
          readDirectory: ts.sys.readDirectory,
        };
        const languageService = ts.createLanguageService(
          servicesHost,
          ts.createDocumentRegistry(),
        );
        const lsDefs = languageService.getDefinitionAtPosition(absFile, defPos) || [];
        if (lsDefs.length) {
          defs = lsDefs;
        }
      }

      debugStage = "pickBest";
      const picked = pickBestDefinition(defs, repoRoot);

      let fullDefSource = null;
      let definitionPath = null;
      let definitionRange = null;
      let nodeKind = null;

      if (picked) {
        const extracted = extractFullDefinitionSource(picked);
        fullDefSource = extracted.text;
        definitionPath = picked.fileName;
        definitionRange = extracted.range;
        nodeKind = extracted.nodeKind;
      }

      debugStage = "output";
      const out = {
        ok: !!picked,
        usageKind,
        definitionPath,
        definitionRange,
        fullDefSource,
        nodeKind,
        error: null,
      };

      process.stdout.write(JSON.stringify(out));
    } catch (innerErr) {
      // Re-throw with stage information so we can see where navigation failed.
      const msg =
        (innerErr && innerErr.message ? innerErr.message : String(innerErr)) || "";
      throw new Error(`${debugStage}: ${msg}`);
    }
  } catch (err) {
    const out = {
      ok: false,
      usageKind: "other",
      definitionPath: null,
      definitionRange: null,
      fullDefSource: null,
      nodeKind: null,
      error: String(err && err.message ? err.message : err),
    };
    process.stdout.write(JSON.stringify(out));
    process.exitCode = 1;
  }
}

if (require.main === module) {
  main();
}

