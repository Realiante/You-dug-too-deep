import resources

# Requirements for player are an existing control scheme and
# 1 preview and 6 running frames as standard images stored in resources/images/character/{character}
import resources


class CharacterData:

    def __init__(self, doc):
        self.name = doc.getAttribute("name")
        chr_name = doc.getAttribute("character")
        self.character_path = f"character/{chr_name}/"
        self.preview = resources.images.load_img(self.character_path + "_preview.png")
        self.scheme = resources.schemes.load_scheme(doc.getAttribute("control"))

    def create_character(self, spd: int, shield: int):
        return Character(data=self, spd=spd, shield=shield)


class Character:

    def __init__(self, data: CharacterData, spd: int, shield: int):
        self.name = data.name
        self.spd = spd
        self.shield = shield

        # preview image for the character
        path = data.character_path
        self.preview_img = resources.images.load_img(path + "_preview.png")

        # immutable collection of run animation frames consisting of 6 frames
        path = path + "_run_f{}.png"
        self.run_anim = (
            resources.images.load_img(path.format(0)), resources.images.load_img(path.format(1)),
            resources.images.load_img(path.format(2)),
            resources.images.load_img(path.format(3)), resources.images.load_img(path.format(4)),
            resources.images.load_img(path.format(5)))
        self.cur_frame = 0
        # loading the control scheme
        self.scheme = data.scheme
        # setting game related parameters
        self.health = 3
        self.can_exit = False
        self.win = False
        self.dead = False

    def take_damage(self, damage: int):
        if self.shield > 0:
            self.shield -= damage
            if self.shield < 0:
                self.shield = 0
        else:
            self.health -= damage
            if self.health <= 0:
                self.health = 0
                self.dead = True
