@echo off
REM ====================================================================
REM  cnn2 klasorunu gorkenvm/Presentations reposunun cnn2/ dizinine gonderir.
REM
REM  Kullanim (cmd, bu klasorde):
REM      push.bat
REM      push.bat "Adim 10: transfer learning"
REM
REM  Gereken: git kurulu ve GitHub kimlik dogrulamasi yapilmis olmali.
REM  Not: commit mesajinda Turkce karakter kullanmayin (cmd kod sayfasi).
REM ====================================================================
setlocal

set "KAYNAK=%~dp0"
if "%KAYNAK:~-1%"=="\" set "KAYNAK=%KAYNAK:~0,-1%"
for %%I in ("%KAYNAK%\..") do set "UST=%%~fI"

set "REPOURL=https://github.com/gorkenvm/Presentations.git"
set "DAL=main"
set "KLON=%UST%\.gitrepo\Presentations"
set "HEDEF=%KLON%\cnn2"

set "MESAJ=%~1"
if "%MESAJ%"=="" set "MESAJ=cnn2: ders materyali guncellendi"

where git >nul 2>&1
if errorlevel 1 (
    echo HATA: git bulunamadi. Kurun: https://git-scm.com/download/win
    goto :son
)

REM --- 1) Klon var mi? Yoksa olustur, varsa guncelle -------------------
if not exist "%KLON%\.git" (
    echo [1/4] Repo klonlaniyor -^> %KLON%
    if not exist "%UST%\.gitrepo" mkdir "%UST%\.gitrepo"
    git clone --branch %DAL% "%REPOURL%" "%KLON%"
    if errorlevel 1 echo HATA: klonlama basarisiz. & goto :son
) else (
    echo [1/4] Repo guncelleniyor ^(pull^)
    git -C "%KLON%" checkout %DAL%
    git -C "%KLON%" pull --ff-only
    if errorlevel 1 echo HATA: pull basarisiz. Repoda cakisma olabilir: %KLON% & goto :son
)

REM --- 2) Dosyalari aynala ---------------------------------------------
echo [2/4] Dosyalar kopyalaniyor -^> cnn2\
if not exist "%HEDEF%" mkdir "%HEDEF%"
robocopy "%KAYNAK%" "%HEDEF%" /MIR /NFL /NDL /NJH /NJS /NP /XD ".git" ".ipynb_checkpoints" /XF "push.ps1" "push.bat" "README.md" "*.paint" >nul
if errorlevel 8 echo HATA: robocopy hatasi. & goto :son

REM --- 3) Degisiklik var mi? -------------------------------------------
echo [3/4] Degisiklikler hazirlaniyor
git -C "%KLON%" add -A -- cnn2
git -C "%KLON%" diff --cached --quiet -- cnn2
if not errorlevel 1 (
    echo Degisiklik yok, push atlandi.
    goto :son
)
git -C "%KLON%" --no-pager diff --cached --stat -- cnn2

REM --- 4) Commit + push ------------------------------------------------
echo [4/4] Commit + push
git -C "%KLON%" commit -m "%MESAJ%"
if errorlevel 1 echo HATA: commit basarisiz. & goto :son
git -C "%KLON%" push origin %DAL%
if errorlevel 1 echo HATA: push basarisiz. Kimlik dogrulamasini kontrol edin. & goto :son

echo.
echo TAMAM.
echo   Repo  : https://github.com/gorkenvm/Presentations/tree/%DAL%/cnn2
echo   Colab : https://colab.research.google.com/github/gorkenvm/Presentations/blob/%DAL%/cnn2/cnn2_ders.ipynb
echo.
echo Colab eski surumu gosterirse sekmede Ctrl+Shift+R yapin.

:son
endlocal
pause
