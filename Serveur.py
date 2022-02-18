import tkinter as tk
import socket as soc
import os
import time


def debut():
    global server_socket, t_IP, t_PORT, Fen, txt_etat
    Fen = tk.Tk()
    Fen.title("Tunnel de données (Serveur)")
    Fen.geometry("400x150")

    txt_etat = tk.Label(Fen, text="Erreur.")
    txt_etat.grid(row=0, column=0, columnspan=4)
    attente()

    B_envoyer = tk.Button(Fen, text="Envoyer", command=envoyer)
    B_envoyer.grid(row=2, column=1)

    B_recevoir = tk.Button(Fen, text="Recevoir", command=recevoir)
    B_recevoir.grid(row=2, column=3)

    MSG_IP = tk.Label(Fen, text="IP:")
    MSG_IP.grid(row=1, column=0)

    t_IP = tk.StringVar()
    D_IP = tk.Entry(Fen, textvariable=t_IP, bg='white', fg='black')
    D_IP.grid(row=1, column=1)

    MSG_PORT = tk.Label(Fen, text="Port:")
    MSG_PORT.grid(row=1, column=2)

    t_PORT = tk.StringVar()
    D_PORT = tk.Entry(Fen, textvariable=t_PORT, bg='white', fg='black')
    D_PORT.grid(row=1, column=3)

    B_connexion = tk.Button(Fen, text="Connexion", command=connexion)
    B_connexion.grid(row=1, column=4)

    B_fermer = tk.Button(Fen, text="Fermer", command=fermer)
    B_fermer.grid(row=3, column=1)

    Fen.mainloop()

def envoyer():
    global path_env
    debut = time.time()
    fichiers = os.listdir(path_env)
    print(fichiers)
    nbre_de_fichiers = str(len(fichiers))
    message = nbre_de_fichiers.encode('utf-8')
    client_socket.send(message)
    a = client_socket.recv(2).decode('utf-8')
    if a != "ok":
        print("Erreur")
    i = 0
    for nom_fichier in fichiers:
        i += 1
        message = nom_fichier.encode('utf-8')
        client_socket.send(message)
        a = client_socket.recv(2).decode('utf-8')
        if not a == "ok":
            print("Erreur")
        fichier = path_env+"\\"+nom_fichier
        taille = os.path.getsize(fichier)
        message = str(taille).encode('utf-8')
        client_socket.send(message)
        a = client_socket.recv(2).decode('utf-8')
        if not a == "ok":
            print("Erreur")
        num = 1
        with open(fichier, "rb") as f:
            while num <= taille:
                if taille-num > 10000000:
                    octet = f.read(10000000)
                    client_socket.send(octet)
                    num += 10000000
                elif taille-num > 1000000:
                    octet = f.read(1000000)
                    client_socket.send(octet)
                    num += 1000000
                elif taille-num > 100000:
                    octet = f.read(100000)
                    client_socket.send(octet)
                    num += 100000
                elif taille-num > 10000:
                    octet = f.read(10000)
                    client_socket.send(octet)
                    num += 10000
                elif taille - num > 1000:
                    octet = f.read(1000)
                    client_socket.send(octet)
                    num += 1000
                elif taille-num > 100:
                    octet = f.read(100)
                    client_socket.send(octet)
                    num += 100
                else:
                    octet = f.read(1)
                    client_socket.send(octet)
                    num += 1
                print("Fichier numéro",i,"sur",nbre_de_fichiers,". Paquet numéro", num - 1, "/", taille, "envoyé. Progression:", str(((num - 1) / taille) * 100), "%")
                a = client_socket.recv(2).decode('utf-8')
                if not a == "ok":
                    print("Erreur")
        fin = time.time()
        print("Envoi de {taille} octets réussi en {temps} secondes.".format(taille = taille, temps = fin-debut))
        debut = time.time()

