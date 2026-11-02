#!/usr/bin/env bash
# Install or update the `waiching-sun-writing` global skill/plugin for:
#   1. Google Antigravity (~/.gemini/config/plugins/waiching-sun-writing)
#   2. Claude Code        (~/.claude/skills/waiching-sun-writing)
#   3. OpenAI Codex       (~/.codex/skills/waiching-sun-writing)

set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_SRC="${REPO_DIR}/skills/waiching-sun-writing"

AGY_PLUGIN_DIR="${HOME}/.gemini/config/plugins/waiching-sun-writing"
AGY_LEGACY_SKILL="${HOME}/.gemini/config/skills/waiching-sun-writing"
CLAUDE_SKILL_DIR="${HOME}/.claude/skills/waiching-sun-writing"
CODEX_SKILL_DIR="${HOME}/.codex/skills/waiching-sun-writing"

chmod +x "${SKILL_SRC}/scripts/"*.py

echo "==> [1/3] Installing for Google Antigravity (${AGY_PLUGIN_DIR})..."
if [ -L "${AGY_LEGACY_SKILL}" ] || [ -e "${AGY_LEGACY_SKILL}" ]; then
  rm -rf "${AGY_LEGACY_SKILL}"
fi
mkdir -p "${AGY_PLUGIN_DIR}"
rsync -a --delete \
  --exclude '.git' \
  --exclude '.agents' \
  --exclude '__pycache__' \
  "${REPO_DIR}/plugin.json" \
  "${REPO_DIR}/README.md" \
  "${REPO_DIR}/assets" \
  "${REPO_DIR}/skills" \
  "${AGY_PLUGIN_DIR}/"

echo "==> [2/3] Installing for Claude Code (${CLAUDE_SKILL_DIR})..."
mkdir -p "${HOME}/.claude/skills"
if [ -L "${CLAUDE_SKILL_DIR}" ]; then
  rm -f "${CLAUDE_SKILL_DIR}"
fi
mkdir -p "${CLAUDE_SKILL_DIR}"
rsync -a --delete \
  --exclude '__pycache__' \
  "${SKILL_SRC}/" \
  "${CLAUDE_SKILL_DIR}/"

echo "==> [3/3] Installing for OpenAI Codex (${CODEX_SKILL_DIR})..."
mkdir -p "${HOME}/.codex/skills"
if [ -L "${CODEX_SKILL_DIR}" ]; then
  rm -f "${CODEX_SKILL_DIR}"
fi
mkdir -p "${CODEX_SKILL_DIR}"
rsync -a --delete \
  --exclude '__pycache__' \
  "${SKILL_SRC}/" \
  "${CODEX_SKILL_DIR}/"

echo ""
echo "Success! 'waiching-sun-writing' is now installed globally for:"
echo "  - Antigravity : ${AGY_PLUGIN_DIR}"
echo "  - Claude Code : ${CLAUDE_SKILL_DIR}"
echo "  - OpenAI Codex: ${CODEX_SKILL_DIR}"
