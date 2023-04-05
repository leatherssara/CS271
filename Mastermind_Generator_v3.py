""" Mastermind_Generator_v3.py by Sara Leathers

    This program creates the code-breaking game Mastermind.

    Instructions:
    
        -The first prompt asks if you want to change the game parameters.
        A choice of "y" or "yes" will start a series of prompts for code
        length, duplicate allowance, and guess limit. These settings will
        be saved to a .txt file.
        
        -A choice of "n" or "no" will skip ahead, having either read an
        existing .txt file, or, if no file exists, preset with the default
        settings: code length = 4, duplicates disabled, and guess limit = 10.
        
        -A code meeting the length and duplicates parameters will be
        generated.
        
        -Enter a numeric guess (no spaces or separators) of the appropriate
        length at the associated prompt and press Enter to submit the guess.
        
        -Your guess will be evaluated for:
            a. The number of correct digits in the correct position, and
            b. The number of correct digits (i.e. present in the code) that
               are not in the correct position.
               
        -If you successfully guess the entire code correctly, you win!
        
        -If you fail to guess the code within the guess limit, the program
        will tell you the correct answer.
"""

import os
import random


class Parameters:
    """ A class for the parameters required for the game """
    
    def __init__(self, settings = None):
        """
            Takes user input for game parameters
            Args:
                settings: (length, duplicates, limit) parameters
            Returns: None
        """
        if __name__ == "__main__":
            try:
                self.length, self.duplicates, self.limit, self.suffix_dict = self.read_param()
                print("Previously set parameters identified.")
            except FileNotFoundError:
                self.length, self.duplicates, self.limit, self.suffix_dict = 4, False, 10, self.generate_dictionary()
                print("No previous parameters found, default settings used.")

            print(self)
            change_parameters = input("Change settings? (Y/N) ")

            while True:
                if change_parameters.lower() in {"y", "yes"}:
                    self.set_param()
                    self.length, self.duplicates, self.limit, self.suffix_dict = self.read_param()
                    break
                elif change_parameters.lower() in {"n", "no"}:
                    break
                else:
                    print("Invalid input, please try again.")
        else:
            if settings is not None:
                self.save_param(settings[0], settings[1], settings[2])
            try: self.length, self.duplicates, self.limit, self.suffix_dict = self.read_param()
            except FileNotFoundError: self.length, self.duplicates, self.limit, self.suffix_dict = 4, False, 10, self.generate_dictionary()

    def set_param(self):
        """
            Takes user input for game parameters
            Args:
                None
            Returns:
                None
        """
        ## Set length
        while True:
            try:
                length = int(input("How many digits should the code have? "))

                if length < 2:
                    print("Invalid length, must be at least 2. Please try again.")
                    continue
                elif length > 10:
                    print("Duplicates required.")
                break
            
            except ValueError:
                print("Invalid length, must be an integer. Please try again.")
                continue

        ## Set allowance of duplicate digits
        if length <= 10:
            while True:
                duplicates_allowed = input("Are duplicate digits allowed? (Y/N) ")
                if duplicates_allowed.lower() in {"y", "yes", "n", "no"}:
                    duplicates = duplicates_allowed.lower() in {"y", "yes"}
                    break
                else:
                    print("Invalid input, please try again.")
        else:
            duplicates = True
        
        ## Set guess limit
        while True:
            try:
                limit = int(input("How many guesses are allowed? "))
                if limit < 1 or limit > 99:
                    print("Invalid limit, must be at least 1 and less than 99. Please try again.")
                    continue
                break
            except ValueError:
                print("Invalid limit, must be an integer. Please try again.")
        
        self.save_param(length, duplicates, limit)
        
        return None


    def save_param(self, length, duplicates, limit):
        """
            Creates/writes user-input parameters to param.txt
            Args:
                length (int): the length of the code
                duplicates (bool): True if duplicate digits are allowed
                limit (int): the limit to the number of allowed guesses
            Returns:
                None
        """
        dirname = os.path.dirname(__file__)
        file_w = os.path.join(dirname, "./param.txt")
        param_file = open(file_w, "w", encoding='utf-8')
        param_file.write(f"length: {str(length)}\n")
        param_file.write(f"duplicates: {int(duplicates)}\n")
        param_file.write(f"limit: {str(limit)}")
        param_file.close()

        if __name__ == "__main__":
            # This function is called in Tk_Mastermind, where printouts are not needed.
            print("Parameters saved!\n")
        
        return None


    def generate_dictionary(self):
        """
            Creates a dictionary of numeral suffixes ("1st", "2nd", etc.)
            Args:
                self: length, deuplicates, limit, and suffix_dict parameters
            Returns:
                suffix_dict: a dictionary with string numbers as keys
                and string suffixes as values
        """
        suffix_dict = {}
        for num in range(14):
            match num:
                case 1:
                    suffix = "st"
                case 2:
                    suffix = "nd"
                case 3:
                    suffix = "rd"
                case _:
                    suffix = "th"

            suffix_dict.update({str(num): suffix})
        
        return suffix_dict


    def read_param(self):
        """Reads parameters from param.txt file
            Args:
                self: length, deuplicates, limit, and suffix_dict parameters
            Returns:
                length (int): the length of the code to be generated
                duplicates (bool): whether duplicate digits are allowed
                limit (int): the number of guesses allowed before "game over"
                suffix_dict (dictionary): the integer suffix dictionary
        """
        dirname = os.path.dirname(__file__)
        file_r = os.path.join(dirname, "./param.txt")
        param_file = open(file_r, "r", encoding='utf-8')
        
        for line_str in param_file:
            if "length: " in line_str:
                length = int(line_str.split("length: ")[1].split("\n")[0])
            elif "duplicates: " in line_str:
                duplicates = bool(int(line_str.split("duplicates: ")[1].split("\n")[0]))
            elif "limit: " in line_str:
                limit = int(line_str.split("limit: ")[1].split("\n")[0])

        param_file.close()
        suffix_dict = self.generate_dictionary()
        
        return length, duplicates, limit, suffix_dict


    def __str__(self):
        """string method for Parameters object"""
        return("Parameters:\n\tlength: {}\n\tduplicates: {}\n\tguess limit: {}"
                  .format(self.length, self.duplicates, self.limit))


