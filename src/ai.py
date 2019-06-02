class Ai:

    def __init__(self, field, last_input):
        self.field = field
        self.last_input = last_input

    def calculate(self):
        self.__check_for_field_end()
        return self.last_input

    def __check_for_field_end(self):
        pass

    def __check_for_3_in_a_row(self):
        pass
