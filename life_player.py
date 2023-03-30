from enum import Enum
from random import randint

class Race(Enum):
    White = 1
    Black = 2
    Hispanic = 3
    Asian = 4
    All_Races = 5 # not an option for game.

    # https://www.census.gov/content/dam/Census/library/visualizations/2022/demo/p60-276/figure2.pdf
    # median household income by race.
    @classmethod
    def income(cls, race):
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


class SchoolOptions(Enum):
    Ivey = 1
    State = 2
    Community = 3


class JobOptions(Enum):
    FAANG = 1
    Startup = 2
    Local_IT_Company = 3
    McDonalds = 4


class LifePlayer:
    # randomly assign race, gender. Then household income.
    def __init__(self):
        self.race = Race(randint(1, 4))
        self.gender = Gender(randint(1, 3))
        self.household_income = Race.income(self.race)

        self.job_hops = 0
        self.promotions = 0
        self.jobs = []

    # takes array of SchoolOptions, return filtered array of SchoolOptions.
    # return empty array for not accepted anywhere.
    def school_apply(self, school_opts):
        return school_opts

    def school_select(self, school):
        self.school = school

    # just returns the 'best' option.
    def intern_apply(self, job_opts):
        i = randint(0, len(job_opts)-1)
        self.jobs.append(job_opts[i])
        return self.jobs[-1]

    def job_apply(self, job_opts):
        # tier the jobs.
        # only return a job > the cur job.

        # for earlier iterations, weight the school and internship more heavily.
        i = randint(0, len(job_opts)-1)
        
        self.job_hops += 1
        self.jobs.append(job_opts[i])
        return self.jobs[-1]

    # return true if promoted, else false.
    def job_promotion(self):
        v = randint(0, 1)
        if v == 1:
            self.promotions += 1
            return True
        return False

    def summary(self):
        return {
            'final_salary': 200000,
            'promotions': self.promotions,
            'job_hops': self.job_hops,
        }



