#!/usr/bin/python3
"""
Command-line interpreter module
"""
import cmd
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models import storage


class HBNBCommand(cmd.Cmd):
    """
    Creates an entry point of the command interpreter
    """
    prompt = "(hbnb) "
    classes = ("BaseModel", "User", "State", "Amenity",
               "City", "Place", "Review")

    # classes = {
    #            'BaseModel': BaseModel, 'User': User, 'Place': Place,
    #            'State': State, 'City': City, 'Amenity': Amenity,
    #            'Review': Review
    #           }


    def do_quit(self, line):
        """
        Command to exit the console
        """
        return True

    def do_EOF(self, line):
        """
        Command to exit the console
        """
        return True

    def emptyline(self):
        """
        Command to do nothing when newline is entered
        """
        return

    def do_create(self, name):
        """
        Creates a new instance of BaseModel,
        saves it (to the JSON file) and prints the id
        """
        if not name:
            return

        class_name, *parameters = name.split(" ")
        if class_name not in self.classes:
            print("** class doesn't exist **")
            return

        Obj = eval(class_name)  # BaseModel
        new_instance = Obj() # BaseModel()

        for key_value in parameters:
            key, value = key_value.split("=")
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1].replace("_", " ") #.replace(r'\"', '"')
            elif "." in value:
                try:
                    value = float(value)
                except ValueError:
                    continue
            else:
                try:
                    value = int(value)
                except ValueError:
                    continue
            setattr(new_instance, key, value)

        print(new_instance.id)
        storage.save()

    def do_show(self, str):
        """
        Prints the string representation of
        an instance based on the class name and id
        """
        if str:
            tok = str.split()
            if tok[0] not in self.classes:
                print("** class doesn't exist **")
            elif len(tok) < 2:
                print("** instance id missing **")
            else:
                key = "{}.{}".format(tok[0], tok[1])
                if key in storage.all():
                    print(storage.all()[key])
                    storage.save()
                else:
                    print("** no instance found **")
        else:
            print("** class name missing **")

    def do_destroy(self, str):
        """
        Deletes an instance based on the class name and id
        and saves the change into the JSON file
        """
        if str:
            tok = str.split()
            if tok[0] not in self.classes:
                print("** class doesn't exist **")
            elif len(tok) < 2:
                print("** instance id missing **")
            else:
                key = "{}.{}".format(tok[0], tok[1])
                objects = storage.all()
                if key in objects:
                    del objects[key]
                    storage.save()
                else:
                    print("** no instance found **")
        else:
            print("** class name missing **")

    def do_all(self, cmd_args):
        """
        Prints all string representation of all instances
        based or not on the class name
        """
        list_of_strings = []
        if not cmd_args:
            for key in storage.all():
                objects = str(storage.all()[key])
                list_of_strings.append(objects)

            print(list_of_strings)
        else:
            if cmd_args in self.classes:

                for key in storage.all():
                    class_name = key.split(".")

                    if class_name[0] == cmd_args:
                        objects = str(storage.all()[key])
                        list_of_strings.append(objects)

                print(list_of_strings)
            else:
                print("** class doesn't exist **")

    def do_update(self, cmd_args):
        """
        Updates an instance based on the class name and id
        by adding or updating attribute and save the
        change into the JSON file
        """
        if cmd_args:
            tok = cmd_args.split()
            if tok[0] in self.classes:
                if len(tok) < 2:
                    print("** instance id missing **")
                else:
                    key = "{}.{}".format(tok[0], tok[1])
                    if key in storage.all():
                        if len(tok) < 3:
                            print("** attribute name missing **")
                        elif len(tok) < 4:
                            print("** value missing **")
                        else:
                            for k, v in storage.all().items():
                                if k == key:
                                    attr = eval(tok[3])
                                    setattr(v, tok[2], attr)
                                    storage.save()
                                    break
                    else:
                        print("** no instance found **")
            else:
                print("** class doesn't exist **")
        else:
            print("** class name missing **")

    def do_count(self, cmd_args):
        """
        Retrieves the number of instances of a class
        """
        count = 0
        objects = storage.all()
        for key, value in objects.items():
            if type(value).__name__ == cmd_args:
                count += 1

        print(count)

    def custom_split(self, cmd_args):
        args = cmd_args.replace(".", " ").replace("(", " ").\
            replace(",", " ").replace(")", " ").split()
        return args

    def default(self, cmd_args):
        """
        Method called on an input line
        when the command prefix is not recognized
        """
        if cmd_args.endswith(".all()"):
            args = self.custom_split(cmd_args)
            class_name = args[0]
            self.do_all(class_name)
        elif cmd_args.endswith(".count()"):
            args = self.custom_split(cmd_args)
            class_name = args[0]
            self.do_count(class_name)
        elif ".show" in cmd_args:
            args = self.custom_split(cmd_args)
            if args[0] not in self.classes:
                print("** class doesn't exist **")
            elif len(args) < 3:
                print("** instance id missing **")
            else:
                try:
                    eval_args = eval(args[2])
                    class_name = "{} {}".format(args[0], eval_args)
                    self.do_show(class_name)
                except Exception:
                    print("** Invalid syntax **")
        elif ".destroy" in cmd_args:
            args = self.custom_split(cmd_args)
            if args[0] not in self.classes:
                print("** class doesn't exist **")
            elif len(args) < 3:
                print("** instance id missing **")
            else:
                try:
                    eval_args = eval(args[2])
                    class_name = "{} {}".format(args[0], eval_args)
                    self.do_destroy(class_name)
                except Exception:
                    print("** Invalid destroy command syntax **")
        elif ".update" in cmd_args:
            if "{" not in cmd_args and "}" not in cmd_args:
                args = self.custom_split(cmd_args)

                if len(args) < 3:
                    print("** instance id missing **")
                elif len(args) < 4:
                    print("** attribute name missing **")
                elif len(args) < 5:
                    print("** value missing **")

                try:
                    class_name = args[0]
                    instance_id = eval(args[2])
                    attribute_name = eval(args[3])
                    attribute_value = args[4]
                    update_cmd = f"{class_name} {instance_id}\
                        {attribute_name} {attribute_value}"
                    self.do_update(update_cmd)
                except Exception:
                    print("** Invalid update command syntax **")
            else:
                args = self.custom_split(cmd_args)

                if len(args) < 3:
                    print("** instance id missing **")
                else:
                    start_idx = cmd_args.find("{")
                    end_idx = cmd_args.find("}")

                    json_str = str(cmd_args[start_idx:end_idx+1]).\
                        replace("'", "\"").replace("'", "\"")

                    py_dict = json.loads(json_str)

                    for key, value in py_dict.items():
                        class_name = args[0]
                        instance_id = eval(args[2])
                        attribute_name = key
                        if type(value) is str:
                            attribute_value = f'"{value}"'
                        else:
                            attribute_value = value
                        update_cmd = f"{class_name} {instance_id}\
                            {attribute_name} {attribute_value}"
                        self.do_update(update_cmd)

    def postloop(self):
        """
        Prints a new line when the interpreter exits
        """
        print()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
