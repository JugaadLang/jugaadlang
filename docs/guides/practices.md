# Best practices

Readable JugaadLang uses familiar Hindi keywords with clear names and predictable structure.

## Make code easy to follow

- Use four spaces per indentation level and avoid mixing tabs and spaces.
- Use `snake_case` for variables and functions, and descriptive class names.
- Keep functions focused on one task. Prefer parameters and return values to global state.
- Explain why a decision exists in comments; avoid repeating what the next line does.
- Use parentheses to make complex boolean conditions unambiguous.

## Validate boundaries

Convert input explicitly and catch the specific conversion error. Validate file paths, collection indexes, and external data before using them. Do not silently catch every exception: unexpected failures should remain visible while debugging.

## Make examples reproducible

Show input and expected output. Keep beginner examples independent of network services, randomness, local credentials, and existing files. Create disposable files in a dedicated example folder when teaching file operations.

## Organize a project

Start with `jug new my_project`. Keep source, tests, and supporting data clearly separated. Use a virtual environment and record Python dependencies. Keep credentials out of source files and Git history.

## Before sharing

Run syntax checks, exercise the program with representative inputs, and document the command needed to run it. Contributors should also run the repository's checks in the [contributor guide](contributing.html).

Related: [functions and modules](functions.html), [debugging](debugging.html), and the [tutorial](tutorials.html).
