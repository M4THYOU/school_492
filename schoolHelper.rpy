##Helper file for all the code related to school application calculations is declared and defined.

init python:
    # using Harvard stats to approximate.
    # gets a weight.
    # < 1 => harms chances.
    # = 1 => no bias.
    # > 1 => helps chances.

    def compute_school_acceptance_bias(player: LifePlayer):
        # no data for non-binary. group with woman.
        # https://news.harvard.edu/gazette/story/2021/04/harvard-college-accepts-1968-to-class-of-2025/ -> 52.9% of class is women. 47.1 men.
        # by race: https://college.harvard.edu/admissions/admissions-statistics
        if player.race == Race.White and player.gender == Gender.Man:
            # 38.2% of white men go to college.
            # 40.6% of harvard acceptance is white.
            # 47.1% of that is 19.1%
            # portion: 34.7%
            return 19.1 / 24.7
        elif player.race == Race.White and (player.gender == Gender.Woman or
                                        player.gender == Gender.Nonbinary):
            # 39.5% of white women go to college.
            # 40.6% of harvard acceptance is white.
            # 52.9% of that is 21.5%
            # portion: 37.1%
            return 21.5 / 27.1
        elif player.race == Race.Black and player.gender == Gender.Man:
            # 21.6% of black men go to college.
            # 15.2% of harvard acceptance is black.
            # 47.1% of that is 7.6%
            # portion: 3.5%
            return 7.6 / 3.5
        elif player.race == Race.Black and (player.gender == Gender.Woman or
                                        player.gender == Gender.Nonbinary):
            # 27.7% of black women go to college.
            # 15.2% of harvard acceptance is black.
            # 52.9% of that is 8.0%
            # portion: 5.1%
            return 8.0 / 5.1
        elif player.race == Race.Asian and player.gender == Gender.Man:
            # 58.2% of asian men go to college.
            # 27.9% of harvard acceptance is asian.
            # 47.1% of that is 13.1%
            # portion: 4.9%
            return 13.1 / 4.9
        elif player.race == Race.Asian and (player.gender == Gender.Woman or
                                        player.gender == Gender.Nonbinary):
            # 54.9% of asian women go to college.
            # 27.9% of harvard acceptance is asian.
            # 52.9% of that is 14.8%
            # portion: 5.3%
            return 14.8 / 5.3
        elif player.race == Race.Hispanic and player.gender == Gender.Man:
            # 17.8% of hispanic men go to college.
            # 12.6% of harvard acceptance is hispanic.
            # 47.1% of that is 5.9%
            # portion: 4.3%
            return 5.9 / 4.3
        elif player.race == Race.Hispanic and (player.gender == Gender.Woman or
                                            player.gender == Gender.Nonbinary):
            # 21.8% of hispanic women go to college.
            # 12.6% of harvard acceptance is hispanic.
            # 52.9% of that is 6.7%
            # portion: 5.1%
            return 6.7 / 5.1
    
    def is_ivey_accept(player: LifePlayer):
        # actual is 0.03 but that's not very good for a game.
        # so scale by 3 factor.
        harvard_acceptance = 0.1
        p = min(1, compute_school_acceptance_bias(player) * harvard_acceptance)
    
        if IS_DEBUG:
            print('\t Harvard:', p)
        return player.biased_flip(p)


    def is_state_accept(player: LifePlayer):
        # assume the same bias as harvard.
        acceptance = 0.6  # seems about right, based on google searches.
        p = min(1, compute_school_acceptance_bias(player) * acceptance)

        if IS_DEBUG:
            print('\t State:', p)
        return player.biased_flip(p)

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
    def school_apply(player, school_opts):
        res = []
        for opt in school_opts:
            if opt == SchoolOptions.Ivey and is_ivey_accept(player):
                res.append(opt)
            elif opt == SchoolOptions.State and is_state_accept(player):
                res.append(opt)
            elif opt == SchoolOptions.Community:
                # there exist community colleges with 100% acceptance.
                res.append(opt)
        return res

    def school_select(player, school):
        player.school = school    