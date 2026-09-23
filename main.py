#archaic-spin_v1.014
#redo dmg and stamina, standardised defence
#next to start doing ults
#milestone goal: ults

import pygame
import math
import asyncio

pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode((750, 750))
font = pygame.font.Font(None, size=30)
timestop = 0
p1_skill = False
p2_skill = False

center_x, center_y = 375,375
center= pygame.Vector2(center_x, center_y)
collided = False

dir_key1 = True
dir_key2 = True
C1 = 'einherjar'
C2 = 'titantrium'
C1_movement_skill = 'accel'
C2_movement_skill = 'anchor'



def make_circle_points(radius, num_points=30):
    points = []
    for i in range(num_points):
        angle = 2 * math.pi * i / num_points
        points.append([radius * math.cos(angle), radius * math.sin(angle)])
    return points


movement_skills = {
    "accel": {
        "cooldown": 250,
        "duration": 40,
        "vel_boost": 2.5,
        "kb_reflect": False,
        "desc":["accelerates in current ",
                "direction, ",
                "[does not affect hit velocity]"]
    },
    "guard": {
        "cooldown": 200,
        "duration": 20,
        "vel_boost": 1.5,
        "kb_reflect": True,     # hit_vel gets flipped
        "desc": ['flips direction to counter, ',
                 'gives a slight base',
                 'velocity boost']
    },
    "anchor": {
        "cooldown": 200,
        "duration": 70,
        "vel_boost": 0.05,       # slows down
        "kb_reflect": False,
        'desc': ['drops all velocity, ',
                 '[affects hit velocity]',
                 'regains some stamina ',
                 'if user is a stamina type']

    }
}



