import \
    random  # Questa è una "scatola di strumenti" di Python. La usiamo per mescolare le carte a caso, così ogni partita è una sorpresa!
import \
    tkinter as tk  # Questa è un'altra "scatola di strumenti". È il "muratore" del nostro gioco: ci aiuta a creare finestre, pulsanti e disegnare le carte sullo schermo.
from tkinter import messagebox  # Reintrodotto per i messaggi di vittoria.


# --- PARTE 1: Come sono fatte le nostre carte (le "carte-biglietto") ---
# Nel nostro gioco, una carta non è un oggetto complicato. Immagina che ogni carta sia come un semplice "biglietto"
# scritto a mano con tre informazioni importanti, messe in un ordine preciso:
# [ il_seme_della_carta, il_valore_della_carta, è_coperta_o_scoperta ]

# Esempi di "biglietti-carta":
# ['♥', 'A', True]   -> Significa: è l'Asso (A) di Cuori (♥), ed è "scoperta" (True significa visibile).
# ['♠', 'K', False]  -> Significa: è il Re (K) di Picche (♠), ed è "coperta" (False significa nascosta, vedi il retro).

# Questa è la nostra prima "funzione". Una funzione è come una "ricetta" o un "piccolo robot"
# che sa fare un compito specifico e ripeterlo.
# Il nome della funzione è 'crea_carta'.
# Le cose tra parentesi (seme, valore) sono gli "ingredienti" che devi dare a questa ricetta.
def crea_carta(seme, valore):
    # Questo è il risultato della nostra "ricetta crea_carta":
    # crea un nuovo "biglietto" (una lista) con le informazioni della carta.
    # Ogni volta che creiamo una carta, all'inizio è sempre "coperta" (False),
    # perché le carte vengono distribuite a faccia in giù.
    return [seme, valore, False]  # Restituisce (cioè, "ti dà indietro") la lista della nuova carta.


# Questa è un'altra "funzione" (ricetta) ci dice se una carta è "rossa" o "nera".
# Prende come "ingrediente" una 'carta' (cioè una lista come ['♥', 'A', True]).
def ottieni_colore_carta(carta):
    # La prima informazione sul nostro "biglietto-carta" è il seme (il suo "posto" nella lista è l'indice 0).
    seme = carta[0]
    # Ora controlliamo il seme:
    # Se il seme è Cuori (♥) o Quadri (♦), allora la carta è rossa.
    if seme in ['♥', '♦']:  # 'in' è un modo per dire "questo seme è presente in questa lista di semi rossi?".
        return "red"  # Se la condizione è vera (il seme è rosso), restituisci la parola "red".
    # Altrimenti (cioè, se il seme non è Cuori né Quadri, quindi è Picche ♠ o Fiori ♣)...
    else:
        return "black"  # ...allora la carta è nera, quindi restituisci la parola "black".


# Questa funzione (ricetta) ci serve per sapere il "valore numerico" di una carta.
# Ad esempio, l'Asso vale 1, il 2 vale 2, la Regina vale 12, il Re vale 13.
# Questo è fondamentale perché nel Solitario le carte si mettono in ordine decrescente (es. un 2 va su un 3).
# Prende come "ingrediente" una 'carta'.
def ottieni_valore_numerico_carta(carta):
    # La seconda informazione sul nostro "biglietto-carta" è il valore (indice 1).
    valore_simbolo = carta[1]  # Questo sarà una scritta come 'A', '2', '10', 'J', 'Q', 'K'.
    # Questo è un "dizionario". Immagina un dizionario come un elenco telefonico:
    # a ogni "nome" (il simbolo della carta) corrisponde un "numero di telefono" (il valore numerico).
    # È come un libretto: 'A' -> 1, '2' -> 2, ..., 'K' -> 13.
    valori_numerici = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11,
                       'Q': 12, 'K': 13}
    # Restituisce il numero corrispondente al simbolo della carta che abbiamo cercato nel dizionario.
    return valori_numerici[valore_simbolo]


# --- PARTE 2: Il Mazzo di Carte (la "scatola di carte mescolate") ---
# Il mazzo di carte è semplicemente una "lista" grande che contiene tutti i nostri 52 "biglietti-carta".

# Questa funzione è la ricetta per preparare un mazzo completo di 52 carte e mescolarlo bene.
def crea_mazzo_completo():
    mazzo = []  # Iniziamo con una lista completamente vuota. Sarà il nostro mazzo.
    semi = ['♥', '♦', '♠', '♣']  # Questa lista contiene tutti i tipi di semi che useremo.
    valori = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q',
              'K']  # Questa lista contiene tutti i valori delle carte.

    # Questo è un "doppio ciclo". Immagina che per ogni tipo di seme...
    for seme in semi:  # ...fai un giro (prima per '♥', poi per '♦', ecc.)...
        # ...e per ogni giro del seme, fai un altro giro per tutti i valori.
        for valore in valori:  # (prima 'A', poi '2', ecc., per il seme corrente).
            nuova_carta = crea_carta(seme,
                                     valore)  # Usiamo la nostra ricetta 'crea_carta' per creare un biglietto-carta.
            mazzo.append(nuova_carta)  # Aggiungiamo il biglietto-carta appena creato alla fine della lista 'mazzo'.

    random.shuffle(mazzo)  # Qui usiamo lo strumento 'shuffle' (che significa "mescola") dalla scatola 'random'.
    # Questo è fondamentale! Mescola tutte le carte nella lista 'mazzo' in modo casuale,
    # così il gioco è sempre diverso ogni volta che inizi una nuova partita.
    return mazzo  # Restituiamo la lista 'mazzo' che ora è piena di carte mescolate.


# --- PARTE 3: Le Variabili Globali del Gioco (le "scatole centrali") ---
# Queste variabili sono speciali: sono "globali". Immagina che siano delle "scatole molto grandi"
# che abbiamo messo al centro del tavolo.
# Qualsiasi "ricetta" (funzione) nel nostro programma può vedere cosa c'è dentro queste scatole
# e può anche cambiarne il contenuto.
# Servono a tenere traccia di tutto quello che succede nel gioco, come un "cervello" del Solitario.

global_mazzo = []  # Questa è la scatola per le carte del mazzo principale (quelle da cui si distribuisce all'inizio).
global_colonne_tableau = []  # Questa è una scatola grande che contiene 7 scatoline più piccole. Ogni scatolina è una "colonna" del tabellone principale del Solitario. Dentro ogni scatolina ci sono delle carte impilate.
global_pila_riserva = []  # Questa scatola contiene le carte che restano dopo la distribuzione iniziale. Il giocatore può "pescare" da qui.
global_pila_scarto = []  # Questa scatola contiene la carta più recente che il giocatore ha pescato dalla pila di riserva.

# Questa è una scatola speciale: un "dizionario" con 4 scomparti "nominati" (uno per i Cuori, uno per i Quadri, uno per le Picche, uno per i Fiori).
# Qui vengono accumulate le carte in ordine crescente (Asso, 2, 3... fino al Re) per ogni seme.
global_pile_fondazioni = {}

global_carta_selezionata_info = None  # Questa è la scatola che ricorda quale carta hai cliccato per prima (quella che si illumina di giallo).
# Quando una carta è selezionata, questa scatola conterrà un "biglietto" (un dizionario) con 4 informazioni su quella carta:
# {'carta_dati': la_nostra_lista_carta,             # Il biglietto-carta vero e proprio (es. ['♥', 'A', True])
#  'tipo_sorgente': da_dove_viene_la_carta,         # È una scritta: 'tableau' (se viene da una colonna) o 'discard' (se viene dalla pila di scarto)
#  'indice_sorgente': il_numero_della_colonna,      # Il numero della colonna da cui viene (da 0 a 6). Se viene da 'discard', sarà None (niente).
#  'indice_carta_nella_sorgente': la_posizione_della_carta_nella_colonna} # La posizione della carta nella sua colonna (0 è la più in alto). Se viene da 'discard', sarà None.

# Variabili che si riferiscono agli "oggetti" grafici che il nostro "muratore" Tkinter crea sullo schermo.
global_root = None  # Questa è la "finestra" principale del gioco. Immagina sia il grande foglio bianco dove disegniamo tutto.
global_canvas_tableau = []  # Questa è una lista di 7 "tele da disegno" (chiamate 'canvas'). Ogni tela è dedicata a disegnare le carte di una colonna del tabellone.
global_frame_fondazioni = {}  # Questo è un dizionario di 4 "scatole invisibili" (chiamate 'frame') per le pile finali. Le usiamo per tenere in ordine le carte delle fondazioni.
global_frame_stock = None  # Questa è la "scatola invisibile" per l'area della pila di riserva.
global_frame_discard = None  # Questa è la "scatola invisibile" per l'area della pila di scarto.

