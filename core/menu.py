class MenuItem:
    def __init__(self, name, child=None, action=None):
        self.name = name
        self.child = child
        self.action = action


class Menu:
    def __init__(self, banner, level_items, parent=None):
        self.banner = banner
        self.items = [MenuItem(n) for n in level_items]
        self.parent = parent
        self.pos = 0

    def reset(self):
        self.pos = 0

    def cur_item(self):
        return self.items[self.pos]

    def down(self) -> MenuItem:
        try:
            target = self.items[self.pos+1]
            self.pos += 1
        except IndexError:
            target = self.items[0]
            self.pos = 0
        return target

    def up(self) -> MenuItem:
        if self.pos >= 1:
            target = self.items[self.pos-1]
            self.pos -= 1
        else:
            target = self.items[-1]
            self.pos = len(self.items)
        return target


class Navigation:
    def __init__(self, lcd, kpd, top: Menu):
        self.lcd = lcd
        self.kpd = kpd
        # self.cur_item = top.items[top.pos]
        self.branch = [top]

    def _cur_menu(self):
        return self.branch[-1]

    def _draw(self):
        menu = self.branch[-1]
        self.lcd.clear()
        self.lcd.move_to(0, 0)
        self.lcd.putstr("{}\n{}".format(menu.banner, menu.cur_item().name))

    def start(self):
        self._draw()

    def down(self):
        menu = self.branch[-1]
        if menu.pos + 1 < len(menu.items):
            menu.pos += 1
        else:
            menu.pos = 0
        self._draw()

    def up(self):
        menu = self.branch[-1]
        if menu.pos >= 1:
            # target = menu.items[menu.pos-1]
            menu.pos -= 1
        else:
            # target = menu.items[-1]
            menu.pos = len(menu.items) - 1
        self._draw()

    def enter(self):
        # NOTE Fixed to work on site, chech for redundant conds
        menu_item = self.branch[-1].cur_item()
        if menu_item.action is None and menu_item.child is not None:
            self.branch.append(menu_item.child)
            self._draw()
        elif menu_item.action is not None:
            menu_item.action()
            self._draw()  # added on site

    def level_up(self):
        if self.branch[-1].parent is not None:
            self.branch[-1].pos = 0
            del self.branch[-1]
            self._draw()
        else:
            pass
