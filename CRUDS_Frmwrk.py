# SQLite CRUDS Framework Program

import sqlite3

connection = sqlite3.connect("FrameWork.db")
cursor = connection.cursor()

config_table = "ConfigFile"
target_table = cursor.execute("SELECT value FROM " + config_table + " WHERE key = ?", ("Title",)).fetchone()[0]

column_info = cursor.execute("PRAGMA table_info(" + target_table + ")").fetchall()
column_names = [col[1] for col in column_info]

def add_record():
    record_values = []
    for column in column_names:
        record_values.append(input("Enter the " + column + " : "))
    record_values = tuple(record_values)
    cursor.execute("INSERT INTO " + target_table + " VALUES " + str(record_values))

def display_records():
    print(" | ".join(column_names))
    all_rows = cursor.execute("SELECT * FROM " + target_table).fetchall()
    for row in all_rows:
        print(" | ".join(str(value) for value in row))

def update_record():
    record_id = input(f"Enter the {column_names[0]} to Update: ")
    for idx, column in enumerate(column_names[1:], start=1):
        print(f"{idx}. {column}")
    chosen_column_idx = int(input(f"Enter your choice to Update: "))
    new_value = input(f"Enter the new value for {column_names[chosen_column_idx]}: ")
    cursor.execute(f"UPDATE {target_table} SET {column_names[chosen_column_idx]} = ? WHERE {column_names[0]} = ?", (new_value, record_id))

def delete_record():
    record_id = input(f"Enter the {column_names[0]} to delete: ")
    cursor.execute(f"DELETE FROM {target_table} WHERE {column_names[0]} = ?", (record_id,))
    saved_message = cursor.execute(f"SELECT value FROM {config_table} WHERE key = ?", ("Message",)).fetchone()[0]
    print(saved_message)

def show_menu():
    menu_text = cursor.execute(f"SELECT value FROM {config_table} WHERE key = ?", ("Menu",)).fetchone()[0]
    print(menu_text.replace("\\n", "\n"))
    user_choice = int(input("Enter your choice: "))
    menu_actions[user_choice - 1]()
    connection.commit()
    show_menu()

menu_actions = [add_record, display_records, update_record, delete_record, exit]
show_menu()
