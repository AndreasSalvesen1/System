#!/bin/bash

SOURCE_DIR="$HOME/ws/System/Neovim"
TARGET_DIR="$HOME/.config/nvim"

# Backup existing config if it’s not a symlink
if [ -e "$TARGET_DIR" ] && [ ! -L "$TARGET_DIR" ]; then
  echo "[!] Backing up existing ~/.config/nvim to ~/.config/nvim.backup"
  mv "$TARGET_DIR" "$TARGET_DIR.backup"
fi

# Ensure ~/.config exists
mkdir -p "$HOME/.config"

# Create symlink
if [ ! -L "$TARGET_DIR" ]; then
  ln -s "$SOURCE_DIR" "$TARGET_DIR"
  echo "[✓] Symlink created: $TARGET_DIR → $SOURCE_DIR"
else
  echo "[=] Symlink already exists: $TARGET_DIR → $(readlink $TARGET_DIR)"
fi

