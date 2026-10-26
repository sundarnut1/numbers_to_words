import sys

class NumberTranslator:
    __instance = None
    __allow_creation = False

    def __init__(self):

        if not NumberTranslator.__allow_creation:
            raise RuntimeError("This class is a singleton! Use get_instance() method to get the instance.")
        
        self.__number_mapping = {
            0: "zero",
            1: "one",
            2: "two",
            3: "three",
            4: "four",
            5: "five",
            6: "six",
            7: "seven",
            8: "eight",
            9: "nine",
            10: "ten",
            11: "eleven",
            12: "twelve",
            13: "thirteen",
            14: "fourteen",
            15: "fifteen",
            16: "sixteen",
            17: "seventeen",
            18: "eighteen",
            19: "nineteen",
            20: "twenty",
            30: "thirty",
            40: "forty",
            50: "fifty",
            60: "sixty",
            70: "seventy",
            80: "eighty",
            90: "ninety"            
        }
        
        self.__power_mapping = {
            1: " thousand",
            2: " million",
            3: " billion",
            4: " trillion",
            5: " quadrillion",
            6: " quintillion",
            7: " sextillion",
            8: " septillion",
            9: " octillion",
            10: " nonillion",
            11: " decillion",
            12: " undecillion"
        }        

    @staticmethod
    def get_instance():

        if NumberTranslator.__instance is None:
            NumberTranslator.__allow_creation = True
            NumberTranslator.__instance = NumberTranslator()
            NumberTranslator.__allow_creation = False

        return NumberTranslator.__instance


    def get_word(self, number):
        return self.__number_mapping.get(number, "Number not found")


    def get_power_word(self, number):
        return self.__power_mapping.get(number, "Number not found")


def convert_to_text(number):

    # Get a reference to the singleton instance
    translator = NumberTranslator.get_instance()

    # Special case for zero
    if number == 0:
        return translator.get_word(number)

    num_builder = ""
    threes = (len(str(number)) - 1) // 3

    if threes > 12:
        return "Number too large"

    while True:

        unit = 0
        added = 0

        power_10 = 10 ** (threes * 3)
        working_set = number // power_10
        next_set = number % power_10
        over = working_set % 100;

        if working_set > 99:

            if len(num_builder) > 0:
                num_builder += ' '

            num_builder += translator.get_word(working_set // 100) + " hundred"

            added = 1

        if over >= 20:

            unit = over % 10

            if added == 1:
                num_builder += " and "

            elif added == 0:
                if len(num_builder) > 0:
                    num_builder += ' '

            num_builder += translator.get_word((over // 10) * 10)

            added |= 2

        else:
            unit = over


        if unit > 0:
            
            if added & 2 == 2: 
                # Suffix a space if the tens place was added
                num_builder += ' '

            elif added & 1 == 1:
                # Suffix " and " if we have a tens and a units place
                num_builder += " and "

            elif len(num_builder) > 0 and num_builder[-1] != ' ': 
                # Suffix a space if num_builder is not blank and we have a non-blank value as the last character
                num_builder += ' '

            num_builder += translator.get_word(unit)

            added |= 4

        if added > 0 and threes > 0:
            num_builder += translator.get_power_word(threes)

        threes -= 1
        number = next_set

        if threes < 0:
            break

    return num_builder

def main():

    if len(sys.argv) >= 2:
        str_number = sys.argv[1]

        try:
            number = int(str_number)

            if number < 0:
                print("Please enter a valid positive number.")
                return

            print(convert_to_text(number))

        except (ValueError, TypeError):
            print("Please enter a valid positive number.")

    else:

        numbers = [0, 1, 20, 31, 100, 156, 400, 985, 1000, 1005, 12345, 100000, 800005, 2000005, 12345678, 9876543210, 1234567890, 1000000000000001, 90000000000000000000000000000000000000]
        valid_answers = ["zero", "one", "twenty", "thirty one", "one hundred", "one hundred and fifty six", "four hundred", "nine hundred and eighty five", "one thousand", "one thousand five", "twelve thousand three hundred and forty five", "one hundred thousand", "eight hundred thousand five", "two million five", "twelve million three hundred and forty five thousand six hundred and seventy eight", "nine billion eight hundred and seventy six million five hundred and forty three thousand two hundred and ten", "one billion two hundred and thirty four million five hundred and sixty seven thousand eight hundred and ninety", "one quadrillion one", "ninety undecillion"]

        failures = 0
        numbers_in_words = [convert_to_text(number) for number in numbers]
        counter = 1

        for i in range(len(numbers)):

            if (numbers_in_words[i] != valid_answers[i]):
                print(counter, "Test failed for ", numbers[i])
                print("Expected:", valid_answers[i], "but got:", numbers_in_words[i])
                failures += 1
            
            counter += 1

        if failures == 0:
            print("All tests passed!")

if __name__ == "__main__":
    main()
