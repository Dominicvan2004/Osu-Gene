import os
from random import randint
from dotenv import load_dotenv
from Osu_gene.user import user_fitness
from math import ceil
import asyncio as a

from Osu_gene.classes import( 
    Genome,
    beatmap_dna            
  )

from osu import (
    Client,
    Beatmapset,
    AsynchronousClient as Aclient,
    BeatmapsetSearchFilter as Filter,
    BeatmapsetSearchStatus as Status,
    BeatmapsetLanguage as Language,
    BeatmapsetGenre as Genre,
    GameModeInt as Mode,
    GameModeStr as ModeStr,
    BeatmapsetSearchSort as Sort
)

load_dotenv()


client_id = int(os.getenv('CLIENT_ID'))
client_secret = os.getenv('CLIENT_SECRET')
redirect_url = os.getenv('REDIRECT_URL')

client = Client.from_credentials(client_id, client_secret, redirect_url, request_wait_time = 00.1)
aclient = Aclient.from_credentials(client_id, client_secret, redirect_url, request_wait_time = 00.1)
client = Client.from_credentials(client_id, client_secret, redirect_url, request_wait_time = 0.1)
aclient = Aclient.from_credentials(client_id, client_secret, redirect_url, request_wait_time = 0.1)

async def osu_gene(id: int):

    #retrieving the beatmaps within the given parameters 
    user_fitness_base: list = await user_fitness(id)
    print(user_fitness_base)

    #a list to hold all of the beatmaps 
    beatmapset_list: list[Beatmapset]= []
    

    song_page = 1
    song = client.search_beatmapsets(
    Filter()
    .set_language(Language.ENGLISH)
    .set_genre(Genre.METAL)
    .set_status(Status.RANKED)
    .set_mode(Mode.STANDARD),
    page = song_page
    )   

    beatmapset_list.extend(song.beatmapsets)
    song_page = 1

    while len(song.beatmapsets) > 0 and  song_page < 10:
        song = client.search_beatmapsets(
        Filter()
        .set_language(Language.ENGLISH)
        .set_genre(Genre.METAL)
        .set_status(Status.RANKED)
        .set_mode(Mode.STANDARD),
        page = song_page
        )

        beatmapset_list.extend(song.beatmapsets)
        song_page += randint(1,3)

    
    print(len(beatmapset_list))
    beatmap_list: list[beatmap_dna] = [] # a list thats serves a container for beatmaps so we can randomly populate our genomes 
    genome_list: list[Genome] = [] # this serves as a contianer to hold all of our random genomes 
    pop_size: int = 4000 # pop_size will control how many genomes there are in our initial generatiion 
    generations: int = 3000 # how many time the crossove funtion will run
    pop_size: int = 200 # pop_size will control how many genomes there are in our initial generatiion 
    generations: int = 1000 # how many time the crossove funtion will run
    dna_size: int = 10 # size of the dna list in each genome 
    bm_list: list = [] #serves as the task list for all the get beatmap co routines 
    bma_list: list = [] #serves as the task list for all the get beatmap attribute co routines 
    selection_pressure: int = 10 #the population size of parents for a tournament selection in the grab parent method 
    test_list: list = []

    # create a list of beatmap objects
    
    for beatmapset in beatmapset_list: 
        for map in beatmapset.beatmaps: #for each beatmapset we go through each beatmap
            if(map.mode == ModeStr.STANDARD): #if the beatmap is of mode standard 
                # bm_list.append(aclient.get_beatmap(map.id))
                # bma_list.append(aclient.get_beatmap_attributes(map.id))
                test_list.extend([aclient.get_beatmap(map.id),aclient.get_beatmap_attributes(map.id)])
    print("tasks gathered")
    
    print(len(bm_list), len(bma_list))
    # bm_result: list = await a.gather(*bm_list) 
    # bma_result: list = await a.gather(*bma_list)
    test_list = await a.gather(*test_list)

    # for bm, bma in zip(bm_result, bma_result):
    #     beatmap_list.append(beatmap_dna(user_fitness_base, bm, bma))
    for i in range(0,len(test_list),2):
        beatmap_list.append(beatmap_dna(user_fitness_base, test_list[i], test_list[i+1]))

    #creates a list of 10 random beatmaps to use as a parameter for the genome class
    def random_genome() -> list[beatmap_dna]:
        rand_list: list[beatmap_dna] = []
        
        for i in range(dna_size):
           
            ran = randint(0,(len(beatmap_list)-1))
            rand_list.append(beatmap_list[ran])
                

        return(rand_list)
    print(beatmap_list)
    #populate our genome list with pop_size amount of genomes 
    for i in range(pop_size):
        
        genome_list.append(Genome(random_genome()))


    def grab_parent():
        """
        Tounrament selection for the genetic algorithm

        chooses the fitess genome from a predetermined amount of random genomes
        """

        pop:list[Genome] = []

        for i in range(selection_pressure):

            ran = randint(0,pop_size)
            pop.append(genome_list[ran])

        pop.sort(key=lambda p: p.genome_fitness)
        
        return(pop[0])
        

    def cross_over():
        
        #cross over function , this will populate our new generation of solutions 
        #getting the two parents 
        parent1:Genome = grab_parent()
        parent2:Genome = grab_parent()

        # check if their the same 
        #if inbreeding occurs the corssover is ignore and the parent is passed into the next generation
        if(parent1 == parent2): 
            return
        
        #combine two lists from both parents 
        new_list: list[beatmap_dna]  = list(set((parent1.dna_list+parent2.dna_list)))
        new_list.sort(key=lambda p: p.fitness_score)

        for i in new_list:

            print(i.fitness_score)

        #make a copy of the new dna lists 
        for i in new_list[:ceil(len(new_list)/2)]:

            print(i.fitness_score)
        
        child: Genome = Genome(new_list[:ceil(len(new_list)/2)])

        #append the new child
        genome_list.append(child)  

    #running the corssover function for a given amount of generations 
    for i in range(generations):
        
        cross_over()
    
    #sorting via lambda 
    genome_list.sort(key=lambda p: p.genome_fitness)

    #returning the list of fitess genome
    return genome_list[0].print_beatmap_list()


