import tkinter as tk
import pygame

# Classe de base pour les entités du jeu comme Mario et Goomba
class EntiteJeu:
    def __init__(self, canvas, x, y, image):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.image = image
        self.sprite = self.canvas.create_image(self.x, self.y, image=self.image)

    def deplacer(self, dx, dy):
        self.x += dx
        self.y += dy
        self.canvas.coords(self.sprite, self.x, self.y)

# Classe pour les éléments du niveau comme Brique et Echelle
class Brique:
    def __init__(self, canvas, x, y, image):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.image = image
        self.sprite = self.canvas.create_image(self.x, self.y, image=self.image)

    def afficher(self):
        self.canvas.coords(self.sprite, self.x, self.y)

class Echelle:
    def __init__(self, canvas, x, y, image):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.image = image
        self.sprite = self.canvas.create_image(self.x, self.y, image=self.image)

    def afficher(self):
        self.canvas.coords(self.sprite, self.x, self.y)

# Classe concrète pour Mario
class Mario(EntiteJeu):
    def deplacer(self, dx, dy):
        self.x += dx
        self.y += dy
        self.canvas.coords(self.sprite, self.x, self.y)

# Classe concrète pour Goomba
class Goomba(EntiteJeu):
    def deplacer(self, dx, dy):
        self.x += dx
        self.y += dy
        self.canvas.coords(self.sprite, self.x, self.y)

