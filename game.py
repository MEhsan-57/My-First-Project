from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.button import MDRaisedButton
from kivymd.toast import toast
from kivy.metrics import dp

KV = '''
MDScreen:

    MDBoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: "Tic Tac Toe"
            elevation: 10

        GridLayout:
            id: grid
            cols: 3
            rows: 3
            spacing: 10
            padding: 20
'''

class TicTacToeApp(MDApp):
    def build(self):
        self.current_player = "X"
        self.buttons = []  # ✅ بٹنوں کی لسٹ
        self.root = Builder.load_string(KV)
        self.create_grid()
        return self.root

    def create_grid(self):
        grid = self.root.ids.grid
        for i in range(3):
            row = []
            for j in range(3):
                btn = MDRaisedButton(
                    text='',
                    font_size = 30,
                    size_hint=(1, 1),
                    on_release=self.on_button_press
                )
                grid.add_widget(btn)
                row.append(btn)
            self.buttons.append(row)

    def on_button_press(self, instance):
        if instance.text != '':
            return  # ✅ پہلے سے دبے ہوئے بٹن پر دوبارہ کچھ نہ ہو

        instance.text = self.current_player

        if self.check_winner(self.current_player):
            toast(f"{self.current_player} wins!")
            self.disable_all_buttons()
            return

        self.current_player = "O" if self.current_player == "X" else "X"

    def disable_all_buttons(self):
        for row in self.buttons:
            for btn in row:
                btn.disabled = True

    def check_winner(self, player):
        b = self.buttons

        # ✅ Rows
        for row in b:
            if all(btn.text == player for btn in row):
                return True

        # ✅ Columns
        for col in range(3):
            if all(b[row][col].text == player for row in range(3)):
                return True

        # ✅ Diagonals
        if all(b[i][i].text == player for i in range(3)):
            return True
        if all(b[i][2 - i].text == player for i in range(3)):
            return True

        return False

if __name__ == "__main__":
    TicTacToeApp().run()