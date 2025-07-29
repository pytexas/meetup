# PyTexas Meetup Site's Justfile
# Available commands for MkDocs website development

# Default recipe - show available commands
default:
    @just --list

# Install dependencies using uv
install:
    uv sync

# Build the documentation site
build:
    uv run mkdocs build

# Run local development server with hot reload
serve:
    uv run mkdocs serve

# Run local development server on specific port
serve-port PORT="8001":
    uv run mkdocs serve --dev-addr=127.0.0.1:{{PORT}}

# Check all links using lychee with caching (avoids 429 errors)
link-check:
    lychee --cache --verbose .

# Clean generated files and cache
clean:
    rm -rf site/
    rm -rf .lycheecache/
    rm -rf __pycache__/
    find . -name "*.pyc" -delete
    find . -name ".DS_Store" -delete

# Run all quality checks (build + link check)
check: build link-check

# Validate mkdocs configuration
validate:
    uv run mkdocs build --strict

# Show help for common workflows
help:
    @echo "=== PyTexas Meetup Site - Available Commands ==="
    @echo ""
    @echo "== Setup & Development =="
    @echo "  just install              Install dependencies using uv"
    @echo "  just serve                Start development server (port 8000)"
    @echo "  just serve-port 8001      Start dev server on specific port"
    @echo ""
    @echo "== Building & Validation =="
    @echo "  just build                Build the documentation site"
    @echo "  just validate             Build with strict validation"
    @echo "  just link-check           Check all links (with caching)"
    @echo "  just check                Run all quality checks"
    @echo ""
    @echo "== Content Creation =="
    @echo "  just new-meetup 'Title' 'YYYY-MM-DD'  Create a new meetup post"
    @echo ""
    @echo "== Utilities =="
    @echo "  just clean                Clean generated files and cache"
    @echo "  just help                 Show this help message"
    @echo ""
    @echo "=== Common Workflows ==="
    @echo "Development:       just install && just serve"
    @echo "Pre-publish:       just check"
    @echo "New meetup post:   just new-meetup 'June Meetup' '2025-06-03'"
    @echo "Clean start:       just clean && just build"
    @echo "Full validation:   just validate && just link-check"