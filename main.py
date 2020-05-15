import copy
import re

memory_in = open("memory_in.txt", "r")

copy_from_in_to_out_do_pice = memory_in.read()

memory_out_txt = open("memory_out.txt", "w")

rules = open("rules.txt", "r")

print(copy_from_in_to_out_do_pice, file=memory_out_txt)

memory_out_txt.close()
memory_in.close()


class Rule:
    def __init__(self, index):
        self.index = index
        self.name = self.get_name()
        self.conditions_string = self.get_conditions()
        self.conditions = self.conditions_string.split(",")
        self.post_conditions_string = self.get_post_conditions()
        self.post_conditions = self.post_conditions_string.split(",")
        self.max_depth = len(self.conditions)

    def get_name(self):
        rules.seek(0)
        lines = rules.readlines()

        for i in range(len(lines)):
            line = lines[i]

            lines[i] = line.replace("\n", "")

        index = 0
        for i in lines:
            if i == '':
                lines.pop(index)
            index += 1

        name_list = []

        for i in range(len(lines)):
            if i % 3 == 0:
                name_list.append(lines[i].replace("Meno: ", ""))

        return name_list[(self.index)]

    def get_conditions(self):
        rules.seek(0)
        lines = rules.readlines()

        for i in range(len(lines)):
            line = lines[i]

            lines[i] = line.replace("\n", "")

        index = 0
        for i in lines:
            if i == '':
                lines.pop(index)
            index += 1

        conditions_list = []

        for i in range(len(lines)):
            if i % 3 == 1:
                conditions_list.append(lines[i].replace("AK    ", ""))
        array = conditions_list[self.index]

        return array

    def get_post_conditions(self):
        rules.seek(0)
        lines = rules.readlines()

        for i in range(len(lines)):
            line = lines[i]

            lines[i] = line.replace("\n", "")

        index = 0
        for i in lines:
            if i == '':
                lines.pop(index)
            index += 1

        post_conditions_list = []

        for i in range(len(lines)):
            if i % 3 == 2:
                post_conditions_list.append(lines[i].replace("POTOM ", ""))

        array = post_conditions_list[self.index]

        return array


class Memory_output:
    def __init__(self):
        self.memory = []
        self.get_memory()

    def get_memory(self):
        memory_out_file = open("memory_out.txt", "r")
        for line in memory_out_file.readlines():
            self.memory.append(line.strip())


def get_number_of_variables(rule):
    list_of_var = []
    for har in range(len(rule.conditions_string)):

        if rule.conditions_string[har] == "?":

            if rule.conditions_string[har + 1] not in list_of_var:
                list_of_var.append(rule.conditions_string[har + 1])
    return len(list_of_var)


def execute_condition(rule, dict_of_variables, depth, memory_out, helper_outputs):
    actual_condition = rule.conditions[depth]

    actual_condition_with_names = actual_condition
    raw_condition = actual_condition

    for key, value in dict_of_variables.items():
        actual_condition_with_names = actual_condition_with_names.replace(f"?{key}", value)

    actual_condition_with_everything = actual_condition_with_names.strip()
    actual_condition_with_names = re.sub(r'\?.', "", actual_condition_with_names).strip()
    raw_condition = re.sub(r'\?.', "", raw_condition).strip()

    useful_facts = []
    for fact in memory_out.memory:
        match = re.search(actual_condition_with_names, fact)

        if match:
            useful_facts.append(fact)

    new_variable_keys = actual_condition_with_everything.replace(
        actual_condition_with_names, "").replace("?", "").replace(" ", "")

    if "<>" in actual_condition:
        two_variables = actual_condition.replace("<>", "").replace("?", "").strip().split(" ")
        if dict_of_variables[two_variables[0]] != dict_of_variables[two_variables[1]]:
            if rule.max_depth != (depth + 1):
                execute_condition(rule, dict_of_variables, depth + 1, memory_out, helper_outputs)
            else:
                number_of_variables = get_number_of_variables(rule)

                if number_of_variables == len(dict_of_variables):
                    new_helper_output = rule.post_conditions_string

                    for key, value in dict_of_variables.items():
                        new_helper_output = new_helper_output.replace(f"?{key}", value)

                    new_helper_output = f"{rule.name}, {new_helper_output}"

                    if new_helper_output not in helper_outputs:
                        helper_outputs.append(new_helper_output)


        print(f"{rule.name}")
    else:
        for output in useful_facts:
            new_variable_names = output.replace(actual_condition_with_names, "").replace("  ", " ").strip().split(" ")
            new_dict_variables = copy.deepcopy(dict_of_variables)

            for index in range(len(new_variable_keys)):
                new_dict_variables[new_variable_keys[index]] = new_variable_names[index]

            if rule.max_depth != (depth + 1):
                execute_condition(rule, new_dict_variables, depth + 1, memory_out, helper_outputs)
            else:
                number_of_variables = get_number_of_variables(rule)

                if number_of_variables == len(new_dict_variables):
                    new_helper_output = rule.post_conditions_string
                    for key, value in new_dict_variables.items():
                        new_helper_output = new_helper_output.replace(f"?{key}", value)

                    new_helper_output = f"{rule.name}, {new_helper_output}"

                    if new_helper_output not in helper_outputs:
                        helper_outputs.append(new_helper_output)


if __name__ == '__main__':
    helper_outputs = []
    prd = Rule(1)
    rules.seek(0)
    number_of_rules = rules.readlines()

    fuj = Memory_output()

    object_rules = []

    for i in range(round(len(number_of_rules) / 4)):
        object = Rule(i)

        object_rules.append(object)

    for i in range(len(object_rules)):
        execute_condition(object_rules[i], {}, 0, fuj, helper_outputs)
    print(helper_outputs)
