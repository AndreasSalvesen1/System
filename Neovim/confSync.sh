#!/bin/bash
set -e  # Exit on error

# --- RETURNHOST SETUP ---
mkdir -p ~/.local/bin ~/.cache

cat << 'EOF' > ~/.local/bin/returnhost
#!/bin/bash
echo shutdown > ~/.cache/exitflag
EOF

chmod +x ~/.local/bin/returnhost
export PATH="$HOME/.local/bin:$PATH"

# --- CLONE OR UPDATE REPO ---
cd ~
REPO_DIR="$HOME/System"
REPO_URL="https://github.com/AndreasSalvesen1/System"

if [ ! -d "$REPO_DIR" ]; then
    echo "[*] Cloning $REPO_URL"
    git clone "$REPO_URL" "$REPO_DIR"
elif [ -d "$REPO_DIR/.git" ]; then
    echo "[*] Pulling latest in $REPO_DIR"
    git -C "$REPO_DIR" pull
else
    echo "[!] $REPO_DIR exists but is not a Git repo. Skipping."
fi

# --- SYMLINK NEOVIM CONFIG ---
SOURCE_DIR="$HOME/System/Neovim"
TARGET_DIR="$HOME/.config/nvim"

mkdir -p "$HOME/.config"

# If symlink exists but is broken or wrong, replace it
if [ -L "$TARGET_DIR" ] && [ ! -e "$TARGET_DIR" ]; then
  echo "[!] Broken symlink detected at $TARGET_DIR — removing it"
  rm "$TARGET_DIR"
elif [ -e "$TARGET_DIR" ] && [ ! -L "$TARGET_DIR" ]; then
  echo "[!] Backing up real directory: $TARGET_DIR → $TARGET_DIR.backup"
  mv "$TARGET_DIR" "$TARGET_DIR.backup"
fi

# Create new symlink if needed
if [ ! -L "$TARGET_DIR" ]; then
  ln -s "$SOURCE_DIR" "$TARGET_DIR"
  echo "[✓] Symlink created: $TARGET_DIR → $SOURCE_DIR"
else
  echo "[=] Symlink OK: $TARGET_DIR → $(readlink "$TARGET_DIR")"
fi

# --- OPTIONAL: GIT COMMIT & PUSH (if working tree changed) ---
cd "$REPO_DIR"
if ! git diff --quiet || ! git diff --cached --quiet; then
  echo "[*] Changes detected – committing and pushing"
  git add .
  git commit -m "Auto update from container"
  git push || echo "[!] Push failed"
else
  echo "[=] No changes to push"
fi
