#!/usr/bin/env python3
"""
Console-based Student Management System (CRUD) with optional JSON persistence.
Python 3.8+
"""
import json
import os
from typing import List, Dict, Optional

DATA_FILE = "data.json"
students: List[Dict[str, str]] = []  # in-memory store


# -------------- Persistence --------------
def load_data(path: str = DATA_FILE) -> List[Dict[str, str]]:
    """Load student records from JSON file; returns list or empty list if not found/invalid."""
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                # ensure keys exist
                cleaned = []
                for s in data:
                    if isinstance(s, dict):
                        cleaned.append({
                            "roll_no": str(s.get("roll_no", "")).strip(),
                            "name": str(s.get("name", "")).strip(),
                            "grade": str(s.get("grade", "")).strip(),
                            "age": str(s.get("age", "")).strip() if s.get("age") not in (None, "") else ""
                        })
                return cleaned
    except Exception:
        pass
    return []


def save_data(path: str = DATA_FILE) -> None:
    """Save in-memory students list to JSON file."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(students, f, indent=2, ensure_ascii=False)


# -------------- Helpers (non-interactive, testable) --------------
def add_student_record(roll_no: str, name: str, grade: str, age: str = "") -> bool:
    """Add a student if roll_no is unique and required fields provided. Returns True if added."""
    roll_no = roll_no.strip()
    name = name.strip()
    grade = grade.strip()
    age = age.strip()
    if not roll_no or not name or not grade:
        return False
    if any(s["roll_no"] == roll_no for s in students):
        return False
    students.append({"roll_no": roll_no, "name": name, "grade": grade, "age": age})
    return True


def search_by_roll(roll_no: str) -> Optional[Dict[str, str]]:
    """Find a student by exact roll_no."""
    for s in students:
        if s["roll_no"] == roll_no.strip():
            return s
    return None


def search_by_name_part(name_part: str) -> List[Dict[str, str]]:
    """Case-insensitive partial match on name."""
    q = name_part.strip().lower()
    return [s for s in students if q in s["name"].lower()]


def update_student_record(roll_no: str, name: Optional[str] = None,
                          grade: Optional[str] = None, age: Optional[str] = None) -> bool:
    """Update fields for a student by roll_no. Returns True if updated."""
    s = search_by_roll(roll_no)
    if not s:
        return False
    if name is not None and name.strip():
        s["name"] = name.strip()
    if grade is not None and grade.strip():
        s["grade"] = grade.strip()
    if age is not None:
        age = age.strip()
        s["age"] = age
    return True


def delete_student_record(roll_no: str) -> bool:
    """Delete a student by roll_no. Returns True if deleted."""
    s = search_by_roll(roll_no)
    if not s:
        return False
    students.remove(s)
    return True


# -------------- CLI (interactive) --------------
def print_header():
    print(f"{'Roll':<10}{'Name':<22}{'Grade':<8}{'Age':<6}")
    print(f"{'-'*10}{'-'*22}{'-'*8}{'-'*6}")


def view_students():
    if not students:
        print("No records.")
        return
    print_header()
    for s in students:
        print(f"{s['roll_no']:<10}{s['name']:<22}{s['grade']:<8}{s.get('age',''):<6}")


def add_student():
    print("Add student")
    roll = input("Roll no: ").strip()
    if search_by_roll(roll):
        print("Roll no already exists.")
        return
    name = input("Name: ").strip()
    grade = input("Grade: ").strip()
    age = input("Age (optional): ").strip()
    ok = add_student_record(roll, name, grade, age)
    print("Added." if ok else "Failed to add (check inputs).")


def search_menu():
    print("Search")
    mode = input("Search by (1) Roll no or (2) Name? ").strip()
    if mode == "1":
        roll = input("Enter roll no: ").strip()
        s = search_by_roll(roll)
        if s:
            print_header()
            print(f"{s['roll_no']:<10}{s['name']:<22}{s['grade']:<8}{s.get('age',''):<6}")
        else:
            print("Not found.")
    elif mode == "2":
        name_part = input("Enter part of name: ").strip()
        matches = search_by_name_part(name_part)
        if matches:
            print_header()
            for s in matches:
                print(f"{s['roll_no']:<10}{s['name']:<22}{s['grade']:<8}{s.get('age',''):<6}")
        else:
            print("No matches.")
    else:
        print("Invalid choice.")


def update_student():
    print("Update student")
    roll = input("Roll to update: ").strip()
    s = search_by_roll(roll)
    if not s:
        print("Not found.")
        return
    new_name = input(f"Name [{s['name']}]: ").strip()
    new_grade = input(f"Grade [{s['grade']}]: ").strip()
    new_age = input(f"Age [{s.get('age','')}]: ").strip()
    update_student_record(roll,
                          name=new_name if new_name else None,
                          grade=new_grade if new_grade else None,
                          age=new_age if new_age != "" else None)
    print("Updated.")


def delete_student():
    print("Delete student")
    roll = input("Roll to delete: ").strip()
    s = search_by_roll(roll)
    if not s:
        print("Not found.")
        return
    if input(f"Delete {s['name']} (roll {s['roll_no']})? (y/N): ").strip().lower() == 'y':
        delete_student_record(roll)
        print("Deleted.")
    else:
        print("Cancelled.")


def main():
    global students
    # Load persistence (if file exists)
    students = load_data()

    while True:
        print("\n--- Student Management ---")
        print("1) Add  2) View  3) Search  4) Update  5) Delete  6) Save  7) Exit")
        choice = input("Choice: ").strip()
        if choice == "1":
            add_student()
        elif choice == "2":
            view_students()
        elif choice == "3":
            search_menu()
        elif choice == "4":
            update_student()
        elif choice == "5":
            delete_student()
        elif choice == "6":
            save_data()
            print(f"Saved to {DATA_FILE}.")
        elif choice == "7":
            # Save on exit?
            if input("Save before exit? (y/N): ").strip().lower() == 'y':
                save_data()
                print(f"Saved to {DATA_FILE}.")
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
