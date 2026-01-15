# Claude-Code---1.15.26

This repository is configured for Claude Code on the web.

## SessionStart Hook

This repository includes a SessionStart hook (`.claude/hooks/session-start.sh`) that automatically installs dependencies when you open the repository in Claude Code on the web.

The hook supports multiple languages and package managers:
- **Node.js/JavaScript/TypeScript**: npm, yarn, or pnpm
- **Python**: pip (requirements.txt) or Poetry (pyproject.toml)
- **Ruby**: bundler (Gemfile)
- **Go**: go mod
- **Rust**: cargo

## Getting Started

Once you add your project files and dependencies, the SessionStart hook will automatically install them when you open this repository in Claude Code on the web.

## Configuration

The hook configuration is stored in `.claude/settings.json`. The hook only runs in Claude Code on the web (remote environments) and skips running locally.
