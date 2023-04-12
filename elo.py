class Player:
    def __init__(self, name, rating = 1200, set = 0, k = 40):
        self.name = name
        self.rating = rating
        self.set = set
        self.k = k

class EloSystem:
    def expected_score(self, player1, player2):
        return 1 / (1 + 10 ** ((player2 - player1) / 400))

    def update_k(self, player):
        if (player.set >= 30 or player.rating >= 2000):
            player.k = 20
        if (player.rating >= 2000):
            player.k = 10

    def update_rating(self, player1, player2, winner):
        expected_score1 = self.expected_score(player1.rating, player2.rating)
        expected_score2 = self.expected_score(player2.rating, player1.rating)

        self.update_k(player1)
        self.update_k(player2)

        if winner == 1:
            player1.rating += player1.k * (1 - expected_score1)
            player2.rating += player2.k * (0 - expected_score2)
            player1.set += 1
            player2.set += 1
        elif winner == 2:
            player1.rating += player1.k * (0 - expected_score1)
            player2.rating += player2.k * (1 - expected_score2)
            player1.set += 1
            player2.set += 1