def recevoir():
    global client_socket, Taille_du_fichier, num
    nbre_de_fichiers = int(client_socket.recv(100).strip().decode('utf-8'))
    msg = "ok".encode('utf-8')
    client_socket.send(msg)
    i = 1
    while i <= nbre_de_fichiers:
        Nom_du_fichier = b''
        while Nom_du_fichier == b'':
            Nom_du_fichier = client_socket.recv(100).strip().decode('utf-8')
        msg = "ok".encode('utf-8')
        client_socket.send(msg)
        Taille_du_fichier = b''
        while Taille_du_fichier == b'':
            Taille_du_fichier = int(client_socket.recv(100).strip().decode('utf-8'))
        msg = "ok".encode('utf-8')
        client_socket.send(msg)
        print(Taille_du_fichier)
        fichier = path_rec+'\\'+Nom_du_fichier
        num = 1
        donnees = b''
        while num <= Taille_du_fichier:
            if Taille_du_fichier-num > 10000000:
                octet = client_socket.recv(10000000)
                num += 10000000
            elif Taille_du_fichier-num > 1000000:
                octet = client_socket.recv(1000000)
                num += 1000000
            elif Taille_du_fichier-num > 100000:
                octet = client_socket.recv(100000)
                num += 100000
            elif Taille_du_fichier-num > 10000:
                octet = client_socket.recv(10000)
                num += 10000
            elif Taille_du_fichier - num > 1000:
                octet = client_socket.recv(1000)
                num += 1000
            elif Taille_du_fichier - num > 100:
                octet = client_socket.recv(100)
                num += 100
            else:
                octet = client_socket.recv(1)
                num += 1
            donnees += octet
            print("Fichier numéro",i,"sur",nbre_de_fichiers,". Paquet numéro", num - 1, "/", Taille_du_fichier, "reçu. Progression:", str(((num - 1) / Taille_du_fichier) * 100), "%")
            msg = "ok".encode('utf-8')
            client_socket.send(msg)
        with open (fichier, "wb") as f:
            f.write(donnees)
        i += 1
    print("Opération terminée")

def fermer():
    global path_env, path_rec
    try:
        os.removedirs(path_env)
        os.removedirs(path_rec)
    except:
        print("Clean")

def connexion():
    global server_socket, client_socket
    try:
        IP = str(t_IP.get())
        PORT = int(t_PORT.get())
        #print(type(IP), IP, type(PORT), PORT)
        server_socket = soc.socket(soc.AF_INET, soc.SOCK_STREAM)
        server_socket.bind((IP, PORT))
        server_socket.listen(5)
        client_socket, adresse = server_socket.accept()
        co_reu()
    except Exception as e:
        Fen.after(2000, attente)
        co_echec()
        print(e)

def co_echec():
    txt_etat.config(text="Connexion échouée.")

def co_reu():
    global path_env, path_rec
    txt_etat.config(text="Connexion établie.")
    path = os.path.expanduser("~")
    try:
        path_env = path + "\\Desktop\\Envoyer (Serveur TDD)"
        path_rec = path + "\\Desktop\\Recevoir (Serveur TDD)"
        os.mkdir(path_env)
        os.mkdir(path_rec)
        txt_etat.config(text="Bureau localisé.")
    except:
        try:
            path_env = path + "\\Bureau\\Envoyer (Serveur TDD)"
            path_rec = path + "\\Bureau\\Recevoir (Serveur TDD)"
            os.mkdir(path_env)
            os.mkdir(path_rec)
            txt_etat.config(text="Bureau localisé.")
        except:
            try:
                path_env = path + "\\OneDrive\\Bureau\\Envoyer (Serveur TDD)"
                path_rec = path + "\\OneDrive\\Bureau\\Recevoir (Serveur TDD)"
                os.mkdir(path_env)
                os.mkdir(path_rec)
                txt_etat.config(text="Bureau localisé.")
            except:
                txt_etat.config(text="Échec lors de la recherche du path du bureau.")
        print(path_env)

def attente():
    txt_etat.config(text="En attente de connexion.")

debut()