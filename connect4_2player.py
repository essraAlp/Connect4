import pygame
import numpy as np
SIZE=100
ROW=6
COL=7
RADIUS=SIZE//2

GREYISH = (90, 90, 105) 
WHITE = (255, 255, 255)
BLUE = (175, 0, 255)
PINK = (255, 105, 150)
BLACK =(0, 0, 0)
RED = (255, 0, 0)
REDISH = (180, 100, 100)
BLUEB = (0, 0, 255)

pygame.init()
screen = pygame.display.set_mode((COL * SIZE, (ROW + 1) * SIZE))
pygame.display.set_caption("Connect Four")
clock = pygame.time.Clock()

def main():
    board = np.zeros((ROW, COL), dtype=int)
    game_over=False
    turn=1 

    while not game_over:
        #screen.fill(BLACK)
        draw_board(board)
        draw_moving_circle()
        pygame.display.flip()
        clock.tick(30)
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()  # Fare pozisyonunu al
                col = x // SIZE  # Fare X koordinatını, sütun indeksine dönüştür
                row = (y // SIZE) - 1
                if(calculateROW(col,turn,board)):
                    if(winOrNot(board, turn)):
                        draw_board(board)
                        draw_winner(turn)
                        game_over = True
                    else:
                        if turn == 1:
                            turn = 2
                        else:
                            turn = 1 
    pygame.quit()

def draw_moving_circle():
    
    # Fare konumunu al
    x, _ = pygame.mouse.get_pos()
    y = SIZE // 2
    # Fare imlecinin üst kısmı için daireyi çiziyoruz
    pygame.draw.circle(screen, BLUEB, (x, y), RADIUS*11//12)
    #pygame.display.update()
def winOrNot(board, turn):

    #For Horizontal win
    for c in range(COL-3):
        for r in range (ROW):
            if board[r,c] == turn and board[r,c+1] == turn and board[r,c+2]==turn and board[r,c+3]==turn:
                return True

    #For Vertical win
    for r in range(ROW-3):
        for c in range(COL):
            if board[r,c]==turn and board[r+1,c]==turn and board[r+2,c]==turn and board[r+3,c]==turn:
                return True

    #For Cross Win - positive sloped
    for r in range(ROW-3):
        for c in range(COL-3):
            if board[r,c]==turn and board[r+1,c+1]==turn and board[r+2,c+2]==turn and board[r+3,c+3]==turn:
                return True
    # For Cross Win - Negative sloped
    for c in range(COL-3):
        for r in range(3, ROW):
            if board[r,c]==turn and board[r-1,c+1]==turn and board[r-2,c+2]==turn and board[r-3,c+3]==turn:
                return True
    
    totalMove = np.count_nonzero(board)
    if(totalMove == 42):
        draw_quits()
    
    return False

def calculateROW(col,turn,board):
    for r in range(ROW-1,-1,-1):
        if board[r,col] == 0:
            board[r,col] = turn 
            return True 
    return False
def draw_board(board):
    screen.fill(BLACK)
    for r in range(ROW):
        for c in range(COL):
            pygame.draw.rect(screen, GREYISH, (c * SIZE, (r + 1) * SIZE, SIZE, SIZE))
            color = WHITE

            if board[r,c] == 1:
                color = PINK
            elif board[r,c] == 2:
                color = BLUE
            
            pygame.draw.circle(screen, color, (c*SIZE + SIZE//2, (r+1)*SIZE + SIZE//2), RADIUS*11/12)
    pygame.display.update()

def draw_quits():
    winnerScreen = pygame.display.set_mode((COL* SIZE, (ROW - 1) * SIZE))
    pygame.display.set_caption("Game Over")
    # Renkler
    
    font = pygame.font.Font(None, 74)

    message = "Oyun Berabere!!"
    text = font.render(message, True, WHITE)
    text_rect = text.get_rect(center=(winnerScreen.get_width() // 2, winnerScreen.get_height() // 2))

    winnerScreen.fill(REDISH)
    # Yazıyı ekranda ortalıyoruz
    winnerScreen.blit(text, text_rect)
    # Ekranı güncelliyoruz
    pygame.display.update()
    # Kullanıcı bir tuşa basana kadar bekliyoruz
    waiting_for_quit = True
    while waiting_for_quit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting_for_quit = False
            elif event.type == pygame.KEYDOWN:  # Bir tuşa basılmasını bekliyoruz
                waiting_for_quit = False

    pygame.quit()

    
def draw_winner(turn):
    winnerScreen = pygame.display.set_mode((COL* SIZE, (ROW - 1) * SIZE))
    pygame.display.set_caption("Game Over")

    # Yazı fontu ve boyutu
    font = pygame.font.Font(None, 74)
    # Kazanan oyuncuyu belirleme
    congrats = "*TEBRİKLER*"
    if turn == 1:
        winner_text = "Oyuncu 1 oyunu kazandı!"
    else:
        winner_text = "Oyuncu 2 oyunu kazandı!"
    # Kazanan mesajını yazdırıyoruz
    textPlayer = font.render(winner_text, True, WHITE)
    textCongrat = font.render(congrats, True, WHITE)

    text_rect = textPlayer.get_rect(center=(winnerScreen.get_width() // 2, winnerScreen.get_height()*3 // 5))
    text_otherrect = textCongrat.get_rect(center=(winnerScreen.get_width() // 2, winnerScreen.get_height()*2 // 5))
    # Ekranı siyah yapıyoruz
    winnerScreen.fill(REDISH)
    # Yazıyı ekranda ortalıyoruz
    winnerScreen.blit(textPlayer, text_rect)
    winnerScreen.blit(textCongrat, text_otherrect)
    # Ekranı güncelliyoruz
    pygame.display.update()
    # Kullanıcı bir tuşa basana kadar bekliyoruz
    waiting_for_quit = True
    while waiting_for_quit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting_for_quit = False
            elif event.type == pygame.KEYDOWN:  # Bir tuşa basılmasını bekliyoruz
                waiting_for_quit = False

    pygame.quit()
if __name__ == "__main__":
    main()