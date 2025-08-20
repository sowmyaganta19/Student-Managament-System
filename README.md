# Student Management System (Console, Python)

Simple console app for managing student records (CRUD) with optional JSON persistence.

## Requirements
- Python 3.8+
- Terminal (CMD/PowerShell on Windows, or bash/zsh on macOS/Linux)
- (Optional) Git

## Quick start
```bash
# 1) Enter the project
cd student-management

# 2) Run the app
python student_mgmt.py
# or on some systems
python3 student_mgmt.py
```

## Features
- Add, View, Search (by roll or name), Update, Delete
- Save/Load to `data.json`

## Tips
- Press Enter during Update to keep the current value.
- Choose "Save" to write changes to `data.json`, or save on exit when prompted.

## Example menu
```
--- Student Management ---
1) Add  2) View  3) Search  4) Update  5) Delete  6) Save  7) Exit
```

## Next steps
- Export to CSV
- Sort by name/roll
- Unit tests under `tests/`
