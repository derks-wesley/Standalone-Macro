# Standalone Macro Studio

Een simpele desktop-app in Python om macro's op te nemen en af te spelen (vergelijkbaar met de basis van Logitech G Hub).

## Ik wil alleen een kant-en-klare installer (geen Python nodig)
Gebruik de **Releases** pagina en download:
- `StandaloneMacroSetup.exe` (aanbevolen, normale installer)
- of `StandaloneMacro.exe` (portable)

De release-workflow bouwt dit automatisch op Windows en plaatst de bestanden direct bij een GitHub Release. 【zie `.github/workflows/release-windows.yml`】

## Features
- Toetsenbord-events opnemen (press/release)
- Muis-klikken en scroll opnemen
- Macro opslaan en laden als JSON
- Macro afspelen met speed multiplier
- Herhalen of oneindige loop

## Installatie (development)
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Starten
```bash
python3 macro_app.py
```

## Belangrijk
- De opname en playback zijn **globaal**: ook buiten de app worden inputs vastgelegd/uitgevoerd.
- Sommige systemen vereisen extra rechten voor input-control (bijv. macOS Accessibility, Linux X11).

## Windows build + installer
Deze repository bevat nu ook een **fatsoenlijke Windows EXE + installer-flow**:

1. Installeer Python 3.11+ op Windows.
2. (Optioneel maar aanbevolen) Installeer [Inno Setup 6](https://jrsoftware.org/isinfo.php).
3. Open `cmd.exe` in de projectmap en run:

```bat
build_installer.bat
```

Optioneel kun je metadata meegeven (handig voor release builds):

```bat
set APP_VERSION=1.2.0
set APP_PUBLISHER=Jouw Bedrijf
set APP_URL=https://jouwdomein.nl
build_installer.bat
```

Wat je krijgt:
- Zonder Inno Setup: `dist\StandaloneMacro.exe` (onefile GUI executable)
- Met Inno Setup: `installer\output\StandaloneMacroSetup.exe` (wizard installer + uninstall + snelkoppelingen)

## Klaar EXE bestand (zonder lokaal Windows te bouwen)
Als je lokaal nog geen `.exe` ziet: de repo bevat nu een GitHub Actions workflow die automatisch buildt op `windows-latest` en artifacts uploadt:

- Workflow: `.github/workflows/build-windows.yml`
- Artifacts:
  - `StandaloneMacro-exe` → `StandaloneMacro.exe`
  - `StandaloneMacro-installer` → `StandaloneMacroSetup.exe`

Na een push of handmatige run (`workflow_dispatch`) kun je de bestanden direct downloaden vanuit het Actions-tabblad.

Voor eindgebruikers is **Releases** nog makkelijker: daar staat direct de installer als download.

### Windows-opmerkingen
- Start de app bij voorkeur als Administrator als bepaalde toetsen/muis-events niet replayen in elevated apps.
- De app zet DPI-awareness voor betere schaalbaarheid op high-DPI schermen.
- De build gebruikt Windows version metadata via `windows\version_info.txt`.

## Code signing (nu of later)
Ondertekenen kan later makkelijk toegevoegd worden:

1. Build eerst de EXE + installer (`build_installer.bat`).
2. Onderteken daarna beide artifacts:

```powershell
powershell -ExecutionPolicy Bypass -File .\sign_windows.ps1 -PfxPath "C:\certs\codesign.pfx" -PfxPassword "<wachtwoord>"
```

Hiermee teken je:
- `dist\StandaloneMacro.exe`
- `installer\output\StandaloneMacroSetup.exe`

## Snelle checks
```bash
python3 -m py_compile macro_app.py
python3 -m unittest tests/test_project_files.py
```
