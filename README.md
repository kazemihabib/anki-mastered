# Mastered

Anki add-on to quickly manage cards you already know perfectly. It suspends them and flags them Green (3) so you can distinguish them from difficult suspended cards.

## Features

- **Suspend & Flag Green**: Marks cards as "Mastered" by suspending them and adding a green flag.
- **Works in Reviewer & Browser**: accessible via keyboard shortcuts.
- **Card or Note Application**: Apply to a single card or all cards of the same note.

## Shortcuts

### In Reviewer
- `Shift+C`: Master the current **Card** (Suspend + Green Flag) and move to next.
- `Shift+N`: Master the current **Note** (Suspend all sibling cards + Green Flag) and move to next.

### In Browser
- `Shift+C`: Master selected **Cards**.
- `Shift+N`: Master **Notes** of the selected cards.

## Installation

The easiest way to install Mastered is through AnkiWeb.

1. Open Anki and navigate to **Tools** -> **Add-ons**.
2. Click on **Get Add-ons...**.
3. Paste the code: `578865686`
4. Click **OK** to download.
5. Restart Anki to complete the installation.

View the add-on page on [AnkiWeb](https://ankiweb.net/shared/info/578865686).

## Development Setup

### 1. Link to Anki
Instead of copying files back and forth, create a symbolic link (symlink) from this repository directly into Anki's add-on folder. 

**For Mac:**
```bash
ln -s "$(pwd)/mastered" "~/Library/Application Support/Anki2/addons21/mastered"
```
*(Make sure Anki is closed and there isn't already a `mastered` folder in the `addons21` directory before running this).*

### 2. Python Environment
1. Ensure you have `uv` installed.
2. In the root of this repository, run:
```bash
uv sync
```

Whenever you make changes to `mastered/__init__.py`, simply restart Anki to see your changes live.

### 3. Building for Release
To package the add-on for sharing (via AnkiWeb or direct download), use the included build script. It will safely zip only the necessary files into a .ankiaddon package, ignoring your development environment.

Open your terminal in the root of the project repository.

```bash
./build.sh
```

This will generate a `mastered_release.ankiaddon` file in your project folder, which is ready to be uploaded to AnkiWeb or shared directly.

## Disclaimer
This tool is being developed for personal use, quickly and mostly by AI. Please use at your own risk.

## License
This project is licensed under the MIT License.