layers = {
    "Calesvol": {
        "type": "attack",
        "weight":0.06,
        "grip": 0.07,
        "inertia_strength":2,
        "color": (240,0,10),
        'desc':['attack type with strong crit ',
                'but only on the tip'],
#weight= 0.06, grip = 0.07,inertia_strength= 2,
        "parts": [
            {
                "name": "core",
                "points": make_circle_points(30),
                "color": (0, 170, 220),
                "knockback": 0.1,
                "resistance": 0,
                "the_core": True
            },

            {
                "name": "left_hilt",
                "points": [[-30.11, -17.5], [-8, -32], [-22, -8], [-18, 18], [-30, 5]],
                "color": (240, 0, 10),
                "knockback": 10,
                "resistance": 0.9
            },
            {
                "name": "right_hilt",
                "points": [[30.11,-17.5],[8,-32],[22,-8],[18,18],[30,5]],
                "color": (240, 0, 10),
                "knockback": 10,
                "resistance": 0.9

            },
            {
                "name": "big_blade",
                "points": [[0, 38], [13, 22], [17, -4], [0, -25], [-17, -4], [-13, 22]],
                "color": (240, 0, 10),
                "knockback": 17,
                "resistance": 1
            },
            {
                "name": "diamond",
                "points": [[12, 0],[0, -14],[-12, 0], [0,28]],
                "color": (255, 255, 0),
                "knockback": 0,
                "resistance": 0,
            },

        ]
    },
    "Garmr": {
        "type":"defence",
#weight= 0.08, grip =0.05,inertia_strength=0.5,
        "weight": 0.08,
        "grip": 0.06,
        "inertia_strength": 0.7,
        "color": (20,180,20),
        'desc': ['defence type with two guards ',
                 'that tank hits and two pokes ',
                 'that do minor knockback'],

        "parts": [
            {
                "name": "core",
                "points": make_circle_points(30),
                "color": (100, 100, 110),
                "knockback": 0.1,
                "resistance": 0,
                "the_core": True
            },
            {
                "name": "guard_1",
                "points": [[-34, -12], [-23, -26], [-9, -26], [-5, -24], [-17, -4], [-13, 20], [-28, 18], [-32, 2],
                           [-27, -4]],
                "color": (20, 180, 20),
                "knockback": 6,
                "resistance": 0.6
            },
            {
                "name": "guard_2",
                "points": [[34, 12], [23, 26], [9, 26], [5, 24], [17, 4], [13, -20], [28, -18], [32, -2],
                           [27, 8]],
                "color": (20, 180, 20),
                "knockback": 6,
                "resistance": 0.6
            },
            {
                "name": "prod_1",
                "points": [[-21, 25], [-25, 2], [-4, 35]],
                "color": (20, 100, 20),
                "knockback": 11,
                "resistance": 0.75
            },
            {
                "name": "prod_2",
                "points": [[21, -25], [25, -2], [4, -35]],
                "color": (20, 100, 20),
                "knockback": 11,
                "resistance": 0.75
            },

        ]
    },
"einherjar": {
        "type":"attack",
#stats
        "weight": 0.07,
        "grip": 0.05,
        "inertia_strength": 3,
        "color": (50, 150, 250),
        'desc': ['attack type with three menacing','blades with crit on the red, ',
                 'has a very steep launch pattern'],

    "parts": [

            {
                "name": "core",
                "points": make_circle_points(30),
                "color": (100, 100, 100),
                "knockback": 0.1,
                "resistance": 0,
                "the_core": True
            },
            {
                "name": "blade_1",
                "points": [[25.9808, -15], [26, -26], [19, -32.5], [19, -26], [12, -34], [1, -35], [11, -25]],
                "color": (50, 150, 250),
                "knockback": 9,
                "resistance": 0.9
            },
            {
                "name": "blade_2",
                "points": [[-0.0004, 30.0000], [9.5167, 35.5167], [18.6458, 32.7045], [13.0167, 29.4545],
                           [23.4449, 27.3923], [29.8109, 18.3660], [16.1506, 22.0263]],
                "color": (50, 150, 250),
                "knockback": 9,
                "resistance": 0.9
            },
            {
                "name": "blade_3",
                "points": [[-25.9804, -15.0000], [-35.5167, -9.5167], [-37.6458, -0.2045],
                           [-32.0167, -3.4545], [-35.4449, 6.6077], [-30.8109, 16.6340], [-27.1506, 2.9737]],
                "color": (50, 150, 250),
                "knockback": 9,
                "resistance": 0.9
            },


            {
                "name": "crit_1",
                "points": [[25.9808,-15], [28, -28], [30,-7], ],
                "color": (240, 0, 10),
                "knockback": 13,
                "resistance": 0.95
            },
            {
                "name": "crit_2",
                "points": [[-0.0004, 30.0],[10.2487, 38.2487],[-8.9378, 29.4808]],
                "color": (240, 0, 10),
                "knockback": 13,
                "resistance": 0.95
            },
            {
                "name": "crit_3",
                "points": [[-25.9804, -15.0],[-38.2487, -10.2487],[-21.0622, -22.4808]],
                "color": (240, 0, 10),
                "knockback": 13,
                "resistance": 0.95
            },

        ]
    },
"Götterdämmerung": {
        "type":"stamina",
#stats
        "weight": 0.085,
        "grip": 0.05,
        "inertia_strength": 0.5,
        "color": (255, 120, 0),
        'desc': ['stamina type that can hold',
                 'its weight using its two guards'],

        "parts": [
            {
                "name": "core",
                "points": make_circle_points(30),
                "color": (250, 190, 100),
                "knockback": 0.1,
                "resistance": 0,
                "the_core": True
            },
            {
                "name": "blade_1",
                "points": [[0, -30], [-8, -33], [-23, -28], [-29, -15], [-33, 2], [-25, 8], [-22, -7]],
                "color": (255, 120, 0),
                "knockback": 5,
                "resistance": 0.8
            },
            {
                "name": "blade_2",
                "points": [[-0, 30], [8, 33], [23, 28], [29, 15], [33, -2], [25, -8], [22, 7]],
                "color": (255, 120, 00),
                "knockback": 5,
                "resistance": 0.8
            },

        ]
    },
"titantrium": {
        "type":"attack",
#stats
        "weight": 0.075,
        "grip": 0.07,
        "inertia_strength": 2.1,
        "color": (80, 80, 80),
        'desc': ['attack type with two ',
                 'blunt heavy blows'],

        "parts": [
            {
                "name": "core",
                "points": make_circle_points(30),
                "color": (120, 120, 120),
                "knockback": 0.1,
                "resistance": 0,
                "the_core": True
            },
            {
                "name": "titanium_blade_1",
                "points": [[0, 30], [-7, 34], [-23, 28], [-29, 15], [-22, 7]],
                "color": (80,80 , 80),
                "knockback": 12,
                "resistance": 0.8
            },
            {
                "name": "titanium_hilt_1",
                "points": [[-20, 25], [-34, -7.5],[-27,-20] ,[-20,-20],[-18,10] ],
                "color": (170, 170, 170),
                "knockback": 10,
                "resistance": 0.75
            },
            {
                "name": "titanium_blade_2",
                "points": [[0, -30], [7, -34], [23, -28], [29, -15], [22, -7]],
                "color": (80, 80, 80),
                "knockback": 12,
                "resistance": 0.8
            },
            {
                "name": "titanium_hilt_2",
                "points": [[20, -25], [34, 7.5], [27, 20], [20, 20], [18, -10]],
                "color": (170, 170, 170),
                "knockback": 10,
                "resistance": 0.75
            },

        ]
    },
}


def polygons_overlap(poly1, poly2):
    # Check both polygons' edges as potential separating axes
    for polygon in [poly1, poly2]:
        n = len(polygon)
        for i in range(n):
            # Get one edge of the polygon
            ax = polygon[i][0]
            ay = polygon[i][1]
            bx = polygon[(i + 1) % n][0]
            by = polygon[(i + 1) % n][1]

            # The axis perpendicular to this edge (the "shadow direction")
            axis_x = -(by - ay)
            axis_y = bx - ax

            # Project all points of both shapes onto this axis
            min1 = max1 = ax * axis_x + ay * axis_y
            for px, py in polygon:
                p = px * axis_x + py * axis_y
                min1 = min(min1, p)
                max1 = max(max1, p)

            min2 = max2 = poly2[0][0] * axis_x + poly2[0][1] * axis_y
            for px, py in poly2:
                p = px * axis_x + py * axis_y
                min2 = min(min2, p)
                max2 = max(max2, p)

            # If shadows don't overlap on this axis → shapes not touching
            if max1 < min2 or max2 < min1:
                return False

    return True  # All axes overlapped → shapes ARE colliding

