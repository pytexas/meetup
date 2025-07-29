# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the PyTexas Foundation Meetup website built with MkDocs Material. It's a static documentation site that showcases past meetups, provides information about joining the PyTexas community, and maintains a blog-style format for meetup posts.

## Core Architecture

- **Static Site Generator**: MkDocs with Material theme
- **Content Structure**: Markdown-based documentation and blog posts
- **Dependency Management**: Uses `uv` for modern Python package management
- **Deployment**: GitHub Actions with automated CI/CD to GitHub Pages
- **Content Types**:
  - Main documentation pages (`docs/*.md`)
  - Blog-style meetup posts (`docs/past_meetups/posts/YYYY-MM-DD.md`)
  - Asset management (`docs/assets/images/` and `docs/assets/docs/`)

## Essential Commands

### Just Commands (Recommended)
This project includes a `justfile` for common development tasks:
- `just install`: Install all dependencies using uv
- `just serve`: Start development server with hot reload on port 8000
- `just serve-port 8001`: Start development server on specific port
- `just build`: Build the static site to `site/` directory
- `just validate`: Build with strict validation enabled
- `just link-check`: Check all links using lychee with caching
- `just check`: Run all quality checks (build + link check)
- `just clean`: Clean generated files and cache
- `just help`: Show all available commands

### Direct uv/MkDocs Commands
- `uv sync`: Install all dependencies from lockfile
- `uv run mkdocs serve`: Start local development server with hot reload
- `uv run mkdocs build`: Build static site to `site/` directory
- `uv run mkdocs build --strict`: Build with strict validation
- `uv run mkdocs gh-deploy`: Deploy to GitHub Pages (production only)

### Package Management
- `uv add <package>`: Add new dependency
- `uv remove <package>`: Remove dependency
- `uv lock`: Update lockfile after dependency changes

## Content Guidelines

### Adding Meetup Posts

1. Create new file: `docs/past_meetups/posts/YYYY-MM-DD.md`
2. Use frontmatter with required fields:
   ```yaml
   ---
   title: "Meetup Title"
   description: Brief description
   date: YYYY-MM-DD
   categories:
       - Category1
       - Category2
   authors:
       - username
   ---
   ```
3. Include speaker image in `docs/assets/images/` 
4. Use `<!-- more -->` tag to separate excerpt from full content
5. Make sure the speaker is listed in the `.authors.yml` file. If they aren't, add a new entry for them based on prior format of the others

### Site Configuration
- Main site config: `mkdocs.yml`
- Theme customizations: `overrides/main.html`
- Navigation structure defined in `mkdocs.yml` nav section

## CI/CD Pipeline

The repository uses a three-stage GitHub Actions workflow:
1. **Link Check** (`link-check.yml`): Validates all links in markdown/HTML files
2. **Dependency Review** (`check.yml`): Security scanning on PRs  
3. **Deploy** (`ci.yml`): Builds and deploys to GitHub Pages after successful link check

## Project Structure

```
docs/                    # Main content directory
├── index.md            # Homepage
├── about.md            # About page
├── past_meetups/       # Blog-style meetup posts
│   ├── index.md        # Archive landing page
│   └── posts/          # Individual meetup posts
├── assets/             # Static assets
│   ├── images/         # Speaker photos, logos
│   └── docs/           # Downloadable documents/slides
overrides/              # Theme customizations
mkdocs.yml              # Site configuration
pyproject.toml          # Python project configuration
uv.lock                 # Dependency lockfile
justfile                # Task automation with just command runner
```

## Development Notes

- The site uses MkDocs blog plugin for the past meetups section
- Social card generation is enabled for better sharing
- Custom theme overrides in `overrides/main.html` for announcements
- Dependencies include imaging support for automatic social card generation