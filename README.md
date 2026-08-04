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

### Automated with Claude Code

The repo ships a Claude Code skill at `.claude/skills/meetup-update/` that runs the full monthly setup.
Invoke it with `/meetup-update` (or ask to "schedule the monthly meetup").

The skill:

1. Pulls the booked speaker from the "PyTexas Meetup CFP (Responses)" sheet in Google Drive and confirms their locked-in date from the email thread
2. Archives the held meetup, adds the speaker to `.authors.yml`, updates the homepage, and opens a PR
3. Creates the month's Drive folder with the run of show doc and attendance form, copied from the templates in Drive
4. Adds the month's card to the season's "Meetup Banners" deck in Canva
5. Drafts the date-offer emails to new CFP submitters (drafts only, never sends) and posts the promo notification to the Discord marketing channel webhook
6. Flags what stays manual: the speaker headshot, the Canva page title rename, the Discord event, the Meetup.com event, and the non-network listings

Everything the skill writes comes from the templates in `.claude/skills/meetup-update/references/`.
Edit those files to change what it produces.

### Manual Process

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

## Secrets

Automation secrets (currently the Discord marketing webhook) live encrypted in `secrets/meetup.sops.env`, managed with [sops](https://github.com/getsops/sops) and [age](https://github.com/FiloSottile/age).
The encrypted file is safe to commit; only the age keys listed in `.sops.yaml` can decrypt it.
This is the same pattern as the [infrastructure repo](https://github.com/pytexas/infrastructure).

### Reading or Changing a Secret

1. Install `sops` and `age`, with your age key at `~/.config/sops/age/keys.txt`
2. Run `sops secrets/meetup.sops.env` to open the decrypted values in your editor; saving re-encrypts

### Onboarding an Organizer

1. Have them generate a key with `age-keygen -o ~/.config/sops/age/keys.txt` and send you the public key (starts with `age1`)
2. Add their public key to `.sops.yaml`
3. Run `sops updatekeys secrets/meetup.sops.env` and commit both files

Adding a key to `.sops.yaml` grants nothing by itself.
The file only decrypts for the keys it was encrypted to, and re-encrypting it for a new recipient (`sops updatekeys`) can only be done by someone who already holds a listed private key.
A pull request that adds an unknown key to `.sops.yaml` cannot read any secrets and should simply be closed.

### If You Lose Your Key

Back up `~/.config/sops/age/keys.txt` to the password manager now; restoring that one file on a new machine restores access.

If the key is gone with no backup, the encrypted file is unrecoverable, but the secrets are not: re-obtain each one from its source (the Discord webhook URL is viewable under the channel's Integrations settings, and API tokens get re-issued by their providers).
Then generate a fresh key with `age-keygen`, replace the old public key in `.sops.yaml`, re-create `secrets/meetup.sops.env` with the re-obtained values, and commit.
The old blobs in git history stay permanently unreadable, which is the point.

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