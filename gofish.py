import random
import tkinter as tk
import sys

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"this card is the {self.rank} of {self.suit}"

class Player:
    def __init__(self, name, book, hand):
        self.name = name
        self.book = book
        self.hand = hand

    def __str__(self):
        return f"The {self.name} has {self.book} books"

    def check_for_new_books(self):
        count = {}
        made_book_details = []
        for card in self.hand:
            current_rank = card.rank
            count[current_rank] = count.get(current_rank, 0) + 1
            
        books_made_this_check = 0
        ranks_booked = []
        for rank, num in list(count.items()):
            if num >= BOOK_VALUE:
                books_made_this_check += 1
                self.book += 1
                ranks_booked.append(rank)
                made_book_details.append(f"You made a book of {rank}s!")

                # remove all cards of the same rank
                self.hand = [card for card in self.hand if card.rank != rank]

        if made_book_details:
            return "\n".join(made_book_details)
        return None

    def check_books(self):
        return self.book

BOOK_VALUE = 4
WIN_VALUE = 2

suits = ['hearts', 'spades', 'diamonds', 'clubs']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'jack', 'queen', 'king', 'ace']

deck = [Card(suit, rank) for rank in ranks for suit in suits]

def main():

    random.shuffle(deck)
    player = Player("player", 0, create_deck())
    opponent = Player("opponent", 0, create_deck())

    root = tk.Tk()
    root.title("go fish")

    ui_elements = {}

    # --- FRAME FOR PLAYERS HAND ---
    player_hand_frame = tk.Frame(root, borderwidth=2, relief="groove")
    player_hand_frame.pack(side=tk.LEFT, pady=10, padx=10, fill=tk.Y, anchor='nw')
    ui_elements['player_hand_frame'] = player_hand_frame

    your_hand_title_label = tk.Label(player_hand_frame, text="Your Hand:")
    your_hand_title_label.pack(anchor='w')

    for card in player.hand:
        card_label = tk.Label(player_hand_frame, text=str(card))
        card_label.pack(anchor='w')


    # --- FRAME FOR OPPONENT HAND ---
    opponent_hand_frame = tk.Frame(root, borderwidth=2, relief="groove")
    opponent_hand_frame.pack(side=tk.RIGHT, pady=10, padx=10, fill=tk.Y, anchor='ne')

    opponent_hand_title_label = tk.Label(opponent_hand_frame, text="Opponent's Hand:")
    opponent_hand_title_label.pack()

    for card in opponent.hand:
        card_label = tk.Label(opponent_hand_frame, text=str(card))
        card_label.pack(anchor='w')


    # --- INFO and ACTION FRAME ---
    info_frame = tk.Frame(root)
    info_frame.pack(padx=10, pady=10)
    
    player_name_label = tk.Label(info_frame, text=f"Player: {player.name}")
    player_name_label.pack(anchor='w')
    player_book_label = tk.Label(info_frame, text=f"Books: {player.book}")
    player_book_label.pack(anchor='w')
    ui_elements['player_book_label'] = player_book_label

    opponent_name_label = tk.Label(info_frame, text=f"Player: {opponent.name}")
    opponent_name_label.pack(anchor='w')
    opponent_book_label = tk.Label(info_frame, text=f"Books: {opponent.book}")
    opponent_book_label.pack(anchor='w')
    ui_elements['opponent_book_label'] = opponent_book_label

    game_message_var = tk.StringVar()
    game_message_label = tk.Label(info_frame, textvariable=game_message_var, wraplength=200)
    game_message_var.set("Lets play Go Fish! Enter a rank and click 'Ask!'.")
    game_message_label.pack(anchor='w', pady=10)
    ui_elements['game_message_var'] = game_message_var


    # --- Entry and Button for asking for card
    ask_rank_entry = tk.Entry(info_frame, width=15)
    ask_rank_entry.pack(pady=5)
    ui_elements['ask_rank_entry'] = ask_rank_entry

    def check_for_books_and_update_gui(p_obj, asked_rank):
        book_message = p_obj.check_for_new_books()
        if book_message:
            if p_obj.name == player.name:
                ui_elements['player_book_label'].config(text=f"Books: {p_obj.book}")
            elif p_obj.name == opponent.name:
                ui_elements['opponent_book_label'].config(text=f"Books: {p_obj.book}")
            return book_message
        return None

    def on_ask_button_click():
        rank_to_ask = ui_elements['ask_rank_entry'].get().strip().lower()
        ui_elements['ask_rank_entry'].delete(0, tk.END)


        if not rank_to_ask:
            ui_elements['game_message_var'].set("please enter a rank to ask for.")
            return

        if rank_to_ask not in ranks:
            ui_elements['game_message_var'].set(f"Invalid rank: '{rank_to_ask}'. Try again")
            return
        
        # game logic for ask button
        ui_elements['game_message_var'].set(f"You asked for {rank_to_ask}s.")

        cards_received = []

        for card_in_opponent_hand in list(opponent.hand):
            if card_in_opponent_hand.rank == rank_to_ask:
                cards_received.append(card_in_opponent_hand)
                player.hand.append(card_in_opponent_hand)
                opponent.hand.remove(card_in_opponent_hand)

        refresh_player_hand_display(player, ui_elements['player_hand_frame'])

        if cards_received:
            message = f"Opponent had {len(cards_received)} {rank_to_ask}(s)! you get:"
            for card_obj in cards_received:
                message += f"\n - {str(card_obj)}"
            ui_elements['game_message_var'].set(message)
        else:
            ui_elements['game_message_var'].set(f"Opponent has no {rank_to_ask}s. go fish!")
            if deck:
                drawn_card = deck.pop(random.randrange(len(deck)))
                player.hand.append(drawn_card)
                ui_elements['game_message_var'].set(
                    f"Go Fish! You drew the {str(drawn_card)}."
                )
                if drawn_card.rank == rank_to_ask:
                    ui_elements['game_message_var'].set(
                        f"Go Fish! you draw the {str(drawn_card)}. Lucky draw!")

            else:
                ui_elements['game_message_var'].set("Go Fish! The deck is empty!")


        player_made_book_message = check_for_books_and_update_gui(player, rank_to_ask)
        ui_elements['player_book_label'].config(text=f"Books: {player.book}")

        if player.book >= WIN_VALUE:
            ui_elements['game_message_var'].set(f"PLAYER WINS with {player.book} books!")
            ui_elements['ask_rank_entry'].config(state=tk.DISABLED)
            ui_elements['ask_button'].config(state=tk.DISABLED)
            return


    ask_button = tk.Button(info_frame, text="Ask for Card", command=on_ask_button_click)
    ask_button.pack(pady=5)
    ui_elements['ask_button'] = ask_button

    refresh_player_hand_display(player, ui_elements['player_hand_frame'])

    root.mainloop()

    sys.exit("game over")


def refresh_player_hand_display(current_player, hand_frame):
    for widget in list(hand_frame.winfo_children()):
        if widget != hand_frame.winfo_children()[0]:    
            widget.destroy()

#    your_hand_title_label = tk.Label(hand_frame, text="Your Hand:")
#    your_hand_title_label.pack(anchor='w')

    for card_obj in current_player.hand:
        card_label = tk.Label(hand_frame, text=str(card_obj))
        card_label.pack(anchor='w')

def create_deck():
    global deck
    d = []
    for _ in range(7):
        randomcard = random.choice(deck)
        d.append(randomcard)
        deck.remove(randomcard)
    return d

def pick_card(r):
    while True:
        try:
            choice = input("choose a card: ")
            if choice not in r:
                raise ValueError
            if choice in r:
                return choice
        except ValueError:
            print("card must be a valid pick")


if __name__ == "__main__":
    main()































