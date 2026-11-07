# Contributing to JugaadLang

Welcome! We are excited that you want to contribute to JugaadLang — a Hindi-keyword programming language for Indian developers. By contributing, you help make coding more accessible to millions of developers.

Please take a moment to review this document before submitting contributions.

---

## Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](https://github.com/JugaadLang/jugaadlang/blob/main/CONTRIBUTING.md). Please report any unacceptable behavior to `jugaadlang@gmail.com`.

---

## Reporting Issues & Feature Requests

We use GitHub Issues to track bugs and feature requests.

### Standard Bugs & Feature Requests
For general bugs or proposing new features:
1. Search existing issues to ensure it hasn't already been reported.
2. If it is new, open a [new GitHub issue](https://github.com/jugaadlang/jugaadlang/issues).
3. Provide a clear description, reproduction steps, expected behavior, and system details (OS version, Python version).

### Security Bug Reports
> [!IMPORTANT]
> If you discover a security vulnerability or sensitive bug, **do not** open a public issue. Please refer to our [Security Policy](https://github.com/JugaadLang/jugaadlang/blob/main/SECURITY.md) and email the details confidentially to **jugaadlang@gmail.com**.

---

## Pull Request Workflow & Automated Checks

We welcome contributions via Pull Requests (PRs). To contribute code:

### 1. Local Development Setup
First, fork the repository and clone it to your local machine.

Initialize your development environment:
```bash
# Install package in editable mode with development and optional dependencies
pip install -e .[dev,all]
```

### 2. Making Changes
* Create a descriptive branch from `main` (e.g., `feature/loops` or `bugfix/parser-error`).
* Write clean, documented code.
* Ensure code follows project standards by running tests and formatting checks locally.

### 3. Local Verification
Before opening a PR, run the following tools locally to verify your changes:

* **Linting & Formatting (Ruff)**:
  We use `ruff` to enforce code style and formatting standards.
  ```bash
  ruff check .
  ```
  To automatically fix formatting/linting issues:
  ```bash
  ruff check --fix .
  ```

* **Running Tests (Pytest)**:
  Ensure all existing tests pass and write new tests for your features.
  ```bash
  pytest
  ```

### 4. Automated Pull Request Checks (CI)
When you submit or update a Pull Request, GitHub Actions will automatically run the **JugaadLang CI** workflow (`ci.yml`):
* **Multi-Version Testing**: Pytest runs across Python versions `3.10`, `3.11`, `3.12`, `3.13`, `3.14`, and `3.15`.
* **Automated Linting**: The codebase is checked using `ruff`.

> [!NOTE]
> All automated status checks must pass green before a Pull Request can be merged.

---

## Pip Package Publishing

JugaadLang is published to PyPI as `jugaadlang`.

### Automated Release Pipeline (CD)
Maintainers publish packages automatically using GitHub Actions:
1. Create and publish a new GitHub Release on the repository web interface.
2. The **JugaadLang Release** workflow (`release.yml`) is triggered on the `published` release event.
3. The workflow automatically:
   - Sets up Python.
   - Installs build tools (`build`, `twine`).
   - Builds binary wheels and source tarballs (`python -m build`).
   - Uploads the assets to PyPI using the secured `PYPI_API_TOKEN` secret.

### Manual Release (Maintainers Only)
If a manual release needs to be performed:

1. Ensure the version is updated in [pyproject.toml](https://github.com/JugaadLang/jugaadlang/blob/main/pyproject.toml).
2. Install release dependencies:
   ```bash
   pip install build twine
   ```
3. Build the distribution packages:
   ```bash
   python -m build
   ```
   This will generate a source tarball (`.tar.gz`) and a binary wheel (`.whl`) in the `dist/` directory.
4. Upload to PyPI:
   ```bash
   twine upload dist/*
   ```
