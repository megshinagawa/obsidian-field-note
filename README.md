# Field Notes

A simple command-line tool for creating timestamped field notes in your Obsidian vault. This tool helps you quickly capture thoughts, insights, and observations throughout your day, automatically organizing them into daily notes.

## Features

- Create timestamped field notes with a single command
- Categorize notes by type (Insight, Idea, Energy, Focus, Mood, Event, Later, or Other)
- Automatic organization into daily notes
- Interactive mode for easy note entry
- Customizable configuration through `config.yaml`

## Installation

1. Clone this repository:

2. Install the required dependencies:

```bash
pip install pyyaml
```

OR if you don't use pip

```bash
brew install libyaml
```

3. Make the script executable:

```bash
chmod +x field_notes.py
```

## Configuration

The tool uses a `config.yaml` file for configuration. If the file doesn't exist, it will use default settings. You can create a custom `config.yaml` file in the same directory as the script with the following structure:

```yaml
vault:
  path: "~/Obsidian"  # Path to your Obsidian vault
datetime:
  date_format: "%Y-%m-%d"
  time_format: "%H:%M:%S"
  daily_note_title: "Daily Note - {date}"
files:
  daily_notes_dir: "Daily Notes"
  extension: ".md"
notes:
  template: "## {time}\n{content}\n"
```

## Usage

### Basic Usage

Run the script and follow the prompts:

```bash
./field_notes.py
```

You will be prompted to:

1. Enter your note content
2. Select a note type from the following options:
   - Insight
   - Idea
   - Energy
   - Focus
   - Mood
   - Event
   - Later
   - Other

The selected type will be added as a hashtag to your note (e.g., `#insight`).

### Specifying Vault Location

If your Obsidian vault is not in the default location, you can modify the `vault.path` setting in your `config.yaml` file.

## How It Works

1. The tool creates a timestamped note with your content
2. The note is automatically added to today's daily note in your Obsidian vault
3. Notes are organized by time and include the note type as a hashtag
4. If the daily note doesn't exist, it will be created automatically

## Requirements

- Python 3.x
- PyYAML
- Obsidian (for viewing and managing the notes)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 