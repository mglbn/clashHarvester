import psycopg2
from datetime import datetime, timezone



class DB():

    _conn = None
    _cur = None

    @staticmethod
    def connect(host, user, password, dbname):
        DB._conn = psycopg2.connect(host=host, user=user, password=password, dbname=dbname)
        DB._cur = DB._conn.cursor()

    @staticmethod
    def insert(players):
        playertuples, cardtuples = DB._createTuplesFromJson(players)

        #insert into player TB
        records_list_template_players = ','.join(['%s'] * len(playertuples))
        insert_query_player = 'insert into tb_player values {}'.format(records_list_template_players)
        DB._cur.execute(insert_query_player, playertuples)

        #save current DECK
        try:
            if len(cardtuples)>0:
                records_list_template_cards = ','.join(['%s'] * len(cardtuples))
                insert_query_card = 'insert into tb_plays values {}'.format(records_list_template_cards)
                DB._cur.execute(insert_query_card, cardtuples)
        except:
            print(records_list_template_cards)
            print(cardtuples)

        DB._conn.commit()

    @staticmethod
    def _createTuplesFromJson(jsonlist):
        playertups = list()
        cardtups = list()
        now = datetime.now()
        for json in jsonlist:
            yearsPlayed = None
            for badge in json.get("badges"):
                if badge.get("name") == "YearsPlayed":
                    yearsPlayed = badge.get("level")
                    break
            
            if "currentDeck" in json.keys():
                for card in json.get("currentDeck"):
                    cardtups.append((
                        json.get("tag")[1:],
                        card.get("id"),
                        card.get("level")
                    ))
            
            
            currentTrophies = None
            currentBestTrophies= None
            prevTrophies= None
            prevBestTrophies = None
            bestSeasonTrophies = None
            previousSeason = None
            bestSeason = None
            if "leagueStatistics" in json.keys():
                leaque = json.get("leagueStatistics")
                if "currentSeason" in leaque.keys():
                    currentTrophies = leaque.get("currentSeason").get("trophies")
                    currentBestTrophies = leaque.get("currentSeason").get("bestTrophies")
                if "previousSeason" in leaque.keys():
                    previousSeason = leaque.get("previousSeason").get("id")
                    prevTrophies = leaque.get("previousSeason").get("trophies")
                    prevBestTrophies = leaque.get("previousSeason").get("bestTrophies")
                if "bestSeason" in leaque.keys():
                    bestSeason = leaque.get("bestSeason").get("id")
                    bestSeasonTrophies = leaque.get("bestSeason").get("trophies")
                
            playerTub = (
                json.get("tag")[1:],
                json.get("wins"),
                json.get("losses"),
                json.get("threeCrownWins"),
                json.get("trophies"),
                json.get("bestTrophies"),
                json.get("expLevel"),
                yearsPlayed,
                now.strftime("%Y-%m"),
                previousSeason,
                bestSeason,
                datetime.now(timezone.utc),
                prevBestTrophies,
                prevTrophies,
                bestSeasonTrophies,
                currentBestTrophies,
                currentTrophies
            )
            playertups.append(playerTub)
        return (playertups,cardtups)

    @staticmethod
    def close():
        DB._cur.close()
        DB._conn.close()