# Queste sono delle "costanti", cioè dei numeri fissi che non cambiano mai nel gioco.
LARGHEZZA_CARTA = 70  # La larghezza (in pixel, i puntini sullo schermo) di ogni carta.
ALTEZZA_CARTA = 100  # L'altezza (in pixel) di ogni carta.
SOVRAPPOSIZIONE_Y = 20  # Quanti pixel le carte si sovrappongono verticalmente nelle colonne del tabellone. Questo crea l'effetto "a cascata" per farle vedere tutte.


# --- PARTE 4: Funzioni di Aiuto per Tkinter e il Gioco (piccole ricette utili) ---

# Questa funzione converte un carattere breve per il seme (tipo 'H' per Cuori) nel simbolo vero (tipo '♥').
# Ci aiuta a passare tra il modo in cui pensiamo ai semi nel codice e come li vede il giocatore.
def _ottieni_simbolo_seme(carattere_breve):
    if carattere_breve.upper() == 'H': return '♥'  # '.upper()' trasforma il carattere in maiuscolo, così funziona sia con 'h' che con 'H'.
    if carattere_breve.upper() == 'D': return '♦'
    if carattere_breve.upper() == 'S': return '♠'
    if carattere_breve.upper() == 'C': return '♣'
    return None  # Se il carattere non è uno dei nostri semi, restituisce "niente".


# Questa funzione fa il contrario: converte un simbolo del seme (tipo '♥') nel carattere breve (tipo 'H').
# È utile per le chiavi nei nostri dizionari.
def _ottieni_carattere_seme(simbolo_completo):
    if simbolo_completo == '♥': return 'H'
    if simbolo_completo == '♦': return 'D'
    if simbolo_completo == '♠': return 'S'
    if simbolo_completo == '♣': return 'C'
    return None


# La funzione mostra_messaggio è stata rimossa, in quanto ora usiamo print direttamente per il debug.
# def mostra_messaggio(titolo, messaggio):
#     print(f"MESSAGGIO: {titolo} - {messaggio}")

# --- PARTE 5: Funzioni per Disegnare le Carte e il Tabellone (le "ricette del pittore") ---

# Questa è una funzione molto importante: disegna una singola carta sulla nostra "tela da disegno" (un canvas).
# È come dare istruzioni dettagliate a un pittore per disegnare un solo biglietto-carta.
# 'canvas_area': la tela specifica dove disegnare (es. la tela della colonna 0).
# 'carta_da_disegnare': il biglietto-carta (lista) che dobbiamo disegnare.
# 'x_pos', 'y_pos': le coordinate (where to start drawing the ticket, from the top left corner).
# 'indice_colonna', 'indice_carta_in_colonna': informazioni extra per sapere dove si trova la carta nel gioco (ci servono per i clic).
def disegna_carta_su_canvas(canvas_area, carta_da_disegnare, x_pos, y_pos, indice_colonna, indice_carta_in_colonna):
    # Qui decidiamo i colori della carta in base al suo stato (se è coperta o scoperta).
    if carta_da_disegnare[2]:  # Se la carta è scoperta (il terzo elemento della lista è True)...
        colore_carta_testo = ottieni_colore_carta(
            carta_da_disegnare)  # ...usiamo la nostra ricetta per sapere se è "red" o "black".
        colore_riempimento = "white"  # Lo sfondo della carta scoperta sarà bianco.
        colore_testo = "red" if colore_carta_testo == "red" else "black"  # Il colore del testo (numero/simbolo) dipende dal colore del seme.
        colore_bordo = colore_testo  # Il bordo della carta scoperta sarà dello stesso colore del testo.
    else:  # Se la carta è coperta (il terzo elemento della lista è False)...
        colore_riempimento = "#8B0000"  # Lo sfondo sarà rosso scuro (per fare il retro della carta).
        colore_testo = "white"  # Il testo "Retro" sarà bianco.
        colore_bordo = "#4a5568"  # Il bordo del retro sarà grigio scuro.

    # Disegniamo la forma rettangolare della carta sulla tela.
    # 'canvas_area.create_rectangle' disegna un rettangolo. Gli diamo 4 numeri:
    # 1. 'x_pos': la coordinata X di partenza (sinistra).
    # 2. 'y_pos': la coordinata Y di partenza (alto).
    # 3. 'x_pos + LARGHEZZA_CARTA': la coordinata X di arrivo (destra).
    # 4. 'y_pos + ALTEZZA_CARTA': la coordinata Y di arrivo (basso).
    # 'fill' è il colore di riempimento interno, 'outline' è il colore del bordo, 'width' è lo spessore del bordo.
    rettangolo_carta = canvas_area.create_rectangle(x_pos, y_pos, x_pos + LARGHEZZA_CARTA, y_pos + ALTEZZA_CARTA,
                                                    fill=colore_riempimento, outline=colore_bordo, width=1)

    if carta_da_disegnare[2]:  # Se la carta è scoperta, disegniamo il suo valore e il suo seme.
        # Disegniamo il valore (es. 'A', '2') nell'angolo in alto a sinistra della carta.
        # 'anchor="nw"' significa che il testo si attacca all'angolo "North-West" (alto-sinistra).
        canvas_area.create_text(x_pos + 10, y_pos + 10, text=carta_da_disegnare[1], anchor="nw",
                                font=("Arial", 12, "bold"), fill=colore_testo)
        # Disegniamo il valore anche nell'angolo in basso a destra (capovolto, per un effetto più realistico).
        # 'anchor="se"' significa "South-East" (basso-destra).
        canvas_area.create_text(x_pos + LARGHEZZA_CARTA - 10, y_pos + ALTEZZA_CARTA - 10, text=carta_da_disegnare[1],
                                anchor="se", font=("Arial", 12, "bold"), fill=colore_testo)
        # Disegniamo il simbolo del seme (es. '♥', '♠') al centro della carta, più grande.
        # 'anchor="center"' centra il testo.
        canvas_area.create_text(x_pos + LARGHEZZA_CARTA / 2, y_pos + ALTEZZA_CARTA / 2, text=carta_da_disegnare[0],
                                anchor="center", font=("Arial", 24), fill=colore_testo)
    else:  # Se la carta è coperta, disegniamo semplicemente la scritta "Retro" al centro.
        canvas_area.create_text(x_pos + LARGHEZZA_CARTA / 2, y_pos + ALTEZZA_CARTA / 2, text="Retro", anchor="center",
                                font=("Arial", 10, "bold"), fill=colore_testo)

    # Questa parte è CRUCIALE per far funzionare i clic del mouse sulle carte.
    # Colleghiamo la nostra "ricetta gestisci_click_carta" a questo rettangolo (la carta disegnata).
    # 'tag_bind' serve a dire: "Quando qualcuno clicca su questo elemento disegnato (il rettangolo della carta), esegui questa ricetta".
    # "<Button-1>" significa specificamente "il clic con il pulsante sinistro del mouse".
    # `lambda event: ...` è un modo rapido e comodo per creare una mini-ricetta "al volo".
    # Questa mini-ricetta, quando viene chiamata dal clic, a sua volta chiama la nostra ricetta 'gestisci_click_carta'
    # passando tutte le informazioni necessarie sulla carta che è stata cliccata.
    canvas_area.tag_bind(rettangolo_carta, "<Button-1>",
                         lambda event: gestisci_click_carta(event, carta_da_disegnare, 'tableau', indice_colonna,
                                                            indice_carta_in_colonna))
    # Facciamo la stessa cosa anche per l'area occupata dal testo e dai simboli della carta.
    # 'find_enclosed' trova tutti gli elementi disegnati all'interno di una certa area (cioè il testo e i simboli della carta).
    # Questo assicura che tu possa cliccare ovunque sulla carta (anche sul numero o sul seme) e il clic funzioni.
    canvas_area.tag_bind(canvas_area.find_enclosed(x_pos, y_pos, x_pos + LARGHEZZA_CARTA, y_pos + ALTEZZA_CARTA),
                         "<Button-1>",
                         lambda event: gestisci_click_carta(event, carta_da_disegnare, 'tableau', indice_colonna,
                                                            indice_carta_in_colonna))

    # Se questa carta è quella che abbiamo "preso" (cioè la scatola 'global_carta_selezionata_info' contiene le sue informazioni)...
    global global_carta_selezionata_info
    if global_carta_selezionata_info and global_carta_selezionata_info['carta_dati'] == carta_da_disegnare:
        # ...allora disegniamo un bordo giallo più spesso intorno alla carta per mostrare che è selezionata.
        canvas_area.create_rectangle(x_pos, y_pos, x_pos + LARGHEZZA_CARTA, y_pos + ALTEZZA_CARTA, outline="yellow",
                                     width=3)


