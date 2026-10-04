/**
 * JugaadLang Online Compiler — website/compiler.js
 * Client-side browser compiler and runtime powered by Pyodide (WebAssembly).
 * 100% client-side execution — No backend server required.
 */

(() => {
  'use strict';

  // ===== SAMPLE PROGRAMS =====
  const SAMPLES = {
    namaste: `# Namaste Duniya! 🙏
# JugaadLang runs 100% in your browser via WebAssembly!

naam = "Duniya"
bolo("Namaste " + naam + "! 🚀")

# Built-in blessings
namaste()
chai()
`,
    variables: `# 📦 Variables & Types in JugaadLang
naam = "Sumangal"
age = 20
chai_lover = sahi

bolo("Developer: " + naam)
bolo("Age: " + shabd(age))

agar chai_lover:
    bolo("Status: Chai pe charcha chalu hai ☕")
warna:
    bolo("Status: Coffee peete ho kya? 🙃")
`,
    loops: `# 🔁 Loops in JugaadLang (ghumo)
bolo("Counting 1 to 5:")
ghumo i mein range(1, 6):
    agar i == 5:
        bolo("Punch (5)! Bas ho gaya.")
    warna:
        bolo("Ginti: " + shabd(i))
`,
    functions: `# 🔢 Functions (banao) & Recursion
banao fibonacci(n):
    agar n <= 1:
        wapas n
    wapas fibonacci(n - 1) + fibonacci(n - 2)

bolo("Fibonacci Series:")
ghumo i mein range(7):
    bolo(shabd(i) + " -> " + shabd(fibonacci(i)))
`,
    match: `# 🎯 Pattern Matching (agar_match / kaand)
order = "cutting"

agar_match order:
    kaand "cutting":
        bolo("Ek kadak cutting chai! ☕")
    kaand "masala":
        bolo("Spicy Masala chai coming up! 🌶️")
    kaand _:
        bolo("Pani peelo pehle! 💧")
`,
    ganit: `# 📐 Ganit Stdlib Module
lao ganit

radius = 7
area = ganit.pi * ganit.square(radius)

bolo("Radius: " + shabd(radius))
bolo("Area: " + shabd(round(area, 2)))
bolo("Factorial of 5: " + shabd(ganit.factorial(5)))
bolo("Square root of 144: " + shabd(ganit.sqrt(144)))
`
  };

  // ===== STATE =====
  let pyodideInstance = null;
  let pyodideLoadingPromise = null;
  let isExecuting = false;
  let lastTranspiledPython = '';
  let activeTab = 'output'; // 'output' | 'python'

  // ===== DOM REFS =====
  let editorEl, lineNumbersEl, runBtn, runBtnIcon, runBtnText;
  let downloadJugBtn, downloadPyBtn, outputEl, pythonCodeEl;
  let statusDotEl, statusTextEl, tabOutputBtn, tabPythonBtn;
  let outputSectionEl, pythonSectionEl, outputMetaEl;

  // ===== INIT DOM HOOKS =====
  function init() {
    editorEl = document.getElementById('jug-editor');
    lineNumbersEl = document.getElementById('editor-line-numbers');
    runBtn = document.getElementById('run-btn');
    runBtnIcon = document.getElementById('run-btn-icon');
    runBtnText = document.getElementById('run-btn-text');
    downloadJugBtn = document.getElementById('download-jug-btn');
    downloadPyBtn = document.getElementById('download-py-btn');
    outputEl = document.getElementById('compiler-output');
    pythonCodeEl = document.getElementById('transpiled-python');
    statusDotEl = document.getElementById('compiler-status-dot');
    statusTextEl = document.getElementById('compiler-status-text');
    tabOutputBtn = document.getElementById('tab-btn-output');
    tabPythonBtn = document.getElementById('tab-btn-python');
    outputSectionEl = document.getElementById('panel-compiler-output');
    pythonSectionEl = document.getElementById('panel-compiler-python');
    outputMetaEl = document.getElementById('output-meta');

    if (!editorEl || !runBtn) return;

    // Load initial code
    editorEl.value = SAMPLES.namaste;
    updateLineNumbers();

    // Editor event listeners
    editorEl.addEventListener('input', updateLineNumbers);
    editorEl.addEventListener('scroll', syncLineNumberScroll);
    editorEl.addEventListener('keydown', handleEditorKeydown);

    // Run button
    runBtn.addEventListener('click', runCode);

    // Download buttons
    downloadJugBtn.addEventListener('click', downloadJug);
    downloadPyBtn.addEventListener('click', downloadPy);

    // Tab buttons
    if (tabOutputBtn) tabOutputBtn.addEventListener('click', () => switchCompilerTab('output'));
    if (tabPythonBtn) tabPythonBtn.addEventListener('click', () => switchCompilerTab('python'));

    // Sample buttons
    document.querySelectorAll('.sample-btn[data-sample]').forEach(btn => {
      btn.addEventListener('click', () => {
        const key = btn.getAttribute('data-sample');
        if (SAMPLES[key]) {
          editorEl.value = SAMPLES[key];
          updateLineNumbers();
          document.querySelectorAll('.sample-btn').forEach(b => b.classList.remove('active'));
          btn.classList.add('active');
          editorEl.focus();
        }
      });
    });

    // Copy editor button
    const copyEditorBtn = document.getElementById('copy-editor-btn');
    if (copyEditorBtn) {
      copyEditorBtn.addEventListener('click', () => {
        navigator.clipboard.writeText(editorEl.value).then(() => {
          showCopiedFeedback(copyEditorBtn, '📋 Copied!');
        });
      });
    }

    // Clear editor button
    const clearEditorBtn = document.getElementById('clear-editor-btn');
    if (clearEditorBtn) {
      clearEditorBtn.addEventListener('click', () => {
        editorEl.value = '';
        updateLineNumbers();
        editorEl.focus();
      });
    }

    // Reset editor button
    const resetEditorBtn = document.getElementById('reset-editor-btn');
    if (resetEditorBtn) {
      resetEditorBtn.addEventListener('click', () => {
        editorEl.value = SAMPLES.namaste;
        updateLineNumbers();
        document.querySelectorAll('.sample-btn').forEach(b => b.classList.remove('active'));
        const defaultSampleBtn = document.querySelector('.sample-btn[data-sample="namaste"]');
        if (defaultSampleBtn) defaultSampleBtn.classList.add('active');
        editorEl.focus();
      });
    }

    // Copy output button
    const copyOutputBtn = document.getElementById('copy-output-btn');
    if (copyOutputBtn) {
      copyOutputBtn.addEventListener('click', () => {
        navigator.clipboard.writeText(outputEl.textContent || '').then(() => {
          showCopiedFeedback(copyOutputBtn, '📋 Copied!');
        });
      });
    }

    // Clear output button
    const clearOutputBtn = document.getElementById('clear-output-btn');
    if (clearOutputBtn) {
      clearOutputBtn.addEventListener('click', () => {
        outputEl.textContent = 'Output cleared.';
        outputEl.className = 'terminal-display placeholder';
        if (outputMetaEl) outputMetaEl.textContent = '';
        setStatus('ready', 'Ready');
      });
    }

    // Copy Python button
    const copyPyBtn = document.getElementById('copy-py-btn');
    if (copyPyBtn) {
      copyPyBtn.addEventListener('click', () => {
        navigator.clipboard.writeText(pythonCodeEl.textContent || '').then(() => {
          showCopiedFeedback(copyPyBtn, '📋 Copied!');
        });
      });
    }

    // Lazy Pyodide background pre-load when user scrolls near compiler
    setupLazyPreload();
  }

  function showCopiedFeedback(btn, text) {
    const orig = btn.textContent;
    btn.textContent = text;
    setTimeout(() => { btn.textContent = orig; }, 1500);
  }

  // ===== LINE NUMBERS & SCROLL SYNC =====
  function updateLineNumbers() {
    if (!editorEl || !lineNumbersEl) return;
    const lines = editorEl.value.split('\n');
    const count = Math.max(lines.length, 1);
    let nums = '';
    for (let i = 1; i <= count; i++) {
      nums += i + '\n';
    }
    lineNumbersEl.textContent = nums;
  }

  function syncLineNumberScroll() {
    if (!editorEl || !lineNumbersEl) return;
    lineNumbersEl.scrollTop = editorEl.scrollTop;
  }

  // ===== EDITOR KEYBOARD CONTROLS =====
  function handleEditorKeydown(e) {
    // Ctrl+Enter or Cmd+Enter -> Run
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
      e.preventDefault();
      runCode();
      return;
    }

    // Tab -> 4 spaces indentation
    if (e.key === 'Tab') {
      e.preventDefault();
      const start = editorEl.selectionStart;
      const end = editorEl.selectionEnd;

      if (e.shiftKey) {
        // Shift+Tab -> Dedent 4 spaces
        const val = editorEl.value;
        const lineStart = val.lastIndexOf('\n', start - 1) + 1;
        const linePrefix = val.slice(lineStart, lineStart + 4);
        if (linePrefix === '    ') {
          editorEl.value = val.slice(0, lineStart) + val.slice(lineStart + 4);
          editorEl.selectionStart = Math.max(lineStart, start - 4);
          editorEl.selectionEnd = Math.max(lineStart, end - 4);
        }
      } else {
        // Tab -> Insert 4 spaces
        document.execCommand('insertText', false, '    ');
      }
      updateLineNumbers();
      return;
    }

    // Enter -> Smart auto-indent
    if (e.key === 'Enter') {
      const val = editorEl.value;
      const pos = editorEl.selectionStart;
      const lineStart = val.lastIndexOf('\n', pos - 1) + 1;
      const currentLine = val.slice(lineStart, pos);
      const indentMatch = currentLine.match(/^[ \t]*/);
      let indent = indentMatch ? indentMatch[0] : '';

      // If line ends with colon (:), increase indent by 4 spaces
      if (currentLine.trim().endsWith(':')) {
        indent += '    ';
      }

      if (indent.length > 0) {
        e.preventDefault();
        document.execCommand('insertText', false, '\n' + indent);
        updateLineNumbers();
      }
    }
  }

  // ===== TABS SWITCHING =====
  function switchCompilerTab(tab) {
    activeTab = tab;
    if (tab === 'output') {
      if (tabOutputBtn) tabOutputBtn.classList.add('active');
      if (tabPythonBtn) tabPythonBtn.classList.remove('active');
      if (outputSectionEl) outputSectionEl.style.display = 'flex';
      if (pythonSectionEl) pythonSectionEl.style.display = 'none';
    } else {
      if (tabPythonBtn) tabPythonBtn.classList.add('active');
      if (tabOutputBtn) tabOutputBtn.classList.remove('active');
      if (outputSectionEl) outputSectionEl.style.display = 'none';
      if (pythonSectionEl) pythonSectionEl.style.display = 'flex';
    }
  }

  // ===== STATUS DISPLAY =====
  function setStatus(type, text) {
    if (!statusDotEl || !statusTextEl) return;
    statusDotEl.className = `status-dot ${type}`;
    statusTextEl.textContent = text;
  }

  // ===== LAZY PRELOAD =====
  function setupLazyPreload() {
    const target = document.getElementById('try-online');
    if (!target || !('IntersectionObserver' in window)) return;

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          // Preload Pyodide lazily in background
          initPyodide().catch(() => {
            // Silently ignore preload failures; explicit Run will retry and display error
          });
          observer.disconnect();
        }
      });
    }, { rootMargin: '300px' });

    observer.observe(target);
  }

  // ===== PYODIDE INITIALIZATION =====
  async function initPyodide() {
    if (pyodideInstance) return pyodideInstance;
    if (pyodideLoadingPromise) return pyodideLoadingPromise;

    setStatus('loading', 'Loading Python runtime...');

    pyodideLoadingPromise = (async () => {
      // 1. Ensure pyodide.js script is loaded
      if (typeof loadPyodide === 'undefined') {
        await new Promise((resolve, reject) => {
          const script = document.createElement('script');
          script.src = 'https://cdn.jsdelivr.net/pyodide/v0.26.4/full/pyodide.js';
          script.async = true;
          script.onload = resolve;
          script.onerror = () => reject(new Error('Network error: CDN pyodide.js failed to load.'));
          document.head.appendChild(script);
        });
      }

      // 2. Initialize Pyodide WASM runtime
      const pyodide = await loadPyodide({
        indexURL: 'https://cdn.jsdelivr.net/pyodide/v0.26.4/full/'
      });

      // 3. Fallback stdin handler for interactive poochho() calls
      try {
        pyodide.setStdin({
          stdin: () => {
            const promptVal = window.prompt('JugaadLang poochho() input:');
            return promptVal !== null ? promptVal : '';
          }
        });
      } catch (e) {
        // Safe fallback
      }

      // 4. Setup Python environment and rich shim
      await pyodide.runPythonAsync(`
import sys, types, io, ast, json, base64, zipfile

# Provide lightweight rich console shim for error formatting
rich = types.ModuleType('rich')
rich_console = types.ModuleType('rich.console')

class _Capture:
    def __init__(self, c):
        self.c = c
        self.lines = []
    def __enter__(self):
        self.orig = self.c.print
        self.lines = []
        def cap(*args, **kwargs):
            import re
            text = " ".join(str(a) for a in args)
            clean = re.sub(r'\\[/?[a-zA-Z0-9_ #]+\\]', '', text)
            self.lines.append(clean)
        self.c.print = cap
        return self
    def __exit__(self, *args):
        self.c.print = self.orig
    def get(self):
        return "\\n".join(self.lines)

class _Console:
    def __init__(self, *args, **kwargs): pass
    def capture(self): return _Capture(self)
    def print(self, *args, **kwargs):
        import re
        text = " ".join(str(a) for a in args)
        print(re.sub(r'\\[/?[a-zA-Z0-9_ #]+\\]', '', text))

rich_console.Console = _Console
rich_console.RenderableType = object
rich.console = rich_console
sys.modules['rich'] = rich
sys.modules['rich.console'] = rich_console
`);

      // 5. Unpack JugaadLang package bundle into /home/pyodide
      const zipBase64 = window.JUGAADLANG_ZIP_BASE64;
      if (!zipBase64) {
        throw new Error('JugaadLang compiler package (assets/jugaad_bundle.js) is not loaded.');
      }

      pyodide.globals.set('__JUGAAD_ZIP_B64__', zipBase64);
      await pyodide.runPythonAsync(`
zip_bytes = base64.b64decode(__JUGAAD_ZIP_B64__)
with zipfile.ZipFile(io.BytesIO(zip_bytes)) as zf:
    zf.extractall('/home/pyodide')

if '/home/pyodide' not in sys.path:
    sys.path.insert(0, '/home/pyodide')

# Import core compiler modules to verify installation
from jugaadlang.lexer.lexer import Lexer
from jugaadlang.parser.parser import Parser
from jugaadlang.transformer.to_python import JugaadToPythonTransformer
from jugaadlang.errors.messages import format_error
from jugaadlang.runtime.interpreter import JugaadInterpreter

def _run_jugaad(source, filename="program.jug"):
    # ── Phase 1: Real JugaadLang Transpilation ──
    try:
        lexer = Lexer(source, filename)
        tokens = lexer.tokenize()
        parser = Parser(tokens, filename, source)
        ast_mod = parser.parse()
        transformer = JugaadToPythonTransformer(filename)
        py_ast = transformer.transform(ast_mod)
        py_source = ast.unparse(py_ast)
    except Exception as e:
        err_msg = format_error(e, source, filename)
        return json.dumps({
            "phase": "compile",
            "success": False,
            "py_source": None,
            "output": "",
            "error": err_msg
        })

    # ── Phase 2: Python Execution via Pyodide ──
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    out_buf = io.StringIO()
    err_buf = io.StringIO()
    sys.stdout = out_buf
    sys.stderr = err_buf

    try:
        interp = JugaadInterpreter(filename=filename)
        code_obj = compile(py_ast, filename, "exec")
        exec(code_obj, interp.globals, interp.globals)
        return json.dumps({
            "phase": "complete",
            "success": True,
            "py_source": py_source,
            "output": out_buf.getvalue(),
            "error": err_buf.getvalue()
        })
    except Exception as e:
        err_msg = format_error(e, source, filename)
        return json.dumps({
            "phase": "runtime",
            "success": False,
            "py_source": py_source,
            "output": out_buf.getvalue(),
            "error": err_msg
        })
    finally:
        sys.stdout = old_stdout
        sys.stderr = old_stderr

__run_jugaad = _run_jugaad
`);

      pyodideInstance = pyodide;
      setStatus('ready', 'Ready');
      return pyodide;
    })();

    try {
      return await pyodideLoadingPromise;
    } catch (err) {
      pyodideLoadingPromise = null;
      setStatus('error', 'Initialization Failed');
      throw err;
    }
  }

  // ===== RUN CODE =====
  async function runCode() {
    if (isExecuting) return;

    const source = editorEl.value;
    if (!source.trim()) {
      outputEl.className = 'terminal-display placeholder';
      outputEl.textContent = 'Editor khaali hai! Kuch code likho ya upar se koi sample choose karo. 🙏';
      switchCompilerTab('output');
      return;
    }

    isExecuting = true;
    runBtn.disabled = true;
    runBtnIcon.innerHTML = '<span class="compiler-loading-spinner" aria-hidden="true"></span>';
    runBtnText.textContent = 'Chala raha hai...';
    setStatus('loading', 'Running...');

    // Switch to output tab and show executing state
    switchCompilerTab('output');
    outputEl.className = 'terminal-display placeholder';
    outputEl.textContent = 'Running code in WebAssembly...';
    if (outputMetaEl) outputMetaEl.textContent = '';

    const startTime = performance.now();

    try {
      // Step 1: Ensure Pyodide runtime is ready
      let pyodide;
      try {
        pyodide = await initPyodide();
      } catch (loadErr) {
        displayLoadError(loadErr);
        return;
      }

      // Step 2: Pass source code to Pyodide
      pyodide.globals.set('__user_code__', source);
      const jsonResult = await pyodide.runPythonAsync('__run_jugaad(__user_code__, "program.jug")');
      const res = JSON.parse(jsonResult);

      const elapsed = ((performance.now() - startTime) / 1000).toFixed(2);

      // Handle Python code update
      if (res.py_source) {
        lastTranspiledPython = res.py_source;
        pythonCodeEl.textContent = res.py_source;
        downloadPyBtn.disabled = false;
        downloadPyBtn.removeAttribute('aria-disabled');
      }

      // Handle output and errors
      outputEl.className = 'terminal-display';
      outputEl.textContent = '';

      if (res.success) {
        setStatus('ready', 'Success');
        const outputText = res.output ? res.output.trimEnd() : '(Program executed successfully with no output)';
        outputEl.textContent = outputText;
        if (outputMetaEl) {
          outputMetaEl.textContent = `Completed in ${elapsed}s • Status: 0 (OK)`;
        }
      } else {
        setStatus('error', res.phase === 'compile' ? 'Compilation Error' : 'Runtime Error');

        if (res.phase === 'compile') {
          // Compilation error
          const errBox = document.createElement('div');
          errBox.className = 'compiler-error-box';

          const title = document.createElement('div');
          title.className = 'compiler-error-title';
          title.textContent = '⚠️ JugaadLang Compilation Error';

          const content = document.createElement('div');
          content.className = 'compiler-error-content';
          content.textContent = res.error || 'Syntax error occurred during transpilation.';

          errBox.appendChild(title);
          errBox.appendChild(content);
          outputEl.appendChild(errBox);

          if (outputMetaEl) {
            outputMetaEl.textContent = `Transpilation failed in ${elapsed}s`;
          }
        } else {
          // Runtime error with partial output if any
          if (res.output) {
            const partialText = document.createTextNode(res.output + '\n');
            outputEl.appendChild(partialText);
          }

          const errBox = document.createElement('div');
          errBox.className = 'compiler-error-box';

          const title = document.createElement('div');
          title.className = 'compiler-error-title';
          title.textContent = '💥 Python Runtime Error';

          const content = document.createElement('div');
          content.className = 'compiler-error-content';
          content.textContent = res.error || 'Exception occurred during execution.';

          errBox.appendChild(title);
          errBox.appendChild(content);
          outputEl.appendChild(errBox);

          if (outputMetaEl) {
            outputMetaEl.textContent = `Execution failed in ${elapsed}s`;
          }
        }
      }
    } catch (err) {
      displayUnexpectedError(err);
    } finally {
      isExecuting = false;
      runBtn.disabled = false;
      runBtnIcon.textContent = '⚡';
      runBtnText.textContent = 'Chalao (Run)';
    }
  }

  // ===== ERROR DISPLAYS =====
  function displayLoadError(err) {
    setStatus('error', 'Runtime Load Error');
    outputEl.className = 'terminal-display';
    outputEl.textContent = '';

    const errBox = document.createElement('div');
    errBox.className = 'compiler-error-box';

    const title = document.createElement('div');
    title.className = 'compiler-error-title';
    title.textContent = '❌ Unable to load the Python runtime.';

    const content = document.createElement('div');
    content.className = 'compiler-error-content';
    content.textContent =
      'Please check your internet connection and try again.\n\n' +
      'Details: ' + (err.message || String(err)) + '\n\n' +
      'Note: Pyodide loads from the official jsDelivr CDN upon first run.';

    errBox.appendChild(title);
    errBox.appendChild(content);
    outputEl.appendChild(errBox);
  }

  function displayUnexpectedError(err) {
    setStatus('error', 'Unexpected Error');
    outputEl.className = 'terminal-display';
    outputEl.textContent = '';

    const errBox = document.createElement('div');
    errBox.className = 'compiler-error-box';

    const title = document.createElement('div');
    title.className = 'compiler-error-title';
    title.textContent = '❌ Unexpected Browser Execution Error';

    const content = document.createElement('div');
    content.className = 'compiler-error-content';
    content.textContent = String(err.stack || err.message || err);

    errBox.appendChild(title);
    errBox.appendChild(content);
    outputEl.appendChild(errBox);
  }

  // ===== DOWNLOAD HANDLERS =====
  function downloadJug() {
    const code = editorEl.value;
    triggerFileDownload(code, 'program.jug', 'text/plain;charset=utf-8');
  }

  function downloadPy() {
    if (!lastTranspiledPython) return;
    triggerFileDownload(lastTranspiledPython, 'program.py', 'text/x-python;charset=utf-8');
  }

  function triggerFileDownload(content, filename, mimeType) {
    const blob = new Blob([content], { type: mimeType });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    setTimeout(() => {
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    }, 100);
  }

  // Bootstrap when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