def wall_hit_circle(wall, circle):
    segments = [wall.world_points_1, wall.world_points_3, wall.world_points_2]
    for segment in segments:
        for part in circle.world_parts:
            if polygons_overlap(segment, part["points"]):

                wall_cx = sum(p[0] for p in segment) / len(segment)
                wall_cy = sum(p[1] for p in segment) / len(segment)
                normal = (circle.pos - pygame.Vector2(wall_cx, wall_cy))
                if normal.length() > 0:
                    normal = normal.normalize()
                    circle.base_vel += normal * 1.5
                    circle.hit_vel += normal * 1.5
                    circle.stamina -= 0.00002

                    circle.inertia += 2
                return True
    return False



class Circle:
    def __init__(self, pos, last_distance, calc_distance, inertia, count,
                 duration, startx, starty,domain,grip,inertia_strength,base_vel,hit_vel,vel,
                 angle,layers,stamina,lose,hit_cooldown,movement_skill):
        self.pos = pos
        self.last_distance = last_distance
        self.calc_distance = calc_distance
        self.inertia = inertia
        self.count = count
        self.duration = duration
        self.startx = startx
        self.starty = starty
        self.domain = domain
        self.grip = grip
        self.inertia_strength = inertia_strength
        self.base_vel = base_vel
        self.hit_vel = hit_vel
        self.vel= vel
        self.angle = angle
        self.layers = layers
        self.stamina = stamina
        self.world_parts = []
        self.lose = lose
        self.hit_cooldown = hit_cooldown
        self.contact_cd = 0
        self.trail = []
        self.ult_trail = []
        self.movement_skill_trail = []

        # physics using vectors
        self.pos = pygame.Vector2(self.startx, self.starty)

        #movement skill
        self.movement_skill = movement_skill
        self.movement_skill_cd = 0
        self.in_movement_skill = 0


    def inspin(self,center, ):

        self.angle += self.stamina*4+0.001
        self.stamina -= 0.000005
        if self.stamina < 0.07:
            self.stamina -= 0.00001
            if self.stamina < 0.05:
                self.stamina -= 0.0002
                if self.stamina < 0.03:
                    self.stamina -= 0.0003

        if self.stamina < 0:
            self.stamina = 0
        self.duration -= 0.000001 * self.count
        self.duration = max(0.3, self.duration)

        self.vel = self.base_vel + self.hit_vel

        # direct toward the center
        self.direction = center - self.pos

        # distance
        distance = self.direction.length()
        if distance != 0:
            self.direction = self.direction / distance

        # gravity
        weight = layers[self.layers]["weight"]
        turn_rate = 1
        if distance >310:
            if layers[self.layers]["type"] == "attack":
                turn_rate = turn_rate * 1.2

        gravity = self.direction * weight *(1 + distance * 0.003) *turn_rate
        turn_rate *= 0.5
        if turn_rate < 1:
            turn_rate = 1

        # Pull force
        # acceleration = direction * 0.3
        grip = layers[self.layers]["grip"]
        tangent = pygame.Vector2(-self.direction.y, self.direction.x)
        orbit = tangent * grip * self.duration

        # inertia
        if self.last_distance is not None:
            self.calc_distance = self.last_distance - distance
        if self.calc_distance > 0:
            self.inertia += 1
        if self.calc_distance < 0:
            self.inertia -= 1

        self.last_distance = distance





        inertia_strength = layers[self.layers]["inertia_strength"]


        #the dash into center attack
        if self.inertia > 25 and self.duration < 700:
            self.base_vel += gravity * 12*inertia_strength + orbit * 0.55
            self.base_vel *= 0.98
            self.inertia -= 5
            if layers[self.layers]["type"] == "attack":
                self.stamina -= 0.00005
                self.grip = 200


        elif self.inertia > 20:
            self.base_vel += gravity * 6*inertia_strength + orbit * 0.6
            self.base_vel *= 0.98
            self.inertia -= 5
            if layers[self.layers]["type"] == "attack":
                self.stamina -= 0.00005
                if distance > 130:
                    self.base_vel += gravity * 2*inertia_strength
                    if distance > 280:
                         self.grip = 200
                    self.stamina -= 0.00005

        else:
            self.base_vel += (gravity*1.2 + orbit)
            self.base_vel *= 0.985
            if distance > 280:
                if layers[self.layers]["type"] == "attack":
                    self.grip = 200

        #rush launch cushion




        #ko
        if self.count > 1:
            if self.stamina == 0:
                self.lose = True
            if distance > 360:  # leeway + circle
                self.lose = True

        #debuffs
        if layers[self.layers]["type"] == "attack":
            if distance <100:
                self.stamina += 0.0000015
        else:
            if self.stamina > 0:
                if distance < 105:
                    self.stamina += 0.0000025
                    self.domain = True


                    if layers[self.layers]["type"] == "stamina":
                        self.stamina += 0.0000015
                        if distance > 20:
                            self.stamina += 0.0000008
                    if self.stamina < 0.07:
                        self.stamina += 0.000005
                        if self.stamina < 0.05:
                            self.stamina += 0.00002
                else:
                    self.domain = False
                if distance > 220:
                    self.stamina -= 0.0000025

        #trail
        self.trail.append((self.pos.x, self.pos.y))

        if len(self.trail) > 60:
            self.trail.pop(0)

        #hit cd
        if self.hit_cooldown > 0:
            self.hit_cooldown -= 1

        # contact cd
        if self.contact_cd > 0:
            self.contact_cd -= 1

        #max speed
        max_speed = 12  #rigged
        if self.vel.length() > max_speed:
            self.vel.scale_to_length(max_speed)


        #movement_skills timer
        if self.movement_skill_cd> 0:
            self.movement_skill_cd -= 1
        if self.in_movement_skill > 0:
            self.in_movement_skill -= 1
        #movement_skills code
        movement_skill = movement_skills[self.movement_skill]
        if self.in_movement_skill > 0:
            if movement_skill["kb_reflect"]:
                self.hit_vel *= -1
            if self.movement_skill == 'anchor':
                self.hit_vel *= 0.5
                self.base_vel *= 0.5
                self.inertia += 1



        #movement_skill indicator == the trail
        self.movement_skill_trail.append((self.pos.x, self.pos.y))

        if len(self.movement_skill_trail) > 25:
            self.movement_skill_trail.pop(0)





        #physcis update per frame
        self.pos += self.vel
        self.count += 1
        if layers[self.layers]["type"] == "attack":
            self.hit_vel *= 0.9
        else:
            self.hit_vel *= 0.95


    def draw(self,R,G,B):
        text_count = font.render(str(self.count), True, (255, 255, 255))
        text_inertia = font.render(str(self.inertia), True, (255, 255, 255))

        pygame.draw.circle(screen, (R, G, B), self.pos, 30)

        #screen.blit(text_inertia, (20, 20))


    def update_parts(self):

        self.world_parts = []
        layer = layers[self.layers]
        for part in layer["parts"]:
            rotated = []
            for px, py in part["points"]:
                rx = self.pos.x + px * math.cos(self.angle) - py * math.sin(self.angle)
                ry = self.pos.y + px * math.sin(self.angle) + py * math.cos(self.angle)
                rotated.append((rx, ry))
            self.world_parts.append({
                "name": part["name"],
                "points": rotated,
                "color": part["color"],
                "knockback": part["knockback"],
                "resistance": part["resistance"],
                "is_core": part.get("is_core", False)
            })

    def draw_parts(self):
        for part in self.world_parts:
            pygame.draw.polygon(screen, part["color"], part["points"])

    def draw_trail(self):

        if len(self.trail) < 2:
            return

        for i in range(1, len(self.trail)):
            age = i / len(self.trail)

            brightness = int(255 * age)

            pygame.draw.line(
                screen,
                (brightness, brightness, brightness),
                self.trail[i - 1],
                self.trail[i],
                2
            )

    def draw_movement_skill_trail(self):
        color = layers[self.layers]["color"]
        if len(self.movement_skill_trail) < 2:
            return

        for i in range(1, len(self.movement_skill_trail)):


            pygame.draw.line(
                screen,
                (250,10,250 ),
                self.movement_skill_trail[i - 1],
                self.movement_skill_trail[i],
                25
            )
            pygame.draw.line(
                screen,
                (210,0 ,200  ),
                self.movement_skill_trail[i - 1],
                self.movement_skill_trail[i],
                20
            )

    def hit(self, other):
        if self.hit_cooldown > 0:
            return False
        if self.contact_cd > 0 or other.contact_cd > 0:
            return False

        delta = self.pos - other.pos
        if delta.length() == 0:
            return False
        normal = delta.normalize()

        # ---- PHASE 1: scan, don't apply anything ----
        best = None
        best_score = -1

        for my_part in self.world_parts:
            for their_part in other.world_parts:
                if not polygons_overlap(my_part["points"], their_part["points"]):
                    continue

                # TODO: compute whatever "how strong is this contact" score you want
                # stating vars
                #vel_strength = len(self.vel)/3 so interesting how i got this wrong
                vel_strength = self.vel.length() / 3
                if layers[self.layers]["type"] == "attack":
                    vel_strength = max(0.9, min(vel_strength, 3))
                else:
                    vel_strength = max(1.5, min(vel_strength, 4))
                kb = my_part["knockback"]
                kb = kb * vel_strength
                res_other = their_part["resistance"]

                #print(vel_strength)
                force = kb * res_other

                if force < 2.5:
                    continue
                if res_other == 0:  # ignore deco
                    continue

                if force > best_score:
                    best_score = force
                    best = {
                        "my_part": my_part,
                        "their_part": their_part,
                        "kb": kb,
                        "res_other": their_part["resistance"],
                        "res": my_part["resistance"],
                        "vel_strength": vel_strength,
                        "force": force,
                    }
                avg_x = sum(p[0] for p in my_part["points"] + their_part["points"]) / (
                        len(my_part["points"]) + len(their_part["points"]))
                avg_y = sum(p[1] for p in my_part["points"] + their_part["points"]) / (
                        len(my_part["points"]) + len(their_part["points"]))
                pygame.draw.circle(screen, (255, 255, 255), (avg_x, avg_y), 6)

                print(my_part["name"], "vs", their_part["name"])

        if best is None:
            return  # nothing valid overlapped



        # ---- PHASE 2: apply damage exactly once ----
        # TODO: your new damage/knockback formula goes here,
        # using my_part / their_part / normal
        stamina_dmg = 0
        stamina_dmg_other = 0

        my_part = best["my_part"]
        their_part = best["their_part"]
        kb = best["kb"]
        res = best["res"]
        res_other = best["res_other"]
        force = best["force"]
        vel_strength = best["vel_strength"]

        weight = layers[self.layers]["weight"]
        weight2 = layers[other.layers]["weight"]

        #core hit
        if their_part["is_core"]:

            stamina_dmg_other -= kb
            other.hit_vel += -normal * kb
            self.hit_vel += -normal * force
            if my_part["is_core"]:
                stamina_dmg -= kb


        # excalibur buff
        elif my_part["name"] == "big_blade":

            print(f"big hit")
            if layers[other.layers]["type"] == "defence":
                other.hit_vel += -normal * kb * weight/weight2
                #stamina_dmg += 0.0005
                self.hit_vel += normal * force  * weight/weight2
            else:
                other.hit_vel += -normal * kb * weight/weight2
                #stamina_dmg += 0.0009
                self.hit_vel += normal * force * weight/weight2
            stamina_dmg -= force * 0.00008
            other.stamina -= force * 0.00018
            pygame.draw.circle(screen, (240, 240, 240), (avg_x, avg_y), 20)


        else:
        #normal hit
            other.hit_vel += -normal * force * (weight/weight2)
            self.hit_vel += normal * force * (weight / weight2)

            stamina_dmg -= force * 0.00008
            other.stamina -= force * 0.00018

        # stamina movement_skill
        if layers[self.layers]["type"] == "stamina":
            if self.in_movement_skill > 0:
                stamina_dmg *= 0.2
                self.hit_vel *= 0.3
            if self.domain == True:
                stamina_dmg *= 0.7
                self.hit_vel *= 0.9

        self.stamina += stamina_dmg
        other.stamina += stamina_dmg_other
        print(
            f"{my_part['name']} -> {their_part['name']} | "
            f"speed={self.vel.length():.2f} | "
            f"vel_strength={vel_strength:.2f} | "
            f"force={force:.3f}"
        )

        #self.hit_cooldown = 20
        self.contact_cd = 10
        other.contact_cd = 10
        global timestop
        timestop = 20
        print("distance after hit:", self.pos.distance_to(other.pos))
        return True

