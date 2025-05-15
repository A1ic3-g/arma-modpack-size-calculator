# Arma 3 Modpack Size Calculator

Simple script to calculate how much disk space an Arma 3 modpack uses.

> **NOTE:** For all scripts, the workshop path required is the one inside the `SteamLibrary\workshop\content\107410` folder — **not** the `!WORKSHOP` folder in the Arma installation directory. The `107410` folder corresponds to the Steam game ID for Arma 3.

## Windows (PowerShell)

1. Place your modpack `.html` file exported from the Arma 3 launcher in the same folder as this script. This makes it easier to reference the file when prompted.

2. Run the `arma-modpack-size-windows.ps1` script. You can do this by:

    - Double-clicking the script in File Explorer (a PowerShell window will open), or
    - Running it manually from a PowerShell terminal.

3. When prompted, enter the name or path of your modpack HTML file.

    - If the file is in the same folder as the script, just type the filename (e.g. `modpack.html`).

4. When asked for the Arma 3 workshop folder path, provide the location where Steam stores downloaded workshop mods for Arma 3.
    This path should end in \workshop\content\107410, for example:

    - On a default Steam installation on the C: drive:

        ```txt
        C:\Program Files (x86)\Steam\steamapps\workshop\content\107410
        ```

    - On a secondary drive (e.g. D:)

        ```txt
        D:\SteamLibrary\steamapps\workshop\content\107410
        ```

5. Once complete, the script will display a table showing each mod's size and total usage.

## Linux (Bash)

1. Make the script executable:

    ```bash
    chmod +x arma-modpack-size-linux.sh
    ```

2. Run it from the terminal:

    ```bash
    ./arma-modpack-size-linux.sh
    ```

3. Provide the path to the Arma 3 modpack HTML file exported from the launcher.

4. When prompted, enter the path to your Steam workshop content folder, typically:

    ```bash
    ~/.steam/steam/SteamApps/workshop/content/107410
    ```

5. The script will parse the mod list, check each mod's folder size, and output a table sorted by size in megabytes.

## System-agnostic (Python)

This version runs on both Windows and Linux systems and is ideal if you already have Python installed. It's also useful if you want to generate graphs using matplotlib, or export the data to a CSV file for visualisation in spreadsheet software such as Excel.

The python script has been moved to the `python` subfolder since for most users this will be harder to use.

### Usage

1. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

2. Run the script:

    ```bash
    python3 arma-modpack-size-tool.py
    ```

3. Enter the path to the exported modpack `.html` file and the workshop folder path (`SteamLibrary/workshop/content/107410`) when prompted.
