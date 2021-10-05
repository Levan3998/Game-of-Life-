import pygame
import time

# Logics

# column functions
# True if one in the column
def one_in_col(col, M):
    for row in M:
        if(row[col] == 1):
            return True
    return False
# pops the entire column
def pop_col(col,M):
    for row in M:
        row.pop(col)

# interactions
# returns alive neighbors count
def check_neighbors(x, y, M):
    sum = 0
    for i in [x-1,x,x+1]:
        for j in [y-1,y,y+1]:
            if (j != y) or (i != x):
               sum += M[i][j]
    return sum
# the block is (x,y) decides if he lives or dies and saves it in the live/dead list
def interact(x,y,M,list_l,list_d):
    n = check_neighbors(x,y,M)
    state = M[x][y]
    if(state == 0):#lives
        if(n == 3):
            list_l.append((x,y))
    if(state == 1):
        if(n < 2):#dies
            list_d.append((x,y))
        elif(n > 3):#dies
            list_d.append((x,y))
# check the edges of the board apart from the main board
def check_edges(M,list_l = []):
    #tl --> tr
    for i in range(1,len(M[0])-1):
        if(M[1][i-1] == 1) and (M[1][i] == 1) and (M[1][i+1] == 1):
            list_l.append((0,i))
        #M[0][i] = 3
    #tl --> bl
    for i in range(1,len(M)-1):
        if(M[i-1][1] == 1) and (M[i][1] == 1) and (M[i+1][1] == 1):
            list_l.append((i,0))
        #M[i][0] = 4
    #tr --> br
    for i in range(1,len(M)-1):
        if (M[i - 1][-2] == 1) and (M[i][-2] == 1) and (M[i + 1][-2] == 1):
            list_l.append((i,len(M[i])-1))
        #M[i][len(M[i])-1] = 5
    #bl --> br
    for i in range(1,len(M[len(M)-1])-1):
        if(M[-2][i-1] == 1) and (M[-2][i] == 1) and (M[-2][i+1] == 1):
            list_l.append((len(M[-1])-1,i))
        #M[len(M)-1][i] = 6
    return M
# makes an nxm matrix
def make_matrix(n,m):
    M = []
    for i in range(n):
        M.insert(0, [])
        for j in range (m):
            M[0].insert(0,0)
    return M
# adds new edges to the matrix filled with '0'
def matrix_size_up(old_m):
    if(len(old_m) == 0):
        return [0]
    old_m.insert(0,create_list_of_zeros(len(old_m[0])))
    old_m.append(create_list_of_zeros(len(old_m[0])))
    for i in old_m: # add to the start and end of each list a '0'
        i.insert(0,0)
        i.append(0)
    return old_m
# creates a list of '0' with length = n    (used in size_up)
def create_list_of_zeros(n):
    L = []
    for i in range (n):
        L.append(0)
    return L
# cut the '0' rows and columns at the edges
def matrix_size_down(old_m):
    if(len(old_m) == 0):
        return old_m
    if(len(old_m) == 1):
        return [[0]]
    while  len(old_m)>0 and  not (1 in old_m[0]):
        old_m.pop(0)
        if(len(old_m) == 0):
            break
    while len(old_m)>0 and (not (1 in old_m[-1])):
        old_m.pop(-1)
        if(len(old_m) == 0):
            break
    while len(old_m)>0 and not(one_in_col(0,old_m)):
        pop_col(0,old_m)
        if(len(old_m) == 0):
            break
    while len(old_m)>0 and not (one_in_col(-1,old_m)):
        pop_col(-1,old_m)
        if(len(old_m) == 0):
            break

    return old_m
# apply next step to the whole matrix
def next_gen(mat):
    if(len(mat) == 0): # check if empty
        return mat
    new_mat = matrix_size_up(mat) # patten it first to avoid index errors
    list_d = [] # will die
    list_l = [] # will be born
    for i in range (1, len(new_mat)-1):
        for j in range(1, len(new_mat[0])-1):
            interact(i, j, new_mat, list_l, list_d)
    check_edges(new_mat, list_l)
    for pos in list_l: # add and remove "new born" and "new dead"
        new_mat[pos[0]][pos[1]] = 1
    for pos in list_d:
        new_mat[pos[0]][pos[1]] = 0
    return new_mat
def draw(M):
    for i in M:
        print(i)
# pyGame

# get the fitting size block to the matrix board
def get_size(b):
    n = max(len(b)-1,len(b[0])-1)
    return 1000/n
def get_img(s,size):
    image = pygame.Surface((size, size))
    if(s==2):
        image.fill((000,150,150))
    elif(s==1):
        image.fill((155, 000, 155))
    else:
        image.fill((000, 000, 100))
    return image
def draw_board(b):
    for i in range(len(b)):
        if(type(b[i]) == list):
            for j in range(len(b[i])):
                s = b[i][j]
                size = get_size(b)
                screen.blit(get_img(s,size),(j*size,i*size))
# "Done" button
def draw_button():
    font = pygame.font.Font(None, 45)
    survivedtext = font.render("Done".zfill(2), True, (150, 0, 0))
    textRect = survivedtext.get_rect()
    textRect.topright = [width-5, 10]
    screen.blit(survivedtext, textRect)

M = make_matrix(20,20)  # base matrix
temp = M
pygame.init()
width, height = 1000, 1000
screen=pygame.display.set_mode((width, height))
screen.fill((000,000,100))
size1 = max(width,height) / max(len(temp),len(temp[0]))
flag = True
while(flag):  # while the "Done" button hadn't been clicked
    screen.fill((000, 000, 100))
    pos = pygame.mouse.get_pos()
    mx, my = pos
    mx = int(mx//size1)
    my = int(my//size1)
    draw_board(temp)
    screen.blit(get_img(2,size1/2),((mx+0.6)*size1,(my+0.6)*size1))  # draw where you will add a block
    draw_button()
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos_x, pos_y = pygame.mouse.get_pos()
            if(pos_x > width-100) and (pos_y < 50):  # if clicked the "Done" button
                flag = False
            else:
                temp[my][mx] = 1  # add desired block



draw_board(temp)
pygame.display.flip()
time.sleep(0.1)
for i in range(1000):
    if(len(temp)>1) :
        screen.fill((000, 000, 100))  # clear the screen
        temp = next_gen(temp)  # do a step
        temp = matrix_size_down(temp)  # cut edges if needed
        temp = matrix_size_up(temp)  # size up for next iteration and better drawing
        draw_board(temp)  # draw the board
        pygame.display.flip()  # display
        time.sleep(0.1)  # wait a bit for nicer visuals
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # if it is quit the game
                pygame.quit()
                exit(0)
while(True):  # end screen
    font = pygame.font.Font(None, 200)
    survivedtext = font.render("The End".zfill(2), True, (200, 0, 50))
    textRect = survivedtext.get_rect()
    textRect.topright = [width*0.8, height/2]
    screen.blit(survivedtext, textRect)
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # if it is quit the game
            pygame.quit()
            exit(0)
