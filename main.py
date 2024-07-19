# main.py
import tkinter as tk
from Mario_game import MarioGame, afficher_menu

def main():
    root = tk.Tk()
    root.title("Jeu Mario")
    root.geometry("1000x600")  # Ajustez la taille de la fenêtre selon vos besoins

    canvas = tk.Canvas(root, width=1000, height=600)
    canvas.pack()

    jeu = MarioGame(canvas)
    jeu.lecture_niveau("niveau1.txt")  # Assurez-vous que ce fichier existe
    jeu.affichage_niveau()
    jeu.label_timer = tk.Label(root, text="02:00", font=('Helvetica', 16))
    jeu.label_timer.place(x=700, y=10)  # Positionnez le timer selon vos besoins
    jeu.mise_a_jour_timer()  # Démarrer le timer

    root.bind('<KeyPress>', jeu.enfoncee)
    root.bind('<KeyRelease>', jeu.relachee)

    jeu.animation()  # Démarrer l'animation

    root.mainloop()

if __name__ == "__main__":
    main()