class Wall :
    def __init__(self, length, breadth,  circle , angle, spread ):
        self.length = length
        self.breadth = breadth
        self.circle = circle
        self.angle = angle
        self.world_points_1 = []
        self.world_points_2 = []
        self.world_points_3 = []
        self.spread = math.radians(spread)



    def update(self, direction):
        # direction = -1, 0, or +1 based on player input

        self.angle += 0.04 * direction

        self.world_points_1 =self.build_segment(-self.spread)
        self.world_points_2 = self.build_segment(self.spread)
        self.world_points_3 = self.build_segment(0)

    def build_segment(self, spread):
        seg_angle = self.angle + spread  # THIS combines orbit rotation + offset
        cx = center.x + 360 * math.cos(seg_angle)
        cy = center.y + 360 * math.sin(seg_angle)

        half_len = self.length / 2
        half_wid = self.breadth / 2
        local_points = [(-half_len, -half_wid), (half_len, -half_wid),
                        (half_len, half_wid), (-half_len, half_wid)]

        world_points = []
        for px, py in local_points:
            rx = cx + px * math.cos(seg_angle) - py * math.sin(seg_angle)
            ry = cy + px * math.sin(seg_angle) + py * math.cos(seg_angle)
            world_points.append((rx, ry))
        return world_points
    def draw(self,C ):
        pygame.draw.polygon(screen, (layers[C]["color"]), self.world_points_1)
        pygame.draw.polygon(screen, (layers[C]["color"]), self.world_points_2)
        pygame.draw.polygon(screen, (layers[C]["color"]), self.world_points_3)


