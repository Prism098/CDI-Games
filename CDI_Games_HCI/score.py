class ScoreSystem:
    def __init__(self, initial_score, penalty):
        self.score = initial_score
        self.penalty = penalty

    def apply_penalty(self):
        self.score = max(0, self.score - self.penalty)

    def get_score(self):
        return self.score
    
    def add_score(self, points):
        self.score += points
    
    def reset_score(self):
        self.score = 0 
    
    def apply_bonus(self, time_remaining):
        if time_remaining > 20:
            self.score += 700
        else:
            bonus = int(time_remaining * 32)  # points per second remaining
            self.score += bonus