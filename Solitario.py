import random #mi serve per mescolare le carte
import tkinter as tk #la utilizzo per disegnare le carte e la chiamo tk per comodità
from tkinter import messagebox #box per avvisi vittoria

from main import global_mazzo


#ho deciso di creare un mazzo che viene popolato tramite una funzione, che crea una carta alla volta, ad ogni carta
#corrispondono 3 caratteristiche, è scoperta (booleana), il suo valore (A,2,3...K), il suo seme (fiori, picche...)
#chiamerò questa funzione quando creerò il mazzo, passandole i valori seme e valore che tramite iterazione for
#avranno valori rispettivamente da 0 a 3 e da 0 a 12
def carta (seme,valore):
    return (seme,valore,False) #torna false perchè prima che le carte vengano distribuite sono tutte coperte
def colore_carta(carta): #questa funzione è necessaria per una questione di logica, infatti è necessario alternare il rosso con il nero
    seme=carta[0] #il primo valore della lista carta, quindi in posizione 0 è il seme
    if seme in ['♥', '♦']: #se il seme è di cuori o diamanti
        return "red" #colore rosso
    else:
        return "black" #picche e fiori
#la funzione che adesso definirò è necessaria per ottenere i valori numerici della carta, dato che nella prossima funzione vedremo che i valori possono essere in lettere
# ex. A,J,Q,K c'è bisogno di convertirli in valori numerici, quindi faremo uso di un dictionary
def valori (carta):
    valore=carta[1] #posizione 1, valori
    valori_num={'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11,'Q': 12, 'K': 13}
    #ad ogni stringa corrisponde un valore effettivo della carta
    return valori_num[valore] #facciamo tornare il valore che corrisponde alla stringa e quindi alla lettera ex: se carta[1] fosse A, allora il return varrebbe 1
#ora creeremo il nostro mazzo
def crea_mazzo ():
    mazzo=[] #una lista vuota che riempiremo tramite le altre funzioni e la funzione append
    semi = ['♥', '♦', '♠', '♣'] #i semi che possono esserci: cuori, diamanti, picche e fiori
    #ora faremo una lista simile con i valori che vanno da A a K
    valori=["A","1","2","3","4","5","6","7","8","9","10","J","Q","K"]
    #ora popoleremo il mazzo con 52 iterazioni, 13 per seme
    for seme in semi:
        for valore in valori:
            nuovacarta=carta(seme,valore) #chiamo la funzione carta per generare la carta del valore attuale del seme e del valore
            #ex: asso di cuori corrisponde a posizioni 0 0 quindi alla prima iterazione, dove passa il parametro seme ♥ e valore A
            #tornerà ad aggiungersi false ovvero carta coperta e alla seconda iterazione di passerà al 2 ♥ poi 3 fino a passare agli altri
            #semi
            mazzo.append(nuovacarta) #tramite append aggiungo alla lista del mazzo un nuovo elemento, una carta.

    #ora che abbiamo ottenuto il nostro mazzo al completo ed ordinato, tramite shuffle lo mischiamo
    random.shuffle(mazzo)
    return mazzo #la funzione restituirà il mazzo mischiato da 52 carte

#visto che ho la necessità di utilizzare alcune variabili durante tutto il codice e in diverse funzioni
#ho deciso di fare uso di variabili globali
mazzo=[]
colonnetableau=[] #7 colonne
pilariserva=[] #lista per le carte del mazzo non utilizzate
pilascarto=[] #carte pescate e non utilizzate
pilefondazione={} #dictionary perchè entrano in gioco i 4 semi
cartaselezionata=None #la prima carta che l'utente clicca
#passiamo alle variabili globali che ci serviranno per la grafica
root=None #finestra principale di gioco
canvastableau=[] #lista da 7 per i canvas del tableau che contiene 7 colonne
framefondazioni={} #dizionario per i quattro spazi che vanno dall' asso al re, necessari per la vittoria
frameriserva=None #frame per la pila di riserva
framescarto=None #frame per le carte pescate e non utilizzate
#ora assegnerò delle costanti, necessarie per le dimensioni delle carte da gioco
larghezza=70 #70 pixel di larghezza della carta
altezza=100 #100 pixel di lunghezza della carta
sovrapposizione=20 #di quanti pixel le carte sono sovrapposte verticalmente
#le due funzioni che ora scriverò serviranno all'interfaccia per convertire le lettere dei semi, in simboli e viceversa (logica: H,D,S,C)
#interfaccia tkinter:♥, ♦, ♠, ♣ 
def simboloseme(carattere): #utilizzo upper in modo da confrontare sempre con le lettere maiuscole
    if carattere.upper=="H":
        return "♥"
    if carattere.upper=="D":
        return "♦"
    if carattere.upper=="S":
        return "♠"
    if carattere.upper=="C":
        return "♣"
    # nel caso in cui non dovesse essere nessuno dei 4 carta allora return none
    return None
def carattereseme (simbolo):  #qui non abbiamo bisogno di upper perchè si tratta di simboli
    if simbolo== "♥":
        return "H"
    if simbolo== "♦":
        return "D"
    if simbolo== "♠":
        return "S"
    if simbolo== "♣":
        return "C"
    #nel caso in cui non dovesse essere nessuno dei 4 simboli allora return none
    return None

