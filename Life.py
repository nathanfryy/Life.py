from world import World
from cell import Cell
from rule import Rule
from time import sleep
import time
import toolbox
import os


class Life(object):

    def __init__(self):
        self.__world = World(34, 69)
        self.__fillrate = 25
        self.__delay = 0.5
        self.__generation = 0
        self.random()
        self.__lastWorld = ''
        self.__secondWorld = ''

    def main(self):
        """
        Main event loop for store.
        :return: None
        """
        command = 'help'
        parameter = None
        while command != 'quit':
            if command == 'help':
                self.help('help.txt')
                self.random()
            elif command == 'next generation':
                self.next_generation(parameter)
            elif command == 'run simulation':
                self.run_simulation(parameter)
            elif command == 'skip generations':
                self.skip_generations(parameter)
            elif command == 'random world':
                self.random()
            elif command == 'change fillrate':
                self.change_fillrate(parameter)
            elif command == 'change delay':
                self.change_delay(parameter)
            elif command == 'change size':
                self.change_size(parameter)
            elif command == 'change display':
                self.change_display(parameter)
            elif command == 'customize-world':
                print('[F]illrate   [D]elay   [S]ize   d[I]splay  sa[V]e to disk    load [W]orld   c[u]stom display     li[B]rary')
            elif command == 'save world':
                self.save(parameter, './worlds/')
            elif command == 'open world':
                self.open(parameter, './worlds/')
            elif command == 'custom-cells':
                self.user_display()
                self.change_display(parameter)
            elif command == 'geometry':
                self.set_geometry()
            elif command == 'library':
                self.from_library(parameter, './library/')
            elif command == 'change rules':
                self.change_rule(parameter)

            self.menu()

            command, parameter = self.get_command()
        print('goodbye')

    def menu(self):
        """
        returns a string containing the menu.
        :return: Menu string
        """
        return '[N]ext  [R]un   s[K]ip   n[E]w   [H]elp   [Q]uit   [C]ustom     [G]eometry   Ch[A]nge Rules '

    def get_command(self):
        """
        Get a valid command from the user.
        :return: command, parameter
        """
        commands = {'n': 'next generation',
                    'r': 'run simulation',
                    'k': 'skip generations',
                    'e': 'random world',
                    'f': 'change fillrate',
                    'd': 'change delay',
                    's': 'change size',
                    'i': 'change display',
                    'h': 'help',
                    '?': 'help',
                    'q': 'quit',
                    'c': 'customize-world',
                    'v': 'save world',
                    'w': 'open world',
                    'u': 'custom-cells',
                    'g': 'geometry',
                    'b': 'library',
                    'a': 'change rules'}

        validCommands = commands.keys()

        userInput = '&'
        parameter = None
        while userInput[0].lower() not in validCommands:
            userInput = input()
            if userInput == '':
                userInput = 'n'
                parameter = 1
        command = commands[userInput[0].lower()]
        if len(userInput) > 1:
            parameter = userInput[1:].strip()
        return command, parameter

    def status(self):
        """
        Returns a string representing the status of the world.
        :return: string
        """
        geometry = self.__world.get_currentGeo()
        #ruleSet = Rule.__currentRuleSet
        rows = self.__world.get_rows()
        columns = self.__world.get_columns()
        percentAlive = self.find_percentage()
        speed = self.__delay
        generation = self.__generation
        string = 'Status:   '
        string += f'size:[{rows}x{columns}]      '
        string += f'alive: {percentAlive}%      '
        string += f'speed: 1 gen every {speed} seconds     '
        string += f'generation: {generation}    '
        string += f'geometry: {geometry}    '
        #string += f'ruleSet: {ruleSet}    '
        return string

    def help(self, filename, prompt = None):
        """
        Displays instructions.
        :param filename: The string of helping instructions.
        :param prompt:
        :return: None
        """
        with open(filename, 'r') as file:
            help = file.read()
        print(help, end='')
        if prompt:
            input('\n' + prompt)
        hi = input("\n\npress <return> to continue")

    def next_generation(self, parameter):
        """
        Displays the next generation of the world.
        :param parameter:
        :return: None
        """
        self.__world.next_generation()
        self.__generation += 1
        print(self.__world, end='')
        print()
        print('You have now gone 1 gen forward.')
        print()
        print(self.status() + '\n' + self.menu(), end = ' ')

    def run_simulation(self, parameter):
        """
        Displays the next generation of the world.
        :param parameter:
        :return: None
        """
        if toolbox.is_integer(parameter) and int(parameter) > 0:
            generations = int(parameter)
        else:
            prompt = 'How many generations would you like to simulate?'
            generations = toolbox.get_integer_between(1, 10000, prompt)
        for generation in range(generations):
            self.__world.next_generation()
            self.__generation += 1
            if self.__world.is_stable() == True:
                "It is stable now."
                break
            else:
                pass

            #self.__world.__lastWorld = self.__world.__secondWorld
            string = self.__world.__str__()
            string += self.status()
            string += f'left: {generations - generation}'
            print(string)
            time.sleep(self.__delay)

        print()
        print(f'You have now been through {generations} generations. ')
        print()
        print(self.menu(), end=' ')
        #self.__generation += generations

    def skip_generations(self, parameter):
        """
        Displays the next generation of the world.
        :param parameter:
        :return: None
        """
        if toolbox.is_integer(parameter) and int(parameter) > 0:
            generations = int(parameter)
        else:
            prompt = 'How many generations would you like to skip?'
            generations = toolbox.get_integer_between(1, 10000, prompt)
        print(f'Skipping {generations} generations.', end='')
        for generation in range(generations):
            self.__world.next_generation()
            if self.__world.is_stable() == True:
                "It is stable now."
                break
            else:
                pass
            if generation % 100 == 0:
                print('.', end='')
        print(' done!')
        self.__generation += generations
        time.sleep(2)
        string = self.__world.__str__()
        string += self.status()
        print(string)
        print()
        print(f'You now have skipped forward {generations} generations.')
        print()
        print(self.menu(), end=' ')


    def change_fillrate(self, parameter):
        """
        Takes percentage from user on how much of the cells in the world are alive
        :param parameter: percent of cells alive to advance if user specifies in menu
        :return:
        """
        if parameter:
            self.__world.randomize(int(parameter))
        else:
            self.__world.randomize(self.get_percentage())
        sleep(2)
        print(f"\nFillrate changed to {self.__percentage}%")
        self.__generation = 0
        print(self.__world)
        print(self.status() + '\n' + self.menu(), end=' ')

    def change_delay(self, parameter):
        """
        Change the delay betwen generations of the simulation.
        :param parameter:
        :return: None
        """
        if toolbox.is_number(parameter):
            delay = float(parameter)
        else:
            prompt = 'Seconds of delay between generations?'
            delay = toolbox.get_number(prompt)
        self.__delay = delay
        print(f'Your speed of running the simulation is now 1 gen every {delay} seconds.')

    def change_display(self, parameter):
        """
        Change the live and dead characters for the cells.
        :param parameter:
        :return: None
        """
        if toolbox.is_integer(parameter) and \
                1 <= int(parameter) <= len(Cell.displaySets.keys()):
            setNumber = int(parameter)
        else:
            print('**************************************')
            for number, set in enumerate(Cell.displaySets):
                liveChar = Cell.displaySets[set]['liveChar']
                deadChar = Cell.displaySets[set]['deadChar']
                print(f'{number + 1}: living cells: {liveChar} dead cells: {deadChar}')
            print('**************************************')
            prompt = 'What character set would you like to use?'
            setNumber = toolbox.get_integer_between(1, number + 1, prompt)
        setString = list(Cell.displaySets.keys())[setNumber - 1]
        Cell.set_display(setString)
        print(self.__world, end='')
        print()
        print(f'Your living cell is now {liveChar} and a dead cell is {deadChar}.')
        print()
        print(self.status() + '\n' + self.menu(), end = ' ')

    def user_display(self):
        living = toolbox.get_string('What would you like your living cell to be?')
        dead = toolbox.get_string('What would you like your dead cell to be?')
        Cell.set_display_user_values(living, dead)
        print()
        print(f"You now have a choice of a '{living}' as a living cell and a dead cell as '{dead}'.")
        print()

    def random(self):
        """
        Create a random world
        :return: None
        """
        self.__world.randomize(self.__fillrate)
        print(self.__world, end='')
        print()
        print(' You just created a brand new random world.')
        print()
        self.__generation = 0
        print(self.status() + '\n' + self.menu(), end = ' ')

    def change_size(self, parameter):
        """
        changes the size of the current grid world.
        :param parameter:
        :return: None
        """
        if parameter:
            rows, columns = parameter.split('x',2)
            if toolbox.is_integer(rows) and toolbox.is_integer(columns):
                rows = int(rows)
                columns = int(columns)
        else:
            print("You cannot choose 1 for rows or columns.")
            prompt = 'How many rows of cells?'
            rows = toolbox.get_integer_between(2,40,prompt)
            prompt = 'How many cells in each row?'
            columns = toolbox.get_integer_between(2,120,prompt)
        self.__world = World(rows, columns)
        self.random()
        print(self.__world, end='')
        self.__generation = 0
        print()
        print(f'Your world size is now {rows} by {columns}.')
        print()
        print(self.status() + '\n' + self.menu(), end=' ')

    def save(self, filename, myPath='./'):
        """
        Save the current generation of the current world as a text file.
        :param filename: name of the file, may be None at this point.
        :param myPath: Where the file should be saved.
        :return: None
        """
        replace = False
        Cell.set_display('basic')
        if filename == None:
            filename = toolbox.get_string('What do you want to call the file? ')

        #
        # Make sure the file has the correct file extension.
        #
        if filename[-5:] != '.life':
            filename = filename + '.life'
        allFiles = os.listdir(myPath)

        if filename in allFiles:
            replace = toolbox.get_boolean('There is already a file with this name. Would like to replace it?')

        if replace == True:

            #
            # if the path doesn't already exist, create it.
            #
            if not os.path.isdir(myPath):
                os.mkdir(myPath)

            #
            # Add on the correct path for saving files if the user didn't
            # include it in the filename.
            #
            if filename[0:len(myPath)] != myPath:
                filename = myPath + filename
            self.__world.save(filename)
            print()
            print('You now saved this world.')
            print()
        else:
            print("Okay I won't save it.")
            print(self.__world, end='')
        print()
        print(self.status() + '\n' + self.menu(), end=' ')

    def get_percentage(self):
        """
        gets a number as a percent from the user
        :return: the percentage inputted
        """
        self.__percentage = toolbox.get_integer_between(1, 100, "What percent of cells do you want alive? (just enter integer) ")
        return self.__percentage


    def open(self, filename, myPath='./'):
        """
        open a text file and use it to populate a new world.
        :param filename: name of the file, may be None at this point.
        :param myPath: Where the file is located.
        :return: None
        """
        Cell.set_display('basic')
        if filename == None:
            filename = toolbox.get_string('Which file do you want to open?')
        #
        # Check for and add the correct file extension.
        #
        if filename[-5:] != '.life':
            filename = filename + '.life'
        allFiles = os.listdir(myPath)
        if filename not in allFiles:
            print('404: File not found...')
            for filenames in allFiles:
                print(filenames)
            print('Try one of these next time.')
            print()
        else:
            #
            # Add on the correct path for saving files if the user didn't
            # include it in the filename.
            #
            if filename[0:len(myPath)] != myPath:
                filename = myPath + filename
            self.__world = World.from_file(filename)
            print(self.__world, end='')
            print()
            print(f'You now opened {filename} world.')
            print()
        print(self.status() + '\n' + self.menu(), end=' ')

    def set_geometry(self):
        userGeo = toolbox.get_integer_between(1, 2, """
        Choose 1 or 2:
        1. Basic Geometry 
        2. Donut Geometry""")
        self.__world.set_geometry(userGeo)
        print(self.__world, end='')
        print(self.status() + '\n' + self.menu(), end=' ')

    def from_library(self, filename, myPath= './'):
        Cell.set_display('basic')
        files = []
        number = 1
        print('**************************************')
        for file in os.listdir(myPath):
            print(f'{number}: {file}')
            files.append(file)
            number += 1
        print('**************************************')
        prompt = 'Which file would you like to open? '
        fileNumber = toolbox.get_integer_between(1, number - 1, prompt)
        filename = files[fileNumber - 1]
        print(filename)
        #
        # Check for and add the correct file extension.
        #
        if filename[-5:] != '.life':
            filename = filename + '.life'
        allFiles = os.listdir(myPath)
        if filename not in allFiles:
            print('404: File not found...')
            for filenames in allFiles:
                print(filenames)
            print('Try one of these next time.')
            print()
        else:
            #
            # Add on the correct path for saving files if the user didn't
            # include it in the filename.
            #
            if filename[0:len(myPath)] != myPath:
                filename = myPath + filename
            self.__world = World.from_file(filename)
            print(self.__world, end='')
            print()
            print(f'You now opened {filename} world.')
            print()
        print(self.status() + '\n' + self.menu(), end=' ')

    def get_alive(self):
        """
        calculates the number of cells alive in the current world
        :return: returns the number of alive cells
        """
        alive = 0
        for row in self.__world.get_grid():
            for cell in row:
                if cell.get_living():
                    alive += 1
        return alive

    def get_total(self):
        """
        calculates the total number of cells in the world
        :return: the total number of cells in the world
        """
        return (self.__world.get_rows())*(self.__world.get_columns())

    def find_percentage(self):
        """
        gets the number of living cells and dead cells and divides them then times by 100
        :return: percentage of Living cells
        """
        return round((self.get_alive()/self.get_total())*(100))

    def change_rule(self, parameter):
        """
        Change the number of neighbors a cell needs to live or die.
        :param parameter:
        :return: None
        """
        if toolbox.is_integer(parameter) and \
                1 <= int(parameter) <= len(Rule.ruleSets.keys()):
            setNumber = int(parameter)
        else:
            print('**************************************')
            for number, set in enumerate(Rule.ruleSets):
                neighbor1 = Rule.ruleSets[set]['neighbor1']
                neighbor2 = Rule.ruleSets[set]['neighbor2']
                neighbor3 = Rule.ruleSets[set]['neighbor3']
                print(f'{number + 1}: neighbor1: {neighbor1} neighbor2: {neighbor2} neighbor3: {neighbor3}')
            print('**************************************')
            prompt = 'What rule set would you like to use?'
            setNumber = toolbox.get_integer_between(1, number + 1, prompt)
        setString = list(Rule.ruleSets.keys())[setNumber - 1]
        Rule.set_rule(setString)
        print(self.__world, end='')
        print()
        print(f'Your rule set is now neighbor1:{neighbor1}, neighbor2:{neighbor2}, neighbor3:{neighbor3}.')
        print()
        print(self.status() + '\n' + self.menu(), end = ' ')





if __name__ =='__main__':
    simulation = Life()
    simulation.main()
