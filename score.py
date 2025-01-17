class ScoreSystem:
    def __init__(self, initial_score=700, penalty=300):
        self.total_score = initial_score  # Starting score
        self.penalty = penalty            # Points to subtract for incorrect color

    def apply_penalty(self):
        """Subtract points if the wrong color is chosen."""
        self.total_score -= self.penalty
        if self.total_score < 0:
            self.total_score = 0  # Ensure score doesn't go below 0

    def apply_correct_choice(self):
        """Apply correct choice and retain score."""
        pass

    def get_score(self):
        """Return the current score."""
        return self.total_score

    def reset_score(self, initial_score=700):
        """Reset score to the initial score for a new round."""
        self.total_score = initial_score
