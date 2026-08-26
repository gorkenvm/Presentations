<#
    cnn2 klasorunu gorkenvm/Presentations reposunun cnn2/ dizinine gonderir.

    Kullanim (PowerShell, bu klasorde):
        .\push.ps1
        .\push.ps1 -Message "Adim 2: convolution GIF"

    Gereken: git kurulu ve GitHub kimlik dogrulamasi yapilmis olmali
    (Git Credential Manager ya da 'gh auth login').

    Nasil calisir: repo'yu .gitrepo\ altina bir kez klonlar, sonraki
    calistirmalarda oradan pull eder. Bu klasordeki dosyalari klonun
    cnn2/ dizinine aynalar, commit'ler ve push eder.
#>

[CmdletBinding()]
param(
    [string]$Message = "cnn2: ders materyali guncellendi",
    [string]$Branch  = "main"
)

$ErrorActionPreference = "Stop"

$Kaynak   = $PSScriptRoot
$RepoUrl  = "https://github.com/gorkenvm/Presentations.git"
$Klon     = Join-Path (Split-Path $Kaynak -Parent) ".gitrepo\Presentations"
$Hedef    = Join-Path $Klon "cnn2"

# Repoya gonderilmeyecekler
$Haric = @("push.ps1", "push.bat", "README.md", "*.paint", "~`$*")

# Repoya gonderilmeyecek KLASORLER
# 04_cnn_course_materials icinde yolov3.weights (237 MB) var; GitHub 100 MB
# ustu dosya kabul etmez ve TUM push basarisiz olur.
# Veri seti bunun yerine veri/garbage_classification.zip (43 MB) olarak gidiyor.
$HaricKlasor = @(".git", ".ipynb_checkpoints", "04_cnn_course_materials")

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    throw "git bulunamadi. https://git-scm.com/download/win adresinden kurun."
}

# --- 1) Klon var mi? Yoksa olustur, varsa guncelle ---------------------------
if (-not (Test-Path (Join-Path $Klon ".git"))) {
    Write-Host "[1/4] Repo klonlaniyor -> $Klon" -ForegroundColor Cyan
    New-Item -ItemType Directory -Force -Path (Split-Path $Klon -Parent) | Out-Null
    git clone --branch $Branch $RepoUrl $Klon
    if ($LASTEXITCODE -ne 0) { throw "Klonlama basarisiz." }
} else {
    Write-Host "[1/4] Repo guncelleniyor (pull)" -ForegroundColor Cyan
    git -C $Klon checkout $Branch
    git -C $Klon pull --ff-only
    if ($LASTEXITCODE -ne 0) {
        throw "Pull basarisiz. Repoda cakisma olabilir: $Klon"
    }
}

# --- 2) Dosyalari aynala -----------------------------------------------------
Write-Host "[2/4] Dosyalar kopyalaniyor -> cnn2/" -ForegroundColor Cyan
New-Item -ItemType Directory -Force -Path $Hedef | Out-Null

# /MIR: hedefi kaynakla birebir esitler (silinenler repodan da silinir)
$rc = @("/MIR", "/NFL", "/NDL", "/NJH", "/NJS", "/NP")
foreach ($k in $HaricKlasor) { $rc += @("/XD", $k) }
foreach ($f in $Haric)       { $rc += @("/XF", $f) }
robocopy $Kaynak $Hedef @rc | Out-Null
if ($LASTEXITCODE -ge 8) { throw "robocopy hatasi (kod $LASTEXITCODE)." }

# --- 2b) GitHub 100 MB sinirini asan dosya var mi? --------------------------
$Buyuk = Get-ChildItem $Hedef -Recurse -File | Where-Object { $_.Length -gt 100MB }
if ($Buyuk) {
    $Buyuk | ForEach-Object {
        Write-Host ("COK BUYUK: {0}  ({1:N0} MB)" -f $_.FullName, ($_.Length/1MB)) -ForegroundColor Red
    }
    throw "GitHub 100 MB ustu dosya kabul etmez. Bu dosyalari `$HaricKlasor / `$Haric listesine ekleyin."
}

# --- 3) Degisiklik var mi? ---------------------------------------------------
Write-Host "[3/4] Degisiklikler hazirlaniyor" -ForegroundColor Cyan
git -C $Klon add -A -- cnn2
git -C $Klon diff --cached --quiet -- cnn2
if ($LASTEXITCODE -eq 0) {
    Write-Host "Degisiklik yok, push atlandi." -ForegroundColor Yellow
    exit 0
}

git -C $Klon --no-pager diff --cached --stat -- cnn2

# --- 4) Commit + push --------------------------------------------------------
Write-Host "[4/4] Commit + push" -ForegroundColor Cyan
git -C $Klon commit -m $Message
if ($LASTEXITCODE -ne 0) { throw "Commit basarisiz." }
git -C $Klon push origin $Branch
if ($LASTEXITCODE -ne 0) { throw "Push basarisiz. Kimlik dogrulamasini kontrol edin." }

Write-Host ""
Write-Host "Tamam." -ForegroundColor Green
Write-Host "  Repo  : https://github.com/gorkenvm/Presentations/tree/$Branch/cnn2"
Write-Host "  Colab : https://colab.research.google.com/github/gorkenvm/Presentations/blob/$Branch/cnn2/cnn2_ders.ipynb"
Write-Host ""
Write-Host "Colab eski surumu gosterirse sekmede Ctrl+Shift+R yapin." -ForegroundColor DarkGray
