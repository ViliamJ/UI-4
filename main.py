import copy
import re

memory_in = open("memory_in.txt", "r")

copy_from_in_to_out_do_pice = memory_in.read()

memory_out = open("memory_out.txt", "w")

rules = open("rules.txt", "r")

print(copy_from_in_to_out_do_pice, file=memory_out)

memory_out.close()
memory_in.close()


class Rule:
    def __init__(self, index):
        self.index = index
        self.name = self.get_name()
        self.conditions = self.get_condition()
        self.post_condition = self.get_post_condition()

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

    def get_condition(self):
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

        return array.split(",")

    def get_post_condition(self):
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

        return array.split(",")


class Memory_output:
    def __init__(self):
        self.memory = []
        self.get_memory()

    def get_memory(self):
        memory_out_file = open("memory_out.txt", "r")
        for line in memory_out_file.readlines():
            self.memory.append(line.strip())


def execute_condition(rule, dict_of_variables, depth, memory_out):
    actual_condition = rule.conditions[depth]

    actual_condition_with_names = actual_condition

    for key, value in dict_of_variables.items():
        actual_condition_with_names = actual_condition_with_names.replace(f"?{key}", value)

    actual_condition_with_names = re.sub(r'\?.', "", actual_condition_with_names).strip()

    print(actual_condition_with_names)
    keep_outputs = []

    for fact in memory_out.memory:
        match = re.search(actual_condition_with_names, fact)

        if match:
            keep_outputs.append(fact)

    new_variable_keys = actual_condition.replace(actual_condition_with_names, "").replace("?", "").replace(" ", "")
    print(new_variable_keys)

    for output in keep_outputs:
        new_variable_names = output.replace(actual_condition_with_names, "").replace("  ", " ").split(" ")

        new_dict_variables = copy.deepcopy(dict_of_variables)
        for index in range(len(new_variable_keys)):
            new_dict_variables[new_variable_keys[index]] = new_variable_names[index]

            execute_condition(rule, new_dict_variables, depth + 1, memory_out)

    '''for var in new_variable_keys:
        print(var)
'''


if __name__ == '__main__':
    prd = Rule(1)
    rules.seek(0)
    number_of_rules = rules.readlines()

    fuj = Memory_output()

    object_rules = []

    for i in range(round(len(number_of_rules) / 4)):
        object = Rule(i)

        object_rules.append(object)

    for i in range(1):
        execute_condition(object_rules[i], {}, 0, fuj)