game_state = 'menu'

menu = {
    "p1": {"layer": list(layers.keys())[0], "movement_skill": list(movement_skills.keys())[0]},
    "p2": {"layer": list(layers.keys())[1], "movement_skill": list(movement_skills.keys())[1]},
}



def build_buttons():
    movement_skill_names = list(movement_skills.keys())
    buttons = {
        "p1_movement_skills": [], "p2_movement_skills": [],
        "start": pygame.Rect(275, 680, 200, 45),
        "p1_layer_prev": pygame.Rect(30, 220, 40, 40),
        "p1_layer_next": pygame.Rect(305, 220, 40, 40),
        "p2_layer_prev": pygame.Rect(390, 220, 40, 40),
        "p2_layer_next": pygame.Rect(680, 220, 40, 40),
    }

    for i, name in enumerate(movement_skill_names):
        buttons["p1_movement_skills"].append({"rect": pygame.Rect(15 + i * 120, 490, 110, 40), "value": name})
        buttons["p2_movement_skills"].append({"rect": pygame.Rect(390 + i * 120, 490, 110, 40), "value": name})

    return buttons

menu_buttons = build_buttons()
Circle1 = Circle2 = None
Wall1 = Wall2 = None


def cycle_layer(side, direction):
    names = list(layers.keys())
    idx = names.index(menu[side]["layer"])
    idx = (idx + direction) % len(names)
    menu[side]["layer"] = names[idx]