# Questa funzione disegna solo la carta che sta in cima a un "frame" (una delle nostre scatole invisibili).
# La usiamo per disegnare la carta visibile nelle fondazioni (le pile finali), nella pila di riserva e nella pila di scarto.
def disegna_carta_in_frame(frame_area, carta_da_disegnare):
    # Prima di disegnare la nuova carta, dobbiamo "pulire" il frame, togliendo qualsiasi cosa ci fosse prima disegnata.
    for widget in frame_area.winfo_children():  # Cicla su tutti gli elementi (chiamati 'widget') che sono dentro questo 'frame_area'.
        widget.destroy()  # 'destroy()' li rimuove dalla finestra, come se li cancellassimo.

    # Creiamo un'etichetta (chiamata 'Label' in Tkinter). Un Label è un elemento semplice che mostra testo o immagini.
    # Qui, la usiamo per "disegnare" la nostra carta in queste aree (fondazioni, riserva, scarto).
    carta_etichetta = tk.Label(frame_area, width=LARGHEZZA_CARTA // 10, height=ALTEZZA_CARTA // 10, relief="raised",
                               bd=2)

    if carta_da_disegnare[2]:  # Se la carta è scoperta (il suo terzo elemento è True)...
        carta_etichetta.config(bg="white", fg=ottieni_colore_carta(
            carta_da_disegnare))  # ...lo sfondo sarà bianco, il testo rosso o nero.
        # Mettiamo il valore e il seme della carta come testo sull'etichetta.
        carta_etichetta.config(text=f"{carta_da_disegnare[1]}\n{carta_da_disegnare[0]}", font=("Arial", 12, "bold"))
    else:  # Se la carta è coperta...
        carta_etichetta.config(bg="#8B0000", fg="white", text="Retro",
                               font=("Arial", 8, "bold"))  # ...sfondo rosso scuro, testo "Retro" bianco.

    carta_etichetta.pack(
        expand=True)  # Posiziona l'etichetta al centro del frame, facendola espandere per riempire lo spazio disponibile.
    return carta_etichetta  # Restituiamo l'etichetta creata. Questo è utile perché potremmo voler collegare un clic ad essa.


# Questa è la "ricetta" più grande e importante del nostro pittore: ridisegna TUTTO il tabellone di gioco.
# Viene chiamata ogni volta che succede qualcosa nel gioco (un clic, una mossa, una pesca) per aggiornare lo schermo e far vedere i cambiamenti.
def disegna_tabellone():
    # Dobbiamo dire a Python che useremo e potremmo cambiare queste "scatole centrali" (variabili globali).
    global global_canvas_tableau, global_frame_fondazioni, global_frame_stock, global_frame_discard
    global global_pila_riserva, global_pila_scarto, global_pile_fondazioni, global_colonne_tableau
    global global_carta_selezionata_info  # Anche la scatola che tiene la carta selezionata.

    # STEP 1: PULIRE LO SCHERMO prima di ridisegnare.

    # Pulisci tutte le "tele da disegno" delle colonne del tabellone.
    for canvas in global_canvas_tableau:
        canvas.delete("all")  # 'delete("all")' è come cancellare tutto quello che c'era su quella tela.

    # Pulisci e ripristina i "frame" delle fondazioni (le pile finali).
    for seme_key, frame in global_frame_fondazioni.items():  # Per ogni scomparto (frame) delle fondazioni...
        for widget in frame.winfo_children():  # ...e per ogni elemento grafico ('widget') dentro quel scomparto...
            widget.destroy()  # ...cancellalo.
        # Non rimettiamo qui il placeholder "F♥" perché lo faremo più avanti, solo se la fondazione è vuota.
        # La gestione del clic è già collegata al frame stesso, quindi non la ripetiamo qui.

    # Pulisci anche i frame della pila di riserva e della pila di scarto.
    for widget in global_frame_stock.winfo_children():
        widget.destroy()
    for widget in global_frame_discard.winfo_children():
        widget.destroy()

    # STEP 2: INIZIARE A DISEGNARE LE VARIE SEZIONI DEL GIOCO AGGIORNATE.

    # Disegniamo le 4 pile finali (le "fondazioni").
    # Iteriamo su ogni fondazione nel nostro dizionario 'global_pile_fondazioni'.
    # 'seme_simbolo_key' sarà il simbolo del seme (es. '♥'), 'carte_fondazione' sarà la lista di carte di quella fondazione.
    for seme_simbolo_key, carte_fondazione in global_pile_fondazioni.items():
        # Otteniamo il "frame" (la scatola invisibile) di Tkinter corrispondente a questo seme.
        # Usiamo '_ottieni_carattere_seme' per convertire il simbolo (es. '♥') nella chiave breve (es. 'H').
        frame = global_frame_fondazioni[_ottieni_carattere_seme(seme_simbolo_key)]

        if carte_fondazione:  # Se questa pila finale (fondazione) NON è vuota (cioè ha delle carte al suo interno)...
            # Disegniamo solo la carta che sta in cima a questa fondazione (è l'ultima carta nella lista 'carte_fondazione').
            carta_etichetta_fondazione = disegna_carta_in_frame(frame, carte_fondazione[-1])
            # Colleghiamo il clic del mouse anche a questa carta specifica disegnata.
            carta_etichetta_fondazione.bind("<Button-1>", lambda event, s=seme_simbolo_key: gestisci_drop_fondazione(
                _ottieni_carattere_seme(s)))
        else:  # Se la fondazione è vuota, mostriamo il placeholder (es. "F♥").
            seme_simbolo = _ottieni_simbolo_seme(
                frame.seme_carattere)  # Prendo il simbolo completo del seme per il testo.
            tk.Label(frame, text=f"F{seme_simbolo}", font=("Arial", 10), bg="#3CB371", fg="white").pack(expand=True)
        # Colleghiamo sempre il clic al frame della fondazione. Questo serve sia se è vuota (per "droppare" un Asso)
        # sia se c'è una carta (per "droppare" la carta successiva, se non si clicca esattamente sulla carta).
        frame.bind("<Button-1>", lambda event, s=seme_simbolo_key: gestisci_drop_fondazione(_ottieni_carattere_seme(s)))

    # Disegniamo la pila di riserva (quella da cui "peschi" le carte).
    if global_pila_riserva:  # Se ci sono carte in questa scatola (lista 'global_pila_riserva')...
        # Disegniamo una semplice etichetta che rappresenta il retro delle carte (non disegniamo ogni singola carta).
        tk.Label(global_frame_stock, width=LARGHEZZA_CARTA // 10, height=ALTEZZA_CARTA // 10,
                 relief="raised", bd=2, bg="#8B0000", fg="white", text="Retro", font=("Arial", 8, "bold")).pack(
            expand=True)
        global_frame_stock.config(
            cursor="hand2")  # Il cursore del mouse diventa una manina, per far capire che è cliccabile.
    else:  # Se la pila di riserva è vuota...
        tk.Label(global_frame_stock, text="Vuota", font=("Arial", 10), bg="#3CB371", fg="white").pack(expand=True)
        global_frame_stock.config(cursor="hand2")  # IL CURSORE DEVE ESSERE UNA MANINA ANCHE SE VUOTA
    # IL BIND SUL CLICK DEVE ESSERE SEMPRE ATTIVO per permettere il riciclo.
    global_frame_stock.bind("<Button-1>", gestisci_click_riserva)

    # Disegniamo la pila di scarto (where the most recently drawn card goes).
    if global_pila_scarto:  # Se c'è almeno una carta in questa scatola (lista 'global_pila_scarto')...
        carta_scarto = global_pila_scarto[-1]  # Prendiamo l'ultima carta (quella in cima alla pila di scarto).
        carta_etichetta = disegna_carta_in_frame(global_frame_discard,
                                                 carta_scarto)  # Disegniamo la carta usando la nostra funzione.
        global_frame_discard.config(cursor="hand2")  # Il cursore diventa una manina.
        # Colleghiamo il clic del mouse alla carta di scarto disegnata.
        carta_etichetta.bind("<Button-1>", gestisci_click_scarto)
        # Se la carta di scarto è quella che abbiamo "preso" (selezionato), aggiungiamo un bordo giallo.
        if global_carta_selezionata_info and global_carta_selezionata_info['carta_dati'] == carta_scarto:
            carta_etichetta.config(highlightbackground="yellow", highlightthickness=3)
    else:  # Se la pila di scarto è vuota...
        tk.Label(global_frame_discard, text="Vuota", font=("Arial", 10), bg="#3CB371", fg="white").pack(expand=True)
        global_frame_discard.config(cursor="arrow")
        global_frame_discard.bind("<Button-1>", lambda e: None)  # Disabilitiamo il clic.

    # Disegniamo le 7 colonne del tabellone principale (l'area principale dove si gioca).
    # 'enumerate' è una funzione utile: ci dà sia il numero della colonna (col_idx: 0, 1, 2...)
    # sia la colonna vera e propria (colonna: la lista di carte al suo interno).
    for col_idx, colonna in enumerate(global_colonne_tableau):
        canvas = global_canvas_tableau[col_idx]  # Prendiamo la "tela da disegno" (canvas) specifica per questa colonna.
        if not colonna:  # Se la colonna è vuota (non ci sono carte al suo interno)...
            # Disegniamo un rettangolo tratteggiato con un testo "Vuota" come placeholder.
            canvas.create_rectangle(0, 0, LARGHEZZA_CARTA, ALTEZZA_CARTA, outline="#4a5568", fill="#3CB371",
                                    dash=(5, 5))
            canvas.create_text(LARGHEZZA_CARTA / 2, ALTEZZA_CARTA / 2, text=f"C{col_idx + 1}\nVuota", fill="#a0aec0",
                               font=("Arial", 8))
        else:  # Se la colonna non è vuota, disegniamo le carte una per una.
            for card_idx, carta_obj in enumerate(colonna):
                # Calcoliamo la posizione Y della carta. 'SOVRAPPOSIZIONE_Y' serve per farle vedere "a cascata".
                x_pos, y_pos = 0, card_idx * SOVRAPPOSIZIONE_Y
                # Chiamiamo la funzione 'disegna_carta_su_canvas' per disegnare ogni singola carta.
                disegna_carta_su_canvas(canvas, carta_obj, x_pos, y_pos, col_idx, card_idx)

    # Dopo aver disegnato tutto, controlliamo se l'utente ha vinto il gioco.
    controlla_vittoria()


