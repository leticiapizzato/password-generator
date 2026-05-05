param(
    [Parameter(Position = 0)]
    [string]$Target = "install"
)

$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $projectRoot

$venvPython = Join-Path $projectRoot ".venv\Scripts\python.exe"

function Install-Project {
    if (-not (Test-Path $venvPython)) {
        python -m venv .venv
    }
    & $venvPython -m pip install --upgrade pip
    & $venvPython -m pip install -e ".[dev]"
}

function Run-Project {
    if (-not (Test-Path $venvPython)) {
        throw "Ambiente virtual nao encontrado. Execute: make install"
    }
    & $venvPython src/main.py --length 16
}

function Test-Project {
    if (-not (Test-Path $venvPython)) {
        throw "Ambiente virtual nao encontrado. Execute: make install"
    }
    & $venvPython -m pytest -q
}

function Uninstall-Project {
    if (-not (Test-Path $venvPython)) {
        throw "Ambiente virtual nao encontrado. Execute: make install"
    }
    & $venvPython -m pip uninstall -y password-generator
}

switch ($Target.ToLower()) {
    "install" { Install-Project }
    "run" { Run-Project }
    "test" { Test-Project }
    "uninstall" { Uninstall-Project }
    default {
        Write-Host "Uso: make [install|run|test|uninstall]"
        exit 1
    }
}
