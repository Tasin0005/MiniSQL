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
            parse(token_stream)

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

class ASTNode:
    def __init__(self, data, left, right):
        self.data = data
        self.left = left
        self.right = right

def insert_left_node(parent_node, child_node):
    parent_node.left = child_node

def insert_right_node(parent_node, child_node):
    parent_node.right = child_node

def parse(token_stream):
    if not token_stream:
        return

    initial_token = token_stream[0]
    start = initial_token.value

    match start:
        case "CREATE":
            AST = parse_create(token_stream)
        case "INSERT":
            AST = parse_insert(token_stream)
        case "SELECT":
            AST = parse_select(token_stream)
        case "UPDATE":
            AST = parse_update(token_stream)
        case "DELETE":
            AST = parse_delete(token_stream)
        case "DROP":
            AST = parse_drop(token_stream)
        case _:
            print("Please enter a valid SQL command (CREATE, INSERT, SELECT, UPDATE, DELETE, DROP)")

    return

def parse_create(token_stream):

    # Define helper functions before any code that calls them
    def parse_column_list(token_stream, index):

        # Base case: closing parenthesis means no more columns
        if token_stream[index].value == ")":
            return None, index

        column_node, index = parse_column_def(token_stream, index)

        if index < len(token_stream) and token_stream[index].value == ",":
            index += 1  # skip comma
            column_node.right, index = parse_column_list(token_stream, index)

        return column_node, index

    def parse_column_def(token_stream, index):
        column_node = ASTNode(lexer.Token("column", "COLUMN_DEF"), None, None)

        # Define column name node
        name_node = ASTNode(token_stream[index], None, None)
        index += 1

        # Define column type node
        type_node = ASTNode(token_stream[index], None, None)
        index += 1

        # insert nodes into the tree
        name_node.right = type_node
        column_node.left = name_node 

        return column_node, index

    # Create the root node for the AST
    root_node = ASTNode(lexer.Token("keyword", "CREATE TABLE"), None, None)

    index = 2  # skip CREATE and TABLE tokens
    root_node.left = ASTNode(token_stream[index], None, None)  # table name
    index += 2  # skip table name and opening parenthesis

    # Start recursive descent parsing of the column list
    root_node.right, index = parse_column_list(token_stream, index)

    return root_node

def parse_insert(token_stream):

    def parse_value_list(token_stream, index):
        # base case: if closing parenthesis reached, return None as there are no more values
        if token_stream[index].value == ")":
            return None, index
        
        # parse a singular value and create a node for it
        value_node, index = parse_value_def(token_stream, index)

        # continue recursion until base case is reached
        if index < len(token_stream) and token_stream[index].value == ",":
            index += 1 # skip comma
            value_node.right, index = parse_value_list(token_stream, index)

        return value_node, index
    
    def parse_value_def(token_stream, index):

        # create value node and insert the value token as its left child
        value_node = ASTNode(lexer.Token("value", "VALUE_DEF"), None, None)
        value_node.left = ASTNode(token_stream[index], None, None)
        index += 1

        return value_node, index

    # Create the root node for the AST
    root_node = ASTNode(lexer.Token("keyword", "INSERT INTO"), None, None)

    index = 2 # skip INSERT and INTO tokens
    root_node.left = ASTNode(token_stream[index], None, None) # table name
    index += 3 # skip table name, VALUES token and opening parenthesis

    # Start recursive descent parsing of the value list
    root_node.right, index = parse_value_list(token_stream, index)

    return root_node

def parse_select(token_stream):
    root_node = None
    return root_node

def parse_update(token_stream):
    root_node = None
    return root_node

def parse_delete(token_stream):
    root_node = None
    return root_node

def parse_drop(token_stream):
    root_node = None
    return root_node
    
# only run main() if the main.py file was executed as a script and not as a module
if __name__ == "__main__":
    main()