# --- PARTE 6: Funzioni per la Gestione degli Eventi (i clic del mouse) ---

# Questa funzione viene chiamata ogni volta che clicchi su una carta nel tabellone (tableau).
# È il "cervello" che decide cosa fare in base al tuo clic: selezionare una carta o provare a spostarne una.
# 'event': è un oggetto che Tkinter ci dà con dettagli sul clic (non lo usiamo molto qui).
# 'carta_cliccata': è la lista (il "biglietto") della carta su cui hai appena cliccato.
# 'tipo_sorgente': è la scritta 'tableau' (perché la carta viene da lì).
# 'indice_sorgente': è il numero della colonna (da 0 a 6).
# 'indice_carta_in_sorgente': è la posizione della carta all'interno di quella colonna.
def gestisci_click_carta(event, carta_cliccata, tipo_sorgente, indice_sorgente, indice_carta_in_sorgente):
    global global_carta_selezionata_info  # Diciamo a Python che stiamo lavorando con questa scatola globale.

    # SCENARIO 1: C'ERA GIÀ UNA CARTA SELEZIONATA (questo è il tuo SECONDO clic, per spostare).
    if global_carta_selezionata_info:  # Se la scatola 'global_carta_selezionata_info' NON è vuota...
        # ...significa che avevi già selezionato una carta con un clic precedente.
        # Recuperiamo le informazioni della carta che avevi selezionato con il primo clic.
        carta_precedentemente_selezionata = global_carta_selezionata_info['carta_dati']
        prev_tipo_sorgente = global_carta_selezionata_info['tipo_sorgente']
        prev_indice_sorgente = global_carta_selezionata_info['indice_sorgente']
        prev_indice_carta_in_sorgente = global_carta_selezionata_info['indice_carta_nella_sorgente']

        # SOTTOSCENARIO 1.1: Hai cliccato di nuovo sulla *stessa* carta che era già selezionata.
        # Questo serve per "deselezionare" la carta, se hai cambiato idea.
        if carta_cliccata == carta_precedentemente_selezionata:
            global_carta_selezionata_info = None  # Svuota la scatola di selezione (nessuna carta è più selezionata).
            disegna_tabellone()  # Ridisegna per togliere il bordo giallo dalla carta.
            return  # La funzione finisce qui.

        # SOTTOSCENARIO 1.2: Hai cliccato su una *diversa* carta nel tabellone (questa è la DESTINAZIONE della tua mossa).
        if tipo_sorgente == 'tableau':  # Controlliamo che la destinazione sia una colonna del tabellone.
            mossa_riuscita = False  # Iniziamo pensando che la mossa NON riuscirà.

            # SOTTOSCENARIO 1.2a: La carta che avevi selezionato (con il primo clic) veniva da un'altra colonna del tabellone.
            if prev_tipo_sorgente == 'tableau':
                # Calcoliamo quante carte dobbiamo spostare. Si spostano tutte le carte
                # dalla 'carta_precedentemente_selezionata' in giù, fino alla fine della sua colonna.
                num_carte_da_spostare = len(
                    global_colonne_tableau[prev_indice_sorgente]) - prev_indice_carta_in_sorgente
                # Ora proviamo a spostare le carte, chiamando la funzione specifica.
                # 'indice_sorgente' qui è la colonna *dove vuoi mettere* la carta (la destinazione).
                mossa_riuscita = sposta_carte_tableau_a_tableau(
                    prev_indice_sorgente, num_carte_da_spostare, indice_sorgente
                )
            # SOTTOSCENARIO 1.2b: La carta che avevi selezionato (con il primo clic) veniva dalla pila di scarto.
            elif prev_tipo_sorgente == 'discard':
                # Proviamo a spostare la carta dalla pila di scarto alla colonna del tabellone.
                mossa_riuscita = sposta_carta_da_scarto_a_tableau(
                    carta_precedentemente_selezionata, indice_sorgente
                    # 'indice_sorgente' qui è la colonna dove mettere la carta.
                )

            # Controlliamo se la mossa è andata a buon fine (la funzione di spostamento ha restituito True).
            if mossa_riuscita:
                global_carta_selezionata_info = None  # Svuota la scatola di selezione (la mossa è stata fatta!).
                disegna_tabellone()  # Ridisegna tutto il tabellone per mostrare il cambio delle carte.
                return  # La funzione finisce qui.
            # Se la mossa NON è valida (la funzione di spostamento ha restituito False), non facciamo nulla.
            # Non mostriamo nessun messaggio di errore qui, per un'esperienza più fluida.
            else:
                global_carta_selezionata_info = None  # Svuota la scatola di selezione.
                disegna_tabellone()  # Ridisegna per togliere il bordo giallo dalla carta.
                return
        # Se la destinazione del clic non è una colonna del tabellone (es. hai cliccato in un punto non valido).
        else:
            global_carta_selezionata_info = None  # Azzera la selezione.
            disegna_tabellone()
            # Non mostriamo nessun messaggio qui, per un'esperienza più fluida.
            return

    # SCENARIO 2: NON C'ERA NESSUNA CARTA SELEZIONATA (questo è il tuo PRIMO clic, per selezionare).
    # Questo blocco di codice viene eseguito se la scatola 'global_carta_selezionata_info' era vuota.

    # Controlliamo se la carta su cui hai cliccato è scoperta (il terzo elemento della lista è True).
    if carta_cliccata[2]:
        # Se è scoperta, allora la selezioniamo!
        # Salviamo tutte le informazioni della carta cliccata nella scatola globale 'global_carta_selezionata_info'.
        global_carta_selezionata_info = {
            'carta_dati': carta_cliccata,
            'tipo_sorgente': tipo_sorgente,
            'indice_sorgente': indice_sorgente,
            'indice_carta_nella_sorgente': indice_carta_in_sorgente
        }
        disegna_tabellone()  # Ridisegna il tabellone per mostrare il bordo giallo sulla carta selezionata.
    # Se la carta cliccata NON è scoperta (cioè è coperta), semplicemente non facciamo nulla.
    # Non mostriamo nessun messaggio qui, così non è fastidioso!


# Questa funzione viene chiamata quando clicchi sulla pila di riserva (quella con il retro delle carte).
def gestisci_click_riserva(event):
    global global_carta_selezionata_info
    global_carta_selezionata_info = None  # Deseleziona qualsiasi carta fosse selezionata, prima di pescare.
    pesca_carta_da_riserva()  # Chiama la ricetta che gestisce la pesca della carta.
    disegna_tabellone()  # Ridisegna per mostrare la nuova carta pescata nella pila di scarto.


# Questa funzione viene chiamata quando clicchi sulla carta in cima alla pila di scarto.
def gestisci_click_scarto(event):
    global global_carta_selezionata_info, global_pila_scarto
    if global_pila_scarto:  # Se la scatola 'global_pila_scarto' non è vuota (cioè c'è almeno una carta)...
        carta_scarto = global_pila_scarto[-1]  # Prendi l'ultima carta (quella in cima alla pila di scarto).
        # Se la carta cliccata è già quella selezionata, la deseleziona.
        if global_carta_selezionata_info and global_carta_selezionata_info['carta_dati'] == carta_scarto:
            global_carta_selezionata_info = None
        else:  # Altrimenti, seleziona questa carta di scarto.
            global_carta_selezionata_info = {
                'carta_dati': carta_scarto,
                'tipo_sorgente': 'discard',  # Indichiamo che viene dalla pila di scarto.
                'indice_sorgente': None,  # Non ha un indice di colonna specifico.
                'indice_carta_nella_sorgente': None  # O una posizione all'interno di una colonna.
            }
        disegna_tabellone()  # Ridisegna per mostrare la selezione/deselezione.
    # else: # Rimosso il messaggio "Scarto, La pila di scarto è vuota."
    #     mostra_messaggio("Scarto", "La pila di scarto è vuota.")


