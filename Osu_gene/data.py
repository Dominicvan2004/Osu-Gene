from sqlmodel import *
from osu import *
from dotenv import load_dotenv
from os import getenv
#This is a new file to scrape the most recent beatmaps from osu, ideally this is weill update an in memory sqlite database as to not have to make re accuring API calls like an idiot.... sorry peppy <3
#This should be the only file to use the API
#The idea for db would be for one table to hold each song with their stats from website using the beatmap ID as a primary key, then having each maps fitness in a related table as to adhire to second normal form

load_dotenv()

client_id = int(getenv('CLIENT_ID'))
client_secret = getenv('CLIENT_SECRET')
redirect_url = getenv('REDIRECT_URL')

client = Client.from_credentials(client_id, client_secret, redirect_url, request_wait_time = 0.1)

class Beatmap_Item(SQLModel, table=True):
  id: int = Field(default=None, primary_key=True)
  title: str
  author: str
  star_rating: float
  bpm: float
  submission_year: int

engine = create_engine("sqlite:///database.db")
SQLModel.metadata.create_all(engine)


class Scrapper():

  def __init__(self):
    pass

  def scrape(self,):
    """
    This will scrape the osu Standard beatmaps and store them in the database 
    """
    state: bool = True
    page_num = 1

    while page_num <= 1:
      #error handling, pretty much scrape until you can't scrape no more.
      try:
        list_of_songs = client.search_beatmapsets(
        BeatmapsetSearchFilter()
        .set_status(RankStatus.RANKED)
        .set_mode(GameModeInt.STANDARD),
        page=1
        )
      except:
        state = False

      #parse each beatmapset per page store them in the maps table, with their PK(id), bpm, star rating, creator, year of submission, and genre
      for i in list_of_songs.beatmapsets:
        for maps in i.beatmaps:
          with Session(engine) as session:
            session.add(Beatmap_Item(
              id = maps.id,
              title = "test",
              author = "test",
              star_rating = maps.difficulty_rating,
              bpm = maps.bpm,
              submission_year = 2020
            ))
            session.commit()
      page_num += 1
      with Session(engine) as session:
        print(session.exec(select(Beatmap_Item)).all)


scrapper = Scrapper()
scrapper.scrape()
