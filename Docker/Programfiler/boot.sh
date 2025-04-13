#!/bin/bash
set -e  # Exit immediately if a command fails

# -- RETURNHOST SETUP --
mkdir -p ~/.local/bin ~/.cache

cat << 'EOF' > ~/.local/bin/returnhost
#!/bin/bash
echo shutdown > ~/.cache/exitflag
EOF

chmod +x ~/.local/bin/returnhost
export PATH="$HOME/.local/bin:$PATH"

# -- GIT REPO SYNC --
cd ~
REPO_DIR="$HOME/System"
REPO_URL="https://github.com/AndreasSalvesen1/System"

if [ ! -d "$REPO_DIR" ]; then
    echo "[*] Cloning $REPO_URL into $REPO_DIR"
    git clone "$REPO_URL" "$REPO_DIR"
elif [ -d "$REPO_DIR/.git" ]; then
    echo "[*] Repo exists. Pulling latest changes..."
    git -C "$REPO_DIR" pull
else
    echo "[!] $REPO_DIR exists but is not a git repo. Skipping pull."
fi

# -- OPTIONAL: CLEANUP SYMLINK (uncomment if needed) --
# NVIM_CONFIG="$HOME/.config/nvim"
# if [ -L "$NVIM_CONFIG" ]; then
#     echo "[*] Removing existing Neovim symlink: $NVIM_CONFIG"
#     rm "$NVIM_CONFIG"
# fi

# -- START WINDOW MANAGER --
echo "[*] Starting i3..."
exec i3

