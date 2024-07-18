def calculate_fitness(win, walls_placed, opponent_walls_placed, gradient_to_win, opponent_gradient_to_win):
    # Initialize the fitness score
    fitness_score = 0
    
    if win:
        # Base points for a win
        fitness_score += 80
        # Penalty for placing 0 walls
        if walls_placed == 0:
            fitness_score -= 5
        # Points for opponent walls placed
        fitness_score += 2.5 * opponent_walls_placed
        # Points for opponent's gradient to win
        fitness_score += opponent_gradient_to_win * 0.1
    else:
        # Base points for a loss
        fitness_score += 40
        # Penalty for placing 0 walls
        if walls_placed == 0:
            fitness_score -= 10
        # Points for walls placed
        fitness_score += 2 * walls_placed
        # Penalty for opponent walls placed
        fitness_score += (2 * opponent_walls_placed) - 1
        # Points for own gradient to win
        fitness_score += gradient_to_win * 0.1
    
    return fitness_score

    