def draw_layer_design(layer_name, cx, cy, scale=1.0):
    for part in layers[layer_name]["parts"]:
        shifted = []
        for x, y in part["points"]:
            shifted.append((x * scale + cx, y * scale + cy))
        pygame.draw.polygon(screen, part["color"], shifted)
        pygame.draw.polygon(screen, (255, 255, 255), shifted, width=1)

LAYER_PREVIEW_POS = {
    "p1": (375/2, 240),
    "p2": (375*6/4, 240),
}

RESET_BUTTON_RECT = pygame.Rect(345, 345, 60, 60)

p1_skill_btn = pygame.Rect(640, 640, 100, 100)
p2_skill_btn = pygame.Rect(10, 10, 100, 100)

p1_wall_btn = pygame.Rect(10, 645, 100, 100)
p2_wall_btn = pygame.Rect(645, 10, 100, 100)

def draw_menu():
    screen.fill((15, 15, 25))
    pygame.draw.line(screen, (80, 80, 80), (375, 0), (375, 750), 2)

    p1_label = font.render("PLAYER 1", True, (200, 200, 255))
    p2_label = font.render("PLAYER 2", True, (255, 200, 200))
    screen.blit(p1_label, (13, 20))
    screen.blit(p2_label, (388, 20))

    for x in [15, 390]:
        screen.blit(font.render("MYTHOS:", True, (180, 180, 180)), (x, 70))
        screen.blit(font.render("SKILL", True, (180, 180, 180)), (x, 460))


    # Layer arrow selector + design preview
    for side, x_off in [("p1", 15), ("p2", 390)]:
        ly = menu[side]["layer"]


        prev_btn = menu_buttons[f"{side}_layer_prev"]
        next_btn = menu_buttons[f"{side}_layer_next"]

        pygame.draw.rect(screen, (60, 60, 70), prev_btn, border_radius=6)
        pygame.draw.rect(screen, (200, 200, 200), prev_btn, 1, border_radius=6)
        screen.blit(font.render("<", True, (255, 255, 255)), (prev_btn.x + 14, prev_btn.y + 8))

        pygame.draw.rect(screen, (60, 60, 70), next_btn, border_radius=6)
        pygame.draw.rect(screen, (200, 200, 200), next_btn, 1, border_radius=6)
        screen.blit(font.render(">", True, (255, 255, 255)), (next_btn.x + 14, next_btn.y + 8))

        # design preview, hardcoded position
        preview_x, preview_y = LAYER_PREVIEW_POS[side]
        draw_layer_design(ly, preview_x, preview_y, scale=2)

        name_label = font.render(ly, True, (220, 220, 220))
        screen.blit(name_label, (x_off, 100))

    # Movement_skill buttons
    for side, key in [("p1", "p1_movement_skills"), ("p2", "p2_movement_skills")]:
        for btn in menu_buttons[key]:
            selected = menu[side]["movement_skill"] == btn["value"]
            color = (120, 0, 180) if selected else (50, 50, 60)
            pygame.draw.rect(screen, color, btn["rect"], border_radius=6)
            pygame.draw.rect(screen, (200, 200, 200), btn["rect"], 1, border_radius=6)
            label = font.render(btn["value"][:9], True, (255, 255, 255))
            screen.blit(label, (btn["rect"].x + 4, btn["rect"].y + 10))

    # Description previews
    for side, x_off in [("p1", 15), ("p2", 390)]:
        ly = menu[side]["layer"]
        ul = menu[side]["movement_skill"]
        col = layers[ly]["color"]

        pygame.draw.circle(screen, col, (x_off - 30 + 50, 570), 22)
        pygame.draw.circle(screen, (255, 255, 255), (x_off - 30 + 50, 570), 22, 2)

        y = 360
        for line in layers[ly].get("desc", ["No description"]):
            t = font.render(line, True, (210, 210, 210))
            screen.blit(t, (x_off , y))
            y += 22

        movement_skill_y = 560
        screen.blit(font.render("movement_skill:", True, (200, 100, 255)), (x_off - 30 + 85, movement_skill_y))
        movement_skill_y += 22
        for line in movement_skills[ul].get("desc", ["No description"]):
            t = font.render(line, True, (190, 150, 255))
            screen.blit(t, (x_off - 30 + 85, movement_skill_y))
            movement_skill_y += 22

    pygame.draw.rect(screen, (0, 180, 80), menu_buttons["start"], border_radius=8)
    start_text = font.render("START", True, (0, 0, 0))
    screen.blit(start_text, (menu_buttons["start"].x + 60, menu_buttons["start"].y + 12))


