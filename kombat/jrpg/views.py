from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import KombatSerializer
from typing import List, Dict
from .constans import HITS, MESSAGE
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

def count_combinations(player_moving, player_hits):

    """
        This method count the combinations of the player

        :param player_moving: List of movings of the player
        :type player_moving: List[str]
        :param player_hits: List of hits of the player
        :type player_hits: List[str]

        :return: Number of combinations
        :rtype: int
    """

    return len([moving + hit for moving, hit in zip(player_moving, player_hits) if hit and moving])

@swagger_auto_schema(
    methods=['post'],
    request_body=KombatSerializer,
    responses={
        200: openapi.Response(
            description='Success',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'history': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(type=openapi.TYPE_STRING)
                    )
                },
            ),
        )
    },)
@api_view(['POST'])
def kombat(request) -> Response:
    """
        This is the kombat view
        This view validate the information and generate a result with the information of the winner

        :param request: Request object
        :return: Response object

        :return: Response object
        :rtype: Response

    """

    #Validate the information
    serializer = KombatSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    #Get moving of player1 and player2
    moving_player1: list = request.data.get("player1").get("movimientos")
    moving_player2: list = request.data.get("player2").get("movimientos")

    #Get hits of player1 and player2
    hits_player1: list = request.data.get("player1").get("golpes")
    hits_player2: list = request.data.get("player2").get("golpes")

    #Define which player start to hit
    next_turn: str = None

    player1_hit_combinations: int = count_combinations(moving_player1, hits_player1)
    player2_hit_combinations: int = count_combinations(moving_player2, hits_player2)

    if player1_hit_combinations < player2_hit_combinations:
        next_turn: str = "player1"
    elif player1_hit_combinations > player2_hit_combinations:
        next_turn: str = "player2"
    elif len(moving_player1) < len(moving_player2):
        next_turn: str = "player1"
    elif len(moving_player1) > len(moving_player2):
        next_turn: str = "player2"
    elif len(hits_player1) < len(hits_player2):
        next_turn: str = "player1"
    elif len(hits_player1) > len(hits_player2):
        next_turn: str = "player2"
    else:
        next_turn: str = "player1"

    #List with the comments of the kombat
    result: List[str] = []
    winner: str = None
    fight_end: bool = False

    #Save general information of the game
    game: Dict[str, str] = {
        "player1": {
            "live":6,
            "movements":moving_player1,
            "hits":hits_player1,
            "current_movement":0,
        },
        "player2": {
            "live":6,
            "movements":moving_player2,
            "hits":hits_player2,
            "current_movement":0,
        }
    }

    while not winner or not fight_end:

        #Have the player been attacked?
        attacked: bool = False

        #Player that hit
        player_that_hit: str = next_turn
        #Player that receive the hit
        player_that_receive_hit: str = "player1" if next_turn == "player2" else "player2"

        #Movings and hits of the player that hit
        movements = game[player_that_hit]["movements"]
        hits = game[player_that_hit]["hits"]
        current_movement = game[player_that_hit]["current_movement"]

        #Get the next movement and hit
        next_movement: str = movements[current_movement] if current_movement < len(movements) else ""
        next_hit: str = hits[current_movement] if current_movement < len(hits) else ""
        #Combination of the movement and hit is a attack
        attack: str = f"{next_movement}{next_hit}".lower()
        #Mark the attack as used
        game[player_that_hit]["current_movement"]: int = current_movement + 1

        #Get information of the attacks that can hit
        attacks_hit: List[str] = HITS[player_that_hit]

        #Looking for the attack that hit
        for attack_hit in attacks_hit:
            attack_hit_combination: str = attack_hit["combination"].lower()
            if attack.endswith(attack_hit_combination):
                
                #Reduce the live of the player that receive the hit
                game[player_that_receive_hit]["live"]: int = game[player_that_receive_hit]["live"] - attack_hit["energy"]
                #Mark the player as attacked
                attacked: bool = True
                #Add the comment of the attack
                result.append(MESSAGE[f"{player_that_hit}-{attack_hit_combination}"])
                break

        #If the player didn't hit and had a valid attack, add the comment of the movement
        if not attacked and attack:
            result.append(MESSAGE[player_that_hit])

        #Validate if the player that receive the hit is dead
        if game[player_that_receive_hit]["live"] <= 0:
            #Save the winner
            winner: str = player_that_hit
            #Add victory comment
            msg: str = MESSAGE[f"{player_that_hit}-win"] + f" y aun le queda {game[player_that_hit]['live']} de energia"
            result.append(msg)
            break

        #Change the turn
        next_turn: str = player_that_receive_hit

        #Validate that both players have finished their movements
        is_last_movement_player_hit: bool = game[player_that_hit]["current_movement"] >= len(game[player_that_hit]["movements"])
        is_last_movement_player_receive_hit: bool = game[player_that_receive_hit]["current_movement"] >= len(game[player_that_receive_hit]["movements"])

        #Validate if the fight end
        if is_last_movement_player_hit and is_last_movement_player_receive_hit:
            fight_end: bool = True
            result.append(MESSAGE["Empate"])

    return Response(
        data= {
            "history": result
        },
        status= status.HTTP_200_OK
    )



        

       





    
    

