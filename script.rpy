# The script of the game goes in this file.

# Declare characters used by this game. The color argument colorizes the
# name of the character.

define pov = Character("[povname]")
define n = Character("")

# The game starts here.

label start:

    scene bg room

    "Welcome to the Game of Life! Oftentimes in life we may underestimate how much our circumstances, race, sex and other factors that are completely out of our control can affect the path of our life." 

    "This game will take you through the multiple stages of becoming a software engineer all the way from high school to being promoted in your job and show you how these factors can have a significant impact on your career!"

    "You will be assigned a Race, Gender, and Household Income. Then you shall maneuver through life by making decisions each step along the way that will influence your education and career. Good luck!"

    $ povname = renpy.input("To start the game, please enter your name: ", length=32)
    $ user.name = povname
    #show scene 
    "Welcome [user.name]!"

    jump uni_apply

label uni_apply:

    scene bg room
    
    python:
        gender = user.getGender()
        race = user.getRace()

    "For this simulation you have been assigned the following attributes \n Income: [user.household_income] \n Race: [race] \n Gender: [gender]"
    "Keep these attributes in mind when making your choices!"

    "The first step of becoming a software engineer after high school, will be obtaining your degree. Go through each of the university options given
    , read the description and choose which ones you would like to apply. Remmember it is always reccomended to apply to more than one university!"
    
    menu:
        "Would you Like to Apply to an Ivy League University? Ivey League universities are .... (highly selective)"
        "Yes":
            $ ivey_apply = True
        
        "No":
            $ ivey_apply = False

    menu: 
        "Would you Like to Apply to an Local State University? State universities are .... (medium selective)"
        "Yes":
            $ stateUni_apply = True
        
        "No":
            $ stateUni_apply = False
    
    menu: 
        "Would you Like to Apply to a Community College? Community colleges are .... (not selective)"
        "Yes":
            $ community_apply = True
        
        "No":
            $ community_apply = False
        #if no acceptance then force to go to community college
    jump after_uni_apply
    
label after_uni_apply:
    
    python:
        school_opts = []
        if(ivey_apply):
            school_opts.append(SchoolOptions.Ivey)
        if(stateUni_apply):
            school_opts.append(SchoolOptions.State)
        if(community_apply):
            school_opts.append(SchoolOptions.Community)
        
        accepted = school_apply(user, school_opts)
        ivey_acept = SchoolOptions.Ivey in accepted
        community_acept = SchoolOptions.Community in accepted
        state_accept = SchoolOptions.State in accepted
        no_accept = SchoolOptions.No_School in accepted

        if no_accept:
            n("Unfortunately you were accepted to no universities")
            renpy.jump(no_uni)
        if ivey_acept:
            n("Congratulations! You were accepted into an Ivey League University")
        else:
            n("Unfortunately you were not accepted into an Ivey League University")
        if state_accept:
            n("Congratulations! You were accepted into a Local State University")
        else:
            n("Unfortunately you were not accepted into a Local State University")
        if community_acept:
            n("Congratulations! You were accepted into a Community College")
        else:
            n("Unfortunately you were not accepted into a Community College")

    menu:
        "Which school would you like to select to attend?"

        "Ivey League (Cost 50,000 per year)" if ivey_acept:
            #if this option is chosen, check if household income is more than 75,000. If yes then okay,
            #otherwise send to financial aid section
            $ school_select(user, SchoolOptions.Ivey)
        
        "Local State University (Cost 30,000 per year)" if state_accept:
            $ school_select(user, SchoolOptions.State)

        "Community College (Cost 10,000 per year)" if community_acept:
            $ school_select(user, SchoolOptions.Community)
    
    "Congratulation [user] you are going to [user.school]!"

    jump during_uni

label financial_aid:
    return

label during_uni:
    

    # show 3 years later screen

    "Wow time really flew by looks like you are in your last year of university and its time to get an internship to add some
    work experience to your resume! A strong internship can do wonders for a fulltime career so go through the options and apply carefully!"

    menu:
        "Would you Like to Apply to a FAANG SWE internship? FAANG jobs have competitve pay, and require high skill"
        "Yes":
            $ faang_apply = True
        
        "No":
            $ faang_apply = False
    
    menu: 
        "Would you Like to Apply to a Local IT Company? Local IT companies require medium skill"
        "Yes":
            $ local_apply = True
        
        "No":
            $ local_apply = False

    menu: 
        "Would you Like to Apply to a Tech Startup? Tech Startups require medium-low skill"
        "Yes":
            $ startup_apply = True
        
        "No":
            $ startup_apply = False
    
    menu: 
        "Would you Like to Apply to a Minimum wage job? Minimum wage jobs typically require little-no prior skill knowledge"
        "Yes":
            $ minimum_apply = True
        
        "No":
            $ minimum_apply = False
    
        
    jump after_intern_apply
    
