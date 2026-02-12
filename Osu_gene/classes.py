from osu import(
    Client,
    Beatmap,
    BeatmapDifficultyAttributes,
    AsynchronousClient as Aclient,
    UserScoreType as ScoreType,
    GameModeInt as Mode,
    GameModeStr as Modestr,
    BeatmapsetCompact
)
import os
import asyncio as a
from dotenv import load_dotenv
from typing import List
from numpy import var, std
load_dotenv()

client_id = int(os.getenv('CLIENT_ID'))
client_secret = os.getenv('CLIENT_SECRET')
redirect_url = os.getenv('REDIRECT_URL')

client = Client.from_credentials(client_id, client_secret, redirect_url, request_wait_time = 0.1)
aclient = Aclient.from_credentials(client_id, client_secret, redirect_url, request_wait_time = 0.1)


class beatmap_dna:
    """
    A representation of a beatmap
    Includes a fitness score and id 
    """ 

    def __init__(self, user_fitness: dict, bm: Beatmap, bma: BeatmapDifficultyAttributes):
        self.user_fitenss_dict: dict = user_fitness
        self.id: int = bm.id
        self.fitness_score: float
        self.bm = bm
        self.bma = bma
        self.url = bm.url
        self.get_map_fitness()
        

    def get_map_fitness(self): #this function should be called on the instaciation of each new beatmap
        """
        Retunrs a Coroutine to assign the mean average of the deviation 
        from the given user fitness list to the instances fitness score variable 
        """
        avg_deviation:float = 0
       
        print("this is map fitness")
        avg_deviation += 2*abs(self.bm.bpm - self.user_fitenss_dict["bpm"])
        avg_deviation += abs(self.bma.mode_attributes.aim_difficulty - self.user_fitenss_dict["aim"])
        avg_deviation += abs(self.bm.last_updated.year - self.user_fitenss_dict["ranked_year"])
        avg_deviation += 10*abs(self.bma.star_rating - self.user_fitenss_dict["sr"])
        avg_deviation += abs(self.bma.mode_attributes.slider_factor - self.user_fitenss_dict["slider"])

        self.fitness_score = avg_deviation
        
class Genome:
    
    def __init__(self, ten_maps:list[beatmap_dna]):
        self.dna_list: list[beatmap_dna] = ten_maps
        self.genome_fitness: float = self.get_genome_fitness() 

    def print_beatmap_list(self) -> list:
        """
        Prints the beatmaps in the dna list
        """
        result: list = []

        for map in self.dna_list:
            result.append(f"<div class=\"container\"><a href=\"{map.url}\"><p>{client.get_beatmap(map.id).beatmapset.title}</p></a></div>")
        
        return result

    def get_genome_fitness(self) -> float:
        """
        Returns the sum of the beatmap fitness scores within the dna list
        """
        fitness_list: list[float] = []
        fitness_count: float = 0
        for beatmap in self.dna_list:
            fitness_count += beatmap.fitness_score
            fitness_list.append(beatmap.fitness_score*2)
        return((fitness_count/len(self.dna_list)) + 2*(std(fitness_list)))


