import sqlite3

class SQLiteCRUDSFramework:
    def __init__(self, db_name="FrameWork.db"):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.config_table = "ConfigFile"
        self.target_table = self.get_target_table()
        self.column_names = self.get_column_names()
        self.menu_actions = [self.add_record, self.display_records, self.update_record, self.delete_record, exit]

    def get_target_table(self):
        target_table = self.cursor.execute(
            "SELECT value FROM " + self.config_table + " WHERE key = ?", ("Title",)
        ).fetchone()[0]
        return target_table

    def get_column_names(self):
        column_info = self.cursor.execute(f"PRAGMA table_info({self.target_table})").fetchall()
        return [col[1] for col in column_info]

    def add_record(self):
        record_values = [input("Enter the " + column + ": ") for column in self.column_names]
        record_values = tuple(record_values)
        self.cursor.execute(f"INSERT INTO {self.target_table} VALUES {str(record_values)}")

    def display_records(self):
        print(" | ".join(self.column_names))
        all_rows = self.cursor.execute(f"SELECT * FROM {self.target_table}").fetchall()
        for row in all_rows:
            print(" | ".join(str(value) for value in row))

    def update_record(self):
        record_id = input(f"Enter the {self.column_names[0]} to Update: ")
        chosen_column_idx = self.select_option()
        new_value = input(f"Enter the new value for {self.column_names[chosen_column_idx]}: ")
        self.cursor.execute(
            f"UPDATE {self.target_table} SET {self.column_names[chosen_column_idx]} = ? WHERE {self.column_names[0]} = ?",
            (new_value, record_id)
        )

    def select_option(self):
        for idx, column in enumerate(self.column_names[1:], start=1):
            print(f"{idx}. {column}")
        chosen_column_idx = int(input(f"Enter your choice to Update: "))
        return chosen_column_idx

    def delete_record(self):
        record_id = input(f"Enter the {self.column_names[0]} to delete: ")
        self.cursor.execute(f"DELETE FROM {self.target_table} WHERE {self.column_names[0]} = ?", (record_id,))
        saved_message = self.cursor.execute(
            f"SELECT value FROM {self.config_table} WHERE key = ?", ("Message",)
        ).fetchone()[0]
        print(saved_message)

    def show_menu(self):
        menu_text = self.cursor.execute(
            f"SELECT value FROM {self.config_table} WHERE key = ?", ("Menu",)
        ).fetchone()[0]
        print(menu_text.replace("\\n", "\n"))
        user_choice = int(input("Enter your choice: "))
        self.menu_actions[user_choice - 1]()
        self.connection.commit()
        self.show_menu()

if __name__ == "__main__":
    framework = SQLiteCRUDSFramework()
    framework.show_menu()