def handle_menu_click(pos):
    global menu, Circle1, Circle2, Wall1, Wall2, game_state

    if menu_buttons["p1_layer_prev"].collidepoint(pos):
        cycle_layer("p1", -1)
    if menu_buttons["p1_layer_next"].collidepoint(pos):
        cycle_layer("p1", 1)
    if menu_buttons["p2_layer_prev"].collidepoint(pos):
        cycle_layer("p2", -1)
    if menu_buttons["p2_layer_next"].collidepoint(pos):
        cycle_layer("p2", 1)

    for btn in menu_buttons["p1_movement_skills"]:
        if btn["rect"].collidepoint(pos):
            menu["p1"]["movement_skill"] = btn["value"]

    for btn in menu_buttons["p2_movement_skills"]:
        if btn["rect"].collidepoint(pos):
            menu["p2"]["movement_skill"] = btn["value"]
    if menu_buttons["start"].collidepoint(pos):
        global Circle1, Circle2, Wall1, Wall2, game_state

        p1_layer = menu["p1"]["layer"]
        p2_layer = menu["p2"]["layer"]
        if menu_buttons["start"].collidepoint(pos):
            # Build the circles from whatever was selected
            Circle1 = Circle(pos=1, last_distance=None, calc_distance=0,
                             inertia=10, count=0, duration=1, startx=375, starty=500,
                             domain=False, grip=0, inertia_strength=3,
                             base_vel=pygame.Vector2(5, -10),
                             hit_vel=pygame.Vector2(0, 0), vel=pygame.Vector2(0, 0),
                             angle=0, layers=menu["p1"]["layer"],
                             stamina=0.1, lose=False, hit_cooldown=0,
                             movement_skill=menu["p1"]["movement_skill"])

            Circle2 = Circle(pos=1, last_distance=None, calc_distance=0,
                             inertia=10, count=0, duration=1, startx=375, starty=250,
                             domain=False, grip=0, inertia_strength=0.5,
                             base_vel=pygame.Vector2(-5, 10),
                             hit_vel=pygame.Vector2(0, 0), vel=pygame.Vector2(0, 0),
                             angle=0, layers=menu["p2"]["layer"],
                             stamina=0.1, lose=False, hit_cooldown=0,
                             movement_skill=menu["p2"]["movement_skill"])
            # length, breadth,  circle , angle,
            Wall1 = Wall(length=75, breadth=110, circle=Circle1, angle=0, spread=15)
            Wall2 = Wall(length=75, breadth=110, circle=Circle2, angle=135, spread=15)

        game_state = 'playing'

