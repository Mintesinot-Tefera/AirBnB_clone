#!/usr/bin/python3
"""Module for the entry point of the command interpreter."""

import cmd
from models.base_model import BaseModel
import re
import json


class HBNBCommand(cmd.Cmd):

    """Class for the command interpreter."""

    prompt = "(hbnb) "

    def default(self, line):
        """
        Default method called when no other is found.

        It calls the _precmd method to parse the given line.

        Args:
            line (str): The line to parse.

        Returns:
            str: The line if no match is found, otherwise None.
        """
        # print("DEF:::", line)
        # Parse the line and call the _precmd method
        self._precmd(line)

    def _precmd(self, line):
        """
        Parses the given line and calls the appropriate method.

        Args:
            line (str): The line to parse.

        Returns:
            str: The command that was executed.

        """
        # print("PRECMD:::", line)
        # Extracts the class name, method name, and arguments from the line.
        match = re.search(r"^(\w*)\.(\w+)(?:\(([^)]*)\))$", line)
        if not match:
            return line
        classname = match.group(1)
        method = match.group(2)
        args = match.group(3)

        # Extracts the UID and attribute or dictionary from the arguments.
        match_uid_and_args = re.search('^"([^"]*)"(?:, (.*))?$', args)
        if match_uid_and_args:
            uid = match_uid_and_args.group(1)
            attr_or_dict = match_uid_and_args.group(2)
        else:
            uid = args
            attr_or_dict = False

        # Extracts the attribute and value from the attribute or dictionary.
        attr_and_value = ""
        if method == "update" and attr_or_dict:
            match_dict = re.search('^({.*})$', attr_or_dict)
            if match_dict:
                self.update_dict(classname, uid, match_dict.group(1))
                return ""
            match_attr_and_value = re.search(
                '^(?:"([^"]*)")?(?:, (.*))?$', attr_or_dict)
            if match_attr_and_value:
                attr_and_value = (match_attr_and_value.group(
                    1) or "") + " " + (match_attr_and_value.group(2) or "")
        # Constructs the command to be executed.
        command = method + " " + classname + " " + uid + " " + attr_and_value
        # Executes the command.
        self.onecmd(command)
        return command

    def update_dict(self, classname, uid, s_dict):
        """
        Helper method for update() with a dictionary.

        Args:
            classname (str): The class name of the object.
            uid (str): The unique identifier of the object.
            s_dict (str): A JSON string representing the dictionary.

        This helper method is used to update an object's attributes with a dictionary.
        It replaces single quotes with double quotes, loads the JSON string into a dictionary,
        checks if the class name and uid are valid, retrieves the object from storage,
        checks if the object exists, and then updates the object's attributes with the values
        from the dictionary. Finally, it saves the updated object.

        """
        # Replace single quotes with double quotes
        s = s_dict.replace("'", '"')
        # Load the JSON string into a dictionary
        d = json.loads(s)
        # Check if class name is missing
        if not classname:
            print("** class name missing **")
        # Check if class name is valid
        elif classname not in storage.classes():
            print("** class doesn't exist **")
        # Check if uid is missing
        elif uid is None:
            print("** instance id missing **")
        else:
            # Construct the key
            key = "{}.{}".format(classname, uid)
            # Check if object exists in storage
            if key not in storage.all():
                print("** no instance found **")
            else:
                # Get the attributes for the class
                attributes = storage.attributes()[classname]
                # Update the object's attributes with the values from the dictionary
                for attribute, value in d.items():
                    if attribute in attributes:
                        value = attributes[attribute](value)
                    setattr(storage.all()[key], attribute, value)
                # Save the updated object
                storage.all()[key].save()

    def do_EOF(self, line):
        """
        Handles End Of File character.

        This method is called when the user presses the End Of File character.
        It prints a newline and returns True to indicate that the command loop
        should exit.

        Args:
            line (str): The line containing the End Of File character.

        Returns:
            bool: True to indicate that the command loop should exit.

        """
        # Print a newline to separate the command output from the prompt
        print()
        # Return True to indicate that the command loop should exit
        return True

    def do_quit(self, line):
        """
        Exits the program.

        This method is called when the user enters the 'quit' command.
        It returns True to indicate that the command loop should exit.

        Args:
            line (str): The line containing the 'quit' command.

        Returns:
            bool: True to indicate that the command loop should exit.

        """
        # Return True to indicate that the command loop should exit
        return True

    def emptyline(self):
        """Doesn't do anything on ENTER.
        """
        pass

    def do_create(self, line):
        """
        Creates an instance of a class.

        This method is called when the user enters the 'create' command followed by the class name.
        It creates a new instance of the specified class, saves it to the storage, and prints its ID.

        Args:
            line (str): The line containing the 'create' command and the class name.

        """
        # Check if the line is empty or None
        if line == "" or line is None:
            # Print an error message if the class name is missing
            print("** class name missing **")
        # Check if the specified class exists in the storage
        elif line not in storage.classes():
            # Print an error message if the class doesn't exist
            print("** class doesn't exist **")
        else:
            # Create a new instance of the specified class
            b = storage.classes()[line]()
            # Save the new instance to the storage
            b.save()
            # Print the ID of the new instance
            print(b.id)

    def do_show(self, line):
        """
        Prints the string representation of an instance.

        This method is called when the user enters the 'show' command followed by the class name and id of the instance.
        It checks if the class name and id are valid, retrieves the instance from storage, and prints its string representation.

        Args:
            line (str): The line containing the 'show' command, class name, and id.

        """
        # Check if the line is empty or None
        if line == "" or line is None:
            # Print an error message if the class name is missing
            print("** class name missing **")
        else:
            words = line.split(' ')
            # Check if the specified class exists in the storage
            if words[0] not in storage.classes():
                # Print an error message if the class doesn't exist
                print("** class doesn't exist **")
            elif len(words) < 2:
                # Print an error message if the instance id is missing
                print("** instance id missing **")
            else:
                # Construct the key
                key = "{}.{}".format(words[0], words[1])
                # Check if the instance exists in storage
                if key not in storage.all():
                    # Print an error message if the instance is not found
                    print("** no instance found **")
                else:
                    # Print the string representation of the instance
                    print(storage.all()[key])

    def do_destroy(self, line):
        """
        Deletes an instance based on the class name and id.

        This method is called when the user enters the 'destroy' command followed by the class name and id of the instance.
        It checks if the class name and id are valid, retrieves the instance from storage, and deletes it.

        Args:
            line (str): The line containing the 'destroy' command, class name, and id.

        """
        # Check if the line is empty or None
        if line == "" or line is None:
            # Print an error message if the class name is missing
            print("** class name missing **")
        else:
            words = line.split(' ')
            # Check if the specified class exists in the storage
            if words[0] not in storage.classes():
                # Print an error message if the class doesn't exist
                print("** class doesn't exist **")
            elif len(words) < 2:
                # Print an error message if the instance id is missing
                print("** instance id missing **")
            else:
                # Construct the key
                key = "{}.{}".format(words[0], words[1])
                # Check if the instance exists in storage
                if key not in storage.all():
                    # Print an error message if the instance is not found
                    print("** no instance found **")
                else:
                    # Delete the instance from storage
                    del storage.all()[key]
                    # Save the changes to the storage
                    storage.save()

    def do_all(self, line):
        """
        Prints all string representation of all instances.

        If a class name is provided, it prints the string representation of all instances
        of that class. Otherwise, it prints the string representation of all instances.

        Args:
            line (str): The line containing the optional class name.

        """
        # Check if a class name is provided
        if line != "":
            # Split the line into words
            words = line.split(' ')

            # Check if the specified class exists in the storage
            if words[0] not in storage.classes():
                # Print an error message if the class doesn't exist
                print("** class doesn't exist **")
            else:
                # Create a list of the string representation of all instances of the specified class
                nl = [str(obj) for key, obj in storage.all().items()
                      if type(obj).__name__ == words[0]]
                # Print the list
                print(nl)
        else:
            # Create a list of the string representation of all instances
            new_list = [str(obj) for key, obj in storage.all().items()]
            # Print the list
            print(new_list)

    def do_count(self, line):
        """
        Counts the instances of a class.

        This method counts the number of instances of a class.
        It takes a line as input and splits it into words.
        It first checks if the class name is provided,
        and if not, it prints an error message.
        If the class name is provided, it checks if the class exists in the storage.
        If the class does not exist, it prints an error message.
        If the class exists, it counts the number of instances of that class in the storage.
        Finally, it prints the count of instances.

        Args:
            line (str): The line containing the class name.

        """
        # Split the line into words
        words = line.split(' ')

        # Check if the class name is provided
        if not words[0]:
            # Print an error message if the class name is missing
            print("** class name missing **")
        elif words[0] not in storage.classes():
            # Print an error message if the class doesn't exist
            print("** class doesn't exist **")
        else:
            # Count the number of instances of the specified class in the storage
            matches = [
                k for k in storage.all() if k.startswith(
                    words[0] + '.')]
            # Print the count of instances
            print(len(matches))

    def do_update(self, line):
        """
        Updates an instance by adding or updating attribute.

        Args:
            line (str): The line containing the class name, instance id, attribute name, and value.

        This method updates an instance by adding or updating an attribute.
        It takes a line as input and uses regular expressions to extract the class name, instance id,
        attribute name, and value. It first checks if the class name is provided,
        and if not, it prints an error message. If the class name is provided,
        it checks if the class exists in the storage. If the class does not exist,
        it prints an error message. If the class exists, it checks if the instance id is provided.
        If the instance id is not provided, it prints an error message. If the instance id is provided,
        it checks if the instance exists in the storage. If the instance does not exist, it prints
        an error message. If the instance exists, it checks if the attribute name is provided.
        If the attribute name is not provided, it prints an error message. If the attribute name is provided,
        it checks if the value is provided. If the value is not provided, it prints an error message.
        If all the required information is provided, it updates the attribute of the instance with the new value.
        Finally, it saves the updated instance.
        """
        # Check if the line is empty or None
        if line == "" or line is None:
            print("** class name missing **")
            return

        # Use regular expressions to extract the class name, instance id, attribute name, and value
        rex = r'^(\S+)(?:\s(\S+)(?:\s(\S+)(?:\s((?:"[^"]*")|(?:(\S)+)))?)?)?'
        match = re.search(rex, line)

        # Extract the class name, instance id, attribute name, and value from the match
        classname = match.group(1)
        uid = match.group(2)
        attribute = match.group(3)
        value = match.group(4)

        # Check if the class name is provided
        if not match:
            print("** class name missing **")
        # Check if the class exists in the storage
        elif classname not in storage.classes():
            print("** class doesn't exist **")
        # Check if the instance id is provided
        elif uid is None:
            print("** instance id missing **")
        else:
            # Construct the key
            key = "{}.{}".format(classname, uid)
            # Check if the instance exists in the storage
            if key not in storage.all():
                print("** no instance found **")
            # Check if the attribute name is provided
            elif not attribute:
                print("** attribute name missing **")
            # Check if the value is provided
            elif not value:
                print("** value missing **")
            else:
                cast = None
                # Check if the value is a string
                if not re.search('^".*"$', value):
                    # Check if the value contains a decimal point
                    if '.' in value:
                        cast = float
                    else:
                        cast = int
                else:
                    # Remove the double quotes from the value
                    value = value.replace('"', '')
                # Get the attributes for the class
                attributes = storage.attributes()[classname]
                # Update the attribute of the instance with the new value
                if attribute in attributes:
                    value = attributes[attribute](value)
                elif cast:
                    try:
                        value = cast(value)
                    except ValueError:
                        pass  # fine, stay a string then
                setattr(storage.all()[key], attribute, value)
                # Save the updated instance
                storage.all()[key].save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