# Questa funzione viene chiamata quando clicchi su un'area di una pila finale (fondazione).
# Questo succede quando vuoi "lasciare" una carta selezionata su una fondazione.
# Prende 'carattere_seme_fondazione': il carattere breve del seme della fondazione (es. 'H' per Cuori).
def gestisci_drop_fondazione(carattere_seme_fondazione):
    global global_carta_selezionata_info
    if global_carta_selezionata_info:  # Se hai una carta selezionata (cioè 'global_carta_selezionata_info' NON è vuota)...
        carta_da_spostare = global_carta_selezionata_info['carta_dati']  # Prendi la carta che avevi selezionato.
        tipo_sorgente = global_carta_selezionata_info['tipo_sorgente']
        indice_sorgente = global_carta_selezionata_info['indice_sorgente']

        mossa_riuscita = False  # Variabile per indicare se la mossa è andata a buon fine.
        if tipo_sorgente == 'tableau':  # Se la carta selezionata viene da una colonna del tabellone.
            colonna_sorgente = global_colonne_tableau[indice_sorgente]
            # Solo l'ultima carta della colonna (quella più in alto) può essere spostata a una fondazione.
            if colonna_sorgente and carta_da_spostare == colonna_sorgente[-1]:
                mossa_riuscita = sposta_carta_da_tableau_a_fondazione(indice_sorgente, carattere_seme_fondazione)
            else:
                # Non mostriamo nessun messaggio qui, la mossa semplicemente non avviene.
                pass
        elif tipo_sorgente == 'discard':  # Se la carta selezionata viene dalla pila di scarto.
            mossa_riuscita = sposta_carta_da_scarto_a_fondazione(carta_da_spostare, carattere_seme_fondazione)
        else:
            # Non mostriamo nessun messaggio qui.
            pass

        if mossa_riuscita:  # Se la mossa è andata a buon fine.
            global_carta_selezionata_info = None  # Azzera la selezione.
            disegna_tabellone()  # Ridisegna.
        else:
            # Non mostriamo nessun messaggio qui.
            pass
    else:  # Se non c'è una carta selezionata (cioè 'global_carta_selezionata_info' è vuota).
        # Non mostriamo nessun messaggio qui.
        pass


# Questa funzione viene chiamata quando clicchi su un'area di una colonna del tabellone (per "droppare" una carta).
# Questo succede quando vuoi "lasciare" una carta selezionata in una colonna.
# Prende 'indice_colonna_destinazione': il numero della colonna del tabellone dove vuoi spostare la carta.
def gestisci_drop_tableau(indice_colonna_destinazione):
    global global_carta_selezionata_info
    if global_carta_selezionata_info:  # Se hai una carta selezionata.
        carta_da_spostare = global_carta_selezionata_info['carta_dati']
        tipo_sorgente = global_carta_selezionata_info['tipo_sorgente']
        indice_sorgente = global_carta_selezionata_info['indice_sorgente']
        indice_carta_in_sorgente = global_carta_selezionata_info['indice_carta_nella_sorgente']

        mossa_riuscita = False
        if tipo_sorgente == 'tableau':  # Se la carta selezionata viene da un'altra colonna del tabellone.
            # Calcola quante carte devono essere spostate (dalla carta selezionata in poi).
            num_carte_da_spostare = len(global_colonne_tableau[indice_sorgente]) - indice_carta_in_sorgente
            mossa_riuscita = sposta_carte_tableau_a_tableau(indice_sorgente, num_carte_da_spostare,
                                                            indice_colonna_destinazione)
        elif tipo_sorgente == 'discard':  # Se la carta selezionata viene dalla pila di scarto.
            mossa_riuscita = sposta_carta_da_scarto_a_tableau(carta_da_spostare, indice_colonna_destinazione)
        else:
            # Non mostriamo nessun messaggio qui.
            pass

        if mossa_riuscita:  # Se la mossa è andata a buon fine.
            global_carta_selezionata_info = None  # Azzera la selezione.
            disegna_tabellone()  # Ridisegna il tabellone.
        else:
            # Non mostriamo nessun messaggio qui.
            pass
    else:  # Se non c'è una carta selezionata.
        # Non mostriamo nessun messaggio qui.
        pass


# --- PARTE 7: Funzioni di Logica del Gioco (le "regole del Solitario") ---

# Controlla se una mossa tra carte nelle colonne del tabellone è valida.
# Prende la 'carta_sorgente' (quella che vuoi spostare) e la 'carta_destinazione' (quella sotto cui vuoi metterla).
def _è_mossa_tableau_valida(carta_sorgente, carta_destinazione):
    # REGOLA 1: La carta che sposti e la carta sotto cui la metti devono avere colori diversi (rosso su nero o nero su rosso).
    if ottieni_colore_carta(carta_sorgente) == ottieni_colore_carta(carta_destinazione):
        return False  # Stesso colore, mossa non valida.
    # REGOLA 2: Il valore numerico della carta che sposti deve essere esattamente 1 in meno della carta di destinazione.
    # Esempio: il 2 (valore 2) può andare solo sul 3 (valore 3). La Regina (12) può andare solo sul Re (13).
    return ottieni_valore_numerico_carta(carta_sorgente) == ottieni_valore_numerico_carta(carta_destinazione) - 1


# Controlla se una mossa verso una pila finale (fondazione) è valida.
# Prende la 'carta' (che vuoi spostare) e il 'carattere_seme_fondazione' (es. 'H' per Cuori, che indica di quale fondazione parliamo).
def _è_mossa_fondazione_valida(carta, carattere_seme_fondazione):
    # Convertiamo il carattere breve (es. 'H') nel simbolo vero del seme di destinazione (es. '♥').
    seme_destinazione = _ottieni_simbolo_seme(carattere_seme_fondazione)
    # REGOLA 1: La carta deve essere dello stesso seme della fondazione.
    if carta[0] != seme_destinazione:  # carta[0] è il seme della carta.
        return False  # Seme diverso, mossa non valida.

    # Prendiamo la lista di carte di quella pila finale (fondazione).
    fondazione = global_pile_fondazioni[seme_destinazione]
    if not fondazione:  # REGOLA 2a: Se la pila finale è vuota (non ci sono ancora carte)...
        return carta[1] == 'A'  # ...allora può accettare solo un Asso (valore 'A').
    else:  # REGOLA 2b: Se la pila finale NON è vuota...
        # La carta che sposti deve essere quella successiva in ordine crescente rispetto alla carta che sta in cima alla pila finale.
        # Esempio: se in cima alla fondazione c'è un 2, puoi mettere solo un 3. Se c'è un Fante, puoi mettere solo una Regina.
        return ottieni_valore_numerico_carta(carta) == ottieni_valore_numerico_carta(fondazione[-1]) + 1


