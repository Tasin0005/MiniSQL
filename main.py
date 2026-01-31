import sys

# Starting point of program, initiates core while loop for the CLI
def main():
    engine_on = True
    while engine_on:
        user_input = input("MiniSQL> ")
        # Check if input was a meta command if first character is '.'
        if (len(user_input) != 0) and (user_input[0] == '.'):
            meta_command(user_input)
        else:
            token_stream = lexer(user_input)

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

class Token:
    def __init__(self, category, value):
        self.category = category # tokens can either be: keywords, identifiers, separators, operators, numbers, strings
        self.value = value # the actual value of the token

def lexer(input_string):
    token_stream = []
    string_stream = [] # TEMPORARY FOR TESTING PURPOSES ONLY
    index = 0
    while index < len(input_string):
        if (input_string[index] == ' '):
            index += 1
            continue
        elif is_keyword(input_string, index):
            keyword, ending_index = get_keyword(input_string, index) # ending_index should be the index of space after the token, if the token is at the end of the string, it should be len(input_string)
            string_stream.append(keyword) # TEMPORARY FOR TESTING PURPOSES ONLY
            index = ending_index
        elif is_string(input_string, index):
            string, ending_index = get_string(input_string, index)
            string_stream.append(string) # TEMPORARY FOR TESTING PURPOSES ONLY
            index = ending_index
        elif is_separator(input_string, index):
            separator, ending_index = get_separator(input_string, index)
            string_stream.append(separator) # TEMPORARY FOR TESTING PURPOSES ONLY
            index = ending_index
        elif is_operator(input_string, index):
            operator, ending_index = get_operator(input_string, index)
            string_stream.append(operator) # TEMPORARY FOR TESTING PURPOSES ONLY
            index = ending_index
        elif is_number(input_string, index):
            number, ending_index = get_number(input_string, index)
            string_stream.append(number) # TEMPORARY FOR TESTING PURPOSES ONLY
            index = ending_index
        elif is_identifier(input_string, index):
            identifier, ending_index = get_identifier(input_string, index)
            string_stream.append(identifier) # TEMPORARY FOR TESTING PURPOSES ONLY
            index = ending_index
        else:
            print("Please enter a valid SQL command")
            break
    
    print(string_stream) # TEMPORARY FOR TESTING PURPOSES ONLY
    return

def is_keyword(input_string, index):
    keywords = ["CREATE", "TABLE", "INSERT", "INTO", "VALUES", "SELECT", "FROM", "WHERE", "UPDATE", "SET", "DELETE", "DROP", "*"]
    ending_index = index
    while ending_index < len(input_string) and input_string[ending_index] != ' ':
        ending_index += 1
    word = input_string[index:ending_index].upper()
    for keyword in keywords:
        if word == keyword:
            return True
    return False

def get_keyword(input_string, index):
    ending_index = index
    while ending_index < len(input_string) and input_string[ending_index] != ' ':
        ending_index += 1
    keyword = input_string[index:ending_index].upper()
    return keyword, ending_index

def is_string(input_string, index):
    if input_string[index] == '"':
        ending_index = index + 1
        while ending_index < len(input_string) and input_string[ending_index] != '"':
            ending_index += 1
        if (ending_index < len(input_string)):
            return True
    else:
        return False

def get_string(input_string, index):
    ending_index = index + 1
    while ending_index < len(input_string) and input_string[ending_index] != '"':
        ending_index += 1
    string = input_string[index:ending_index + 1]
    return string, ending_index + 1

def is_separator(input_string, index):
    separators = [',', '(', ')', ';']
    for i in range(len(separators)):
        if input_string[index] == separators[i]:
            return True
    return False

def get_separator(input_string, index):
    return input_string[index], index + 1

def is_operator(input_string, index):
    operators = ['>=', '<=', '!=', '=', '>', '<', '+', '-']
    for operator in operators:
        if input_string[index:].startswith(operator):
            return True
    return False

def get_operator(input_string, index):
    operators = ['>=', '<=', '!=', '=', '>', '<', '+', '-']
    for operator in operators:
        if input_string[index:].startswith(operator):
            return operator, index + len(operator)

def is_number(input_string, index):
    if not input_string[index].isdigit():
        return False
    
    ending_index = index
    while ending_index < len(input_string) and input_string[ending_index].isdigit():
        ending_index += 1

    # check if number is followed by a letter/underscore (meaning its treated as an identifier)
    if ending_index < len(input_string) and (input_string[ending_index].isalpha() or input_string[ending_index] == '_'):
        return False
    return True

def get_number(input_string, index):
    ending_index = index
    while ending_index < len(input_string) and input_string[ending_index].isdigit():
        ending_index += 1
    number = input_string[index:ending_index]
    return number, ending_index

def is_identifier(input_string, index):
    if input_string[index].isalnum() or input_string[index] == '_':
        return True
    return False

def get_identifier(input_string, index):
    ending_index = index
    while ending_index < len(input_string) and (input_string[ending_index].isalnum() or input_string[ending_index] == '_'):
        ending_index += 1
    identifier = input_string[index:ending_index]
    return identifier, ending_index

# only run main() if the main.py file was executed as a script and not as a module
if __name__ == "__main__":
    main()