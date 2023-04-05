##Helper file for all the code related to job application calculations is declared and defined.

init python:
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
    def _compute_faang_acceptance_prob(player):
        if player.race == Race.White and player.gender == Gender.Man:
            return 0.254
        elif player.race == Race.White and (player.gender == Gender.Woman or
                                        player.gender == Gender.Nonbinary):
            return 0.148
        elif player.race == Race.Black and player.gender == Gender.Man:
            return 0.05
        elif player.race == Race.Black and (player.gender == Gender.Woman or
                                        player.gender == Gender.Nonbinary):
            return 0.043
        elif player.race == Race.Asian and player.gender == Gender.Man:
            return 0.289
        elif player.race == Race.Asian and (player.gender == Gender.Woman or
                                        player.gender == Gender.Nonbinary):
            return 0.174
        elif player.race == Race.Hispanic and player.gender == Gender.Man:
            return 0.058
        elif player.race == Race.Hispanic and (player.gender == Gender.Woman or
                                            player.gender == Gender.Nonbinary):
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
    def _compute_other_acceptance_prob(player):
        if player.race == Race.White and player.gender == Gender.Man:
            return 0.232
        elif player.race == Race.White and (player.gender == Gender.Woman or
                                        player.gender == Gender.Nonbinary):
            return 0.171
        elif player.race == Race.Black and player.gender == Gender.Man:
            return 0.054
        elif player.race == Race.Black and (player.gender == Gender.Woman or
                                        player.gender == Gender.Nonbinary):
            return 0.04
        elif player.race == Race.Asian and player.gender == Gender.Man:
            return 0.207
        elif player.race == Race.Asian and (player.gender == Gender.Woman or
                                        player.gender == Gender.Nonbinary):
            return 0.153
        elif player.race == Race.Hispanic and player.gender == Gender.Man:
            return 0.057
        elif player.race == Race.Hispanic and (player.gender == Gender.Woman or
                                            player.gender == Gender.Nonbinary):
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
    def school_job_bonus(player):
        job_count = player.job_hops + player.promotions
        bonus_factor = 0.5
        if job_count > 0:
            bonus_factor = bonus_factor ** job_count
        
        bonus = 0.0
        if player.school == SchoolOptions.Ivey:
            bonus = 0.64
        elif player.school == SchoolOptions.State:
            bonus = 0.36

        return bonus * bonus_factor


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
    def compute_promo_prob(player):
        if player.race == Race.White and player.gender == Gender.Man:
            return 0.608
        elif player.race == Race.White and (player.gender == Gender.Woman or
                                        player.gender == Gender.Nonbinary):
            return 0.157
        elif player.race == Race.Black and player.gender == Gender.Man:
            return 0.033
        elif player.race == Race.Black and (player.gender == Gender.Woman or
                                        player.gender == Gender.Nonbinary):
            return 0.008
        elif player.race == Race.Asian and player.gender == Gender.Man:
            return 0.103
        elif player.race == Race.Asian and (player.gender == Gender.Woman or
                                        player.gender == Gender.Nonbinary):
            return 0.027
        elif player.race == Race.Hispanic and player.gender == Gender.Man:
            return 0.039
        elif player.race == Race.Hispanic and (player.gender == Gender.Woman or
                                            player.gender == Gender.Nonbinary):
            return 0.01

    # just returns the 'best' option.
    # now we consider school, race, gender.
    def intern_apply(player, job_opts):
        res = []
        for job in job_opts:
            p = 0.0
            if job == JobOptions.FAANG:
                p = player._compute_faang_acceptance_prob() + school_job_bonus(player)
            elif job == JobOptions.Startup:
                p = player._compute_other_acceptance_prob() + school_job_bonus(player)
            elif job == JobOptions.Local_IT_Company:
                p = player._compute_other_acceptance_prob() + school_job_bonus(player)
            elif job == JobOptions.McDonalds:
                p = 1

            if IS_DEBUG:
                print('\t', job, p)

            if player.biased_flip(p):
                res.append(job)

        if IS_DEBUG:
            print('\t', res)
        return res

    def select_job(player, job):
        player.jobs.append(job)


    def job_apply(player, job_opts):
        # tier the jobs.
        # only return a job > the cur job.

        # for earlier iterations, weight the school and internship more heavily.

        res = []
        for job in job_opts:
            p = 0.0
            if job == JobOptions.FAANG:
                p = player._compute_faang_acceptance_prob() + school_job_bonus(player)
            elif job == JobOptions.Startup:
                p = player._compute_other_acceptance_prob() + school_job_bonus(player)
            elif job == JobOptions.Local_IT_Company:
                p = player._compute_other_acceptance_prob() + school_job_bonus(player)
            elif job == JobOptions.McDonalds:
                p = 1

            if IS_DEBUG:
                print('\t', job, p)

            if player.biased_flip(p):
                res.append(job)

        if IS_DEBUG:
            print('\t', res)
        if res:
            new_job = max(res)
            if player.jobs[-1] <= new_job:
                player.job_hops += 1
                player.jobs.append(max(res))
        return player.jobs[-1]


    # return true if promoted, else false.
    def job_promotion(player):
        p = compute_promo_prob(player)
        res = player.biased_flip(p)
        if res:
            player.promotions += 1
        return res
    
    def summary(player):
        job_count = player.promotions + player.job_hops
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
            'promotions': player.promotions,
            'job_hops': player.job_hops,
        }