import math
import random
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


# Bu fonksiyon, mevcut tahtada en iyi hamleyi bulur.
# Geçerli sütunları kontrol eder ve her sütun için bir skor hesaplar.
# En yüksek skora sahip sütunu döndürür.
def pick_best_move(board, turn):
    valid_columns = find_Valid_Columns(board)
    best = -1000000
    best_col = random.choice(valid_columns) # for a random choice (there will always be zeroth choice)
    for col in valid_columns:
        row = find_empty_row(board, col)
        tempboard = board.copy()
        score = play_move(tempboard, row, col, turn)
        if score > best:
            best = score
            best_col = col
    
    return best_col   

# Bu fonksiyon, bir pencere (4 hücrelik bir dizi) için skoru hesaplar.
# Oyuncunun taşlarının sayısına ve rakibin taşlarının sayısına göre puan verir.
def next_step(window, turn):
    score = 0
    other_player = 1
    if turn == 1: other_player = 2

    player_count = sum(x == turn for x in window)
    empty_count = sum(x == 0 for x in window)
    other_count = sum(x == other_player for x in window)

    if player_count == 4: score += 100
    elif player_count == 3 and empty_count == 1 : score += 5
    elif player_count == 2 and empty_count == 2 : score += 2
    
    if other_count == 3 and empty_count == 1: score -= 8

    return score

# Bu fonksiyon, tahtanın genel skorunu hesaplar.
# Merkezi sütun, yatay, dikey ve çapraz pencereleri değerlendirir.
def get_score(board, turn):
    score = 0

    center_array = [int(i) for i in list(board[:, COL//2])]
    center_count = center_array.count(turn)
    score += center_count * 3

    for row in range(ROW):
        row_arr = list(board[row,:])
        for col in range(COL-3):
            window = row_arr[col:col+4]
            score += next_step(window, turn)

    for col in range(COL):
        col_arr = board[:,col]
        for row in range(ROW-3):
            window = col_arr[row:row+4]
            score += next_step(window, turn)
    
    for row in range(ROW-3):
        for col in range(COL-3):
            window = [board[row+i][col+i] for i in range(4)]
            score += next_step(window, turn)

    for row in range(ROW-3):
        for col in range(COL-3):
            window = [board[row+3-i][col+i] for i in range(4)]
            score += next_step(window, turn)

    return score

# Bu fonksiyon, Greedy Best First algoritmasını uygular.
# Geçerli sütunları kontrol eder ve her sütun için bir skor hesaplar.
# En yüksek skora sahip sütunu ve bu skoru döndürür.
def greedy_best_first(board, turn):
    valid_locs = find_Valid_Columns(board)
    best_score = -math.inf
    best_col = random.choice(valid_locs)  # Varsayılan olarak rastgele bir sütun seç

    for col in valid_locs:
        row = find_empty_row(board, col)
        tempboard = board.copy()
        play_move(tempboard, row, col, turn)
        score = get_score(tempboard, turn)  # Sadece bir adım ileriye bakıyoruz
        if score > best_score:
            best_score = score
            best_col = col

    return best_col, best_score

# Bu fonksiyon, oyunun bitip bitmediğini kontrol eder.
# Kazanan bir durum veya tahtanın dolu olup olmadığını kontrol eder.
def finishing_move(board):
    return winOrNot(board, 1) or winOrNot(board, 2) or len(find_Valid_Columns(board)) == 0

# Bu fonksiyon, oyunun ana döngüsünü içerir.
# Oyuncu ve yapay zeka sırasıyla hamle yapar.
# Oyun bitene kadar devam eder.
def main():
    board = np.zeros((ROW, COL), dtype=int)
    game_over=False
    turn=2

    while not game_over:
        #screen.fill(BLACK)
        draw_board(board)
        draw_moving_circle()
        pygame.display.flip()
        clock.tick(60)
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.MOUSEBUTTONDOWN:

                if turn == 2:
                    x, y = pygame.mouse.get_pos()  # Fare pozisyonunu al
                    col = x // SIZE  # Fare X koordinatını, sütun indeksine dönüştür
                    row = (y // SIZE) - 1
                    if(calculateROW(col,board)):
                        row = find_empty_row(board, col)
                        play_move(board, row, col, turn)
                        if(winOrNot(board, turn)): 
                            draw_board(board)
                            pygame.time.wait(1000)
                            draw_winner(turn)
                            game_over = True
                        
                        turn = 1
                
        if turn == 1 and not game_over:
            col, _ = greedy_best_first(board, turn)  # Greedy Best First çağrısı
            if calculateROW(col, board):
                row = find_empty_row(board, col)
                play_move(board, row, col, turn)
                if winOrNot(board, turn):
                    print("there is a winner with turn equal to AI")
                    draw_board(board)
                    pygame.time.wait(1000)
                    draw_winner(turn)
                    game_over = True
                turn = 2
    if game_over:
        pygame.quit()

# Bu fonksiyon, tahtadaki geçerli sütunları bulur.
# Geçerli sütunlar, en üst hücresi boş olan sütunlardır.
def find_Valid_Columns(board):
    validLocs = []
    for c in range(COL):
        if board[0][c] == 0:
            validLocs.append(c)
    return validLocs

# Bu fonksiyon, bir sütundaki en alt boş satırı bulur.
def find_empty_row(board, col):
    for r in range(ROW-1,-1,-1):
        if board[r][col]==0:
            return r

# Bu fonksiyon, fare hareketine göre üstteki hareketli daireyi çizer.
def draw_moving_circle():
    
    # Fare konumunu al
    x, _ = pygame.mouse.get_pos()
    y = SIZE // 2
    # Fare imlecinin üst kısmı için daireyi çiziyoruz
    pygame.draw.circle(screen, BLUEB, (x, y), RADIUS*11//12)
    #pygame.display.update()

# Bu fonksiyon, bir oyuncunun kazanıp kazanmadığını kontrol eder.
# Yatay, dikey ve çapraz kazanç durumlarını kontrol eder.
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
    for r in range(3,ROW):
        for c in range(COL-3):
            if board[r,c]==turn and board[r-1,c+1]==turn and board[r-2,c+2]==turn and board[r-3,c+3]==turn:
                return True
    return False

# Bu fonksiyon, bir sütunun dolu olup olmadığını kontrol eder.
def calculateROW(col,board):
    return board[0][col] == 0

# Bu fonksiyon, tahtayı çizer.
# Hücrelerin renklerini ve taşları ekrana çizer.
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

# Bu fonksiyon, oyunun berabere bittiği durumda bir ekran çizer.
def draw_quits():
    pygame.time.wait(800)
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
            if event.type in (pygame.QUIT, pygame.KEYDOWN):
                waiting_for_quit = False 

    pygame.quit()

# Bu fonksiyon, tahtaya bir taş yerleştirir.
def play_move(board, row, col, turn):
    board[row][col] = turn

# Bu fonksiyon, kazanan oyuncu için bir ekran çizer.    
def draw_winner(turn):
    winnerScreen = pygame.display.set_mode((COL* SIZE, (ROW - 1) * SIZE))
    pygame.display.set_caption("Game Over")

    # Yazı fontu ve boyutu
    font = pygame.font.Font(None, 74)
    # Kazanan oyuncuyu belirleme
    congrats = "*TEBRİKLER*"
    if turn == 1:
        winner_text = "AI oyunu kazandı!"
    else:
        winner_text = "Player oyunu kazandı!"
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


if __name__ == "__main__":
    main()