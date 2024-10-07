class Player:
    def __init__(self, name: str):
        """
        Initialize player with chosen name and base score of 0
        :param name:
        """
        self.name = name
        self.score = 0

    def get_score(self) -> int:
        """
        returns the current score value
        :return:
        """
        return self.score

    def add_score(self, score: int):
        """
        adds sent value to score
        :param score:
        :return:
        """
        self.score += score

    def __str__(self):
        """
        prints the player name and score
        :return:
        """
        return self.name + ' Score: ' + str(self.score)
