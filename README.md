# 📦 Arma 3 Modpack Size Calculator

A simple script to calculate how much disk space an Arma 3 modpack uses by scanning each subscribed mod’s workshop folder.

> **Important:** The workshop path must be the one inside `SteamLibrary\steamapps\workshop\content\107410`  
> **Do not use** the `!WORKSHOP` folder inside the Arma 3 installation directory.  
>
> `107410` is the Steam App ID for Arma 3.


## 🪟 Windows (PowerShell)

1. Place your exported Arma 3 modpack `.html` file in the same folder as the script. This makes it easier to locate when prompted.

2. Run `arma-modpack-size-windows.ps1` by either:
    - Double-clicking it in File Explorer, **or**
    - Running it from a PowerShell terminal.

3. When prompted:
    - Enter the name or path of your modpack HTML file.  
      If it's in the same folder, just type the filename (e.g. `modpack.html`).

4. When asked for the **workshop folder path**, provide the location where Steam stores Arma 3 workshop content.  
   This should end in `\workshop\content\107410`. Common examples:

    - Default C: drive installation:

      ```txt
      C:\Program Files (x86)\Steam\steamapps\workshop\content\107410
      ```

    - Secondary drive (e.g. D:):

      ```txt
      D:\SteamLibrary\steamapps\workshop\content\107410
      ```

5. The script will display a table of mod sizes and the total usage, then pause with a `"Press Enter to exit"` prompt.

## 🐧 Linux (Bash)

1. Make the script executable:

    ```bash
    chmod +x arma-modpack-size-linux.sh
    ```

2. Run the script:

    ```bash
    ./arma-modpack-size-linux.sh
    ```

3. Provide the full path to your exported modpack HTML file when prompted.

4. When asked for the **workshop folder path**, it is typically:

    ```bash
    ~/.steam/steam/steamapps/workshop/content/107410
    ```

5. The script will scan each mod folder, compute sizes, and display a table sorted by size in MB.

## 🐍 System-Agnostic (Python)

This version works on **Windows** or **Linux** and is recommended if:

- You want to export mod sizes as CSV
- You plan to generate graphs using `matplotlib`
- You want more flexibility in scripting or automation

📁 The script is located in the `python/` subfolder for clarity, as it’s only recommended for more advanced users.

### 🔧 Usage

1. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

2. Run the script:

    ```bash
    python3 python/arma-modpack-size-tool.py
    ```

3. When prompted:
    - Enter the path to your exported modpack `.html` file
    - Enter the path to the Arma 3 workshop folder (e.g. `SteamLibrary/workshop/content/107410`)