# Sposta una sequenza di carte da una colonna del tabellone a un'altra.
# Prende:
#   'indice_colonna_sorgente': il numero della colonna da cui spostare (da 0 a 6).
#   'numero_carte': quante carte spostare (tutte quelle selezionate, dalla cima in giù).
#   'indice_colonna_destinazione': il numero della colonna dove spostare (da 0 a 6).
def sposta_carte_tableau_a_tableau(indice_colonna_sorgente, numero_carte, indice_colonna_destinazione):
    global global_colonne_tableau  # Diciamo a Python che useremo questa scatola globale.
    colonna_sorgente = global_colonne_tableau[indice_colonna_sorgente]  # La lista di carte della colonna di partenza.
    colonna_destinazione = global_colonne_tableau[
        indice_colonna_destinazione]  # La lista di carte della colonna di arrivo.

    if not colonna_sorgente:  # Se la colonna da cui vuoi spostare è vuota.
        # mostra_messaggio("Mossa non valida", "La colonna sorgente è vuota.") # Rimosso il messaggio
        return False  # La mossa non è valida.

    if numero_carte > len(colonna_sorgente):  # Se provi a spostare più carte di quelle che ci sono nella colonna.
        # mostra_messaggio("Mossa non valida", "Numero di carte da spostare superiore a quelle presenti nella colonna.") # Rimosso il messaggio
        return False

    # Prendiamo le carte da spostare: sono le ultime 'numero_carte' dalla fine della lista 'colonna_sorgente'.
    carte_da_spostare = colonna_sorgente[len(colonna_sorgente) - numero_carte:]

    # Controlliamo che *tutte* le carte nella sequenza che vuoi spostare siano scoperte (visibili).
    for carta in carte_da_spostare:
        if not carta[2]:  # carta[2] è il suo stato "è_coperta_o_scoperta". Se è False (coperta)...
            # mostra_messaggio("Mossa non valida", "Impossibile spostare carte coperte in una sequenza.") # Rimosso il messaggio
            return False  # La mossa non è valida.

    # Applichiamo le regole di movimento del tabellone (quelle che abbiamo definito prima).
    if colonna_destinazione:  # Se la colonna di destinazione *non* è vuota (cioè ha già delle carte)...
        # Controlliamo se la *prima* carta della sequenza che sposti (quella in cima) può andare sulla *cima* della colonna di destinazione.
        if not _è_mossa_tableau_valida(carte_da_spostare[0], colonna_destinazione[-1]):
            # mostra_messaggio("Mossa non valida", "La carta non può essere posizionata qui (ordine o colore errato).") # Rimosso il messaggio
            return False  # La mossa non è valida.
    else:  # Se la colonna di destinazione *è* vuota...
        if carte_da_spostare[0][1] != 'K':  # La prima carta della sequenza (quella in cima) deve essere un Re ('K').
            # mostra_messaggio("Mossa non valida", "Una colonna vuota può essere riempita solo da un Re o una sequenza che inizia con un Re.") # Rimosso il messaggio
            return False  # La mossa non è valida.

    # Se tutte le regole sono rispettate, allora possiamo eseguire la mossa vera e propria!
    for _ in range(numero_carte):  # Ripetiamo per il numero di carte da spostare.
        # 'pop()' toglie l'ultima carta dalla 'colonna_sorgente' e la restituisce.
        # 'append()' aggiunge quella carta alla fine della 'colonna_destinazione'.
        colonna_destinazione.append(colonna_sorgente.pop())

    # Dopo aver spostato le carte, controlliamo la colonna da cui abbiamo preso le carte.
    # Se ora c'è una carta coperta in cima a quella colonna, la giriamo (la "riveliamo").
    rivela_carta_cima(indice_colonna_sorgente)
    return True  # Se arriviamo qui, significa che la mossa è stata fatta con successo.


# Sposta una singola carta dalla cima di una colonna del tabellone a una pila finale (fondazione).
def sposta_carta_da_tableau_a_fondazione(indice_colonna_sorgente, carattere_seme_fondazione):
    global global_colonne_tableau, global_pile_fondazioni  # Dichiariamo le scatole globali che useremo.
    colonna_sorgente = global_colonne_tableau[indice_colonna_sorgente]  # La colonna da cui spostare.
    if not colonna_sorgente:  # Se la colonna è vuota.
        # mostra_messaggio("Mossa non valida", "La colonna sorgente è vuota.") # Rimosso il messaggio
        return False

    carta_da_spostare = colonna_sorgente[-1]  # Prendiamo solo l'ultima carta della colonna (quella in cima).
    if not carta_da_spostare[2]:  # Se è coperta.
        # mostra_messaggio("Mossa non valida", "La carta è coperta e non può essere spostata.") # Rimosso il messaggio
        return False

    if _è_mossa_fondazione_valida(carta_da_spostare,
                                  carattere_seme_fondazione):  # Controlla se la mossa è valida con la nostra ricetta.
        # Aggiungi la carta alla pila finale corretta (usando il simbolo del seme).
        global_pile_fondazioni[_ottieni_simbolo_seme(carattere_seme_fondazione)].append(
            colonna_sorgente.pop())  # Togli la carta dalla colonna e mettila nella fondazione.
        rivela_carta_cima(indice_colonna_sorgente)  # Rivela la carta sotto, se ce n'è una.
        return True  # Mossa riuscita.
    else:
        # mostra_messaggio("Mossa non valida", "La carta non può essere posizionata in questa fondazione.") # Rimosso il messaggio
        return False


# Sposta una carta dalla pila di scarto a una colonna del tabellone.
def sposta_carta_da_scarto_a_tableau(carta_da_spostare, indice_colonna_destinazione):
    global global_colonne_tableau, global_pila_scarto
    colonna_destinazione = global_colonne_tableau[indice_colonna_destinazione]

    if colonna_destinazione:  # Se la colonna di destinazione non è vuota.
        if not _è_mossa_tableau_valida(carta_da_spostare, colonna_destinazione[-1]):
            # mostra_messaggio("Mossa non valida", "La carta non può essere posizionata qui (ordine o colore errato).") # Rimosso il messaggio
            return False
    else:  # Se la colonna di destinazione è vuota.
        if carta_da_spostare[1] != 'K':  # La carta deve essere un Re.
            # mostra_messaggio("Mossa non valida", "Una colonna vuota può essere riempita solo da un Re.") # Rimosso il messaggio
            return False

    global_pila_scarto.pop()  # Togli la carta dalla pila di scarto.
    colonna_destinazione.append(carta_da_spostare)  # Aggiungi alla colonna di destinazione.
    return True  # Mossa riuscita.


# Sposta una carta dalla pila di scarto a una pila finale (fondazione).
def sposta_carta_da_scarto_a_fondazione(carta_da_spostare, carattere_seme_fondazione):
    global global_pila_scarto, global_pile_fondazioni
    if _è_mossa_fondazione_valida(carta_da_spostare, carattere_seme_fondazione):  # Controlla se la mossa è valida.
        global_pila_scarto.pop()  # Togli la carta dalla pila di scarto.
        global_pile_fondazioni[_ottieni_simbolo_seme(carattere_seme_fondazione)].append(
            carta_da_spostare)  # Aggiungi alla fondazione.
        return True  # Mossa riuscita.
    else:
        # mostra_messaggio("Mossa non valida", "La carta non può essere posizionata in questa fondazione.") # Rimosso il messaggio
        return False


# Questa funzione gestisce il "pescare" una carta dalla pila di riserva.
def pesca_carta_da_riserva():
    print("\nDEBUG: Funzione pesca_carta_da_riserva() avviata.")  # Debug print all'inizio della funzione
    global global_pila_riserva, global_pila_scarto  # Dichiariamo le scatole globali.

    # Caso 1: Tutte le carte sono finite, sia nella riserva che nello scarto.
    if not global_pila_riserva and not global_pila_scarto:
        print("DEBUG: Nessuna carta disponibile per la pesca o il riciclo (riserva e scarto vuoti).")
        return

    # Caso 2: La pila di riserva è vuota, ma ci sono carte nella pila di scarto.
    # Dobbiamo riciclare le carte dalla pila di scarto alla pila di riserva.
    if not global_pila_riserva:
        print("DEBUG: Pila di riserva attualmente vuota. Tentativo di riciclare dallo scarto.")
        # Se anche lo scarto è vuoto, è un caso già gestito sopra.
        if not global_pila_scarto:
            print("DEBUG: Anche la pila di scarto è vuota. Nessuna carta da riciclare.")
            return

        print(f"DEBUG: Carte nella pila di scarto prima del riciclo: {len(global_pila_scarto)}")

        # Ecco come ricicliamo le carte:
        # 1. Prendiamo le carte dalla 'global_pila_scarto' e le mettiamo nella 'global_pila_riserva'.
        global_pila_riserva = [carta for carta in reversed(global_pila_scarto)]

        # Aggiungiamo il rimescolamento qui!
        random.shuffle(global_pila_riserva)  # MESCOLIAMO le carte riciclate!
        print("DEBUG: Carte della pila di scarto rimescolate e spostate nella pila di riserva.")

        global_pila_scarto.clear()  # Svuotiamo completamente la pila di scarto, perché le carte sono ora nella riserva.
        print("DEBUG: Pila di scarto svuotata.")

        # Ogni carta che viene riciclata deve essere girata a faccia in giù (coperta).
        for carta in global_pila_riserva:
            carta[2] = False  # Impostiamo il suo stato a False (coperta).
        print("DEBUG: Tutte le carte riciclate sono state impostate come coperte.")
        print(f"DEBUG: Nuova pila di riserva ha {len(global_pila_riserva)} carte.")

    # Ora, pesca una carta dalla cima della pila di riserva.
    print(f"DEBUG: Pescando una carta dalla pila di riserva. Carte rimanenti prima di pop: {len(global_pila_riserva)}")
    # 'pop()' toglie l'ultima carta dalla lista 'global_pila_riserva' e te la dà.
    carta_pescata = global_pila_riserva.pop()
    carta_pescata[2] = True  # La carta pescata è sempre scoperta (imposta il suo stato a True).
    global_pila_scarto.append(carta_pescata)  # Aggiungi la carta pescata alla pila di scarto.
    print(
        f"DEBUG: Carta pescata ({carta_pescata[1]}{carta_pescata[0]}) e spostata nello scarto. Carte nello scarto: {len(global_pila_scarto)}")
    print(f"DEBUG: Carte rimanenti nella pila di riserva dopo pop: {len(global_pila_riserva)}")


