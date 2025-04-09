# Using your Pygame setup
def draw_node_counts(node_counts):
    font = pygame.font.SysFont('Arial', 20)
    texts = [
        f"Minimax: {node_counts['minimax']} nodes",
        f"A*: {node_counts['astar']} nodes",
        f"Greedy: {node_counts['greedy']} nodes"
    ]
    for i, text in enumerate(texts):
        txt_surface = font.render(text, True, WHITE)
        screen.blit(txt_surface, (10, 10 + i*25))