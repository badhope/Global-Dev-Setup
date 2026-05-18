# Global Git Configuration

## Setup

Copy these files to your home directory:

```bash
cp .gitignore_global ~/
cp .gitconfig ~/
```

Or run:

```bash
git config --global include.path ~/.gitconfig
```

## Files Included

### .gitconfig
Contains:
- User information
- Aliases
- Color settings
- Diff and merge tools
- Push behavior

### .gitignore_global
Global ignores for:
- OS files (macOS, Windows, Linux)
- IDE files
- Build artifacts
- Logs
- Dependencies

## Customization

Edit ~/.gitconfig to customize:
```bash
git config --global --edit
```

## Recommended Settings

The included configuration includes:

- **Aliases**: st, co, br, lg, etc.
- **Colors**: Auto-colored output
- **Push**: Simple push mode
- **Rebase**: Default to interactive rebase
- **Pull**: Rebase instead of merge

## Tools

Recommended tools:
- Diff: vimdiff
- Merge: vimdiff