async def main():
    global game_state, Circle1, Circle2, Wall1, Wall2
    global dir_key1, dir_key2
    global timestop
    global p1_skill, p2_skill

    running = True

    while running:

        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if game_state == 'menu':
                if event.type == pygame.MOUSEBUTTONDOWN:
                    handle_menu_click(event.pos)
            elif game_state == "playing":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if RESET_BUTTON_RECT.collidepoint(event.pos):
                        game_state = 'menu'
                        Circle1 = Circle2 = None
                        Wall1 = Wall2 = None

                    if p1_skill_btn.collidepoint(event.pos):
                        p1_skill = True
                    else:
                        p1_skill = False

                    if p2_skill_btn.collidepoint(event.pos):
                        p2_skill = True
                    else:
                        p2_skill = False

                    if p1_wall_btn.collidepoint(event.pos):
                        dir_key1 = not dir_key1
                    if p2_wall_btn.collidepoint(event.pos):
                        dir_key2 = not dir_key2


                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        p1_skill = True
                    if event.key == pygame.K_p:
                        p2_skill = True
                    if event.key == pygame.K_a:
                        dir_key1 = not dir_key1
                    if event.key == pygame.K_l:
                        dir_key2 = not dir_key2

        if p1_skill and Circle1.movement_skill_cd == 0:
            Circle1.in_movement_skill = movement_skills[Circle1.movement_skill]["duration"]
            Circle1.movement_skill_cd = movement_skills[Circle1.movement_skill]["cooldown"]
            if Circle1.movement_skill in ("guard", "accel"):
                Circle1.base_vel *= movement_skills[Circle1.movement_skill]["vel_boost"]
            elif Circle1.movement_skill == "anchor":
                Circle1.base_vel *= movement_skills[Circle1.movement_skill]["vel_boost"] * 2
                Circle1.hit_vel *= movement_skills[Circle1.movement_skill]["vel_boost"]
        p1_skill = False

        if p2_skill and Circle2.movement_skill_cd == 0:
            Circle2.in_movement_skill = movement_skills[Circle2.movement_skill]["duration"]
            Circle2.movement_skill_cd = movement_skills[Circle2.movement_skill]["cooldown"]
            if Circle2.movement_skill == "guard":
                Circle2.base_vel *= movement_skills[Circle2.movement_skill]["vel_boost"]
            elif Circle2.movement_skill == "accel":
                Circle2.base_vel *= movement_skills[Circle2.movement_skill]["vel_boost"]
                Circle2.inertia += 12
            elif Circle2.movement_skill == "anchor":
                Circle2.base_vel *= movement_skills[Circle2.movement_skill]["vel_boost"]
                Circle2.hit_vel *= movement_skills[Circle2.movement_skill]["vel_boost"]
        p2_skill = False
        # menu on
        if game_state == 'menu':
            draw_menu()

        elif game_state == 'playing':

            screen.fill((0, 0, 0))
            pygame.draw.circle(screen, (255, 255, 255), center, 350, 7)
            pygame.draw.circle(screen, (255, 0, 0), center, 120, 3)
            #pygame.draw.circle(screen, (220, 220, 220), center, 240, 3)

            #pygame.draw.rect(screen, (180, 180, 180),(374,150,2,450) , border_radius=40)
            #pygame.draw.rect(screen, (180, 180, 180), (150, 374, 450, 2), border_radius=40)
            pygame.draw.rect(screen, (140, 140, 140), p1_wall_btn, border_radius=50)
            pygame.draw.rect(screen, (140, 140, 140), p2_wall_btn, border_radius=50)
            pygame.draw.rect(screen, (layers[Circle1.layers]["color"]), p1_skill_btn, border_radius=50)
            pygame.draw.rect(screen, (layers[Circle2.layers]["color"]), p2_skill_btn, border_radius=50)
            pygame.draw.rect(screen, (250, 40, 40), RESET_BUTTON_RECT, border_radius=60)

            #reset_btn_text = font.render("RESET", True, (255, 255, 255))
            #screen.blit(reset_btn_text, (RESET_BUTTON_RECT.x + 8, RESET_BUTTON_RECT.y + 8))

            if dir_key1 == True:
                direction_wall1 = 1
            else:
                direction_wall1 = -1

            if dir_key2 == True:
                direction_wall2 = 1
            else:
                direction_wall2 = -1


            if timestop > 0:
                timestop -= 1

            else:
                if not Circle1.lose:
                    Circle1.inspin(center)
                    Wall1.update(direction_wall1)

                if not Circle2.lose:
                    Circle2.inspin(center)
                    Wall2.update(direction_wall2)

                if not Circle1.lose and not Circle2.lose:
                    wall_hit_circle(Wall1, Circle2)
                    wall_hit_circle(Wall2, Circle1)
                    wall_hit_circle(Wall1, Circle1)
                    wall_hit_circle(Wall2, Circle2)

                    if Circle1.hit(Circle2):
                        pass
                    else:
                        Circle2.hit(Circle1)

            # =========================
            # DRAWING
            # =========================

            if not Circle1.lose:
                Circle1.draw_trail()
                Circle1.update_parts()
                Circle1.draw(0, 0, 0)
                Circle1.draw_parts()

                if Circle1.in_movement_skill > 0:
                    Circle1.draw_movement_skill_trail()

            if not Circle2.lose:
                Circle2.draw_trail()
                Circle2.update_parts()
                Circle2.draw(0, 0, 0)
                Circle2.draw_parts()

                if Circle2.in_movement_skill > 0:
                    Circle2.draw_movement_skill_trail()

            Wall1.draw(Circle1.layers)
            Wall2.draw(Circle2.layers)

            # win condition check
            if Circle1.lose or Circle1.stamina <= 0:
                text = font.render(f' {Circle2.layers} wins', True, (255, 255, 0))
                screen.blit(text, (280, 375))

            if Circle2.lose or Circle2.stamina <= 0:
                text = font.render(f'{Circle1.layers} wins', True, (255, 255, 0))
                screen.blit(text, (280, 375))

            # if collided == True:
            #    text = font.render('test collided', True, (255, 0, 0))
            #    screen.blit(text, (300, 200))
            c1_hp = (Circle1.stamina - 0.03) * 100 - 1
            if c1_hp <= 0:
                c1_hp = 0
            c2_hp = (Circle2.stamina - 0.03) * 100 - 1
            if c2_hp <= 0:
                c2_hp = 0



            c1_hp = max(0.0, min(Circle1.stamina / 0.1, 1.0))  # clamp

            start_angle = math.pi / 2
            c1_hp = start_angle + c1_hp * 2 * math.pi

            if c1_hp > start_angle:  # avoid a zero-length arc call
                pygame.draw.arc(screen, "green", [630, 630, 120, 120], start_angle, c1_hp, 10)

            c2_hp = max(0.0, min(Circle2.stamina / 0.1, 1.0))  # clamp


            c2_hp = start_angle + c2_hp * 2 * math.pi

            if c2_hp > start_angle:  # avoid a zero-length arc call
                pygame.draw.arc(screen, "green", [0, 0, 120, 120], start_angle, c2_hp, 10)


        pygame.display.flip()
        await asyncio.sleep(0)

asyncio.run(main())