class Mastermind:
    """Mastermind object is the code for the game."""
    
    def __init__(self, length, duplicates):
        """ Initializes Mastermind object.
            Uses length and duplicates arguments to create random code.
        """
        code = []
        
        for _ in range(length):
            if duplicates:
                item = str(random.randint(0,9))
            else:
                while True:
                    item = str(random.randint(0,9))
                    if item not in code:
                        break

            code.append(item)

        self.value = "".join(code)
        self.length = length
        self.duplicates = duplicates
        
        if __name__ == "__main__":
            # This function is called in Tk_Mastermind, where printouts are not needed.
            print(f"Code generated - length: {length}, duplicates", "enabled" if duplicates else "disabled")


    def guess_code(self, guess_count = int, suffix_dict = {}, entered_guess = str):
        """
            Recursively requests user input "guesses" and evaluates validity (not correctness)
            Args:
                self (Mastermind): the code to be guessed
                guess_count (int): the sequential number of the current guess
                suffix_dict: the number suffix dictionary
            Returns:
                if valid code is entered:
                guess (str): a valid user-input guess
        """
        if __name__ == "__main__":
            # determine correct suffix for current guess number
            if str(guess_count) in suffix_dict.keys():
                suffix = suffix_dict[str(guess_count)]    
            else:
                suffix = suffix_dict[str(guess_count)[-1]]
            # this suffix (and the way the dictionary is generated) is the reason for the upper limit
            # of the guess limit being 99. Over 110 guesses, the suffix is not determined properly.
            
            guess = input(f"Enter your {guess_count}{suffix} guess: ")    
        else:
            guess = entered_guess
        
        if len(guess) == self.length and guess.isnumeric():
            # guess is "valid"
            return guess
        else:
            if __name__ == "__main__":
                # when running as a standalone program, this is a recursive funtion
                print("Invalid guess, try again.")
                return self.guess_code(guess_count, suffix_dict)
            else:
                # when running from tkinter, the program will take different actions in response to an invalid entry.
                return False


    def evaluate_guess(self, guess):
        """
            Evaluates correctness of user guess
            Args:
                guess (str): a valid user-input guess
                self (Mastermind): the code to be guessed
            Returns:
                correct_pos (int): number of correct integers in correct position
                correct_int (int): number of correct integers in incorrect position
        """
        correct_pos = 0
        correct_int = 0
        correct_int_index = set() ## indices which contain a correct integer, regardless of position

        for i in range(len(guess)):              
            # check number of digits that are correct AND in the correct position
            if guess[i] == self.value[i]:
                correct_int_index.add(i) ## append the index to the list
                correct_pos += 1
                
        for j in range(len(guess)):
            if guess[j] in self.value:
                for k in correct_int_index:
                    if guess[j] == self.value[k]:
                        break
                else:
                    correct_int_index.add(self.value.find(guess[j])) ## append the index to the list
                    correct_int += 1

            # Saving the index list prevents a guess of repeating digits from counting as more than one correct
            # item in either category

        # print feedback and return values
        if __name__ == "__main__":
            # This function is called in Tk_Mastermind, where printouts are not needed.
            print(f"Correct number AND position: {correct_pos}")
            print(f"Correct number, wrong position: {correct_int}\n")

        return correct_pos, correct_int
    

    def game_outcome(self, guess_count, limit, outcome):
        """
            Runs game, taking guesses and evaluating against set code up to guess limit
            Args:
                guess_count (int): the number of guesses reached
                limit (int): the limit to guesses allowed
                self (Mastermind): the code to be guessed
                outcome (bool): whether or not the code was solved
            Returns:
                str: end of game message
        """        
        # print outcome of game, either lost or won
        if guess_count >= limit and not outcome:
            return f"Guess limit reached. Too bad! \nSolution: {self.value}"
        else:
            return f"{self.value} \nCongratulations! \nYou used {guess_count} out of {limit} guesses."

        return None


    def play_game(self, suffix_dict, limit):
        """
            Runs game, taking guesses and evaluating against set code up to guess limit
            Args:
                self (Mastermind): the code to be guessed
                suffix_dict: the number suffix dictionary
                limit (int): the limit to guesses allowed
            Returns:
                None
        """
        print(f"Guess limit: {limit}\n")
        guess_count = 1
        outcome = False

        # take guesses and evaluate continuously until limit is reached or code is solved
        while guess_count <= limit:
            
            guess = self.guess_code(guess_count, suffix_dict)
            correct_position, correct_integer = self.evaluate_guess(guess)          
            if correct_position == self.length:
                outcome = True
                break
            else:
                guess_count += 1
            
        # once the while loop is broken, evaluate the game outcome
        print(self.game_outcome(guess_count, limit, outcome))

        return None
                   

def main():
    """
        Runs full program, including "play again" and "exit" operations.
        Args: None
        Returns: None
    """
    # Continuous loop to allow multiple game rounds
    playing = True
    while playing:
        try:
            # Establish game parameters
            parameters = Parameters()
            # Initialize code
            code = Mastermind(parameters.length, parameters.duplicates)
            # Run game
            code.play_game(parameters.suffix_dict, parameters.limit)
            # Play again?
            while True:
                play_input = input("\nPlay again? (Y/N) ")
                if play_input.lower() in {"y", "yes"}:
                    # "playing" is already True, no need to set again
                    break
                elif play_input.lower() in {"n", "no"}:
                    playing = False
                    break
                else:
                    print("Invalid input, please try again.")
            print()
        except KeyboardInterrupt:
            break
    
    print("Thanks for playing!")
    
    return None


if __name__ == '__main__':
    main()