label after_intern_apply:
    
    python:
        intern_opts = []
        if(faang_apply):
            intern_opts.append(JobOptions.FAANG)
        if(local_apply):
            intern_opts.append(JobOptions.Local_IT_Company)
        if(startup_apply):
            intern_opts.append(JobOptions.Startup)
        if(minimum_apply):
            intern_opts.append(JobOptions.Minimum_Wage)

        accepted = intern_apply(user, intern_opts)
        faang_acept = JobOptions.FAANG in accepted
        local_acept = JobOptions.Local_IT_Company in accepted
        startup_accept = JobOptions.Startup in accepted
        minimum_accept =  JobOptions.Minimum_Wage in accepted

        if no_accept:
            n("Unfortunately you were accepted to no internships")
            renpy.jump(no_uni)
        if faang_acept:
            n("Congratulations! You were selected for a FAANG SWE Internship")
        else:
            n("Unfortunately you were not selected for a FAANG SWE Internship")
        if local_acept:
            n("Congratulations! You were selected for a Local IT Company")
        else:
            n("Unfortunately you were not selected for a Local IT Company")
        if startup_accept:
            n("Congratulations! You were selected to work for a Startup")
        else:
            n("Unfortunately you were not selected to work for a Startup")
        if minimum_accept:
            n("Congratulations! You were selected to work for a Minimum Wage Job")
        else:
            n("Unfortunately you were not selected to work for a Minimum Wage Job")

    menu:
        "Which internship would you like to select?"

        "FAANG SWE Internship (Pay: $8000 per month)" if faang_acept:
            $ select_job(user, JobOptions.FAANG)
        
        "Local IT Company Internship (Pay: $8000 per month)" if local_acept:
            $ select_job(user, JobOptions.Local_IT_Company)

        "Tech Startup (Pay: $8000 per month)" if startup_accept:
            $ select_job(user, JobOptions.Startup)

        "Minimum Wage job (Pay: $8000 per month)" if minimum_accept:
            $ select_job(user, JobOptions.Minimum_Wage)
    
    "Congratulations [user.name] you are going to work at [user.jobs[0]] for the summer!"

    jump after_uni

label after_uni:
    
    # show 3 years later screen

    "Congratulations on completing your university. It is now time to find a fulltime job! Read the options and apply!"

    menu:
        "Would you Like to Apply to a FAANG SWE full time role? FAANG jobs have competitve pay, and require high skill"
        "Yes":
            $ faang_apply = True
        
        "No":
            $ faang_apply = False
    
    menu: 
        "Would you Like to Apply to a Local IT Company full time SWE role? Local IT companies require medium skill"
        "Yes":
            $ local_apply = True
        
        "No":
            $ local_apply = False

    menu: 
        "Would you Like to Apply to a Tech Startup full time SWE role? Tech Startups require medium-low skill"
        "Yes":
            $ startup_apply = True
        
        "No":
            $ startup_apply = False
    
        
    jump after_job_apply
    
label after_job_apply:
    
    python:
        first_job_opts = []
        if(faang_apply):
            first_job_opts.append(JobOptions.FAANG)
        if(local_apply):
            first_job_opts.append(JobOptions.Local_IT_Company)
        if(startup_apply):
            first_job_opts.append(JobOptions.Startup)
        if(minimum_apply):
            first_job_opts.append(JobOptions.Minimum_Wage)

        accepted = job_apply(user, first_job_opts) #will return array of all possible accepted jobs
        faang_acept = JobOptions.FAANG in accepted
        local_acept = JobOptions.Local_IT_Company in accepted
        startup_accept = JobOptions.Tech_Startup in accepted

        if no_accept:
            #Decide what to do about full time rejection
            n("Unfortunately you were accepted to no jobs, try again!")
            renpy.jump(no_uni)
        if faang_acept:
            n("Congratulations! You were selected for a SWE Fulltime role at FAANG")
        if local_acept:
            n("Congratulations! You were selected for a SWE Fulltime role at Local IT Company")
        if startup_accept:
            n("Congratulations! You were selected to work for a SWE Fulltime role at a Startup")

    menu:
        "Which full time role would you like to select?"

        "FAANG SWE Internship (Pay: $150000 per year)" if faang_acept:
            $ select_job(user, JobOptions.FAANG)
        
        "Local IT Company Internship (Pay: $8000 per month)" if local_acept:
            $ select_job(user, JobOptions.Local_IT_Company)

        "Tech Startup (Pay: $8000 per month)" if startup_accept:
            $ select_job(user, JobOptions.Startup)

        "Minimum Wage job (Pay: $8000 per month)" if minimum_accept:
            $ select_job(user, JobOptions.Minimum_Wage)
    
    "Congratulation [user] you are going to work at [user.job] for your full time job!"

    jump after_uni

default job_loop = 0
default promotion_apply = False
default switch_jobs = False

label after_first_job:
    $ job_loop += 1
    
    "Congratulations on your completing Year [job_loop] of your fulltime career! You are working at current job. Since you have been working for [job_loop] years, you can make the decision of whether to change jobs or apply for a promotion!"

    menu:
        "What would you like to do?"

        "Apply for a promotion":
            $ promotion_apply = True
            jump promotion

        "Switch Jobs":
            $ switch_jobs = True
            jump job_switch
    
        
label promotion:

    python:
        did_get = p.job_promotion()
        
    'Did you get the promotion?'
    
    '[did_get]'

label job_switch:
            
        "Which job would you like to switch to?"

        menu:
            "FAANG SWE (Pay: $150000 per year)":
                $ select_job(user, JobOptions.FAANG)
            
            "Local IT Company (Pay: $8000 per month)":
                $ select_job(user, JobOptions.Local_IT_Company)

            "Tech Startup (Pay: $8000 per month)":
                $ select_job(user, JobOptions.Tech_Startup)
