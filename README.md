# Standalone Macro Studio

Een simpele desktop-app in Python om macro's op te nemen en af te spelen (vergelijkbaar met de basis van Logitech G Hub).

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
Deze repository bevat nu ook een Windows installer-flow:

1. Installeer Python 3.11+ op Windows.
2. (Optioneel maar aanbevolen) Installeer [Inno Setup 6](https://jrsoftware.org/isinfo.php).
3. Open `cmd.exe` in de projectmap en run:

```bat
build_installer.bat
```

Wat je krijgt:
- Zonder Inno Setup: `dist\StandaloneMacro\StandaloneMacro.exe`
- Met Inno Setup: `installer\output\StandaloneMacroSetup.exe`

### Windows-opmerkingen
- Start de app bij voorkeur als Administrator als bepaalde toetsen/muis-events niet replayen in elevated apps.
- De app zet DPI-awareness voor betere schaalbaarheid op high-DPI schermen.
