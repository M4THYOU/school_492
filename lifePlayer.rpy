init python:    
    class LifePlayer:
        # randomly assign race, gender. Then household income.
        def __init__(self):
            self.race = Race(randint(1, 4))
            self.gender = Gender(randint(1, 3))
            self.household_income = Race.income(self.race)
            self.school = SchoolOptions.No_School

            self.job_hops = 0
            self.promotions = 0
            self.jobs = []

        #getter methods

        def getRace(self):
            if self.race == 1:
                return "White"
            elif self.race == 2:
                return "Black"
            elif self.race == 3:
                return "Hispanic"
            else:
                return "Asian"
        
        def getGender(self):
            if self.gender == 1:
                return "Man"
            elif self.gender == 2:
                return "Woman"
            else:
                return "Non-binary"

        def getIncome(self):
            return self.household_income
        

        # p is probability the thing happens. 0 <= p <= 1.
        # return true if it happens, false otherwise.
        def biased_flip(self, p):
            return random() <= p
        
## This is how a LifePlayer Class is created.
default user = LifePlayer()
default IS_DEBUG = False
