import random

from game import base
from game import collision
from game import img
from game import phys
from game import planet
from game import player
from game import ship
from plib import vec2d


def create_system(ecsm, data):
    ecsm.crew_to_rescue = data['crew_to_rescue']
    for member in data['members']:
        type = member['type']
        if type == 'sun' or type == 'planet':

            member_id = ecsm.create_entity(
                [phys.PhysicsEcsComponent(member['x'], member['y'], member['mass'], member['static']),
                 phys.GravityEcsComponent(member['grav_radius']),
                 collision.CollisionEcsComponent(member['size']),
                 planet.PlanetEcsComponent(member['name']),
                 planet.RenderPlanetEcsComponent(member.get('img', ''))])

            satellites = member['satellites']
            for satellite in satellites:
                if satellite['type'] == 'planet':
                    satellite_id = ecsm.create_entity([phys.PhysicsEcsComponent(0.0, 0.0, satellite['mass'], False),
                                                       phys.GravityEcsComponent(satellite['grav_radius']),
                                                       collision.CollisionEcsComponent(satellite['size']),
                                                       planet.PlanetEcsComponent(''),
                                                       planet.RenderPlanetEcsComponent(satellite.get('img', ''))])
                if satellite['type'] == 'base':
                    satellite_id = ecsm.create_entity([phys.PhysicsEcsComponent(0, 0, satellite['mass'], False),
                                                       collision.CollisionEcsComponent(satellite['size']),
                                                       base.BaseEcsComponent(
                                                           radius=satellite['service_radius'],
                                                           fuel_load=satellite['fuel'],
                                                           crew_load=satellite['crew'],
                                                           repairs=satellite['repair'],
                                                           impact_resistance=satellite['impact_resistence'],
                                                           health=satellite['health']),
                                                       base.RenderBaseEcsComponent(satellite.get('img', ''))])

                if satellite['type'] == 'ship':
                    satellite_id = ecsm.create_entity([phys.PhysicsEcsComponent(0, 0, satellite['mass'], False),
                                                       collision.CollisionEcsComponent(satellite['size']),
                                                       player.PlayerIdentityEcsComponent(),
                                                       ship.ShipEcsComponent(
                                                           rotation=satellite['rotation'],
                                                           rotation_speed=satellite['rotation_speed'],
                                                           thrust_force=satellite['thrust_force'],
                                                           impact_resistance=satellite['impact_resistance'],
                                                           fuel=satellite['fuel'],
                                                           passengers=satellite['passengers'],
                                                           health=satellite['health']),
                                                       ship.RenderShipEcsComponent()])

                # put the satelite in orbit
                ecsm.get_system(phys.PhysicsEcsSystem.name()).set_orbit(satellite_id,
                                                                        member_id,
                                                                        satellite['orbit_distance'],
                                                                        satellite['orbit_angle'],
                                                                        satellite['orbit_clockwise'])


def generate_system_data():
    # create some working data
    member_names = ['Tamde', 'Yol', 'Trog', 'Mar', 'Een', 'Sila', 'Ado', 'Khem', 'Teim', 'Tamut', 'Beda', 'Ponni']
    member_position_angles = [i for i in range(0, 360, 40)]
    mass_mod = 10000
    member_padding = 1000
    member_grav_radius = member_padding // 2
    satellite_grav_radius = member_grav_radius // 2
    satellite_orbit_distance = member_grav_radius // 2
    satellite_position_angles = [i for i in range(0, 360, 90)]
    planet_imgs = [img.IMG_P_64_1, img.IMG_P_64_2]
    moon_imgs = [img.IMG_M_48_1, ]

    members = []

    # player ship
    player_ship_data = {'type': 'ship',
                        'size': 14,
                        'mass': 100,
                        'rotation': 90.0,
                        'rotation_speed': 6.0,
                        'thrust_force': 200.0,
                        'impact_resistance': 50.0,
                        'fuel': 700,
                        'passengers': 0,
                        'health': 350,
                        'orbit_distance': member_grav_radius * .75,
                        'orbit_angle': 0,
                        'orbit_clockwise': False
                        }

    # sun
    members.append({'x': 0, 'y': 0,
                    'type': 'sun',
                    'img': 'sun.png',
                    'name': 'Sol',
                    'static': True,
                    'size': 128,
                    'mass': 128 * mass_mod,
                    'grav_radius': member_grav_radius,
                    'satellites': [player_ship_data, ]
                    })

    crew_to_rescue = 0

    # planets
    distance = 0
    num_planets = range(0, 7)  # 7
    for _ in num_planets:
        distance += member_padding

        planet_name = random.choice(member_names)
        member_names.remove(planet_name)

        # generate position
        pos = vec2d.vec2d(0, distance)
        angle = random.choice(member_position_angles)
        pos.rotate(angle)

        # member satellites
        satellites = []
        num_satellites = range(0, 2)
        satellite_angle_options = satellite_position_angles[:]
        for _ in num_satellites:
            satelite_angle = random.choice(satellite_angle_options)
            satellite_angle_options.remove(satelite_angle)

            satellites.append({'type': 'planet',
                               'name': 'Satellite',
                               'img': random.choice(moon_imgs),
                               'size': 24,
                               'mass': 24 * mass_mod,
                               'grav_radius': satellite_grav_radius,
                               'orbit_distance': satellite_orbit_distance,
                               'orbit_angle': satelite_angle,
                               'orbit_clockwise': True
                               })
        # add one base satellite
        satelite_angle = random.choice(satellite_angle_options)
        satellite_angle_options.remove(satelite_angle)
        crew = 30
        crew_to_rescue += 30
        satellites.append({'type': 'base',
                           'name': 'Satellite',
                           'img': img.IMG_BASE,
                           'size': 14,
                           'mass': 300,
                           'service_radius': 65,
                           'fuel': True,
                           'repair': True,
                           'crew': crew,
                           'impact_resistence': 70,
                           'health': 800,
                           'orbit_distance': satellite_orbit_distance,
                           'orbit_angle': satelite_angle,
                           'orbit_clockwise': True
                           })
        members.append({'x': pos.x, 'y': pos.y,
                        'type': 'planet',
                        'img': random.choice(planet_imgs),
                        'name': planet_name,
                        'static': True,
                        'size': 64,
                        'mass': 64 * mass_mod,
                        'grav_radius': member_grav_radius,
                        'satellites': satellites
                        })

    data = {
        'members': members,
        'crew_to_rescue': crew_to_rescue,
    }

    return data


# for planet_gen_id in range(random.randint(PLANETS_MIN, PLANETS_MIN + 1)):

def generate_system(ecsm):
    data = generate_system_data()
    create_system(ecsm, data)
