import ctypes
import subprocess
import sys
import threading
import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk

# ==============================================================================
# DATA DEFINITIONS
# ==============================================================================

UWP_CATEGORIES = {
    "Core Windows Utilities & Media": [
        ("AV1 Video Extension", "*Microsoft.AV1VideoExtension*", True),
        ("AVC Encoder Video Extension", "*Microsoft.AVCEncoderVideoExtension*", True),
        ("Calculator", "*Microsoft.WindowsCalculator*", False),
        ("Clock & Alarms", "*Microsoft.WindowsAlarms*", True),
        ("Dev Home", "*Microsoft.Windows.DevHome*", True),
        ("Feedback Hub", "*Microsoft.WindowsFeedbackHub*", True),
        ("Get Help", "*Microsoft.GetHelp*", True),
        ("Get Started / Tips", "*Microsoft.Getstarted*", True),
        ("HEIF Image Extension", "*Microsoft.HEIFImageExtension*", True),
        ("HEVC Video Extension", "*Microsoft.HEVCVideoExtension*", True),
        ("Intel Graphics Command Center", "*AppUp.IntelGraphicsExperience*", False),
        ("Media Player / Zune Music", "*Microsoft.ZuneMusic*", True),
        ("Movies & TV / Zune Video", "*Microsoft.ZuneVideo*", True),
        ("Bing Search", "*Microsoft.BingSearch*", True),
        ("Clipchamp", "*Clipchamp.Clipchamp*", True),
        ("Microsoft Family", "*MicrosoftCorporationII.MicrosoftFamily*", True),
        ("Microsoft News", "*Microsoft.BingNews*", True),
        ("Microsoft To Do", "*Microsoft.Todos*", True),
        ("Cross Device Experience", "*MicrosoftWindows.CrossDevice*", True),
        ("MPEG-2 Video Extension", "*Microsoft.MPEG2VideoExtension*", True),
        ("Paint", "*Microsoft.Paint*", False),
        ("Paint 3D", "*Microsoft.MSPaint*", True),
        ("3D Viewer", "*Microsoft.Microsoft3DViewer*", True),
        ("Mixed Reality Portal", "*Microsoft.MixedReality.Portal*", True),
        ("Phone Link", "*Microsoft.YourPhone*", True),
        ("Photos", "*Microsoft.Windows.Photos*", False),
        ("Power Automate Desktop", "*Microsoft.PowerAutomateDesktop*", True),
        ("Quick Assist", "*MicrosoftCorporationII.QuickAssist*", True),
        ("Raw Image Extension", "*Microsoft.RawImageExtension*", True),
        ("Snipping Tool", "*Microsoft.ScreenSketch*", False),
        ("Solitaire Collection", "*Microsoft.MicrosoftSolitaireCollection*", True),
        ("Sound Recorder", "*Microsoft.WindowsSoundRecorder*", True),
        ("Sticky Notes", "*Microsoft.MicrosoftStickyNotes*", True),
        ("Microsoft Store", "*Microsoft.WindowsStore*", False),
        ("Store Purchase App", "*Microsoft.StorePurchaseApp*", False),
        ("VP9 Video Extensions", "*Microsoft.VP9VideoExtensions*", True),
        ("Weather", "*Microsoft.BingWeather*", True),
        ("MSN Money", "*Microsoft.BingFinance*", True),
        ("MSN Sports", "*Microsoft.BingSports*", True),
        ("Web Media Extensions", "*Microsoft.WebMediaExtensions*", True),
        ("WebP Image Extension", "*Microsoft.WebpImageExtension*", True),
        ("Windows Apprep ChxApp", "*Microsoft.Windows.Apprep.ChxApp*", True),
        ("Camera", "*Microsoft.WindowsCamera*", True),
        ("Notepad", "*Microsoft.WindowsNotepad*", False),
        ("Windows Maps", "*Microsoft.WindowsMaps*", True),
        ("People", "*Microsoft.People*", True),
        ("Microsoft Wallet / Pay", "*Microsoft.Wallet*", True),
        ("Print 3D", "*Microsoft.Print3D*", True),
        ("Mobile Plans (OneConnect)", "*Microsoft.OneConnect*", True),
        ("Messaging", "*Microsoft.Messaging*", True),
        ("Windows Scan", "*Microsoft.WindowsScan*", True),
        ("Microsoft Whiteboard", "*Microsoft.Whiteboard*", True),
        ("Windows 11 Widgets", "*MicrosoftWindows.Client.WebExperience*", True),
        ("Microsoft Copilot", "*Microsoft.Copilot*", True),
    ],
    "Communication, Office & Xbox": [
        ("Mail and Calendar", "*microsoft.windowscommunicationsapps*", True),
        ("Office / Microsoft 365 Hub", "*Microsoft.MicrosoftOfficeHub*", True),
        ("OneNote for Windows 10", "*Microsoft.Office.OneNote*", True),
        ("Sway", "*Microsoft.Office.Sway*", True),
        ("Skype", "*Microsoft.SkypeApp*", True),
        ("Microsoft Teams (Chat)", "*MicrosoftTeams*", True),
        ("New Microsoft Teams", "*MSTeams*", True),
        ("New Outlook for Windows", "*Microsoft.OutlookForWindows*", True),
        ("OneDrive UWP Sync", "*Microsoft.OneDriveSync*", True),
        ("Xbox App", "*Microsoft.GamingApp*", True),
        ("Xbox Companion App", "*Microsoft.XboxApp*", True),
        ("Xbox Game Bar", "*Microsoft.XboxGamingOverlay*", True),
        ("Xbox Game Overlay", "*Microsoft.XboxGameOverlay*", True),
        ("Xbox Speech to Text", "*Microsoft.XboxSpeechToTextOverlay*", True),
        ("Xbox Identity Provider", "*Microsoft.XboxIdentityProvider*", True),
        ("Xbox TCUI", "*Microsoft.Xbox.TCUI*", True),
    ],
    "Pre-installed 3rd-Party Stubs": [
        ("Spotify", "*SpotifyAB.SpotifyMusic*", True),
        ("Disney+", "*Disney.37853FC22B2CE*", True),
        ("Netflix", "*4DF9E0F8.Netflix*", True),
        ("Candy Crush", "*king.com.CandyCrush*", True),
        ("Facebook", "*Facebook.Facebook*", True),
        ("Instagram", "*Facebook.InstagramBeta*", True),
        ("TikTok", "*BytedancePte.Ltd.TikTok*", True),
        ("Prime Video", "*AmazonVideo.PrimeVideo*", True),
        ("LinkedIn", "*7EE7776C.LinkedInforWindows*", True),
    ],
}

