class ScoreSystem:
    def __init__(self, initial_score, penalty):
        self.score = initial_score
        self.penalty = penalty

    def apply_penalty(self):
        self.score = max(0, self.score - self.penalty)
    
    def add_score(self):
        self.score = self.score + 800

    def get_score(self):
        return self.score
    
    def reset_score(self):
        self.score = 0 