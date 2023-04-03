from life_player import LifePlayer, Race, Gender, SchoolOptions, JobOptions


def main():
    p = LifePlayer()
    print(p.race.name, p.gender.name, p.household_income)

    # apply to schools.
    accepted = p.school_apply([SchoolOptions.Ivey, SchoolOptions.State, SchoolOptions.Community])
    
    # pick which to attend, if accepted.
    p.school_select(accepted[0])
    print('Going to', p.school.name)

    # apply to summer internships.
    job = p.intern_apply([JobOptions.FAANG, JobOptions.Startup, JobOptions.Local_IT_Company, JobOptions.McDonalds])
    print('Interning at', job.name)

    # apply for new grad job.
    job = p.job_apply([JobOptions.FAANG, JobOptions.Startup, JobOptions.Local_IT_Company])
    print('First job at', job.name)

    # LOOP 5 times:
        # pick promotion or job hop
        # did we succeed at the choice?
    for i in range(0, 5):
        if i % 2 == 0:
            did_get = p.job_promotion()
            print('Went for promotion, did you get it?', did_get)
        else:
            old_job = p.jobs[-1]
            new_job = p.job_apply([JobOptions.FAANG, JobOptions.Startup, JobOptions.Local_IT_Company])
            print('Switching jobs from', old_job.name, 'to', new_job.name)

    # all in all you've ended life with x promotions, y job hops, and salary of $zzz.
    print(p.summary())


if __name__ == '__main__':
    main()

