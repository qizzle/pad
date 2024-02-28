import pygame
from translations.translator import Translator


class PixelAndDragons:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("pixel & dragons")

        self.t = Translator("en-US")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("quaver", 15)
        self.screen = pygame.display.set_mode((256, 256), pygame.SCALED)

        self.logo = pygame.image.load("./images/logo.png").convert_alpha()  # Logo
        self.class_select = pygame.image.load("./images/classselect.png").convert()  # Klassen Selektor
        self.select_arrow = pygame.image.load("./images/selectarrow.png").convert_alpha()  # Pfeil im Hauptmenü
        self.select_arrow_h = pygame.image.load("./images/selectarrow_h.png").convert_alpha()  # Pfeil im Klassen Selektor

        self.select_arrow_pos = 1  # Position vom Pfeil im Hauptmenü
        self.select_arrow_h_pos = 1  # Position vom Pfeil im Klassen Selektor
        self.running = True  # Ob das Spiel noch läuft
        self.show_mainscreen = True  # Ob das Hauptmenü geöffnet sein soll
        self.show_class_select = False  # Ob der Klassen Selektor geöffnet sein soll
        self.selected_class = None  # Selektierte Spieler Klasse, entweder "fighter" oder "wizard"

    def run(self) -> None:
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.KEYDOWN and self.show_mainscreen:  # Nur für Hauptbildschirm
                    if event.key == pygame.K_DOWN:
                        self.select_arrow_pos += 1 if self.select_arrow_pos < 3 else 0
                    if event.key == pygame.K_UP:
                        self.select_arrow_pos -= 1 if self.select_arrow_pos > 1 else 0
                    if event.key == pygame.K_RETURN:
                        match self.select_arrow_pos:
                            case 1:  # START Button
                                # starte spiel
                                self.show_mainscreen = False
                                self.show_class_select = True
                                break
                            case 2:  # CHANGE LANGUAGE Button
                                # ändert die Sprache, je nachdem welche grade benutzt wird
                                match self.t.get_lang():
                                    case "de-DE":
                                        self.t.change_lang("en-US")
                                        break
                                    case "en-US":
                                        self.t.change_lang("de-DE")
                                        break
                                break
                            case 3:  # QUIT Button
                                # Schließe spiel
                                self.running = False

                if event.type == pygame.KEYDOWN and self.show_class_select:  # Nur für Klassen Selektor
                    if event.key == pygame.K_LEFT:
                        self.select_arrow_h_pos += 1 if self.select_arrow_h_pos < 2 else -1
                    if event.key == pygame.K_RIGHT:
                        self.select_arrow_h_pos -= 1 if self.select_arrow_h_pos > 1 else -1
                    if event.key == pygame.K_RETURN:
                        classes = ["fighter", "wizard"]
                        self.selected_class = classes[self.select_arrow_h_pos - 1]
                        self.show_class_select = False
            # Scenes

            self.screen.fill((0, 0, 0))

            if self.show_class_select:
                self.screen.blit(self.class_select, (0, 0))

                self.screen.blit(self.font.render(self.t.translate("main.enter"), False, (255, 255, 255)),
                                 (256 - self.font.size(self.t.translate("main.enter"))[0] - 16, 232))

                self.screen.blit(self.font.render(self.t.translate("classes.fighter"), False, (255, 255, 255)),
                                 (47, 64))
                self.screen.blit(self.font.render(self.t.translate("classes.wizard"), False, (255, 255, 255)),
                                 (132, 64))

                self.screen.blit(self.select_arrow_h, (self.select_arrow_h_pos * 78, 256 - 71))

            # Hauptbildschirm
            if self.show_mainscreen:
                self.screen.fill((0, 0, 0))

                self.screen.blit(self.logo, (72, 36))  # Logo rendern
                self.screen.blit(self.font.render(self.t.translate("main.enter"), False, (255, 255, 255)),
                                 (256 - self.font.size(self.t.translate("main.enter"))[0] - 16, 232))  # "ENTER - Confirm" render

                self.screen.blit(self.font.render("{} Dimitri B.".format(self.t.translate("main.by")), False,
                                                  (255, 255, 255)), (16, 232))  # "by" rendern

                self.screen.blit(self.font.render(self.t.translate("main.start"), False, (255, 255, 255)),
                                 (256 / 2 - self.font.size(self.t.translate("main.start"))[0] / 2, 112))  # "START" render
                self.screen.blit(self.font.render(self.t.translate("main.changelang"), False, (255, 255, 255)),
                                 (256 / 2 - self.font.size(self.t.translate("main.changelang"))[0] / 2, 128))  # "CHANGE LANG" render
                self.screen.blit(self.font.render(self.t.translate("main.quit"), False, (255, 255, 255)),
                                 (256 / 2 - self.font.size(self.t.translate("main.quit"))[0] / 2, 144))  # "QUIT" render
                self.screen.blit(self.select_arrow,
                                 (256 / 2 - self.font.size(self.t.translate("main.changelang"))[0] / 2 - 16, 97 +
                                  self.select_arrow_pos * 16))  # Aktiver Pfeil render

            pygame.display.flip()

            self.clock.tick(60)  # max. 60fps

        pygame.quit()
