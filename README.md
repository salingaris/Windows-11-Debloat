# Windows 11 Debloater & Fresh App Setup

> **⚠️ WARNING & DRAWBACKS — READ BEFORE RUNNING**
>
> This tool makes deep, system-level changes to Windows 11, including deprovisioning built-in packages, deleting system services, and locking Group Policies. **Create a Windows System Restore Point before running this application.**
>
> Below are the exact drawbacks and side effects of each option if selected:
>
> * **Microsoft OneDrive (`Uninstall Microsoft OneDrive`):**
>   * **Permanent Local Data Loss Risk:** Deletes `%USERPROFILE%\OneDrive` along with the sync client. Any files stored only in that folder—or unsynced desktop/document folders redirected to OneDrive—will be permanently deleted unless backed up first.
>   * Blocks OneDrive file syncing system-wide via Group Policy (`DisableFileSyncNGSC`).
> * **Microsoft Edge (`Force Uninstall Microsoft Edge`):**
>   * Breaks desktop **Windows Widgets**, **Copilot**, and certain in-app sign-in popups or help menus that rely on Edge's engine (note: separate **WebView2** runtime components used by third-party apps remain intact unless manually removed).
>   * Blocks automatic Edge updates via registry policy.
> * **Microsoft Store (`Microsoft Store` / `Disable Microsoft Store via Group Policy`):**
>   * Prevents installing or updating any UWP/Store apps (such as WhatsApp, Netflix, iCloud, or OEM driver control panels like NVIDIA Control Panel and Intel Graphics Command Center).
>   * `winget` Store-sourced packages will no longer work; only `winget` community repository (`msstore` excluded) and standalone `.exe`/`.msi` installers will function.
> * **Media Codecs (`HEVC`, `HEIF`, `AV1`, `VP9`, `MPEG-2`, `Raw Image`, `WebP`, `Web Media Extensions`):**
>   * Windows Photos, File Explorer thumbnails, and built-in media players will no longer open or preview `.heic` iPhone photos, `.mkv`/`.webm` videos, RAW camera files, or hardware-accelerated AV1/HEVC streams. *(Third-party players like VLC or mpv are unaffected.)*
> * **Xbox Ecosystem (`GamingApp`, `XboxGamingOverlay`, `XboxIdentityProvider`, `Xbox.TCUI`):**
>   * Breaks **PC Game Pass**, Xbox sign-in inside Microsoft games (such as *Minecraft*, *Forza*, or *Halo*), **Xbox Game Bar (`Win + G`)** screen recording, and Windows 11's **Auto HDR / Game Mode** overlay features.
> * **Phone Link & Cross-Device (`YourPhone`, `CrossDevice`):**
>   * Disables Android/iPhone notification mirroring, SMS texting from PC, and using your phone as a wireless webcam.
> * **Core Utilities (Unchecked by Default — `Calculator`, `Photos`, `Snipping Tool`, `Notepad`, `Paint`, `Camera`):**
>   * Removes standard Windows shortcuts such as `Win + Shift + S` (Snipping Tool) and built-in image/text viewers until you install third-party replacements.
> * **Telemetry Services (`DiagTrack` & `WerSvc` Deletion):**
>   * **`DiagTrack` (Connected User Experiences and Telemetry):** Permanently deletes the service (`sc.exe delete`). Stops Windows diagnostic data collection, which can also disable certain Microsoft Store personalization features and Windows Insider Program flighting.
>   * **`WerSvc` (Windows Error Reporting):** Permanently deletes the service. Windows will no longer generate crash reports or check Microsoft's database for known fixes when an application crashes.
> * **Microsoft Compatibility Appraiser (`Scheduled Task`):**
>   * Disables background hardware compatibility scans used by Windows Update to check readiness for major feature upgrades (e.g., 24H2/25H2).
> * **Anti-Bloat Registry Policies (`DisableWindowsConsumerFeatures`, `DisableSoftLanding`, `SilentInstalledAppsEnabled`):**
>   * Stops Start Menu app suggestions, lock-screen tips, and silent Store app installs. Some Windows Update feature upgrades may partially reset certain `HKCU` ContentDeliveryManager keys, requiring a re-run after major OS builds.

---

## Features

* **UWP & Built-In App Removal:** Selectively uninstall and deprovision pre-installed Windows apps (Copilot, Widgets, Clipchamp, News, Weather, Xbox ecosystem, Mail/Calendar, New Outlook, OneDrive UWP, and 3rd-party promoted stubs like TikTok, Candy Crush, Netflix, Spotify, etc.) across all user accounts.
* **System & Desktop Cleanup:**
  * Completely uninstall Microsoft OneDrive (desktop client + local leftovers) and disable sync via policy.
  * Force-uninstall Microsoft Edge and block automatic reinstallation via Windows Update.
  * Disable and delete telemetry services (`DiagTrack`, `WerSvc`) and the `Microsoft Compatibility Appraiser` scheduled task.
  * Apply Group Policy / Registry locks to stop Windows from silently reinstalling bloatware.
* **Fresh App Auto-Installer:** Automatically downloads and silently installs the latest versions of:
  * **Mozilla Firefox (64-bit)**
  * **Revo Uninstaller**
  * **Privacy Eraser (Cybertron)**
* **Live Execution Console:** Real-time PowerShell output log built directly into the GUI.
* **Safe Defaults:** Essential everyday utilities (`Calculator`, `Paint`, `Photos`, `Snipping Tool`, `Notepad`, `Microsoft Store`, and `Intel Graphics Command Center`) are unchecked by default.

---

## Quick Start (Standalone `.exe`)

1. Download **`Win11Debloater.exe`** from the [Releases](../../releases) page.
2. Double-click `Win11Debloater.exe` and click **Yes** on the Windows UAC Administrator prompt.
   > **Note:** Because the executable is unsigned, Windows Defender SmartScreen may display *"Windows protected your PC"*. Click **More info → Run anyway** to launch it.
3. Review the checked boxes across each tab, click **▶ Run Selected Tasks**, and restart your PC when finished.

---

## Running from Source

### Prerequisites
* Windows 10 or Windows 11
* Python 3.10+

### Run the GUI
```powershell
git clone [https://github.com/salingaris/Win11Debloater.git
cd Win11Debloater
python debloat_gui.py
