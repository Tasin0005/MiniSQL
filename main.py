import sys
import lexer

# Starting point of program, initiates core while loop for the CLI
def main():
    engine_on = True
    while engine_on:
        user_input = input("MiniSQL> ")
        # Check if input was a meta command if first character is '.'
        if (len(user_input) != 0) and (user_input[0] == '.'):
            meta_command(user_input)
        else:
            token_stream = lexer.lex(user_input)

# Determines if user text input is a meta command (starts with .) or an SQL command
# Note: User input is strictly either a meta command or an SQL command
def meta_command(string):
    # Message outputted by the .help command
    help_string = """
======================================================
        MiniSQL - A Lightweight SQL DB Engine
======================================================

META COMMANDS:
.help (Shows this help message)
.exit (Exit the program)
.tables (Displays a list of all tables in the database)
.schema (Shows schema for each table in the database)

(SUPPORTED) SQL COMMANDS:
CREATE TABLE (creates a new table)
E.g CREATE TABLE users (id INT, name TEXT, age INT)

INSERT INTO (inserts a row into a table)
E.g INSERT INTO users VALUES (1, "Alice", 25)

SELECT (Queries data from a table)
E.g SELECT * FROM users
E.g SELECT id, name FROM users WHERE age = 25

UPDATE (Updates existing rows)
E.g UPDATE users SET age = 26 WHERE id = 1

DELETE (Deletes rows from a table)
E.g DELETE FROM users WHERE id = 2
    
DROP TABLE (Deletes an entire table)
E.g DROP TABLE users
    
Please visit https://github.com/Tasin0005/MiniSQL/ for more information
            """
    
    # Match case statements to manage meta commands
    match string:
        case ".help":
            print(help_string)
        case ".exit":
            sys.exit(0)
        case ".tables":
            print("Printing out all the table names in the DB...") # placeholder
        case ".schema":
            print("Printing out the schema of all tables in the DB...") # placeholder
        case _:
            print("Please enter a valid meta command (.help, .exit, .tables, .schema)")

# only run main() if the main.py file was executed as a script and not as a module
if __name__ == "__main__":
    main()