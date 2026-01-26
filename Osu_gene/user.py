
#TODO use the variance to determine to get rid of the unbalanced deviation between maps in the genomes.

import math ,os
import asyncio as a
from osu import (
    Client,
    AsynchronousClient as Aclient,
    UserScoreType as ScoreType,
    GameModeInt as Mode,
    Mods,
    LegacyScore,
    SoloScore,
    LazerMod,
    GameModeStr as Modestr
)
from dotenv import load_dotenv

load_dotenv()


client_id = int(os.getenv('CLIENT_ID'))
client_secret = os.getenv('CLIENT_SECRET')
redirect_url = os.getenv('REDIRECT_URL')

client = Client.from_credentials(client_id, client_secret, redirect_url)
aclient = Aclient.from_credentials(client_id, client_secret, redirect_url, request_wait_time=0.09)


#grabs all non osu lazer mods from a score and returns them as a list 
def get_mods_as_list(score: LegacyScore | SoloScore):
    mod_list: list = []

    for mods in score.mods:
        if(mods.mod.name != "Classic"):
            mod_list.append(mods.mod.name)
    return(mod_list)
    
#represents the basis of a fit beat map 
async def user_fitness(user_id: int)->list:
#get top 5 and derive a fitness function based on the bpm, spacing, ar, star rating and genre given
    
    avg_bpm: float = 0
    avg_sr: float = 0
    avg_ranked_year: int = 0
    avg_aim_diff: float = 0
    avg_slider_diff: float = 0
    topplays: list = await aclient.get_user_scores(user_id, ScoreType.BEST, limit=5)
    bm_list: list = []
    bma_list: list = []
    for score in topplays:

        
        bm_list.append(aclient.get_beatmap(score.beatmap_id))
        bma_list.append(aclient.get_beatmap_attributes(score.beatmap_id, mods=get_mods_as_list(score), ruleset=Modestr.STANDARD))
        
    bm_result = await a.gather(*bm_list)
    bma_result = await a.gather(*bma_list)
    
    for bm,bma in zip(bm_result,bma_result):
        # bm = await aclient.get_beatmap(score.beatmap_id)
        # bma = await aclient.get_beatmap_attributes(score.beatmap_id, mods=get_mods_as_list(score), ruleset=Modestr.STANDARD)
        get_mods_as_list(score)
        #adds the year it was last updated to avg_ranked_year
        avg_ranked_year += bm.last_updated.year

        #checks if the score has any BPM altering mods and then applies the scaler of that mod to the BPM then adds it to avg_bpm
        if(Mods.DoubleTime in get_mods_as_list(score) or Mods.Nightcore in get_mods_as_list(score)):
            avg_bpm += bm.bpm * 1.5
        elif(Mods.HalfTime in get_mods_as_list(score)):
            avg_bpm += bm.bpm * .75
        else:
            avg_bpm += bm.bpm

        #applies the mod scaler to the maps star rating then adds that value to avg_sr
        avg_sr +=  bma.star_rating
        avg_aim_diff += bma.mode_attributes.aim_difficulty
        avg_slider_diff += bma.mode_attributes.slider_factor    
    return([avg_bpm/5, avg_aim_diff/5, math.floor(avg_ranked_year/5), avg_sr/5, avg_slider_diff/5])















    