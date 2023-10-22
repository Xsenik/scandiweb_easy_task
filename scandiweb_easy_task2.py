import pandas as pd

# Load the data and extract Names
pokemon_data = pd.read_csv("pokemon.csv")
pokemon_names = pokemon_data['NAME'].tolist()

# Create an empty DataFrame for the damage matrix
damage_matrix = pd.DataFrame(columns=pokemon_names, index=pokemon_names)

# Iterate over each Pokémon and calculate the damage against every other Pokémon
total_pokemon = len(pokemon_names)
for idx, attacker in enumerate(pokemon_data.iterrows()):
    for defender in pokemon_data.iterrows():
        damage = (attacker[1]['ATK'] - defender[1]['DEF']) * 0.8 + (
                    attacker[1]['SP_ATK'] - defender[1]['SP_DEF']) * 0.2
        damage = max(0, damage)  # if damage less than defence
        damage_matrix.at[attacker[1]['NAME'], defender[1]['NAME']] = damage

    # Display progress
    progress = (idx + 1) / total_pokemon * 100
    print(f"Progress: {progress:.2f}%")

# Add a new column for the total damage dealt by each Pokémon
damage_matrix['Total_Damage_Dealt'] = damage_matrix.sum(axis=1)

#identify the pokemon that dealth the most damage
top_damager = damage_matrix["Total_Damage_Dealt"].idxmax()
top_damage_value = damage_matrix['Total_Damage_Dealt'].max()
print(f"{top_damager} dealt the most total damage, with a value of {top_damage_value}.")
# Save to CSV
damage_matrix.to_csv('pokemon_battle_damage.csv')

print("Calculation complete and saved to 'pokemon_battle_damage.csv'")
