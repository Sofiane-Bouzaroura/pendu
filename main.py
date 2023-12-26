import pygame
import random
import os

# Initialiser Pygame et les polices de caractères
pygame.init()
pygame.font.init()

# Obtenir le chemin absolu du répertoire du script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Construire la liste des chemins complets des images
images_pendu = [os.path.join(script_dir, f"pendu{i:02d}.png") for i in range(1, 8)]

# Définir des constantes
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Initialiser la fenêtre
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jeu de mots")

# Charger la liste de mots depuis le fichier
with open("mots.txt", "r") as file:
    mots = file.read().splitlines()

# Fonction pour choisir un mot aléatoire
def choisir_mot():
    return random.choice(mots)

# pour les lettres non découvertes
def afficher_mot(mot, lettres_devinees):
    affichage = ""
    for lettre in mot:
        if lettre in lettres_devinees:
            affichage += lettre + " "
        else:
            affichage += "_ "
    return affichage.strip()

# Fonction principale du jeu
def jouer_une_partie():
    mot_a_deviner = choisir_mot()
    lettres_devinees = set()
    erreurs = 0

    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in range(97, 123):  # Vérifie si la touche appuyée est une lettre
                    touche = chr(event.key).lower()
                    if touche not in lettres_devinees:
                        lettres_devinees.add(touche)
                        if touche not in mot_a_deviner:
                            erreurs += 1

        screen.fill(WHITE)

        # Afficher le mot avec les lettres devinées
        mot_affiche = afficher_mot(mot_a_deviner, lettres_devinees)
        text = font.render("Mot à deviner: " + mot_affiche, True, BLACK)
        screen.blit(text, (10, 10))

        # Vérifier si le joueur a gagné ou perdu
        if set(mot_a_deviner) <= lettres_devinees:
            text = font.render("Félicitations ! Vous avez deviné le mot : " + mot_a_deviner, True, BLACK)
            screen.blit(text, (10, 50))
            pygame.display.flip()
            pygame.time.delay(2000) 
            running = False

        elif erreurs >= 7:
            text = font.render("Vous avez perdu ! Le mot était : " + mot_a_deviner, True, BLACK)
            screen.blit(text, (10, 50))
            pygame.display.flip()
            pygame.time.delay(2000)  
            running = False

        # Afficher l'image du pendu en fonction du nombre d'erreurs
        if erreurs <= 7:
            image_path = images_pendu[erreurs - 1]
            try:
                image_pendu = pygame.image.load(image_path)
                screen.blit(image_pendu, (10, 100))
            except pygame.error as e:
                print("Erreur lors du chargement de l'image:", e)
                print("Chemin de l'image utilisé:", image_path)

        pygame.display.flip()
        clock.tick(FPS)

    # Afficher la demande de rejouer
    font_rejouer = pygame.font.Font(None, 36)
    text_rejouer = font_rejouer.render("Appuyez sur 'R' pour rejouer ou 'Q' pour quitter.", True, BLACK)
    screen.blit(text_rejouer, (10, 500))
    pygame.display.flip()

    reponse = None
    while reponse not in ['r', 'q']:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reponse = 'r'
                elif event.key == pygame.K_q:
                    reponse = 'q'

    return reponse == 'r'

# Boucle principale pour gérer les parties successives
while jouer_une_partie():
    pass

pygame.quit()
