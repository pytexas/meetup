# PyTexas Meetup Website

The official website for the PyTexas Foundation Virtual Meetups, built with MkDocs Material. This site showcases upcoming & past meetups, and provides community information about local meetups in the state of Texas.

**Live Site**: [pytexas.org/meetup](https://pytexas.org/meetup)

## Development

Install the following tools for development:

### uv (Python Package Manager)
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### just (Command Runner)
```bash
# macOS
brew install just

# Linux/macOS via cargo
cargo install just
```

### lychee (Link Checker)
```bash
# macOS
brew install lychee

# Linux/macOS via cargo
cargo install lychee
```

## Quick Start

1. **Clone and setup**:
   ```bash
   git clone https://github.com/pytexas/meetup.git
   cd meetup-site
   just install
   ```

2. **Start development server**:
   ```bash
   just serve
   ```

3. **View site**: Open http://localhost:8000

## Development Commands

Use `just` for common tasks:

- `just help` - Show all available commands
- `just serve` - Start development server
- `just build` - Build static site
- `just check` - Run quality checks (build + link validation)
- `just clean` - Clean generated files

## Monthly Process

1. Add the upcoming meetup to the home page by modifying `index.md`
    1. When adding a new presenter, try to use a URL for the photo. Only upload a file if you must, and upload it to `assets/images`
        * **Tip**: A person's GitHub avatar is always available at `https://github.com/USERNAME.png` so use that
    2. Follow the previous month's format as your guide, with title, image, name, and bio.
2. Take the previous meetup from the previous month, and add a new page to `past_meetups/posts` using the following front matter
    ```markdown
    title: "The title"
    description: A description
    date: 2025-06-03
    categories:
        - cat1
        - cat2
        - catX
    authors:
        - author_name_in_.authors.yml
    ---
    ```
    1. If the presenter is not in the `.authors.yml` file, add them using the format that's already defined in the file. The presenter of the meetup is deemed the "author" of the "blog" (past meetup).
    2. If the presenter gave you any documents to share, upload them to `docs/assets/docs/` and link to them. However, try to encourage the presenter to share URLs we can link to instead of files we have to host.
    3. Write a short summary of the meetup and how it went in the body of the post. Use past blogs as a guide.
3. Test the site before committing using `just check` to check for any broken links. If you don't, the CI will catch it anyways.


## Adding Announcement Banners

Add announcement banners by editing `overrides/main.html`:

```html
{% block announce %}
    <p>Attend the <a href="https://conference.pytexas.org">PyTexas 2024 Conference</a> April 19 - 21, 2024</p>
{% endblock %}
```

## Project Structure

```
docs/                    # Main content
├── past_meetups/posts/  # Meetup blog posts
├── assets/             # Images and documents
└── *.md                # Site pages

mkdocs.yml              # Site configuration
justfile                # Development commands
```

## Deployment

The site automatically deploys to GitHub Pages via GitHub Actions when changes are pushed to the `main` branch. The deployment process includes:

1. **Link Validation**: All links are checked for validity
2. **Dependency Security**: Dependencies are scanned for vulnerabilities  
3. **Build & Deploy**: Site is built and deployed to GitHub Pages

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add your content or changes
4. Run `just check` to validate
5. Submit a pull request

## License

This project is maintained by the PyTexas Foundation.