# Classe principale du jeu
class MarioGame:
    def __init__(self, canvas):
        self.canvas = canvas
        self.fond_ecran = None
        self.champis_ramasse = 0
        self.champis = []
        self.niveau = []
        self.touches = []
        self.Vm = 40
        self.Vg = 40
        self.niveau_actuel = 1
        self.temps_restant = 120  # 2 minutes en secondes
        self.labels = []  # Liste pour stocker les labels

        # Chargement des images
        self.img_brique = tk.PhotoImage(file="images/brick.png")
        self.img_echelle = tk.PhotoImage(file="images/echelle.gif")
        self.img_cube = tk.PhotoImage(file="images/cube.png")
        self.img_goomba = tk.PhotoImage(file="images/goomba.png")
        self.img_goombaD = tk.PhotoImage(file="images/goombaD.png")
        self.img_mario = tk.PhotoImage(file="images/mario.png")
        self.img_marioG = tk.PhotoImage(file="images/marioG.png")
        self.img_champi = tk.PhotoImage(file="images/champi.png")
        self.img_fond = tk.PhotoImage(file="images/ciel.png")

        self.goomba = None
        self.mario = None
        self.label_timer = None

    def lecture_niveau(self, fichier):
        with open(fichier, 'r') as f:
            self.niveau = [list(ligne.strip()) for ligne in f]

    def affichage_niveau(self):
        self.canvas.delete("all")
        self.champis.clear()
        TB = 40  # Taille du bloc
        Y = TB // 2
        for ligne in self.niveau:
            X = TB // 2
            for case in ligne:
                if case == 'X':
                    Brique(self.canvas, X, Y, self.img_brique)
                elif case == 'H':
                    Echelle(self.canvas, X, Y, self.img_echelle)
                elif case == 'T':
                    Brique(self.canvas, X, Y, self.img_cube)
                elif case == 'G':
                    self.goomba = Goomba(self.canvas, X, Y, self.img_goomba)
                elif case == 'M':
                    self.mario = Mario(self.canvas, X, Y, self.img_mario)
                elif case == 'C':
                    self.champis.append(self.canvas.create_image(X, Y, image=self.img_champi))
                X += TB
            Y += TB

    def mise_a_jour_timer(self):
        if self.temps_restant > 0:
            self.temps_restant -= 1
            minutes = self.temps_restant // 60
            secondes = self.temps_restant % 60
            self.label_timer.config(text=f"{minutes:02}:{secondes:02}")
            self.canvas.after(1000, self.mise_a_jour_timer)
        else:
            self.canvas.delete(self.mario.sprite)
            self.canvas.delete(self.goomba.sprite)
            label_temps_ecoule = tk.Label(self.canvas, text="Temps écoulé!", font=('Helvetica', 16))
            label_temps_ecoule.place(x=320, y=280)
            self.labels.append(label_temps_ecoule)  # Ajouter le label à la liste
            self.canvas.after(2000, afficher_menu)  # Retourner à la page d'accueil après 2 secondes

    def animation(self):
        TB = 40  # Taille du bloc
        Xg, Yg = self.canvas.coords(self.goomba.sprite)
        Xg = int(Xg)
        Yg = int(Yg)
        Xm, Ym = self.canvas.coords(self.mario.sprite)
        Xm = int(Xm)
        Ym = int(Ym)

        # Déplacement Mario
        if 'Right' in self.touches and self.niveau[Ym // 40][Xm // 40 + 1] not in ['X', 'T', 'W']:
            self.canvas.itemconfig(self.mario.sprite, image=self.img_mario)
            Xm = Xm + self.Vm

        if 'Left' in self.touches and self.niveau[Ym // 40][Xm // 40 - 1] not in ['X', 'T', 'W']:
            self.canvas.itemconfig(self.mario.sprite, image=self.img_marioG)
            Xm = Xm - self.Vm

        if 'Up' in self.touches and self.niveau[Ym // 40][Xm // 40] == 'H':
            Ym = Ym - self.Vm

        if 'Down' in self.touches and self.niveau[Ym // 40 + 1][Xm // 40] == 'H':
            Ym = Ym + self.Vm

        # Déplacement goomba
        if 'd' in self.touches and self.niveau[Yg // 40][Xg // 40 + 1] not in ['X', 'T', 'W']:
            self.canvas.itemconfig(self.goomba.sprite, image=self.img_goombaD)
            Xg = Xg + self.Vg

        if 'q' in self.touches and self.niveau[Yg // 40][Xg // 40 - 1] not in ['X', 'T', 'W']:
            self.canvas.itemconfig(self.goomba.sprite, image=self.img_goomba)
            Xg = Xg - self.Vg

        if 'z' in self.touches and self.niveau[Yg // 40][Xg // 40] == 'H':
            Yg = Yg - self.Vg

        if 's' in self.touches and self.niveau[Yg // 40 + 1][Xg // 40] == 'H':
            Yg = Yg + self.Vg

        # Chute
        if self.niveau[Ym // 40 + 1][Xm // 40] == ' ':
            Ym += self.Vm

        if self.niveau[Yg // 40 + 1][Xg // 40] == ' ':
            Yg += self.Vg

        # Collision
        if Xg - 20 < Xm < Xg + 20 and Yg - 20 < Ym < Yg + 20:
            self.fin_de_partie("Ne lâche pas et retente !!!")

        # Ramassage champignon
        for champi in self.champis:
            Xc, Yc = self.canvas.coords(champi)
            if Xc - 20 < Xm < Xc + 20 and Yc - 20 < Ym < Yc + 20:
                self.canvas.delete(champi)
                self.champis.remove(champi)
                self.champis_ramasse += 1
                if self.champis_ramasse == 6:
                    if self.niveau_actuel == 1:
                        self.niveau_actuel = 2
                        self.lecture_niveau("niveau2.txt")
                        self.affichage_niveau()
                        self.champis_ramasse = 0
                    else:
                        self.canvas.delete(self.goomba.sprite)
                        label_game_over = tk.Label(self.canvas, text="Félicitations, vous avez gagné !", font=('Helvetica', 16, 'bold'), fg='red')
                        label_game_over.place(x=TB * 10, y=TB * 7)
                        self.labels.append(label_game_over)  # Ajouter le label à la liste
                        self.canvas.after(2000, afficher_menu)  # Retourner à la page d'accueil après 2 secondes
                        return

        self.canvas.coords(self.goomba.sprite, Xg, Yg)
        self.canvas.coords(self.mario.sprite, Xm, Ym)
        self.canvas.after(40, self.animation)

    def fin_de_partie(self, message):
        self.canvas.delete(self.mario.sprite)
        self.canvas.delete(self.goomba.sprite)
        label_fin = tk.Label(self.canvas, text=message, font=('Helvetica', 16, 'bold'), fg='red')
        label_fin.place(x=400, y=280)
        self.labels.append(label_fin)  # Ajouter le label à la liste
        self.canvas.after(2000, afficher_menu)

    def reset(self):
        self.champis_ramasse = 0
        self.champis.clear()
        self.touches.clear()
        self.niveau_actuel = 1
        self.temps_restant = 120
        self.canvas.delete("all")
        for label in self.labels:  # Supprimer tous les labels
            label.destroy()
        self.labels.clear()

    def start(self):
        if self.niveau_actuel == 1:
            self.lecture_niveau("niveau1.txt")
        else:
            self.lecture_niveau("niveau2.txt")
        self.affichage_niveau()
        self.label_timer = tk.Label(self.canvas, text="", font=('Helvetica', 16, 'bold'), fg='Red')
        self.label_timer.place(x=800, y=10)
        self.labels.append(self.label_timer)  # Ajouter le label à la liste
        self.mise_a_jour_timer()

    def play(self):
        self.animation()

    def stop(self):
        # Vous pouvez ajouter d'autres actions d'arrêt ici si nécessaire
        pass

    def enfoncee(self, event):
        touche = event.keysym
        if event.keysym not in self.touches:
            self.touches.append(touche)

    def relachee(self, event):
        touche = event.keysym
        if touche in self.touches:
            self.touches.remove(touche)


def afficher_menu():
    menu_frame.pack(fill='both', expand=True)
    game_canvas.pack_forget()


def lancer_jeu():
    game.reset()
    menu_frame.pack_forget()
    game_canvas.pack(fill='both', expand=True)
    game.niveau_actuel = 1  # Réinitialiser au premier niveau
    game.start()
    game.play()


def quitter_jeu():
    root.quit()


root = tk.Tk()
root.title("Mario Game")
root.geometry("1000x600")

# Initialisation du module de musique pygame
pygame.mixer.init()
pygame.mixer.music.load("Music.mp3")
pygame.mixer.music.play(-1)

menu_frame = tk.Frame(root, bg='Red')
titre_label = tk.Label(menu_frame, text="Mario Game", font=('Helvetica', 24), bg='lightblue')
titre_label.pack(pady=20)
bouton_lancer = tk.Button(menu_frame, text="Lancer le jeu", font=('Helvetica', 16), command=lancer_jeu)
bouton_lancer.pack(pady=10)
bouton_quitter = tk.Button(menu_frame, text="Quitter", font=('Helvetica', 16), command=quitter_jeu)
bouton_quitter.pack(pady=10)
menu_frame.pack(fill='both', expand=True)

game_canvas = tk.Canvas(root, width=1000, height=600)
game = MarioGame(game_canvas)

root.bind("<KeyPress>", game.enfoncee)
root.bind("<KeyRelease>", game.relachee)

root.mainloop()