# Questa funzione serve a "rivelare" la carta coperta in cima a una colonna del tabellone.
# Prende 'indice_colonna': il numero della colonna da controllare.
def rivela_carta_cima(indice_colonna):
    global global_colonne_tableau  # Lavoriamo con la nostra scatola globale delle colonne.
    # Controlliamo due cose:
    # 1. Se la colonna NON è vuota (c'è almeno una carta).
    # 2. Se l'ultima carta della colonna (quella in cima, `[-1]`) è coperta (`not carta[2]` significa "se non è scoperta").
    if global_colonne_tableau[indice_colonna] and not global_colonne_tableau[indice_colonna][-1][2]:
        global_colonne_tableau[indice_colonna][-1][
            2] = True  # Se è coperta, la giriamo (impostiamo il suo stato a True).
        return True  # Diciamo che una carta è stata scoperta.
    return False  # Altrimenti (se la colonna è vuota o la carta era già scoperta), diciamo che non è stato scoperto nulla.


# Controlla se il gioco è stato vinto.
def controlla_vittoria():
    global global_pile_fondazioni  # Lavoriamo con la scatola globale delle fondazioni.
    for seme in global_pile_fondazioni:  # Per ogni pila finale (fondazione) (Cuori, Quadri, Picche, Fiori)...
        if len(global_pile_fondazioni[seme]) != 13:  # ...controlla se ha esattamente 13 carte (dall'Asso al Re).
            return False  # Se anche una sola fondazione non ha 13 carte, il gioco non è ancora vinto.
    # Se il ciclo finisce e non siamo usciti (cioè tutte le fondazioni hanno 13 carte):
    messagebox.showinfo("Solitario", "CONGRATULAZIONI! Hai vinto al Solitario!")  # Mostra il messaggio di vittoria.
    print(
        "MESSAGGIO: Solitario - CONGRATULAZIONI! Hai vinto al Solitario!")  # Mantengo il print per completezza del debug
    return True  # Il gioco è stato vinto.


# Questa funzione gestisce la modalità schermo intero.
# Non prende "event" perché la chiamiamo noi direttamente (tranne quando è collegata al tasto Esc).
def toggle_fullscreen():
    global global_root  # Diciamo a Python che lavoriamo con la finestra principale.
    # Controlliamo lo stato attuale della finestra.
    # 'global_root.attributes('-fullscreen')' ci dice se la finestra è già a schermo intero (1) o meno (0).
    if global_root.attributes('-fullscreen'):  # Se è a schermo intero (è True o 1)...
        global_root.attributes('-fullscreen', False)  # ...allora la riportiamo alla modalità finestra (False o 0).
    else:  # Altrimenti (se non è a schermo intero)...
        global_root.attributes('-fullscreen', True)  # ...la mettiamo a schermo intero (True o 1).


# --- PARTE 8: Funzioni di Inizializzazione e Avvio del Gioco (la "preparazione della partita") ---

# Questa funzione distribuisce le carte all'inizio di una nuova partita.
def distribuisci_carte_iniziali():
    # Dichiariamo le scatole globali che questa funzione userà e modificherà.
    global global_mazzo, global_colonne_tableau, global_pila_riserva, global_pila_scarto, global_pile_fondazioni

    global_mazzo = crea_mazzo_completo()  # Creiamo un nuovo mazzo di 52 carte mescolate usando la nostra ricetta.

    # Inizializziamo (mettiamo a zero/vuoto) tutte le aree di gioco, pulendo il vecchio stato se c'era.
    global_colonne_tableau = [[] for _ in range(7)]  # Creiamo 7 liste vuote, una per ogni colonna del tabellone.
    global_pile_fondazioni = {'♥': [], '♦': [], '♠': [],
                              '♣': []}  # Inizializziamo il dizionario delle 4 fondazioni, tutte liste vuote.
    global_pila_scarto = []  # La pila di scarto inizia vuota.

    # Distribuiamo le carte nelle 7 colonne del tabellone.
    # Questo ciclo esterno va da 0 a 6 (per le 7 colonne). 'i' è il numero della colonna.
    for i in range(7):
        # Questo ciclo interno determina quante carte dare a ogni colonna (la colonna 0 prende 1 carta, la 1 ne prende 2, ecc.).
        # 'j' è la posizione della carta all'interno della colonna.
        for j in range(i + 1):
            carta = global_mazzo.pop(
                0)  # Togli la prima carta dalla cima del mazzo ('pop(0)' la toglie e la restituisce).
            if j == i:  # Se questa è l'ultima carta che stiamo mettendo in questa colonna (quella in cima, visibile)...
                carta[2] = True  # ...la giriamo a faccia in su (impostiamo il suo stato a True).
            global_colonne_tableau[i].append(
                carta)  # Aggiungiamo la carta alla fine della lista della colonna corrente.

    # Le carte che rimangono nella scatola 'global_mazzo' dopo la distribuzione iniziale, vanno nella pila di riserva.
    global_pila_riserva = global_mazzo[
                          :]  # Creiamo una COPIA della lista rimanente. '[:]' serve a fare una copia vera, non solo un riferimento.


# Questa funzione crea la schermata di benvenuto del gioco, quella che appare all'inizio.
def crea_schermata_intro():
    print("DEBUG: Avvio della schermata di introduzione.")  # Debug print
    global global_root  # Dichiariamo che useremo la scatola globale per la finestra principale.
    global_root = tk.Tk()  # Creiamo la finestra principale del nostro gioco. È la "cornice" dove vedrai tutto.
    global_root.title("Solitario Semplice")  # Impostiamo il titolo della finestra che appare in alto.
    global_root.geometry("600x400")  # Impostiamo le dimensioni iniziali della finestra (larghezza x altezza in pixel).
    global_root.resizable(False,
                          False)  # Non permettiamo all'utente di ridimensionare questa finestra iniziale (non è dinamica).
    global_root.configure(
        bg="#2E8B57")  # Impostiamo il colore di sfondo della finestra (un bel verde, come un tavolo da gioco).

    # Creiamo un "frame" (una scatola invisibile) per contenere gli elementi della schermata di introduzione.
    intro_frame = tk.Frame(global_root, bg="#2E8B57", bd=5, relief="raised")
    intro_frame.pack(expand=True,
                     fill="both")  # Facciamo in modo che questo frame occupi tutto lo spazio disponibile nella finestra.

    # Etichetta di benvenuto: un testo grande e accogliente.
    tk.Label(intro_frame, text="Benvenuto al Solitario!", font=("Arial", 28, "bold"), fg="white", bg="#2E8B57").pack(
        pady=30)
    # Istruzioni brevi per il giocatore.
    tk.Label(intro_frame, text="Clicca per selezionare le carte e spostarle.", font=("Arial", 14), fg="white",
             bg="#2E8B57").pack(pady=15)

    # Pulsante "Inizia a Giocare!".
    play_button = tk.Button(intro_frame, text="Inizia a Giocare!", font=("Arial", 18, "bold"),
                            command=lambda: avvia_gioco(intro_frame),
                            # Quando cliccato, chiama la ricetta 'avvia_gioco'.
                            bg="#4CAF50", fg="white", activebackground="#45a049", activeforeground="white",
                            relief="raised", bd=5,
                            cursor="hand2")  # Diamo uno stile al pulsante (colore, bordo, cursore a manina).
    play_button.pack(pady=20, padx=40, ipady=8)  # Posizioniamo il pulsante nel frame, con un po' di spazio intorno.

    global_root.mainloop()  # Avvia il "motore" principale di Tkinter. Questa riga è come accendere il gioco:
    # fa sì che la finestra appaia e rimanga aperta, in attesa che tu faccia qualcosa (come cliccare).


# Questa funzione avvia il gioco vero e proprio dopo la schermata di introduzione.
# Prende 'intro_frame_da_distruggere': la scatola invisibile della schermata iniziale, che poi dobbiamo togliere.
def avvia_gioco(intro_frame_da_distruggere):
    print("DEBUG: Avvio del gioco principale.")  # Debug print
    intro_frame_da_distruggere.destroy()  # Rimuoviamo e distruggiamo il frame della schermata di introduzione dalla finestra.

    # Imposta le dimensioni e la possibilità di ridimensionare la finestra per il gioco
    global_root.geometry("900x700")  # Una dimensione più generosa
    global_root.resizable(True, True)  # Rendi la finestra ridimensionabile

    crea_elements_gioco()  # Chiama la ricetta per creare tutti gli elementi grafici del gioco (le colonne, le fondazioni, i pulsanti).
    distribuisci_carte_iniziali()  # Chiama la ricetta per mettere le carte al loro posto iniziale sul tabellone.
    disegna_tabellone()  # Chiama la ricetta per disegnare tutto il tabellone con le nuove carte.


