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
            12: " undecillion",
            13: " duodecillion",
            14: " tredecillion",
            15: " quattuordecillion"
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


def convert_to_float_text(float_number):

    number = ""

    int_part = int(float_number)
    float_part = round(float_number - int_part, 2)

    cents_value = int(float_part * 100)
    if cents_value == 100:
        int_part += 1
        cents_value = 0

    dollar_part = convert_to_text(int_part)

    if cents_value < 100:
        cent_part = convert_to_text(cents_value)

    if int_part == 1:
        number = dollar_part + " dollar"
    else:
        number = dollar_part + " dollars"

    if cents_value > 0:
        number += " and "

        number += cent_part

        if cents_value == 1:
            number += " cent"
        else:
            number += " cents"

    return number


def convert_to_text(number):

    # Get a reference to the singleton instance
    translator = NumberTranslator.get_instance()

    # Special case for zero
    if number == 0:
        return translator.get_word(number)

    num_builder = ""
    threes = (len(str(number)) - 1) // 3

    if threes > 15:
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

        if '.' not in str_number:

            try:

                number = int(str_number)

                if number < 0:
                    print("Please enter a valid positive number.")
                    return

                print(convert_to_text(number))

            except (ValueError, TypeError):
                print("Please enter a valid positive number.")

        else:

            try:

                float_number = float(str_number)

                if float_number < 0:
                    print("Please enter a valid positive number.")
                    return

                number = convert_to_float_text(float_number)

            except(ValueError, TypeError):
                print("Please enter a valid positive number with a decimal point, if required.")

    else:

        numbers = [0, 1, 20, 31, 100, 156, 400, 985, 1000, 1005, 12345, 100000, 800005, 2000005, 12345678, 9876543210, 1234567890, 1000000000000001, 90000000000000000000000000000000000000, 12345678901234567890123456789012345678901234567890]
        float_numbers = [0., 1.5, 20.999, 31.95, 100.00, 156.58984, 400.336, 985.1, 1000.5, .9876, 12345, 100000.012, 800005.106, 1000.]

        valid_answers = ["zero", "one", "twenty", "thirty one", "one hundred", "one hundred and fifty six", "four hundred", "nine hundred and eighty five", "one thousand", "one thousand five", "twelve thousand three hundred and forty five", "one hundred thousand", "eight hundred thousand five", "two million five", "twelve million three hundred and forty five thousand six hundred and seventy eight", "nine billion eight hundred and seventy six million five hundred and forty three thousand two hundred and ten", "one billion two hundred and thirty four million five hundred and sixty seven thousand eight hundred and ninety", "one quadrillion one", "ninety undecillion", "Number too large"]
        valid_float_answers = ["zero dollars", "one dollar and fifty cents", "twenty one dollars", "thirty one dollars and ninety five cents", "one hundred dollars", "one hundred and fifty six dollars and fifty nine cents", "four hundred dollars and thirty four cents", "nine hundred and eighty five dollars and ten cents", "one thousand dollars and fifty cents", "zero dollars and ninety nine cents", "twelve thousand three hundred and forty five dollars", "one hundred thousand dollars and one cent", "eight hundred thousand five dollars and eleven cents", "one thousand dollars"]

        failures = 0
        numbers_in_words = [convert_to_text(number) for number in numbers]
        counter = 1

        for i in range(len(numbers)):

            if (numbers_in_words[i] != valid_answers[i]):
                print(counter, "Test failed for ", numbers[i])
                print("Expected:", valid_answers[i], "but got:", numbers_in_words[i])
                failures += 1
            
            counter += 1

        float_numbers_in_words = [convert_to_float_text(float_number) for float_number in float_numbers]
        counter = 1

        for i in range(len(float_numbers)):

            if (float_numbers_in_words[i] != valid_float_answers[i]):
                print(counter, "Test failed for ", float_numbers[i])
                print("Expected:", valid_float_answers[i], "but got:", float_numbers_in_words[i])
                failures += 1
            
            counter += 1

        if failures == 0:
            print("All tests passed!")

if __name__ == "__main__":
    main()
