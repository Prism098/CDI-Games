class ScoreSystem:
    def __init__(self, initial_score=700, penalty=300):
        self.score = initial_score
        self.penalty = penalty

    def apply_penalty(self):
        self.score = max(0, self.score - self.penalty)

    def get_score(self):
        return self.score