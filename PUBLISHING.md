# Releasing PaceBar

Checklist for cutting a new release. Replace `X.Y.Z` with the new version (e.g.
`0.1.1`). Run everything in **PowerShell from the project root, on Windows**.

## Prerequisites (one-time)

- A [PyPI](https://pypi.org/) account with **2FA** enabled and an API token
  (<https://pypi.org/manage/account/token/>). Optionally the same on
  [TestPyPI](https://test.pypi.org/) for dry runs.
- [uv](https://docs.astral.sh/uv/) installed.
- Keep tokens secret — type them only in your own terminal, never in chat or
  screenshots. Tip: `$env:UV_PUBLISH_TOKEN = "pypi-..."` for the session keeps the
  token out of command history (then drop `--token` from the commands below).

## Steps

1. **Bump the version** in `pyproject.toml` → `version = "X.Y.Z"`.

2. **Sanity check:**
   ```powershell
   uv run ruff format --check .
   uv run ruff check .
   uv run pacebar            # smoke-test the app
   ```

3. **Commit & push:**
   ```powershell
   git add -A
   git commit -m "chore(release): vX.Y.Z"
   git push origin main
   ```

4. **Build the wheel + sdist:**
   ```powershell
   uv build
   ```
   → `dist/pacebar-X.Y.Z-py3-none-any.whl` and `dist/pacebar-X.Y.Z.tar.gz`.

5. *(Optional)* **Dry-run on TestPyPI**, then eyeball the project page there:
   ```powershell
   uv publish --publish-url https://test.pypi.org/legacy/ --token pypi-TESTTOKEN dist/pacebar-X.Y.Z*
   ```

6. **Publish to PyPI** (the `pacebar-X.Y.Z*` glob uploads only the wheel + sdist, never
   the `.exe`):
   ```powershell
   uv publish --token pypi-TOKEN dist/pacebar-X.Y.Z*
   ```
   > ⚠️ A version on PyPI is **immutable** — it can never be re-uploaded or edited. If
   > something is wrong, bump to the next version and republish.

7. **Tag the release:**
   ```powershell
   git tag -a vX.Y.Z -m "pacebar X.Y.Z"
   git push origin vX.Y.Z
   ```

8. **Build the Windows exe** (PyInstaller does **not** cross-compile — build on the OS
   you target):
   ```powershell
   uv run --extra build pyinstaller --noconfirm --clean pacebar.spec
   Copy-Item dist\pacebar.exe dist\pacebar-X.Y.Z-windows-x64.exe
   ```

9. **Create the GitHub Release** — <https://github.com/Rioran/pacebar/releases/new>:
   - Choose the existing tag `vX.Y.Z`; title `PaceBar X.Y.Z`.
   - Write the notes (do **not** click *Generate release notes* if you wrote your own).
   - Drag `dist\pacebar-X.Y.Z-windows-x64.exe` into **Attach binaries** and wait for the
     upload to finish.
   - Leave the label **None** → **Publish release**.

   With the [GitHub CLI](https://cli.github.com/) installed you can do it in one line
   instead:
   ```powershell
   gh release create vX.Y.Z dist\pacebar-X.Y.Z-windows-x64.exe --title "PaceBar X.Y.Z" --notes-file notes.md
   ```

10. **Verify:**
    ```powershell
    pip install pacebar==X.Y.Z   # in a throwaway venv, then run: pacebar
    ```
    Also download the `.exe` from the release page (unsigned → Windows SmartScreen warns
    on first launch: *More info → Run anyway*).

## Gotchas

- **Build each OS natively.** The `.exe` runs only on Windows. For a Linux binary, build
  on Linux/WSL **in a separate checkout** — Windows and WSL must not share one `.venv`
  (it breaks with "no Python executable was found"). Attach it as another release asset.
- `dist/` and `.venv/` are git-ignored; release assets live on GitHub Releases, not in
  the repo.
- The PyInstaller entry point is `entry.py` (absolute import), **not**
  `src/pacebar/__main__.py` — pointing PyInstaller at the package's `__main__` builds
  fine but crashes at launch ("attempted relative import with no known parent package").
