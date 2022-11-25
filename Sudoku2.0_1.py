import pygame
import requests

width = 550 #valeur de la taille de la page Pygame
background = (251, 247, 245) #couleur de la grille 
grid_origin_color = (52, 31, 151) #couleur des chiffres
buffer = 5

response = requests.get("https://sugoku.herokuapp.com/board?difficulty=easy") #Générateur automatique de Sudoku
grid = response.json()['board']
grid_origin = [[grid[x][y] for y in range(len(grid[0]))]for x in range(len(grid))]

def insert(win, position):
    """ C'est la partie qui va faire tourner le jeu et permet de modifier les cases vides.
        Il verifie bien dabord que la valeur inserée et entre 1 et 9.
        Mais pour une raison que j'ignore celui-ci ne veux pas modifier les valeurs lorsque 
        je clique sur une case vide
       """

    print("insert Ok")
    i,j = position[1], position[0]
    monfont = pygame.font.SysFont('Comic Sans MS', 35)
    
    sortie = False
    while sortie == False :
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sortie = True
            if event.type == pygame.KEYDOWN:
                if (grid_origin[i-1][j-1] != 0):
                    sortie = True
                if (event.key == 48): # Nous vérifions avec 0
                    grid[i-1][j-1] = event.key - 48
                    pygame.draw.rect(win, background, (position[0]*50 + buffer, position[1]*50 + buffer, 50 - 2*buffer, 50 - 2*buffer))
                    pygame.display.update()
                    sortie = True
                if ( 0 < event.key - 48 < 10): # Nous vérifions avec des entrés valides
                    pygame.draw.rect(win, background, (position[0]*50 + buffer, position[1]*50 + buffer, 50 - 2*buffer, 50 - 2*buffer))
                    value = monfont.render(str(event.key - 48), True, (0, 0, 0))
                    win.blit(value, (position[0]*50 + 15, position[1]*50))
                    grid[i-1][j-1] = event.key - 48
                    pygame.display.update()
                    sortie = True
                return 

def main():
""" c'est le coeur du projet, avec le lien du générateur de bibliothèque de sudoku,
    celui-ci va dabord dessiner la grille grace à pygame et ensuite inserera les valeurs de 
    la bibliothèque et pour finir, on a la fontion qui permet de cliquer sur une des cases vides
    et de modifier ce vide qui est en réalité un zéro devenu invisible.
"""

    pygame.init()
    response = requests.get("https://sugoku.herokuapp.com/board?difficulty=easy") #Générateur automatique de Sudoku
    grid = response.json()['board']
    win = pygame.display.set_mode((width, width))
    pygame.display.set_caption("Sudoku")
    win.fill(background)
    monfont = pygame.font.SysFont('Comic Sans MS', 35)
    
    # dessin de la grille 
    for i in range(0, 10):
        if (i%3 == 0):
            pygame.draw.line(win, (0, 0, 0), (50 + 50*i, 50), (50 + 50*i, 500), 4)
            pygame.draw.line(win, (0, 0, 0), (50, 50 + 50*i), (500, 50 + 50*i), 4)
            
        pygame.draw.line(win, (0, 0, 0), (50 + 50*i, 50), (50 + 50*i, 500 ), 2)
        pygame.draw.line(win, (0, 0, 0), (50, 50 + 50*i), (500, 50 + 50*i), 2)
    pygame.display.update()
    
    #Systeme de placement du générateur de sudoku
    for i in range(0, len(grid[0])):
        for j in range(0, len(grid[0])):
            if (0 < grid[i][j] < 10):
                value = monfont.render(str(grid[i][j]), True, grid_origin_color)
                win.blit(value, ((j+1)*50 + 15, (i+1)*50))
    pygame.display.update()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                pos = pygame.mouse.get_pos()
                insert(win, (pos[0]//50, pos[1]//50))
            if event.type == pygame.QUIT :
                pygame.quit()
                return
        
        pygame.display.flip() #Fait apparaitre la grille avec les valeur sur la page
        
main()    
