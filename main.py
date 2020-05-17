import copy
import re


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


def step_2_execute_condition(rule, dict_of_variables, depth, memory_out, helper_outputs):
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
                step_2_execute_condition(rule, dict_of_variables, depth + 1, memory_out, helper_outputs)
            else:
                number_of_variables = get_number_of_variables(rule)

                if number_of_variables == len(dict_of_variables):
                    new_helper_output = rule.post_conditions_string

                    for key, value in dict_of_variables.items():
                        new_helper_output = new_helper_output.replace(f"?{key}", value)

                    new_helper_output = f"{rule.name},{new_helper_output}"

                    if new_helper_output not in helper_outputs:
                        helper_outputs.append(new_helper_output)
    else:
        for output in useful_facts:
            new_variable_names = output.replace(actual_condition_with_names, "").replace("  ", " ").strip().split(" ")
            new_dict_variables = copy.deepcopy(dict_of_variables)

            for index in range(len(new_variable_keys)):
                new_dict_variables[new_variable_keys[index]] = new_variable_names[index]

            if rule.max_depth != (depth + 1):
                step_2_execute_condition(rule, new_dict_variables, depth + 1, memory_out, helper_outputs)
            else:
                number_of_variables = get_number_of_variables(rule)

                if number_of_variables == len(new_dict_variables):
                    new_helper_output = rule.post_conditions_string
                    for key, value in new_dict_variables.items():
                        new_helper_output = new_helper_output.replace(f"?{key}", value)

                    new_helper_output = f"{rule.name},{new_helper_output}"

                    if new_helper_output not in helper_outputs:
                        helper_outputs.append(new_helper_output)


def step_3_execute_filter(helper_outputs, memory):
    for x in range(len(helper_outputs) - 1, -1, -1):
        item = helper_outputs[x]
        item_list = item.split(",")
        correct_output = []

        for y in range(1, len(item_list)):
            actual_item_action_string = item_list[y].strip().split(" ")[0]
            actual_item_string = item_list[y].replace(f"{actual_item_action_string} ", "")

            if actual_item_action_string == "pridaj" and actual_item_string not in memory.memory:
                correct_output.append(item_list[y])
            elif actual_item_action_string == "vymaz" and actual_item_string in memory.memory:
                correct_output.append(item_list[y])
            elif actual_item_action_string == "sprava":
                correct_output.append(item_list[y])

        flag_is_correct = False
        for item_output in correct_output:
            item_output_action = item_output.split(" ")[0]
            if item_output_action != "sprava":
                flag_is_correct = True
                break

        if flag_is_correct:
            correct_output_string = ""
            for correct_output_item in correct_output:
                correct_output_string = f"{correct_output_string},{correct_output_item}"
            helper_outputs[x] = f"{item_list[0]}{correct_output_string}"

        else:
            helper_outputs.pop(x)


def step_5_execute_first(helper_outputs, memory):
    first_rules = helper_outputs[0].split(",")[1:]

    for rule in first_rules:
        action = rule.split(" ")[0]
        new_rule = rule.replace(f"{action} ", "")

        if action == "pridaj":
            memory.memory.append(new_rule)
        elif action == "vymaz":
            memory.memory.remove(new_rule)
        elif action == "sprava":
            print(new_rule)
        else:
            print("WRONG MADAFAKA")

    helper_outputs.pop(0)


if __name__ == '__main__':

    memory_in = open("memory_in.txt", "r")

    copy_from_in_to_out_do_pice = memory_in.read()

    memory_out_txt = open("memory_out.txt", "w")

    rules = open("rules.txt", "r")

    print(copy_from_in_to_out_do_pice, file=memory_out_txt)

    memory_out_txt.close()
    memory_in.close()

    helper_outputs = []

    rules.seek(0)
    number_of_rules = rules.readlines()

    memory_out_list = Memory_output()

    object_rules = []

    for i in range(round(len(number_of_rules) / 4)):
        object = Rule(i)

        object_rules.append(object)

    all_done_flag = False

    # while all_done_flag is False:
    for _ in range(20):

        for i in range(len(object_rules)):
            step_2_execute_condition(object_rules[i], {}, 0, memory_out_list, helper_outputs)

        step_3_execute_filter(helper_outputs, memory_out_list)

        if helper_outputs:
            step_5_execute_first(helper_outputs, memory_out_list)
        else:
            all_done_flag = True

    final_out = open("memory_out.txt", "w")
    [print(x, file=final_out) for x in memory_out_list.memory]
    print(memory_out_list.memory)
    final_out.close()
