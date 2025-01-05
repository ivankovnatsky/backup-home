def get_excludes():
    return [
        "./**/*.sock",
        "./**/node_modules",
        "./**/target",
        "./.Trash",
        "./.cache/nix",
        "./.cargo",
        "./.cursor/extensions",
        "./.gnupg/S.*",
        "./.local/share/nvim",
        "./.npm",
        "./.orbstack",
        "./.pulumi",
        "./.terraform.d",
        "./.vscode/extensions",
        "./Library/Application Support/Chromium",
        "./Library/Application Support/Cursor",
        "./Library/Application Support/FileProvider",
        "./Library/Application Support/Firefox",
        "./Library/Application Support/Google",
        "./Library/Application Support/Slack",
        "./Library/Application Support/rancher-desktop",
        "./Library/Caches",
        "./Library/Caches/CloudKit",
        "./Library/Caches/FamilyCircle",
        "./Library/Caches/Firefox",
        "./Library/Caches/com.anthropic.claudefordesktop.ShipIt",
        "./Library/Caches/com.apple.HomeKit",
        "./Library/Caches/com.apple.Safari",
        "./Library/Caches/com.apple.ap.adprivacyd",
        "./Library/Caches/com.apple.containermanagerd",
        "./Library/Caches/com.apple.homed",
        "./Library/Caches/pypoetry",
        "./Library/Containers",
        "./Library/Developer/Xcode",
        "./Library/Group Containers",
        "./Library/Mobile Documents/com~apple~CloudDocs",
        "./OrbStack",
        "./Pictures",
        "./Sources/github.com/NixOS/nixpkgs",
        "./go",
    ]