# Questa funzione crea tutti gli elementi visivi del gioco (le scatole invisibili, le tele, i pulsanti) una volta che il gioco è iniziato.
def crea_elements_gioco():
    print("DEBUG: Creazione degli elementi grafici del gioco.")  # Debug print
    # Dichiariamo tutte le scatole globali che verranno riempite o modificate qui.
    global global_frame_fondazioni, global_frame_stock, global_frame_discard, global_canvas_tableau
    global global_root  # Serve anche la finestra principale per configurare il fullscreen.

    # Frame superiore: la scatola invisibile che contiene le fondazioni, la pila di riserva e la pila di scarto.
    top_frame = tk.Frame(global_root, bg="#2E8B57",
                         pady=10)  # Lo mettiamo dentro la finestra principale ('global_root').
    top_frame.pack(side="top", fill="x")  # Posiziona il frame in alto e lo fa espandere per tutta la larghezza.

    # Creazione dei "frame" (scatole invisibili) per le 4 fondazioni.
    # Usiamo 'H', 'D', 'S', 'C' come chiavi nel nostro dizionario 'global_frame_fondazioni'.
    for i, seme_char in enumerate(['H', 'D', 'S', 'C']):
        frame = tk.Frame(top_frame, width=LARGHEZZA_CARTA, height=ALTEZZA_CARTA, relief="ridge", bd=2, bg="#3CB371")
        frame.pack(side="left", padx=10)  # Posiziona ogni frame uno accanto all'altro, con un po' di spazio.
        frame.propagate(
            False)  # Impedisce al frame di ridimensionarsi in base al contenuto interno (mantiene la dimensione fissa).
        # Colleghiamo il clic a questo frame: se clicchi qui, provi a "lasciare" una carta selezionata.
        # Il bind specifico per la carta disegnata sopra verrà fatto in 'disegna_tabellone'.
        frame.bind("<Button-1>", lambda event, sc=seme_char: gestisci_drop_fondazione(sc))
        global_frame_fondazioni[seme_char] = frame  # Salviamo il frame nel nostro dizionario globale.
        frame.seme_carattere = seme_char  # Aggiungiamo un'etichetta extra al frame per ricordarci quale seme rappresenta.

    # Frame per la Pila di Riserva.
    global_frame_stock = tk.Frame(top_frame, width=LARGHEZZA_CARTA, height=ALTEZZA_CARTA, relief="ridge", bd=2,
                                  bg="#3CB371")
    global_frame_stock.pack(side="left", padx=20)
    global_frame_stock.propagate(False)
    # Il clic sulla pila di riserva è gestito dalla funzione `gestisci_click_riserva`. Lo colleghiamo in 'disegna_tabellone'.

    # Frame per la Pila di Scarto.
    global_frame_discard = tk.Frame(top_frame, width=LARGHEZZA_CARTA, height=ALTEZZA_CARTA, relief="ridge", bd=2,
                                    bg="#3CB371")
    global_frame_discard.pack(side="left", padx=10)
    global_frame_discard.propagate(False)
    # Il clic sulla pila di scarto è gestito dalla funzione `gestisci_click_scarto`. Lo colleghiamo in 'disegna_tabellone'.

    # Frame per le colonne del Tabellone (l'area principale di gioco).
    tableau_frame = tk.Frame(global_root, bg="#2E8B57", pady=10)
    tableau_frame.pack(side="top", fill="both",
                       expand=True)  # Occupano lo spazio rimanente e si espandono per riempire la finestra.

    global_canvas_tableau = []  # Inizializziamo la lista che conterrà le "tele da disegno" per ogni colonna.
    for i in range(7):  # Per ogni colonna (da 0 a 6)...
        # Creiamo un Canvas (una "tela da disegno") per disegnare le carte di quella colonna.
        canvas = tk.Canvas(tableau_frame, width=LARGHEZZA_CARTA, height=ALTEZZA_CARTA * 6,
                           # Altezza sufficiente per le carte sovrapposte.
                           bg="#3CB371", relief="ridge", bd=2, highlightthickness=0)
        # 'grid' è un modo per posizionare gli elementi in una griglia. 'row=0, column=i' significa riga 0, colonna i-esima.
        canvas.grid(row=0, column=i, padx=5, sticky="nsew")
        # Colleghiamo il clic su questo canvas: se clicchi su questa colonna (vuota o sullo sfondo di una carta), provi a "lasciare" una carta selezionata.
        canvas.bind("<Button-1>", lambda event, col_idx=i: gestisci_drop_tableau(col_idx))
        global_canvas_tableau.append(canvas)  # Aggiungiamo la tela creata alla nostra lista globale.
        tableau_frame.grid_columnconfigure(i, weight=1)  # Fa sì che le colonne si allarghino se la finestra si allarga.

    tableau_frame.grid_rowconfigure(0, weight=1)  # Fa sì che la riga delle colonne si allargi verticalmente.

    # Controlli di gioco (i pulsanti in basso).
    control_frame = tk.Frame(global_root, bg="#2E8B57", pady=10)
    control_frame.pack(side="bottom", fill="x")  # Posiziona il frame in basso e lo espande orizzontalmente.

    # Pulsante "Riavvia Partita".
    restart_button = tk.Button(control_frame, text="Riavvia Partita", command=riavvia_gioco,
                               # Quando clicchi, chiama la ricetta 'riavvia_gioco'.
                               bg="#FFD700", fg="black", activebackground="#DAA520", relief="raised", bd=3,
                               cursor="hand2")
    restart_button.pack(side="left", padx=10)  # Posiziona il pulsante a sinistra.

    # Pulsante per la Modalità Schermo Intero.
    fullscreen_button = tk.Button(control_frame, text="Modalità Schermo Intero", command=toggle_fullscreen,
                                  # Quando clicchi, chiama la ricetta 'toggle_fullscreen'.
                                  bg="#ADD8E6", fg="black", activebackground="#87CEEB", relief="raised", bd=3,
                                  cursor="hand2")
    fullscreen_button.pack(side="left", padx=10)  # Posiziona il pulsante a sinistra, accanto al riavvio.

    # Collega il tasto ESC (Escape) per uscire dalla modalità schermo intero.
    # Quando premi Esc, il gioco torna alla modalità finestra.
    global_root.bind("<Escape>", lambda event: global_root.attributes("-fullscreen", False))

    # Il pulsante "Annulla Mossa" è stato rimosso, non c'è più bisogno di crearlo o posizionarlo.
    # undo_button = tk.Button(control_frame, text="Annulla Mossa",
    #                         command=lambda: messagebox.showinfo("Annulla", "La funzionalità 'Annulla Mossa' in questa versione semplificata riavvia il gioco. Per un vero annullamento, il codice sarebbe molto più complesso!"),
    #                         bg="#B0C4DE", fg="black", activebackground="#A9A9A9", relief="raised", bd=3, cursor="hand2")
    # undo_button.pack(side="right", padx=10)


# Funzione per riavviare il gioco (per iniziare una nuova partita da zero).
def riavvia_gioco():
    # Sostituito messagebox.askyesno con print per debug
    print("DEBUG: Richiesta riavvio partita.")
    # In una versione più complessa, qui si potrebbe chiedere conferma via UI personalizzata
    if messagebox.askyesno("Riavvia Gioco",
                           "Sei sicuro di voler riavviare la partita? Il progresso attuale verrà perso."):
        print("DEBUG: Riavvio della partita in corso.")
        # Rimuoviamo tutti gli elementi grafici ('widget') dalla finestra principale del gioco.
        for widget in global_root.winfo_children():
            widget.destroy()  # Questo "pulisce" lo schermo per la nuova partita.

        # Reinizializziamo tutte le scatole globali del gioco (resetta lo stato delle carte e le posizioni).
        global global_carta_selezionata_info
        global_carta_selezionata_info = None  # Azzera la selezione di carte.

        # Ri-creiamo tutti gli elementi grafici del gioco per la nuova partita.
        crea_elements_gioco()
        # Ridistribuiamo le carte per una nuova partita.
        distribuisci_carte_iniziali()
        # Ridisegniamo il tabellone con le nuove carte.
        disegna_tabellone()
    else:
        print("DEBUG: Riavvio annullato dall'utente.")


# --- IL PUNTO DI PARTENZA DEL PROGRAMMA ---
# Questa parte del codice viene eseguita solo quando avvii il file Python direttamente (non se lo importi in un altro file).
if __name__ == "__main__":
    print("DEBUG: Programma Solitario avviato.")  # Debug print all'avvio
    crea_schermata_intro()  # Per prima cosa, mostriamo la schermata di introduzione al gioco.
