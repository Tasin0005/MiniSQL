
# Starting point of program, initiates core while loop for the CLI
def main():
    engine_on = True
    while engine_on:
        user_input = input("MiniSQL> ")
        # Check if input was a meta command if first character is '.'
        if user_input[0] == '.':
            meta_command(user_input)
        else:
            print("...")

# Determines if user text input is a meta command (starts with .) or an SQL command
# Note: User input is strictly either a meta command or an SQL command
def meta_command(string):
    match string:
        case ".help":
            print("Here is some information") # placeholder
        case ".exit":
            print("Exiting the program...") # placeholder
        case ".tables":
            print("Printing out all the table names in the DB...") # placeholder
        case ".schema":
            print("Printing out the schema of all tables in the DB...") # placeholder
        case _:
            print("Please enter a valid meta command (.help, .exit, .tables, .schema)")

main()