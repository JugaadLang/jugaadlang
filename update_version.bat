@echo off
setlocal EnableExtensions
chcp >nul 65001

if "%~1"=="" (
    echo Usage: %~nx0 ^<new_version^>
    echo Example: %~nx0 1.0.3
    exit /b 1
)

set "NEW_VERSION=%~1"
echo 🚀 Updating version to %NEW_VERSION% across all components...

REM Note: \" inside the quoted python -c payload reaches Python as a literal "

REM 1. Update pyproject.toml
python -c "import re,sys;v=sys.argv[1];s=open('pyproject.toml',encoding='utf-8').read();open('pyproject.toml','w',encoding='utf-8').write(re.sub(r'version = \".[0-9.]+.\"','version = \"'+v+'\"',s,count=1))" %NEW_VERSION% || exit /b 1
echo ✅ Updated pyproject.toml

REM 2. Update jug_cli/main.py
python -c "import re,sys;v=sys.argv[1];p='jug_cli/main.py';s=open(p,encoding='utf-8').read();open(p,'w',encoding='utf-8').write(re.sub(r'@click\.version_option\(version=\".[0-9.]+.\"','@click.version_option(version=\"'+v+'\"',s))" %NEW_VERSION% || exit /b 1
echo ✅ Updated jug_cli/main.py

REM 3. Update vscode_extension/package.json
python -c "import json,sys;v=sys.argv[1];p='vscode_extension/package.json';d=json.load(open(p,encoding='utf-8'));d['version']=v;f=open(p,'w',encoding='utf-8');json.dump(d,f,indent=2);f.write('\n');f.close()" %NEW_VERSION% || exit /b 1
echo ✅ Updated vscode_extension/package.json

REM 4. Update website/index.html
python -c "import re,sys;v=sys.argv[1];p='website/index.html';s=open(p,encoding='utf-8').read();s=re.sub(r'<span class=\"pill-tag pill-new\">v.[0-9.]+</span>','<span class=\"pill-tag pill-new\">v'+v+'</span>',s);s=re.sub(r'JugaadLang v.[0-9.]+ is in development','JugaadLang v'+v+' is in development',s);s=re.sub(r'jugaadlang-.[0-9.]+\.tar\.gz','jugaadlang-'+v+'.tar.gz',s);s=re.sub(r'installed jugaadlang-.[0-9.]+','installed jugaadlang-'+v,s);open(p,'w',encoding='utf-8').write(s)" %NEW_VERSION% || exit /b 1
echo ✅ Updated website/index.html

REM 5. Update jugaadlang/repl/repl.py
python -c "import re,sys;v=sys.argv[1];p='jugaadlang/repl/repl.py';s=open(p,encoding='utf-8').read();open(p,'w',encoding='utf-8').write(re.sub(r'JugaadLang v.[0-9.]+','JugaadLang v'+v,s))" %NEW_VERSION% || exit /b 1
echo ✅ Updated jugaadlang/repl/repl.py

REM 6. Update jugaadlang/__init__.py
python -c "import re,sys;v=sys.argv[1];p='jugaadlang/__init__.py';s=open(p,encoding='utf-8').read();open(p,'w',encoding='utf-8').write(re.sub(r'__version__ = \".[0-9.]+.\"','__version__ = \"'+v+'\"',s))" %NEW_VERSION% || exit /b 1
echo ✅ Updated jugaadlang/__init__.py

echo 🎉 All components updated to v%NEW_VERSION% successfully!
echo Next steps:
echo   1. git add .
echo   2. git commit -m "chore: bump version to v%NEW_VERSION%"
echo   3. git push origin main
echo   4. gh release create v%NEW_VERSION% --generate-notes
