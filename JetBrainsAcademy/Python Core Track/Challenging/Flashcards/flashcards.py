import os
import sys


class FlashCard:
    def __init__(self, term: str, definition: str):
        self.term: str = term
        self.definition: str = definition
        self.mistakes: int = 0

    def __str__(self):
        return "\n".join(("Card:", self.term, "Definition:", self.definition,
                          "Mistakes:", self.mistakes))


class Processor:
    def __init__(self, export_to_param, import_from_param):
        self.cards = []
        self.term_set = set()
        self.definition_set = set()
        self.definition_to_term = dict()
        self.logs = []  # contains all lines of log...
        self.export_to = export_to_param  # feature for stage 7
        self.import_from = import_from_param  # feature for stage 7

    def get_max_mistakes_term_lists_and_value(self):
        mistakes_set = {card.mistakes for card in self.cards}
        max_mistakes = max(mistakes_set) if mistakes_set else 0
        return [card.term for card in self.cards if
                card.mistakes == max_mistakes], max_mistakes

    def print(self, line: str = ""):
        print(line)
        if line:
            self.logs.append(line)

    def input(self, line: str = "") -> str:
        result = input(line)
        if line:
            self.logs.append(line)
        self.logs.append(result)
        return result

    def get_action(self):
        return self.input("Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):")

    def exit_program(self):
        self.print('bye bye')

    def add(self):
        self.print("The card:")
        while True:
            term = self.input()
            if term in self.term_set:
                self.print(f'The term "{term}" already exists. Try again:')
            else:
                break
        self.print("The definition of the card:")
        while True:
            definition = self.input()
            if definition in self.definition_set:
                self.print(f'The definition "{definition}" already exists. Try again:')
            else:
                break
        self.add_card(term, definition)
        self.print(f'The pair ("{term}":"{definition}") has been added.')

    def add_card(self, term, definition):
        self.definition_to_term[definition] = term
        self.term_set.add(term)
        self.definition_set.add(definition)
        f = FlashCard(term, definition)
        self.cards.append(f)

    def check_card(self, term):
        return term in self.term_set

    def remove_card(self, term):
        for definition in self.definition_to_term:
            if self.definition_to_term[definition] == term:
                self.definition_to_term.pop(definition)
                break

        self.term_set.remove(term)
        self.definition_set.remove(definition)
        for card in self.cards:
            if card.term == term:
                self.cards.remove(card)
                break

    def remove(self):
        term = self.input('Which card?')
        if self.check_card(term):
            self.remove_card(term)
            self.print('The card has been removed.')
        else:
            self.print("Can't remove " + f'"{term}"' +
                       ": there is no such card.")

    def import_cards_from_file(self, file_name):
        with open(file_name, 'r') as file:
            lines = file.readlines()
            for line in lines:
                term, definition = line.split('\t')
                self.add_card(term, definition[:-1])
            self.print(f'{len(lines)} cards have been loaded.')

    def import_cards(self):
        file_name = self.input('File name:')
        if os.path.isfile(file_name):
            self.import_cards_from_file(file_name)
        else:
            self.print('File not found.')

    def get_lines_from_cards(self):
        return [f'{card.term}\t{card.definition}' for card in self.cards]

    def export_cards_to_file(self, file_name):
        with open(file_name, 'w') as file:
            card_lines = self.get_lines_from_cards()
            for line in card_lines:
                file.write(f"{line}\n")
            self.print(f"{len(card_lines)}" + " cards have " +
                       "been saved.")

    def export_cards(self):
        file_name = self.input('File name:')
        self.export_cards_to_file(file_name)

    def process(self):
        action = ''
        while action != 'exit':
            self.print()
            action = self.get_action()
            if action == 'add':
                self.add()
            elif action == 'import':
                self.import_cards()
            elif action == 'export':
                self.export_cards()
            elif action == 'exit':
                self.exit_program()
            elif action == 'ask':
                self.ask()
            elif action == 'remove':
                self.remove()
            elif action == 'log':
                self.log()
            elif action == 'hardest card':
                self.get_hardest_card()
            elif action == 'reset stats':
                self.reset_stats()

    def log(self):
        file_name = self.input('File name:')
        with open(file_name, 'w') as file:
            file.writelines(self.logs)
            self.print('The log has been saved.')

    def get_hardest_card(self):
        max_mistakes_term_list, max_mistakes = self.get_max_mistakes_term_lists_and_value()
        list_len = len(max_mistakes_term_list)
        if max_mistakes == 0:
            self.print('There are no cards with errors.')
        elif list_len == 1:
            self.print(f'The hardest card is "{max_mistakes_term_list[0]}". You have {max_mistakes} errors answering it.')
        else:
            terms_str = '"'
            for term in max_mistakes_term_list:
                terms_str += term + '", '
            terms_str = terms_str[:len(terms_str) - 2]
            self.print(f'The hardest cards are {terms_str}. You have {max_mistakes} errors answering it.')

    def reset_stats(self):
        for card in self.cards:
            card.mistakes = 0
        self.print('Card statistics have been reset.')

    def ask(self):
        times = int(self.input('How many times to ask?'))
        self.do_flashcard_exams(times)

    def do_flashcard_exams(self, times):
        for i in range(times):
            flash_card = self.cards[i % len(self.cards)]
            answer = self.input(f'Print the definition of "{flash_card.term}":')
            if answer == flash_card.definition:
                self.print("Correct!")
            else:
                flash_card.mistakes += 1
                result = f'Wrong. The right answer is "{flash_card.definition}"'
                if answer in self.definition_set:
                    result += f', but your definition is correct for "{self.definition_to_term[answer]}".'
                else:
                    result += '.'
                self.print(result)


if __name__ == "__main__":
    # Example: --export_to=vocab.txt --import_from=vocab.txt
    exported_file_name = ''
    imported_file_name = ''
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            if arg.startswith('--export_to='):
                exported_file_name = arg.split('=')[1]
            elif arg.startswith('--import_from='):
                imported_file_name = arg.split('=')[1]

    p = Processor(exported_file_name, imported_file_name)
    if imported_file_name:
        p.import_cards_from_file(imported_file_name)
    p.process()
    if exported_file_name:
        p.export_cards_to_file(exported_file_name)
