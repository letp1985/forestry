import inquirer
import json


class UserInterface:
    """
        Main user interface Class linked to config.json
    """

    def __init__(self, element):
        self.element = element

    def return_function(self, answer_function):
        """
        Returns function (if exists) for a given answer to a question in the UI
        """

        # check if any functions should be called
        if GetAttributes(self.element, 'return_type').get_config_attribute() == "function":

            func = [k for k in answer_function][0]

            # check if there is a function that should be applied for the users answer
            return func if func else False

    def return_function_inputs(self, answer_function):
        """
        Returns function
        """

        # check if any functions should be called
        if GetAttributes(self.element, 'return_type').get_config_attribute() == "function":

            func_input = [v for k, v in answer_function.items()][0]

            return func_input

    def return_choice_list(self):
        """
        Returns the lists of choices dynamically based on a function call or the options in the json
        """

        choices_check = GetAttributes(self.element, 'choices').check_config_attributes()
        # choice_list = GetAttributes(self.element, 'choice_list').check_config_attributes()

        if choices_check:
            choices_list = GetAttributes(self.element, 'choice_list').check_config_attributes()
            return choices_list
        else:
            eval(GetAttributes(self.element, 'choice_list').get_config_attribute())

    def user_interface_generator(self):
        """
        Main UI handler
        """

        message = GetAttributes(self.element, 'message').get_config_attribute()

        choices = self.return_choice_list()

        q = [
            inquirer.List(self.element,
                          message=message,
                          choices=choices
                          ),
        ]

        # get users answer

        answer = inquirer.prompt(q)[self.element]

        # check if functions are required to be ran after selecting an option

        function = self.return_function(choices[answer])

        # check if functions inputs are required i.e. function criteria

        function_inputs = self.return_function_inputs(choices[answer])

        if not isinstance(function, type(None)) and not isinstance(function_inputs, type(None)):

            eval(function)(function_inputs)

        if not isinstance(function, type(None)):

            eval(function)


class GetAttributes:
    """
        Class to retrieve attributes for a given UI step
    """
    def __init__(self, element, attribute):
        self.element = element
        self.attribute = attribute

    def get_json_config(self):
        """
        Loads json config into dictionary
        """

        with open('user_interface/config.json') as f:
            config_json = json.load(f)

        return config_json

    def get_config_attribute(self):
        """
        Returns the specific value for given element and attribute
        """

        ui_config = self.get_json_config()

        attrib = ui_config[self.element][self.attribute]

        return attrib

    def check_config_attributes(self):
        """
        Returns True or False if attribute exists
        """

        ui_config = self.get_json_config()

        return True if self.attribute in ui_config[self.element] else False


def quit_menu():

    print('Thank you for using this service')
    return exit()

#