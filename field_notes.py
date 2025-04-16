#!/usr/bin/env python3
import os
import argparse
import datetime
import yaml
from pathlib import Path

def load_config(config_path=None):
    """
    Load configuration from config.yaml file.
    Returns default configuration if file doesn't exist.
    
    Args:
        config_path (str, optional): Custom path to config file. If None, looks in script directory.
    """
    # If no custom path provided, look in script directory
    if config_path is None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(script_dir, 'config.yaml')
    else:
        # Expand user home directory and make path absolute
        config_path = os.path.abspath(os.path.expanduser(config_path))
    
    default_config = {
        'vault': {
            'path': os.path.join(os.path.expanduser("~"), "Obsidian")
        },
        'datetime': {
            'date_format': "%Y-%m-%d",
            'time_format': "%H:%M:%S",
            'daily_note_title': "Daily Note - {date}"
        },
        'files': {
            'daily_notes_dir': "Daily Notes",
            'extension': ".md"
        },
        'notes': {
            'template': "## {time}\n{content}\n"
        }
    }
    
    try:
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
                # Merge with default config to ensure all settings exist
                for section in default_config:
                    if section not in config:
                        config[section] = default_config[section]
                    else:
                        for key in default_config[section]:
                            if key not in config[section]:
                                config[section][key] = default_config[section][key]
        else:
            print(f"Config file not found at {config_path}. Using default configuration.")
            config = default_config
    except Exception as e:
        print(f"Error loading config file: {e}")
        print("Using default configuration.")
        config = default_config
    
    # Ensure all paths are absolute
    config['vault']['path'] = os.path.abspath(os.path.expanduser(config['vault']['path']))
    
    return config

def create_field_note(note_content, vault_path=None):
    """
    Create a timestamped field note and add it to the daily note in Obsidian.
    
    Args:
        note_content (str): The content of the field note
        vault_path (str, optional): Path to the Obsidian vault. Defaults to None.
    """
    config = load_config()
    
    # Get current date and time
    now = datetime.datetime.now()
    timestamp = now.strftime(config['datetime']['time_format'])
    date_str = now.strftime(config['datetime']['date_format'])
    
    # Extract note type and clean content
    note_type = note_content.split()[-1]
    clean_content = ' '.join(note_content.split()[:-1])
    
    # Format the note with timestamp
    formatted_note = config['notes']['template'].format(
        time=timestamp,
        content=clean_content,
        note_type=note_type
    ) + "\n"
    
    # Determine the Obsidian vault path
    if not vault_path:
        vault_path = config['vault']['path']
    
    # Expand any user home directory references
    vault_path = os.path.expanduser(vault_path)
    
    # Define daily notes directory and file
    daily_notes_dir = os.path.join(vault_path, config['files']['daily_notes_dir'])
    daily_note_path = os.path.join(daily_notes_dir, f"{date_str}{config['files']['extension']}")
    
    # Create daily notes directory if it doesn't exist
    os.makedirs(daily_notes_dir, exist_ok=True)
    
    # Check if the daily note exists, if not create it with a header
    if not os.path.exists(daily_note_path):
        with open(daily_note_path, 'w') as f:
            f.write(f"# {config['datetime']['daily_note_title'].format(date=date_str)}\n")
    
    # Append the new note to the daily note file
    with open(daily_note_path, 'a') as f:
        f.write(formatted_note)
    
    print(f"Field note added to {daily_note_path}")
    return True

def get_note_type():
    """
    Prompt the user to select a note type and return the corresponding hashtag.
    """
    print("\nWhat type of note is this?")
    print("1. Insight")
    print("2. Idea")
    print("3. Energy")
    print("4. Focus")
    print("5. Mood")
    print("6. Event")
    print("7. Later")
    print("8. Other")
    
    while True:
        try:
            choice = int(input("Enter your choice (1-8): "))
            if 1 <= choice <= 8:
                note_types = {
                    1: "#insight",
                    2: "#idea",
                    3: "#energy",
                    4: "#focus",
                    5: "#mood",
                    6: "#event",
                    7: "#later",
                    8: "#other"
                }
                return note_types[choice]
        except ValueError:
            print("Please enter a number between 1-8")

def main():
    parser = argparse.ArgumentParser(description='Field Notes - Quick note taking for Obsidian')
    parser.add_argument('--config', '-c', help='Path to custom config file')
    parser.add_argument('--vault', '-v', help='Path to Obsidian vault (overrides config)')
    args = parser.parse_args()
    
    # Load config with potential custom path
    config = load_config(args.config)
    
    # Override vault path if specified
    if args.vault:
        config['vault']['path'] = os.path.abspath(os.path.expanduser(args.vault))
    
    print("Welcome to Field Notes!")
    print("What would you like to record?")
    
    # Get the note content
    note_content = input("> ")
    
    if not note_content:
        print("No content provided. Exiting...")
        return
    
    # Get note type and append hashtag
    note_type = get_note_type()
    note_content = f"{note_content} {note_type}"
    
    create_field_note(note_content, config['vault']['path'])

if __name__ == "__main__":
    main()