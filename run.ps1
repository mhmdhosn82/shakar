param(
    [switch]$NoInstall,
    [switch]$SkipBackend,
    [switch]$SkipFrontend,
    [switch]$BackendOnly,
    [switch]$FrontendOnly
)

$ErrorActionPreference = 'Stop'

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$backendPath = Join-Path $root 'backend'
$frontendPath = Join-Path $root 'frontend'
$backendVenv = Join-Path $backendPath '.venv'
$backendPython = Join-Path $backendVenv 'Scripts\python.exe'
$frontendNodeModules = Join-Path $frontendPath 'node_modules'

function Write-Step($message) {
    Write-Host "`n==> $message" -ForegroundColor Cyan
}

function Ensure-Command($name, $installHint) {
    if (-not (Get-Command $name -ErrorAction SilentlyContinue)) {
        throw "$name was not found. $installHint"
    }
}

function Ensure-FileFromExample($target, $example) {
    if (-not (Test-Path $target)) {
        if (-not (Test-Path $example)) {
            throw "Example file not found: $example"
        }
        Copy-Item $example $target
        Write-Host "Created $target from example." -ForegroundColor Green
    }
}

function Start-Backend {
    Ensure-Command py 'Install Python 3.11 or newer and ensure the py launcher is available.'

    Write-Step 'Preparing backend environment'
    if (-not (Test-Path $backendVenv)) {
        Push-Location $backendPath
        try {
            py -3.11 -m venv .venv
        }
        finally {
            Pop-Location
        }
    }

    Ensure-FileFromExample (Join-Path $backendPath '.env') (Join-Path $backendPath '.env.example')

    if (-not $NoInstall) {
        Write-Step 'Installing backend dependencies'
        & $backendPython -m pip install --upgrade pip setuptools wheel
        & $backendPython -m pip install -r (Join-Path $backendPath 'requirements.txt')
    }

    Write-Step 'Running backend database migrations'
    Push-Location $backendPath
    try {
        & $backendPython -m alembic upgrade head
        & $backendPython -m app.db.init_db
    }
    finally {
        Pop-Location
    }

    Write-Step 'Starting backend server on http://127.0.0.1:8000'
    Start-Process powershell -ArgumentList @(
        '-NoExit',
        '-Command',
        "Set-Location '$backendPath'; & '$backendPython' -m uvicorn main:app --reload --port 8000"
    ) | Out-Null
}

function Start-Frontend {
    Ensure-Command npm 'Install Node.js 20 or newer so npm is available.'

    Write-Step 'Preparing frontend environment'
    Ensure-FileFromExample (Join-Path $frontendPath '.env.local') (Join-Path $frontendPath '.env.example')

    Push-Location $frontendPath
    try {
        if ((-not (Test-Path $frontendNodeModules)) -or (-not $NoInstall)) {
            Write-Step 'Installing frontend dependencies'
            npm install
        }
    }
    finally {
        Pop-Location
    }

    Write-Step 'Starting frontend server on http://localhost:3000'
    Start-Process powershell -ArgumentList @(
        '-NoExit',
        '-Command',
        "Set-Location '$frontendPath'; npm run dev"
    ) | Out-Null
}

if ($BackendOnly) {
    $SkipFrontend = $true
}

if ($FrontendOnly) {
    $SkipBackend = $true
}

Write-Step 'Shakar one-command development runner'
Write-Host 'Root:' $root -ForegroundColor DarkGray

if (-not $SkipBackend) {
    Start-Backend
}

if (-not $SkipFrontend) {
    Start-Frontend
}

Write-Host "`nEverything has been started in separate PowerShell windows." -ForegroundColor Green
Write-Host 'Backend:  http://127.0.0.1:8000' -ForegroundColor Yellow
Write-Host 'Docs:     http://127.0.0.1:8000/docs' -ForegroundColor Yellow
Write-Host 'Frontend: http://localhost:3000' -ForegroundColor Yellow
