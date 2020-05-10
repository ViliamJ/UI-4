memory_in = open("memory_in.txt", "r")

copy = memory_in.read()

memory_out = open("memory_out.txt", "w")

rules = open("rules.txt", "r")

print(copy, file=memory_out)


class Rule:
    def __init__(self, index):
        self.index = index
        self.name = self.get_name()
        self.conditions = self.get_condition()
        self.post_condition = self.get_post_condition()

    def get_name(self):
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

        return name_list[(self.index) - 1]

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
        array = conditions_list[self.index - 1]

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

        array = post_conditions_list[self.index - 1]

        return array.split(",")


if __name__ == '__main__':
    prd = Rule(7)
    print(prd.__dict__)
