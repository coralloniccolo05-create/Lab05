import flet as ft
from alert import AlertManager
from autonoleggio import Autonoleggio


FILE_AUTO = "automobili.csv"

def main(page: ft.Page):
    page.title = "Lab05"
    page.horizontal_alignment = "center"
    page.theme_mode = ft.ThemeMode.DARK

    # --- ALERT ---
    alert = AlertManager(page)

    # --- LA LOGICA DELL'APPLICAZIONE E' PRESA DALL'AUTONOLEGGIO DEL LAB03 ---
    autonoleggio = Autonoleggio("Polito Rent", "Alessandro Visconti")
    try:
        autonoleggio.carica_file_automobili(FILE_AUTO) # Carica il file
    except Exception as e:
        alert.show_alert(f"❌ {e}") # Fa apparire una finestra che mostra l'errore

    # --- UI ELEMENTI ---

    # Text per mostrare il nome e il responsabile dell'autonoleggio
    txt_titolo = ft.Text(value=autonoleggio.nome, size=38, weight=ft.FontWeight.BOLD)
    txt_responsabile = ft.Text(
        value=f"Responsabile: {autonoleggio.responsabile}",
        size=16,
        weight=ft.FontWeight.BOLD
    )

    # TextField per responsabile
    input_responsabile = ft.TextField(value=autonoleggio.responsabile, label="Responsabile")

    # ListView per mostrare la lista di auto aggiornata
    lista_auto = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)

    # Tutti i TextField per le info necessarie per aggiungere una nuova automobile (marca, modello, anno, contatore posti)
    # TODO
    input_aggiungi_marca = ft.TextField(value='Marca', label="Marca")
    input_aggiungi_modello = ft.TextField(value='Modello', label="Modello")
    input_aggiungi_anno = ft.TextField(value='Anno', label="Anno")

    # --- FUNZIONI APP ---
    def aggiorna_lista_auto():
        lista_auto.controls.clear()
        for auto in autonoleggio.automobili_ordinate_per_marca():
            stato = "✅" if auto.disponibile else "⛔"
            lista_auto.controls.append(ft.Text(f"{stato} {auto}"))
        page.update()

    # --- HANDLERS APP ---
    def cambia_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        toggle_cambia_tema.label = "Tema scuro" if toggle_cambia_tema.value else "Tema chiaro"
        page.update()

    def conferma_responsabile(e):
        autonoleggio.responsabile = input_responsabile.value
        txt_responsabile.value = f"Responsabile: {autonoleggio.responsabile}"
        page.update()

    # Handlers per la gestione dei bottoni utili all'inserimento di una nuova auto
    # TODO
    def handleAdd(e):
        currentVal = num_posti.value
        num_posti.value = currentVal + 1
        num_posti.update()

    def handleRemove(e):
        currentVal = num_posti.value
        num_posti.value = currentVal - 1
        num_posti.update()

    def aggiungi_automobile(e):
        try:
            if not input_aggiungi_anno.value.strip().isdigit():
                alert.show_alert("❌ Inserisci un anno valido")
                return

            if int(num_posti.value) <= 0:
                alert.show_alert("❌ Inserisci un numero di posti valido")
                return
            nuova_auto = autonoleggio.aggiungi_automobile(input_aggiungi_marca.value, input_aggiungi_modello.value, int(input_aggiungi_anno.value), int(num_posti.value))
            input_aggiungi_marca.value = ''
            input_aggiungi_modello.value = ''
            input_aggiungi_anno.value = ''
            num_posti.value = 0
            stato = "✅" if nuova_auto.disponibile else "⛔"
            lista_auto.controls.append(ft.Text(f"{stato} {nuova_auto}"))
            page.update()
        except Exception as e:
            alert.show_alert(f"❌ Errore inserisci valori numerici per anno e posti: {e}")

        # aggiungo contatore
    btnMinus = ft.IconButton(icon=ft.Icons.REMOVE,
                             icon_color="red",
                             icon_size=24, on_click=handleRemove)
    btnAdd = ft.IconButton(icon=ft.Icons.ADD,
                           icon_color="green",
                           icon_size=24, on_click=handleAdd)
    num_posti = ft.TextField(width=100, disabled=True,
                          value=0, border_color="green",
                          text_align=ft.TextAlign.CENTER)
    contatore_posti = ft.Row([btnMinus, num_posti, btnAdd],
                             alignment=ft.MainAxisAlignment.CENTER)

    # --- EVENTI ---
    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    pulsante_conferma_responsabile = ft.ElevatedButton("Conferma", on_click=conferma_responsabile)

    # Bottoni per la gestione dell'inserimento di una nuova auto
    # TODO
    pulsante_aggiungi_auto = ft.ElevatedButton("Aggiungi automobile", on_click=aggiungi_automobile)


    # --- LAYOUT ---
    page.add(
        toggle_cambia_tema,

        # Sezione 1
        txt_titolo,
        txt_responsabile,
        ft.Divider(),

        # Sezione 2
        ft.Text("Modifica Informazioni", size=20),
        ft.Row(spacing=200,
               controls=[input_responsabile, pulsante_conferma_responsabile],
               alignment=ft.MainAxisAlignment.CENTER),

        # Sezione 3
        # TODO
        ft.Text("Aggiungi auto", size=20),
        ft.Row(spacing=20,
               controls=[input_aggiungi_marca, input_aggiungi_modello, input_aggiungi_anno, contatore_posti],
               alignment=ft.MainAxisAlignment.CENTER),
        ft.Row(spacing=20,
               controls=[pulsante_aggiungi_auto],
               alignment=ft.MainAxisAlignment.CENTER),


        # Sezione 4
        ft.Divider(),
        ft.Text("Automobili", size=20),
        lista_auto,
    )
    aggiorna_lista_auto()

ft.app(target=main)
