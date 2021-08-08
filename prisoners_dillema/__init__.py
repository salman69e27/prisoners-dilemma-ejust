from __future__ import annotations

from typing import Any, Protocol, Iterator
from config import MOVE, COOP, DEFECT, PAYOFF


class DuplicateResultError(Exception):
    pass


class ResultNotFoundError(Exception):
    pass


class PlayerNotFoundError(Exception):
    pass


class RegisterationError(Exception):
    pass


class MatchError(Exception):
    pass


class PlayerInterface(Protocol):
    id: str

    def play(self) -> bool:
        ...

    def set_result(self, result: tuple[int, int],
            opponents_move: MOVE) -> None:
        ...


class Results:
    """
    Holds the results of the tournament
    """

    def __init__(self) -> None:
        self.__results: dict[Any, dict[Any, int]] = dict()
        self.__players: set[Any] = set()
        self.__tournament_started = False

    def add_player(self, player: PlayerInterface) -> None:
        if self.__tournament_started:
            raise RegisterationError("Tournament already started")
        self.__results[player] = dict()
        self.__players.add(player)

    def set_result(
        self,
        player1: PlayerInterface,
        player2: PlayerInterface,
        result: tuple[int, int],
    ) -> None:

        # Make sure these players exist
        if player1 not in self.__players or player2 not in self.__players:
            raise PlayerNotFoundError(
                "At least one of the two players is not registered"
            )

        # Make sure this is the first match between the players
        if player1 in self.__results[player2]:
            raise DuplicateResultError(
                f"""There is a previous result between {player1.id} and
                 {player2.id}"""
            )

        self.__tournament_started = True  # To prevent adding new players
        self.__results[player1][player2] = result[0]
        self.__results[player2][player1] = result[1]

    def get_result(
        self, player1: PlayerInterface, player2: PlayerInterface
    ) -> tuple[int, int]:

        """
        Returns the results between to players.
        """

        # Make sure these players exist
        if player1 not in self.__players or player2 not in self.__players:
            raise PlayerNotFoundError(
                """At least one of the players is
                                      not registered"""
            )

        try:
            return (
                self.__results[player1][player2],
                self.__results[player2][player1],
            )
        except KeyError:
            raise ResultNotFoundError(
                "There is no record of a game between the two players"
            )


class Judge:

    """
    Organizes the tournament and runs the matches between bots
    """

    def __init__(self) -> None:
        self.players: list[Any] = list()
        self.results = Results()

        # Holds the report of the game to maybe use later for stats
        self.report = {
            "# betrayals": 0,
            "# trusts": 0,
            "# mutual trusts": 0,
            "# mutual betrayals": 0,
            "# one-sided trusts": 0,
        }

    def register_player(self, player: Any) -> None:
        self.players.append(player)
        self.results.add_player(player)


    def matches(self) -> Iterator[Match]:
        # TODO: Change to generate a fair round-robin schedule

        n = len(self.players)
        for i in range(n):
            for j in range(i + 1, n):
                yield Match(self.players[i], self.players[j], self)

    def play(self) -> None:
        for match in self.matches():
            match.play()
            self.__write_results()

    def __write_results(self):
        # TODO: Write the reults so far to a json file to upload on the website
        ...


class Match:

    """
    Runs individual matches between bots and reports the result back to the
    judge system
    """

    def __init__(
        self, player1: PlayerInterface, player2: PlayerInterface, judge: Judge
    ) -> None:
        self.player1: PlayerInterface = player1
        self.player2: PlayerInterface = player2
        self.judge: Judge = judge
        self.player1_score: int = 0
        self.player2_score: int = 0
        self.num_games: int = 10000
        self.report = {
            "# betrayals": 0,
            "# trusts": 0,
            f"# trusts by {self.player1.id}": 0,
            f"# betrayals by {self.player1.id}": 0,
            f"# trusts by {self.player2.id}": 0,
            f"# betrayals by {self.player2.id}": 0,
            "# mutual trusts": 0,
            "# mutual betrayals": 0,
            f"{self.player1.id} one-sided betrayals": 0,
            f"{self.player2.id} one-sided betrayals": 0,
        }

    def play(self) -> None:
        if self.player1_score + self.player2_score != 0:
            raise MatchError("Match already started")

        for _ in range(self.num_games):
            player1_move = self.__get_move(self.player1)
            player2_move = self.__get_move(self.player2)
            round_report = self.__get_round_result(player1_move, player2_move)
            result = round_report["result"]
            self.player1_score += result[0]
            self.player2_score += result[1]
            # Update match report with the new round report
            for key, val in round_report.items():
                if key == "result":
                    continue
                self.report[key] += val

        self.judge.results.set_result(
            self.player1, self.player2, self.result
        )

        # Update judge report with the new match report
        for key, val in self.report.items():
            if key in self.judge.report:
                self.judge.report[key] += val

        self.judge.report["one-sided trusts"] = (
            self.report[f"{self.player1.id} one-sided betrayals"]
            + self.report[f"{self.player2.id} one-sided betrayals"]
        )

    @property
    def result(self) -> tuple[int, int]:
        return (self.player1_score, self.player2_score)

    def __get_round_result(
        self, player1_move: MOVE, player2_move: MOVE
    ) -> dict[str, Any]:

        result = PAYOFF[(player1_move, player2_move)]

        game_report = {
            "result": result,
            "# betrayals": (player1_move == COOP) + (player2_move == COOP),
            "# trusts": (player1_move == DEFECT) + (player2_move == DEFECT),
            f"# trusts by {self.player1.id}": (player1_move == DEFECT),
            f"# betrayals by {self.player1.id}": (player1_move == COOP),
            f"# trusts by {self.player2.id}": (player2_move == DEFECT),
            f"# betrayals by {self.player2.id}": (player2_move == COOP),
            "# mutual trusts": (player1_move == player2_move == DEFECT),
            "# mutual betrayals": (player1_move == player2_move == COOP),
            f"{self.player1.id} one-sided betrayals": (player1_move == COOP)
            and (player2_move == DEFECT),
            f"{self.player2.id} one-sided betrayals": (player2_move == COOP)
            and (player1_move == DEFECT),
        }
        return game_report

    @staticmethod
    def __get_move(player: PlayerInterface) -> bool:
        return player.play()
