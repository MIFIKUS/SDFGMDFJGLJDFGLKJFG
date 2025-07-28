from pywinauto import Desktop
import time

main_lobby = Desktop(backend="uia").window(title_re="PokerKing Lobby Logged in as.*")


def _get_list_of_tournaments() -> list:
    all_buttons = main_lobby.descendants(control_type="Button")


    matching = []
    for btn in all_buttons:
        name = btn.element_info.name or ""
        if 'Add this event to "Yours" section.' in name:
            matching.append(btn)
    return matching


def _open_tournament(tournament_button):
    tournament_button.click_input()
    time.sleep(10)



 
t = _get_list_of_tournaments()
for i in t:
    _open_tournament(i)




