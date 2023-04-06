from enum import Enum
from random import randint, random, gauss


IS_DEBUG = True

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
        v = 78000
        if race == Race.White:
            v = 78000
        elif race == Race.Black:
            v = 48000
        elif race == Race.Hispanic:
            v = 58000
        elif race == Race.Asian:
            v = 101000
        elif race == Race.All_Races:
            v = 78000
        else:
            raise ValueError('Invalid race')

        return max(v, int(gauss(v, 50000)))


class Gender(Enum):
    Man = 1
    Woman = 2
    Nonbinary = 3


class SchoolOptions(Enum):
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
        self.yoe = 0


    # p is probability the thing happens. 0 <= p <= 1.
    # return true if it happens, false otherwise.
    def biased_flip(self, p):
        return random() <= p


    # using Harvard stats to approximate.
    # gets a weight.
    # < 1 => harms chances.
    # = 1 => no bias.
    # > 1 => helps chances.
    def _compute_school_acceptance_bias(self):
        # no data for non-binary. group with woman.
        # https://news.harvard.edu/gazette/story/2021/04/harvard-college-accepts-1968-to-class-of-2025/ -> 52.9% of class is women. 47.1 men.
        # by race: https://college.harvard.edu/admissions/admissions-statistics
        if self.race == Race.White and self.gender == Gender.Man:
            # 38.2% of white men go to college.
            # 40.6% of harvard acceptance is white.
            # 47.1% of that is 19.1%
            # portion: 34.7%
            return 19.1 / 24.7
        elif self.race == Race.White and (self.gender == Gender.Woman or
                                          self.gender == Gender.Nonbinary):
            # 39.5% of white women go to college.
            # 40.6% of harvard acceptance is white.
            # 52.9% of that is 21.5%
            # portion: 37.1%
            return 21.5 / 27.1
        elif self.race == Race.Black and self.gender == Gender.Man:
            # 21.6% of black men go to college.
            # 15.2% of harvard acceptance is black.
            # 47.1% of that is 7.6%
            # portion: 3.5%
            return 7.6 / 3.5
        elif self.race == Race.Black and (self.gender == Gender.Woman or
                                          self.gender == Gender.Nonbinary):
            # 27.7% of black women go to college.
            # 15.2% of harvard acceptance is black.
            # 52.9% of that is 8.0%
            # portion: 5.1%
            return 8.0 / 5.1
        elif self.race == Race.Asian and self.gender == Gender.Man:
            # 58.2% of asian men go to college.
            # 27.9% of harvard acceptance is asian.
            # 47.1% of that is 13.1%
            # portion: 4.9%
            return 13.1 / 4.9
        elif self.race == Race.Asian and (self.gender == Gender.Woman or
                                          self.gender == Gender.Nonbinary):
            # 54.9% of asian women go to college.
            # 27.9% of harvard acceptance is asian.
            # 52.9% of that is 14.8%
            # portion: 5.3%
            return 14.8 / 5.3
        elif self.race == Race.Hispanic and self.gender == Gender.Man:
            # 17.8% of hispanic men go to college.
            # 12.6% of harvard acceptance is hispanic.
            # 47.1% of that is 5.9%
            # portion: 4.3%
            return 5.9 / 4.3
        elif self.race == Race.Hispanic and (self.gender == Gender.Woman or
                                             self.gender == Gender.Nonbinary):
            # 21.8% of hispanic women go to college.
            # 12.6% of harvard acceptance is hispanic.
            # 52.9% of that is 6.7%
            # portion: 5.1%
            return 6.7 / 5.1

    def _is_ivey_accept(self):
        # actual is 0.03 but that's not very good for a game.
        # so scale by 3 factor.
        harvard_acceptance = 0.1
        p = min(1, self._compute_school_acceptance_bias() * harvard_acceptance)
        
        if IS_DEBUG:
            print('\t Harvard:', p)
        return self.biased_flip(p)


    def _is_state_accept(self):
        # assume the same bias as harvard.
        acceptance = 0.6  # seems about right, based on google searches.
        p = min(1, self._compute_school_acceptance_bias() * acceptance)

        if IS_DEBUG:
            print('\t State:', p)
        return self.biased_flip(p)


    # use google's data
    # https://about.google/belonging/diversity-annual-report/2022/
    # 2022 hiring percentages:
    # white (male): 25.4%
    # white (female): 14.8%
    # black (male): 5.0%
    # black (female): 4.3%
    # asian (male): 28.9%
    # asian (female): 17.4%
    # hispanic (male): 5.8%
    # hispanic (female): 3.2%
    # again, no non-binary data. Will group that with women.
    # we will use these raw probabilities for our computations bc
    # while it is not the true probability of the group getting a job at Google,
    # it helps illustrate the implicit biases we would likely see in the hiring process
    # due to a lack of diversity in the current workforce.
    def _compute_faang_acceptance_prob(self):
        if self.race == Race.White and self.gender == Gender.Man:
            return 0.254
        elif self.race == Race.White and (self.gender == Gender.Woman or
                                          self.gender == Gender.Nonbinary):
            return 0.148
        elif self.race == Race.Black and self.gender == Gender.Man:
            return 0.05
        elif self.race == Race.Black and (self.gender == Gender.Woman or
                                          self.gender == Gender.Nonbinary):
            return 0.043
        elif self.race == Race.Asian and self.gender == Gender.Man:
            return 0.289
        elif self.race == Race.Asian and (self.gender == Gender.Woman or
                                          self.gender == Gender.Nonbinary):
            return 0.174
        elif self.race == Race.Hispanic and self.gender == Gender.Man:
            return 0.058
        elif self.race == Race.Hispanic and (self.gender == Gender.Woman or
                                             self.gender == Gender.Nonbinary):
            return 0.032


    # based on Uber's workforce data. It's not really a startup...
    # but it's closer in culture than a Google would be.
    # though, note that companies with shit diversity would never post their numbers.
    # so what we're seeing is really as good as it gets in terms of diversity...
    # white (male): 23.2%
    # white (female): 17.1%
    # black (male): 5.4%
    # black (female): 4.0%
    # asian (male): 20.7%
    # asian (female): 15.3%
    # hispanic (male): 5.7%
    # hispanic (female): 4.2%
    def _compute_other_acceptance_prob(self):
        if self.race == Race.White and self.gender == Gender.Man:
            return 0.232
        elif self.race == Race.White and (self.gender == Gender.Woman or
                                          self.gender == Gender.Nonbinary):
            return 0.171
        elif self.race == Race.Black and self.gender == Gender.Man:
            return 0.054
        elif self.race == Race.Black and (self.gender == Gender.Woman or
                                          self.gender == Gender.Nonbinary):
            return 0.04
        elif self.race == Race.Asian and self.gender == Gender.Man:
            return 0.207
        elif self.race == Race.Asian and (self.gender == Gender.Woman or
                                          self.gender == Gender.Nonbinary):
            return 0.153
        elif self.race == Race.Hispanic and self.gender == Gender.Man:
            return 0.057
        elif self.race == Race.Hispanic and (self.gender == Gender.Woman or
                                             self.gender == Gender.Nonbinary):
            return 0.042


    # a little bonus we add to prob of getting a job based on the school.
    # less impact the longer since graduating.
    # based on data pulled from LinkedIn:
    # https://www.linkedin.com/company/google/people/?facetSchool=166688%2C4695%2C1646%2C3173
    # in sample size of 3817 Google employees, we have
    # 1657 Harvard
    # 789 Princeton
    # 689 Michigan State
    # 682 Ohio State
    # so 64% ivey, 36% state
    def _school_job_bonus(self):
        job_count = self.job_hops + self.promotions
        bonus_factor = 0.5
        if job_count > 0:
            bonus_factor = bonus_factor ** job_count
        
        bonus = 0.0
        if self.school == SchoolOptions.Ivey:
            bonus = 0.64
        elif self.school == SchoolOptions.State:
            bonus = 0.36

        return bonus * bonus_factor
    

    # these computations are arbitrary.
    # just using it to show that as a person gets more YOE, it's easier to get a job.
    def _job_history_bonus(self):
        c = 0
        for n in self.jobs:
            c += n.value
        c += self.promotions * 2
        c += self.yoe

        if c <= 3:
            return 0
        elif c <= 6:
            return 0.1
        elif c <= 10:
            return 0.2
        elif c <= 15:
            return 0.4
        elif c <= 20:
            return 0.6
        elif c <= 28:
            return 0.8
        else:
            return 1



    # https://www.eeoc.gov/special-report/diversity-high-tech
    # tech jobs percent in management by race.
    # 20.5% women, 79.5% men.
    # white (male): 60.8%
    # white (female): 15.7%
    # black (male): 3.3%
    # black (female): 0.8%
    # asian (male): 10.3%
    # asian (female): 2.7%
    # hispanic (male): 3.9%
    # hispanic (female): 1.0%
    def _compute_promo_prob(self):
        if self.race == Race.White and self.gender == Gender.Man:
            return 0.608
        elif self.race == Race.White and (self.gender == Gender.Woman or
                                          self.gender == Gender.Nonbinary):
            return 0.157
        elif self.race == Race.Black and self.gender == Gender.Man:
            return 0.033
        elif self.race == Race.Black and (self.gender == Gender.Woman or
                                          self.gender == Gender.Nonbinary):
            return 0.008
        elif self.race == Race.Asian and self.gender == Gender.Man:
            return 0.103
        elif self.race == Race.Asian and (self.gender == Gender.Woman or
                                          self.gender == Gender.Nonbinary):
            return 0.027
        elif self.race == Race.Hispanic and self.gender == Gender.Man:
            return 0.039
        elif self.race == Race.Hispanic and (self.gender == Gender.Woman or
                                             self.gender == Gender.Nonbinary):
            return 0.01


    # takes array of SchoolOptions, return filtered array of SchoolOptions.
    # return empty array for not accepted anywhere.
    # https://www.bls.gov/opub/ted/2022/61-8-percent-of-recent-high-school-graduates-enrolled-in-college-in-october-2021.htm -> 61.8% of recent high school graduates go to college. 1.7 mil.
    # percentages of people with >= bachelors degree by race/gender:
    # from https://data.census.gov/table?g=010XX00US&tid=ACSST1Y2021.S1501&moe=false
    # white (male): 26622852/69619868 = 38.2%
    # white (female): 28564949/72347500 = 39.5%
    # black (male): 2649971/12280957 = 21.6%
    # black (female): 3904249/14082626 = 27.7%
    # asian (male): 3732604/6415436 = 58.2%
    # asian (female): 4035827/7355650 = 54.9%
    # hispanic (male): 3267785/18352480 = 17.8%
    # hispanic (female): 3947281/18246375 = 21.8%
    # but what portion of the total is each group?

    # total ppl count: 76725518
    # white (male): 26622852 -> 34.7%
    # white (female): 28564949 -> 37.1%
    # black (male): 2649971 -> 3.5%
    # black (female): 3904249 -> 5.1%
    # asian (male): 3732604 -> 4.9%
    # asian (female): 4035827 -> 5.3%
    # hispanic (male): 3267785 -> 4.3%
    # hispanic (female): 3947281 -> 5.1%
    def school_apply(self, school_opts):
        res = []
        for opt in school_opts:
            if opt == SchoolOptions.Ivey and self._is_ivey_accept():
                res.append(opt)
            elif opt == SchoolOptions.State and self._is_state_accept():
                res.append(opt)
            elif opt == SchoolOptions.Community:
                # there exist community colleges with 100% acceptance.
                res.append(opt)
        return res

    def school_select(self, school):
        self.school = school

    # just returns the 'best' option.
    # now we consider school, race, gender.
    def intern_apply(self, job_opts):
        self.yoe += 1
        res = []
        for job in job_opts:
            p = 0.0
            if job == JobOptions.FAANG:
                p = self._compute_faang_acceptance_prob() + self._school_job_bonus()
            elif job == JobOptions.Startup:
                p = self._compute_other_acceptance_prob() + self._school_job_bonus()
            elif job == JobOptions.Local_IT_Company:
                p = self._compute_other_acceptance_prob() + self._school_job_bonus()
            elif job == JobOptions.McDonalds:
                p = 1

            if IS_DEBUG:
                print('\t', job, p)

            if self.biased_flip(p):
                res.append(job)

        if IS_DEBUG:
            print('\t', res)
        self.jobs.append(max(res))
        return res


    def job_apply(self, job_opts):
        self.yoe += 1
        # tier the jobs.
        # only return a job > the cur job.

        # for earlier iterations, weight the school and internship more heavily.

        res = []
        for job in job_opts:
            p = 0.0
            if job == JobOptions.FAANG:
                p = self._compute_faang_acceptance_prob() + self._school_job_bonus()
            elif job == JobOptions.Startup:
                p = self._compute_other_acceptance_prob() + self._school_job_bonus()
            elif job == JobOptions.Local_IT_Company:
                p = self._compute_other_acceptance_prob() + self._school_job_bonus()
            elif job == JobOptions.McDonalds:
                p = 1

            if IS_DEBUG:
                print('\t', job, p)

            if self.biased_flip(p):
                res.append(job)

        if IS_DEBUG:
            print('\t', res)
        if res:
            self.jobs.append(max(res))
        return res


    # return true if promoted, else false.
    def job_promotion(self):
        self.yoe += 1
        p = self._compute_promo_prob()
        res = self.biased_flip(p)
        if res:
            self.promotions += 1
        return res

    
    def job_switch(self, job_opts):
        self.yoe += 1
        res = []
        for job in job_opts:
            p = 0.0
            if job == JobOptions.FAANG:
                p = self._compute_faang_acceptance_prob()
            elif job == JobOptions.Startup:
                p = self._compute_other_acceptance_prob()
            elif job == JobOptions.Local_IT_Company:
                p = self._compute_other_acceptance_prob()
            elif job == JobOptions.McDonalds:
                p = 1

            p_2 = self._job_history_bonus()
            if IS_DEBUG:
                print('\t', p_2)
            p = min(1, p+p_2)

            if IS_DEBUG:
                print('\t', job, p)

            if self.biased_flip(p):
                res.append(job)

        if IS_DEBUG:
            print('\t', res)
        if res:
            new_job = max(res)
            if self.jobs[-1] <= new_job:
                self.job_hops += 1
                self.jobs.append(max(res))
        return res


    # data comes from https://college.harvard.edu/financial-aid/net-price-calculator
    # Harvard's financial aid calculator. Filled in the fields using the median household income
    # values we found earlier.
    # so financial aid is indirectly dependent on race.
    def financial_aid(self):
        res = 0
        if self.race == Race.White:
            res = 41000
        elif self.race == Race.Black:
            res = 60000
        elif self.race == Race.Hispanic:
            res = 55000
        elif self.race == Race.Asian:
            res = 12000
        elif self.race == Race.All_Races:
            res = 41000
        else:
            raise ValueError('Invalid race')

        return res

    
    def summary(self):
        job_count = self.promotions + self.job_hops
        final_salary = SalaryBands.L3.value
        if job_count == 1:
            final_salary = SalaryBands.L4.value
        elif job_count == 2:
            final_salary = SalaryBands.L5.value
        elif job_count == 3:
            final_salary = SalaryBands.L6.value
        elif job_count == 4:
            final_salary = SalaryBands.L7.value
        elif job_count == 5:
            final_salary = SalaryBands.L8.value

        return {
            'final_salary': final_salary,
            'promotions': self.promotions,
            'job_hops': self.job_hops,
        }



