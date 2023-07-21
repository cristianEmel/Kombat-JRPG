from rest_framework import serializers
from typing import List, Dict

class MovingSerializer(serializers.Serializer):
    movimientos: List[str] = serializers.ListField(
        child=serializers.CharField(
            allow_blank=True,
            max_length=5
        ),
        required=True
    )
    golpes: List[str] = serializers.ListField(
        child=serializers.CharField(
            allow_blank=True,
            max_length=1
        ),
        required=True
    )

    def validate_movimientos(self, movings) -> List[str]:
        """
            This method validate the movings

            :param movings: List of movings
            :type movings: List[str]

            :return: List of movings
            :rtype: List[str]
        """

        movings: str = "".join(movings)
        invalid_moving: set = set(movings) - set("WSADwsad")

        if invalid_moving:
            raise serializers.ValidationError(f"The moving {invalid_moving} is invalid")

        return movings
    
    def validate_golpes(self, hits) -> List[str]:
        """
            This method validate the hits

            :param hits: List of hits
            :type hits: List[str]

            :return: List of hits
            :rtype: List[str]
        """

        hits: str = "".join(hits)
        invalid_hits: set = set(hits) - set("PKpk")

        if invalid_hits:
            raise serializers.ValidationError(f"The hit {invalid_hits} is invalid")
        
        return hits

class KombatSerializer(serializers.Serializer):

    player1: Dict[str,List[str]] = serializers.DictField(
        required=True
    )
    player2: Dict[str,List[str]] = serializers.DictField(
        required=True
    )

    def validate(self, data) -> Dict[str, Dict[str, List[str]]]:
        """
            This method validate the information of the kombat

            :param data: Data of the kombat
            :type data: Dict[str, Dict[str, List[str]]]

            :return: Data of the kombat
            :rtype: Dict[str, Dict[str, List[str]]]
        """

        #Validate the movings and hits of player1
        serializer = MovingSerializer(data=data["player1"])
        serializer.is_valid(raise_exception=True)

        #Validate the movings and hits of player1
        serializer = MovingSerializer(data=data["player2"])
        serializer.is_valid(raise_exception=True)

        return data
