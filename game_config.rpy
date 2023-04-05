init python: 
    from enum import Enum
    from random import randint, random

    class Race(Enum):
        White = 1
        Black = 2
        Hispanic = 3
        Asian = 4
        All_Races = 5 # not an option for game.

        # https://www.census.gov/content/dam/Census/library/visualizations/2022/demo/p60-276/figure2.pdf
        # median household income by race.
        def income(race):
            if race == Race.White:
                return 78000
            elif race == Race.Black:
                return 48000
            elif race == Race.Hispanic:
                return 58000
            elif race == Race.Asian:
                return 101000
            elif race == Race.All_Races:
                return 78000
            else:
                raise ValueError('Invalid race')


    class Gender(Enum):
        Man = 1
        Woman = 2
        Nonbinary = 3
    
    class GenderNames(Enum):
        Man = "Man"
        Woman = "Woman"
        Nonbinary = "Non Binary"


    class SchoolOptions(Enum):
        Ivey = 1
        State = 2
        Community = 3
        No_School = 4

    class SchoolNames (Enum):
        Ivey = 1
        State = 2
        Community = 3
        No_School = 4


    class JobOptions(Enum):
        FAANG = 4
        Startup = 3
        Local_IT_Company = 2
        McDonalds = 1

        def __lt__(self, other):
            return self.value < other.value
        
        def __le__(self, other):
            return self.value <= other.value


    # from levels.fyi
    class SalaryBands(Enum):
        L3 = 140000
        L4 = 170000
        L5 = 210000
        L6 = 240000
        L7 = 280000
        L8 = 330000