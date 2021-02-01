import resources


# Requirements for player are an existing control scheme and
# 1 preview and 6 running frames as standard images stored in resources/img/character/{character}


class Character:

    def __init__(self, texture: str, control_scheme: str, name: str):
        self.texture = texture
        self.name = name

        # preview image for the character
        path = "character/" + texture
        self.preview_img = resources.load_img(path + "_preview.png")

        # immutable collection of run animation frames consisting of 6 frames
        path = path + "_run_f{}.png"
        self.run_anim = (
            resources.load_img(path.format(0)), resources.load_img(path.format(1)), resources.load_img(path.format(2)),
            resources.load_img(path.format(3)), resources.load_img(path.format(4)), resources.load_img(path.format(5)))
        self.cur_frame = 0
        # loading the control scheme
        self.scheme = Scheme(control_scheme)
        # setting game related parameters
        self.health = 3
        self.can_exit = False
        self.win = False
        self.dead = False

    def take_damage(self, damage: int):
        self.health -= damage
        if self.health >= 0:
            self.health = 0
            self.dead = True


class Scheme:

    def __init__(self, control_scheme: str):
        controls = resources.load_scheme(control_scheme)

        self.up = controls[0]
        self.down = controls[1]
        self.left = controls[2]
        self.right = controls[3]
        self.action = controls[4]
        self.switch = controls[5]