SYSTEM_TWEAKS = [
    ("onedrive", "Uninstall Microsoft OneDrive Desktop Client & Leftovers", True),
    ("edge", "Force Uninstall Microsoft Edge & EdgeUpdate", True),
    ("firefox_remove", "Uninstall Existing Mozilla Firefox & Maintenance Service", False),
    ("revo_remove", "Uninstall Existing Revo Uninstaller Pro", False),
    ("telemetry", "Disable & Delete Telemetry Services (DiagTrack, WerSvc) & Appraiser Task", True),
    ("policies", "Apply Registry Policies (Block Consumer Features, Tips & Silent Reinstalls)", True),
    ("store_policy", "Disable Microsoft Store via Group Policy", False),
]

INSTALL_APPS = [
    ("install_firefox", "Download & Install Latest Mozilla Firefox (64-bit)", True),
    ("install_revo", "Download & Install Latest Revo Uninstaller", True),
    ("install_privacy_eraser", "Download & Install Latest Privacy Eraser (Cybertron)", True),
]


# ==============================================================================
# ADMIN CHECK
# ==============================================================================

def is_admin() -> bool:
    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        return False


# ==============================================================================
# MAIN GUI APPLICATION
# ==============================================================================

class DebloaterApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Windows 11 Debloater & App Setup")
        self.root.geometry("950x700")
        self.root.minsize(820, 600)
        self.root.configure(bg="#1e1e1e")

        self.uwp_vars: dict[str, tk.BooleanVar] = {}
        self.tweak_vars: dict[str, tk.BooleanVar] = {}
        self.install_vars: dict[str, tk.BooleanVar] = {}

        self._setup_styles()
        self._build_ui()

    def _setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        bg_dark = "#1e1e1e"
        bg_panel = "#252526"
        fg_text = "#f3f3f3"
        accent = "#0078d4"

        style.configure("TFrame", background=bg_dark)
        style.configure("Panel.TFrame", background=bg_panel)
        style.configure("TLabel", background=bg_dark, foreground=fg_text, font=("Segoe UI", 10))
        style.configure("Header.TLabel", background=bg_dark, foreground="#ffffff", font=("Segoe UI", 15, "bold"))
        style.configure("Sub.TLabel", background=bg_dark, foreground="#aaaaaa", font=("Segoe UI", 9))
        style.configure("PanelInfo.TLabel", background=bg_panel, foreground="#bbbbbb", font=("Segoe UI", 9, "italic"))

        style.configure("TNotebook", background=bg_dark, borderwidth=0)
        style.configure("TNotebook.Tab", background="#2d2d2d", foreground="#cccccc", padding=[12, 6], font=("Segoe UI", 9, "bold"))
        style.map("TNotebook.Tab", background=[("selected", accent)], foreground=[("selected", "#ffffff")])

        style.configure("TCheckbutton", background=bg_panel, foreground=fg_text, font=("Segoe UI", 9))
        style.map("TCheckbutton", background=[("active", "#2a2d2e")])

        style.configure("Accent.TButton", background=accent, foreground="#ffffff", font=("Segoe UI", 10, "bold"), padding=[14, 6])
        style.map("Accent.TButton", background=[("active", "#106ebe")])

        style.configure("Secondary.TButton", background="#333333", foreground="#ffffff", font=("Segoe UI", 9), padding=[10, 5])
        style.map("Secondary.TButton", background=[("active", "#444444")])

    def _build_ui(self):
        # Top Header
        header_frame = ttk.Frame(self.root, padding=(16, 12, 16, 6))
        header_frame.pack(fill="x")

        ttk.Label(header_frame, text="Windows 11 System Debloater & Fresh Installer", style="Header.TLabel").pack(anchor="w")
        ttk.Label(
            header_frame,
            text="Remove Windows bloatware and automatically download & install the latest essential tools.",
            style="Sub.TLabel",
        ).pack(anchor="w", pady=(2, 0))

        # Toolbar Buttons
        toolbar = ttk.Frame(self.root, padding=(16, 4, 16, 8))
        toolbar.pack(fill="x")

        ttk.Button(toolbar, text="Select All", style="Secondary.TButton", command=lambda: self._toggle_all(True)).pack(side="left", padx=(0, 6))
        ttk.Button(toolbar, text="Deselect All", style="Secondary.TButton", command=lambda: self._toggle_all(False)).pack(side="left", padx=(0, 6))
        ttk.Button(toolbar, text="Reset Recommended", style="Secondary.TButton", command=self._reset_defaults).pack(side="left", padx=(0, 6))
        
        # NEW Restore Point Button
        self.restore_btn = ttk.Button(toolbar, text="🛡️ Create Restore Point", style="Secondary.TButton", command=self._start_restore_point)
        self.restore_btn.pack(side="left")

        self.run_btn = ttk.Button(toolbar, text="▶ Run Selected Tasks", style="Accent.TButton", command=self._start_execution)
        self.run_btn.pack(side="right")

        # Notebook Tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=16, pady=(0, 8))

        for category, items in UWP_CATEGORIES.items():
            tab = self._create_scrollable_tab(category)
            for idx, (label, pattern, default) in enumerate(items):
                var = tk.BooleanVar(value=default)
                self.uwp_vars[pattern] = var
                cb = ttk.Checkbutton(tab, text=f"{label}  ({pattern})", variable=var)
                cb.grid(row=idx // 2, column=idx % 2, sticky="w", padx=12, pady=4)

        # System & Desktop Tweaks Tab
        tweaks_tab = self._create_scrollable_tab("Desktop Removal & System Tweaks")
        for idx, (key, label, default) in enumerate(SYSTEM_TWEAKS):
            var = tk.BooleanVar(value=default)
            self.tweak_vars[key] = var
            cb = ttk.Checkbutton(tweaks_tab, text=label, variable=var)
            cb.grid(row=idx, column=0, sticky="w", padx=12, pady=6)

        # Install Fresh Apps Tab
        install_tab = self._create_scrollable_tab("Install Fresh Apps")
        ttk.Label(
            install_tab,
            text="Selected apps will be downloaded and installed silently after cleanup finishes:",
            style="PanelInfo.TLabel",
        ).grid(row=0, column=0, sticky="w", padx=12, pady=(6, 10))

        for idx, (key, label, default) in enumerate(INSTALL_APPS, start=1):
            var = tk.BooleanVar(value=default)
            self.install_vars[key] = var
            cb = ttk.Checkbutton(install_tab, text=label, variable=var)
            cb.grid(row=idx, column=0, sticky="w", padx=12, pady=6)

        # Console Output Frame
        log_frame = ttk.Frame(self.root, padding=(16, 0, 16, 14))
        log_frame.pack(fill="both", expand=False)

        ttk.Label(log_frame, text="Live Execution Log:", style="Sub.TLabel").pack(anchor="w", pady=(0, 4))
        self.console = scrolledtext.ScrolledText(
            log_frame,
            height=11,
            bg="#121212",
            fg="#00ff66",
            insertbackground="#ffffff",
            font=("Consolas", 9),
            relief="flat",
            state="disabled",
        )
        self.console.pack(fill="both", expand=True)

    def _create_scrollable_tab(self, title: str) -> ttk.Frame:
        outer = ttk.Frame(self.notebook, style="Panel.TFrame")
        self.notebook.add(outer, text=title)

        canvas = tk.Canvas(outer, bg="#252526", highlightthickness=0)
        scrollbar = ttk.Scrollbar(outer, orient="vertical", command=canvas.yview)
        inner = ttk.Frame(canvas, style="Panel.TFrame")

        inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=inner, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True, padx=4, pady=6)
        scrollbar.pack(side="right", fill="y")

        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))
        return inner

    def _toggle_all(self, state: bool):
        for var in self.uwp_vars.values():
            var.set(state)
        for var in self.tweak_vars.values():
            var.set(state)
        for var in self.install_vars.values():
            var.set(state)

    def _reset_defaults(self):
        for items in UWP_CATEGORIES.values():
            for _, pattern, default in items:
                self.uwp_vars[pattern].set(default)
        for key, _, default in SYSTEM_TWEAKS:
            self.tweak_vars[key].set(default)
        for key, _, default in INSTALL_APPS:
            self.install_vars[key].set(default)

    def _log(self, text: str):
        self.console.configure(state="normal")
        self.console.insert("end", text)
        self.console.see("end")
        self.console.configure(state="disabled")

    def _build_powershell_script(self) -> str:
        selected_uwp = [pat for pat, var in self.uwp_vars.items() if var.get()]
        ps_lines = [
            '$ErrorActionPreference = "SilentlyContinue"',
            '[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12',
        ]

        # 1. Remove Selected UWP Apps
        if selected_uwp:
            patterns_str = ",\n    ".join(f'"{p}"' for p in selected_uwp)
            ps_lines.append(f"""
Write-Host "=== 1. Removing Selected UWP / Windows Apps ==="
$UwpApps = @(
    {patterns_str}
)
$DeprovRegPath = "HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Appx\\AppxAllUserStore\\Deprovisioned"
New-Item -Path $DeprovRegPath -Force | Out-Null

foreach ($Pattern in $UwpApps) {{
    Get-AppxPackage -AllUsers -Name $Pattern | ForEach-Object {{
        Write-Host "Removing Appx: $($_.Name)"
        $_ | Remove-AppxPackage -AllUsers
    }}
    Get-AppxProvisionedPackage -Online | Where-Object {{ $_.DisplayName -like $Pattern }} | ForEach-Object {{
        Write-Host "Deprovisioning: $($_.DisplayName)"
        New-Item -Path "$DeprovRegPath\\$($_.PackageName)" -Force | Out-Null
        Remove-AppxProvisionedPackage -Online -PackageName $_.PackageName | Out-Null
    }}
    Get-ChildItem -Path "$env:LOCALAPPDATA\\Packages" -Filter $Pattern | Remove-Item -Recurse -Force
}}
""")

        # 2. Desktop Removals
        if self.tweak_vars["onedrive"].get():
            ps_lines.append("""
Write-Host "=== Uninstalling Microsoft OneDrive ==="
Get-Process -Name "OneDrive" | Stop-Process -Force
$OneDriveSetup64 = "$env:SystemRoot\\System32\\OneDriveSetup.exe"
$OneDriveSetup32 = "$env:SystemRoot\\SysWOW64\\OneDriveSetup.exe"
if (Test-Path $OneDriveSetup64) { Start-Process -FilePath $OneDriveSetup64 -ArgumentList "/uninstall" -Wait }
if (Test-Path $OneDriveSetup32) { Start-Process -FilePath $OneDriveSetup32 -ArgumentList "/uninstall" -Wait }
$OneDriveDirs = @("$env:USERPROFILE\\OneDrive", "$env:LOCALAPPDATA\\Microsoft\\OneDrive", "$env:ProgramData\\Microsoft OneDrive")
foreach ($Dir in $OneDriveDirs) { if (Test-Path $Dir) { Remove-Item -Path $Dir -Recurse -Force } }
$OneDrivePolicyPath = "HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows\\OneDrive"
New-Item -Path $OneDrivePolicyPath -Force | Out-Null
Set-ItemProperty -Path $OneDrivePolicyPath -Name "DisableFileSyncNGSC" -Value 1 -Type DWord
""")

        if self.tweak_vars["edge"].get():
            ps_lines.append("""
Write-Host "=== Force Uninstalling Microsoft Edge ==="
Get-Process -Name "msedge", "MicrosoftEdgeUpdate" | Stop-Process -Force
$EdgePath = "${env:ProgramFiles(x86)}\\Microsoft\\Edge\\Application"
if (Test-Path $EdgePath) {
    Get-ChildItem -Path $EdgePath -Directory | ForEach-Object {
        $SetupExe = Join-Path $_.FullName "Installer\\setup.exe"
        if (Test-Path $SetupExe) {
            Start-Process -FilePath $SetupExe -ArgumentList "--uninstall --system-level --verbose-logging --force-uninstall" -Wait
        }
    }
}
$EdgeDirs = @("${env:ProgramFiles(x86)}\\Microsoft\\Edge", "${env:ProgramFiles(x86)}\\Microsoft\\EdgeUpdate", "${env:ProgramFiles(x86)}\\Microsoft\\EdgeCore", "$env:LOCALAPPDATA\\Microsoft\\Edge")
foreach ($Dir in $EdgeDirs) { if (Test-Path $Dir) { Remove-Item -Path $Dir -Recurse -Force } }
$EdgeUpdatePolicy = "HKLM:\\SOFTWARE\\Microsoft\\EdgeUpdate"
New-Item -Path $EdgeUpdatePolicy -Force | Out-Null
Set-ItemProperty -Path $EdgeUpdatePolicy -Name "DoNotUpdateToEdgeWithChromium" -Value 1 -Type DWord
""")

        if self.tweak_vars["firefox_remove"].get():
            ps_lines.append("""
Write-Host "=== Uninstalling Existing Mozilla Firefox ==="
$FirefoxHelper = "${env:ProgramFiles}\\Mozilla Firefox\\uninstall\\helper.exe"
$FirefoxMaint  = "${env:ProgramFiles(x86)}\\Mozilla Maintenance Service\\uninstall.exe"
if (Test-Path $FirefoxHelper) { Start-Process -FilePath $FirefoxHelper -ArgumentList "/S" -Wait }
if (Test-Path $FirefoxMaint)  { Start-Process -FilePath $FirefoxMaint -ArgumentList "/S" -Wait }
foreach ($Dir in @("${env:ProgramFiles}\\Mozilla Firefox", "${env:ProgramFiles(x86)}\\Mozilla Maintenance Service", "$env:APPDATA\\Mozilla", "$env:LOCALAPPDATA\\Mozilla")) {
    if (Test-Path $Dir) { Remove-Item -Path $Dir -Recurse -Force }
}
""")

        if self.tweak_vars["revo_remove"].get():
            ps_lines.append("""
Write-Host "=== Uninstalling Existing Revo Uninstaller Pro ==="
$RevoUninst = "${env:ProgramFiles}\\VS Revo Group\\Revo Uninstaller Pro\\unins000.exe"
if (Test-Path $RevoUninst) { Start-Process -FilePath $RevoUninst -ArgumentList "/VERYSILENT /SUPPRESSMSGBOXES /NORESTART" -Wait }
foreach ($Dir in @("${env:ProgramFiles}\\VS Revo Group", "$env:ProgramData\\VS Revo Group")) {
    if (Test-Path $Dir) { Remove-Item -Path $Dir -Recurse -Force }
}
""")

        # 3. Telemetry & Policies
        if self.tweak_vars["telemetry"].get():
            ps_lines.append("""
Write-Host "=== Disabling Telemetry Services & Tasks ==="
foreach ($Service in @("DiagTrack", "WerSvc")) {
    if (Get-Service -Name $Service) {
        Write-Host "Deleting service: $Service"
        Stop-Service -Name $Service -Force
        Set-Service -Name $Service -StartupType Disabled
        sc.exe delete $Service | Out-Null
    }
}
$TaskPath = "\\Microsoft\\Windows\\Application Experience\\"
$TaskName = "Microsoft Compatibility Appraiser"
if (Get-ScheduledTask -TaskPath $TaskPath -TaskName $TaskName) {
    Write-Host "Disabling task: $TaskName"
    Disable-ScheduledTask -TaskPath $TaskPath -TaskName $TaskName | Out-Null
}
""")

        if self.tweak_vars["policies"].get():
            ps_lines.append("""
Write-Host "=== Applying Anti-Bloat Registry Policies ==="
$CloudContentPath = "HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows\\CloudContent"
New-Item -Path $CloudContentPath -Force | Out-Null
Set-ItemProperty -Path $CloudContentPath -Name "DisableWindowsConsumerFeatures" -Value 1 -Type DWord
Set-ItemProperty -Path $CloudContentPath -Name "DisableSoftLanding" -Value 1 -Type DWord

$ContentDeliveryPath = "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\ContentDeliveryManager"
New-Item -Path $ContentDeliveryPath -Force | Out-Null
Set-ItemProperty -Path $ContentDeliveryPath -Name "SubscribedContent-338389Enabled" -Value 0 -Type DWord
Set-ItemProperty -Path $ContentDeliveryPath -Name "SilentInstalledAppsEnabled" -Value 0 -Type DWord
Set-ItemProperty -Path $ContentDeliveryPath -Name "PreInstalledAppsEnabled" -Value 0 -Type DWord
Set-ItemProperty -Path $ContentDeliveryPath -Name "OemPreInstalledAppsEnabled" -Value 0 -Type DWord
""")

        if self.tweak_vars["store_policy"].get():
            ps_lines.append("""
Write-Host "=== Disabling Microsoft Store via Group Policy ==="
$StorePolicyPath = "HKLM:\\SOFTWARE\\Policies\\Microsoft\\WindowsStore"
New-Item -Path $StorePolicyPath -Force | Out-Null
Set-ItemProperty -Path $StorePolicyPath -Name "RemoveWindowsStore" -Value 1 -Type DWord
Set-ItemProperty -Path $StorePolicyPath -Name "AutoDownload" -Value 2 -Type DWord
""")

        # 4. Download & Install Latest Selected Apps
        any_install = any(var.get() for var in self.install_vars.values())
        if any_install:
            ps_lines.append("""
Write-Host "`n=== Downloading & Installing Latest Selected Apps ==="
$HasWinget = [bool](Get-Command winget -ErrorAction SilentlyContinue)
$TempDir = "$env:TEMP\\Win11SetupDownloads"
New-Item -Path $TempDir -ItemType Directory -Force | Out-Null
""")

            if self.install_vars["install_firefox"].get():
                ps_lines.append("""
Write-Host "Installing latest Mozilla Firefox..."
$Installed = $false
if ($HasWinget) {
    winget install --id Mozilla.Firefox --exact --silent --accept-package-agreements --accept-source-agreements
    if ($LASTEXITCODE -eq 0) { $Installed = $true }
}
if (-not $Installed) {
    Write-Host "Downloading Firefox directly from Mozilla..."
    $FfInstaller = "$TempDir\\FirefoxSetup.exe"
    Invoke-WebRequest -Uri "https://download.mozilla.org/?product=firefox-latest-ssl&os=win64&lang=en-US" -OutFile $FfInstaller -UseBasicParsing
    if (Test-Path $FfInstaller) {
        Start-Process -FilePath $FfInstaller -ArgumentList "/S" -Wait
    }
}
Write-Host "Mozilla Firefox installation finished."
""")

            if self.install_vars["install_revo"].get():
                ps_lines.append("""
Write-Host "Installing latest Revo Uninstaller..."
$Installed = $false
if ($HasWinget) {
    winget install --id RevoUninstaller.RevoUninstaller --exact --silent --accept-package-agreements --accept-source-agreements
    if ($LASTEXITCODE -eq 0) { $Installed = $true }
}
if (-not $Installed) {
    Write-Host "Downloading Revo Uninstaller directly from vendor..."
    $RevoInstaller = "$TempDir\\revosetup.exe"
    Invoke-WebRequest -Uri "https://www.revouninstaller.com/download-freeware-version.php" -OutFile $RevoInstaller -UseBasicParsing
    if (Test-Path $RevoInstaller) {
        Start-Process -FilePath $RevoInstaller -ArgumentList "/VERYSILENT /SUPPRESSMSGBOXES /NORESTART" -Wait
    }
}
Write-Host "Revo Uninstaller installation finished."
""")

            if self.install_vars["install_privacy_eraser"].get():
                ps_lines.append("""
Write-Host "Installing latest Privacy Eraser (Cybertron)..."
$Installed = $false
if ($HasWinget) {
    winget install --id CybertronSoftware.PrivacyEraser --exact --silent --accept-package-agreements --accept-source-agreements
    if ($LASTEXITCODE -eq 0) { $Installed = $true }
}
if (-not $Installed) {
    Write-Host "Downloading Privacy Eraser directly from Cybertron..."
    $PeInstaller = "$TempDir\\privacy-eraser-setup.exe"
    Invoke-WebRequest -Uri "https://www.cybertronsoft.com/download/privacy-eraser-setup.exe" -OutFile $PeInstaller -UseBasicParsing
    if (Test-Path $PeInstaller) {
        Start-Process -FilePath $PeInstaller -ArgumentList "/VERYSILENT /SUPPRESSMSGBOXES /NORESTART" -Wait
    }
}
Write-Host "Privacy Eraser installation finished."
""")

            ps_lines.append('Remove-Item -Path $TempDir -Recurse -Force')

        ps_lines.append('Write-Host "`nAll selected tasks completed! Restart your PC to finalize changes."')
        return "\n".join(ps_lines)

    def _start_restore_point(self):
        self.restore_btn.configure(state="disabled")
        self.run_btn.configure(state="disabled")
        self.console.configure(state="normal")
        self.console.delete("1.0", "end")
        self.console.configure(state="disabled")
        
        script = """
Write-Host "=== Enabling System Protection & Creating System Restore Point ==="
Write-Host "Checking if System Restore is enabled for Drive C:..."

# Enable System Protection (in case Windows 11 default turned it off)
Enable-ComputerRestore -Drive "C:\\" -ErrorAction SilentlyContinue

# Bypasses the 24-hour frequency restriction for scripting
$RegPath = "HKLM:\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\SystemRestore"
if (-not (Test-Path $RegPath)) { New-Item -Path $RegPath -Force | Out-Null }
Set-ItemProperty -Path $RegPath -Name "SystemRestorePointCreationFrequency" -Value 0 -Type DWord -Force -ErrorAction SilentlyContinue

Write-Host "Creating 'Pre-Debloat Backup' System Restore Point..."
Write-Host "This might take a minute. Please do not close the app..."

Checkpoint-Computer -Description "Pre-Debloat Backup" -RestorePointType "MODIFY_SETTINGS" -ErrorAction Stop

if ($LASTEXITCODE -eq 0 -or $?) {
    Write-Host "`n[SUCCESS] System Restore Point 'Pre-Debloat Backup' created successfully!" -ForegroundColor Green
} else {
    Write-Host "`n[ERROR] Failed to create restore point. Make sure Group Policy has not blocked restore point creation." -ForegroundColor Red
}
"""
        threading.Thread(target=self._execute_worker, args=(script, True), daemon=True).start()

    def _start_execution(self):
        if not messagebox.askyesno(
            "Confirm Execution",
            "Run all selected debloat and installation tasks?\n\nMake sure you have backed up any local OneDrive files.",
        ):
            return

        self.run_btn.configure(state="disabled")
        self.restore_btn.configure(state="disabled")
        self.console.configure(state="normal")
        self.console.delete("1.0", "end")
        self.console.configure(state="disabled")

        script = self._build_powershell_script()
        threading.Thread(target=self._execute_worker, args=(script,), daemon=True).start()

    def _execute_worker(self, script: str, is_restore_point_only: bool = False):
        process = subprocess.Popen(
            ["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", "-"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW,
        )

        if process.stdin:
            process.stdin.write(script)
            process.stdin.close()

        if process.stdout:
            for line in iter(process.stdout.readline, ""):
                self.root.after(0, self._log, line)

        process.wait()
        self.root.after(0, lambda: self.run_btn.configure(state="normal"))
        self.root.after(0, lambda: self.restore_btn.configure(state="normal"))
        
        if is_restore_point_only:
            self.root.after(
                0,
                lambda: messagebox.showinfo(
                    "Restore Point Status", 
                    "System Restore Point Creation Task finished! View log for success/failure."
                )
            )
        else:
            self.root.after(
                0,
                lambda: messagebox.showinfo(
                    "Complete", "All tasks finished! Restart your PC to finalize changes."
                ),
            )


def main():
    if sys.platform != "win32":
        print("This application only runs on Windows.")
        sys.exit(1)

    if not is_admin():
        params = " ".join(f'"{arg}"' for arg in sys.argv)
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)
        sys.exit(0)

    root = tk.Tk()
    DebloaterApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()