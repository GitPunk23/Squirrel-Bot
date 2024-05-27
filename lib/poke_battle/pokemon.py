import math
import requests
import random

class Pokemon:
    
    level = 50
    stats = []
    current_hp = 100
    status_condition = "HEALTHY"
    
    def __init__(self, pokemon_identifier):
        if isinstance(pokemon_identifier, int):
            pokemon_data = self.fetch_pokemon_by_number(pokemon_identifier)
        elif isinstance(pokemon_identifier, str):
            pokemon_data = self.fetch_pokemon_by_name(pokemon_identifier)
        else:
            raise ValueError("pokemon_identifier must be either an integer (number) or a string (name)")
        
        self.species = pokemon_data['species']['name']
        self.type_one = pokemon_data['types'][0]['type']['name']
        if len(pokemon_data['types']) > 1:
            self.type_two = pokemon_data['types'][1]['type']['name']
        else:
            self.type_two = None
            
        self.ability = self.extract_ability(pokemon_data['abilities'])
        self.base_stats = self.extract_stats(pokemon_data)     
        self.level = Pokemon.level
        
        self.moves = self.process_moves(pokemon_data['moves'], self.level)
        
        self.spriteURL = self.get_sprite_url(pokemon_data['sprites'])
        
        self.stats = self.calculate_stats()
        self.current_hp = self.stats['hp']
        self.status_condition = Pokemon.status_condition
                      
# --------------FETCH--------------------------------------------------------------------------------------------------------       
    def fetch_pokemon_by_number(self, pokemon_number):
        url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_number}"
        response = requests.get(url)
        if response.status_code == 200:
            pokemon_data = response.json()
            return pokemon_data
        else:
            print(f"Failed to fetch Pokémon with number {pokemon_number}. Status code: {response.status_code}")
            return None

    def fetch_pokemon_by_name(self, pokemon_name):
        url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"
        response = requests.get(url)
        if response.status_code == 200:
            pokemon_data = response.json()
            return pokemon_data
        else:
            print(f"Failed to fetch Pokémon with name {pokemon_name}. Status code: {response.status_code}")
            return None

# --------------STATS--------------------------------------------------------------------------------------------------------       
    def extract_stats(self, response):
        stats = {}
        for stat_data in response['stats']:
            stat_name = stat_data['stat']['name']
            base_stat = stat_data['base_stat']
            stats[stat_name] = base_stat
        return stats
        
    def calculate_stats(self):
        stats = {
        'hp': self.calculate_hp_stat(self.base_stats['hp']),
        'attack': self.calculate_stat(self.base_stats['attack']),
        'defense': self.calculate_stat(self.base_stats['defense']),
        'special-attack': self.calculate_stat(self.base_stats['special-attack']),
        'special-defense': self.calculate_stat(self.base_stats['special-defense']),
        'speed': self.calculate_stat(self.base_stats['speed'])
        }
        return stats
   
    def calculate_hp_stat(self, base_hp):
        # based on math.floor(0.01 * (2 * base_hp + IV + math.floor(0.25 * EV)) * self.level) + self.level + 10
        hp_stat =  math.floor(0.01 * (2 * base_hp) * self.level) + self.level + 10
        return hp_stat
    
    def calculate_stat(self, base_stat):
        # based on (math.floor(0.01 * (2 * base_stat + IV + math.floor(0.25 x EV)) * self.level) + 5) * nature
        stat = (math.floor(0.01 * (2 * base_stat) * self.level) + 5)
        return stat
    
# --------------ABILITY------------------------------------------------------------------------------------------------------
    def extract_ability(self, abilities):
        hidden_abilities = [ability for ability in abilities if ability['is_hidden']]
        non_hidden_abilities = [ability for ability in abilities if not ability['is_hidden']]

        # Determine the probability of selecting a hidden ability
        hidden_ability_chance = 0.1  

        if hidden_abilities:
            return random.choice(hidden_abilities)['ability']['name']
        elif random.random() < hidden_ability_chance and non_hidden_abilities:
            return random.choice(non_hidden_abilities)['ability']['name']

#---------------MOVES--------------------------------------------------------------------------------------------------------
    def process_moves(self, moves_data, pokemon_level):
        move_list = []
        moves = self.extract_moves(moves_data, pokemon_level)
        
        for move in moves:
            move_data = self.fetch_move_info(move['url'])
            
            move_list.append({
                'name': move_data.get('name'),  
                'accuracy': move_data.get('accuracy'),  
                'damage_class': move_data.get('damage_class', {}).get('name', 'Unknown'),  
                'effect_chance': move_data.get('effect_chance'),  
                'ailment': move_data.get('meta', {}).get('ailment', {}).get('name', 'None'), 
                'ailment_chance': move_data.get('ailment_chance'), 
                'crit_rate': move_data.get('crit_rate'), 
                'drain': move_data.get('drain'), 
                'flinch_chance': move_data.get('flinch_chance'), 
                'healing': move_data.get('healing'), 
                'max_hits': move_data.get('max_hits'), 
                'max_turns': move_data.get('max_turns'), 
                'min_hits': move_data.get('min_hits'),
                'min_turns': move_data.get('min_turns'), 
                'stat_chance': move_data.get('stat_chance'),  
                'power': move_data.get('power'),  
                'pp': move_data.get('pp'),  
                'current_pp': move_data.get('pp'), 
                'priority': move_data.get('priority'),
                'stat_changes': move_data.get('stat_changes'),  
                'target': move_data.get('target', {}).get('name', 'Unknown'), 
                'type': move_data.get('type', {}).get('name', 'Unknown Type')  
            })
        print(move_list)
        return move_list
            
    def extract_moves(self, moves_data, pokemon_level):
        available_moves = []
        for move_info in moves_data:
            level_learned_at = move_info['version_group_details'][0]['level_learned_at']
            if level_learned_at <= pokemon_level:
                available_moves.append(move_info['move'])
        random_moves = random.sample(available_moves, min(4, len(available_moves)))
        return random_moves
    
    def fetch_move_info(self, move_url):
        response = requests.get(move_url)
        if response.status_code == 200:
            move_data = response.json()
            return move_data
        else:
            print(f"Failed to fetch move information. Status code: {response.status_code}")
            return None
        
# --------------SPRITE-------------------------------------------------------------------------------------------------------
    def get_sprite_url(self, sprite_data):
        if random.randint(0, 9) < 1:  # 10% chance for shiny front
            sprite_url = sprite_data.get('front_shiny')
        else:
            sprite_url = sprite_data.get('front_default')

        return sprite_url

# --------------BATTLE------------------------------------------------------------------------------------------------------- 
    def attack(self, opponent):
        pass

    def take_damage(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0

    def is_alive(self):
        return self.health > 0

    def level_up(self):
        self.level += 1

    def heal(self):
        self.health = 100

    def __str__(self):
        species_info = f"Species: {self.species}"
        types_info = f"Type: {self.type_one}"
        if self.type_two:
            types_info += f", {self.type_two}"
        ability_info = f"Ability: {self.ability}"
        base_stats_info = "\n".join([f"{stat_name.capitalize()}: {stat_value}" for stat_name, stat_value in self.base_stats.items()])
        moves_info = f"Moves: {', '.join(self.moves)}"
        sprite_info = f"Sprite URL: {self.spriteURL}"
        level_info = f"Level: {self.level}"
        current_hp_info = f"Current HP: {self.current_hp}"
        status_condition_info = f"Status Condition: {self.status_condition}"

        pokemon_info = "\n".join([species_info, types_info, ability_info, base_stats_info, moves_info, sprite_info, level_info, current_hp_info, status_condition_info])
        return pokemon_info

