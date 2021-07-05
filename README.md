# Dungeons and Dragons

This is a project that I started some time ago that I recently put some more time into to get some kind of project out. Generally, speaking, I see three parts to this project, the first focusing on the monsters of Dungeons and Dragons, the second focusing on the players, and the third (and most ambitious) being to develop and AI that learns to play dungeons and dragons (at least the combat portions) so that we can identify optimal strategize, ability choices, and so on. Will I make it that far? Well, probably not for at least a few years, but that's the dream I hope to acheive some day. For now, I have just been focusing on cataloging all of the monsters. 

## Monsters

### Data Scrape
Data for the monsters of Dungeons and Dragons was scraped off the Roll20 website after purchasing digital copies of the books (SRD, Monster Manual, Volo's, and Mordenkainen's Tomes) off that website. I used selenium to open each of the monster's entries and download the page as a text file. It has been brought to my attention that not every entry on Roll20 is 100% accurate, but without manual comparing each entry to my physical copy of the book, this is the best I have to work with. The errors generally seem fairly small in general, and if you find any I'm happy to correct them. 

### Data Cleaning
Once I collected the page for each monster, I wrote a loop to search through each file and extract the features of interest. This included everything from basic demographic details (e.g. the name of the monster, their size, race, statistics, et cetera) to their attacks, abilities, immunities, and everything else useful you might want to know about a monster. This data was then uploaded to SQL for later use; you can find the final results of this analysis in the attached database. 

### Monster Dashboard
<<<<<<< HEAD
The monster dashboard provides visualizations of the most important aspects of the collected data. Most of the graphics are fairly self explanatory, so I do not want to belabor them too much. However, it is worth noting how the attack data is structured. In D&D every monster can (and most do) have multiple attacks, and for each of these attacks they can (and often do) inflict multiple sources of damage. A common example might be a bite from a poisonous creature, which would do piercing damage and poison damage. As such, it is somewhat challenging to assess how much damage a particular monster/attack is expected to do. They might have multiple hits involving multiple rolls and multiple damage sources. Therefore, at the present I just focus on "Damage per Hit," ignoring the fact that one monster might be able to hit 3+ times a round, and focus on the "primary" damage source (i.e. the first one listed). So, for example, if they have a poisonous bite, they would have an attack roll for the bite, bite damage, then a saving throw for the poison (conditional on the fact that they were bitten), and poison damage. We are ignoring the secondary damage source (poison) and just recording the primary (bite) damage at this time. Encapsulating the full picture is certainly possible, and an upgrade to come to the project in the future, but it will take a bit more time and a bit more data wrangling.
=======
The monster dashboard provides visualizations of the most important aspects of the collected data. Most of the graphics are fairly self explanatory, so I do not want to belabor them too much. However, it is worth noting how the attack data is structured. In D&D every monster can (and most do) have multiple attacks, and for each of these attacks they can (and often do) inflict multiple sources of damage. A common example might be a bite from a poisonous creature, which would do piercing damage and poison damage. As such, it is somewhat challenging to assess how much damage a particular monster/attack is expected to do. They might have multiple hits involving multiple rolls and multiple damage sources. Therefore, at the present I just focus on "Damage per Hit," ignoring the fact that one monster might be able to hit 3+ times a round, and focus on the "primary" damage source (i.e. the first one listed). So, for example, if they have a poisonous bite, they would have an attack roll for the bite, bite damage, then a saving throw for the poison (conditional on the fact that they were bitten), and poison damage. We are ignoring the secondary damage source (poison) and just recording the primary (bite) damage at this time. Encapsulating the full picture is certainly possible, and an upgrade to come to the project in the future, but it will take a bit more time and a bit more data wrangling. 
>>>>>>> c3ba50651ae962bd77cab733eff5e7c8b805e848