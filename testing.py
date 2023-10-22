import pandas as pd


# Load the data
pokemon_data = pd.read_csv("pokemon.csv")
pokemon_names = pokemon_data['NAME'].tolist()

#create n empty Dataframe for the damage matrix
damage_matrix = pd.DataFrame(columns=pokemon_names, index=pokemon_names)

# Iterate over each Pokémon and calculate the damage against every other Pokémon
total_pokemon = len(pokemon_names)
for idx, attacker in enumerate(pokemon_data.iterrows()):
    for defender in pokemon_data.iterrows():
        damage = (attacker[1]['ATK'] - defender[1]['DEF']) * 0.8 + (
                    attacker[1]['SP_ATK'] - defender[1]['SP_DEF']) * 0.2
        damage = max(0, damage)  # Set negative values to 0
        damage_matrix.at[attacker[1]['NAME'], defender[1]['NAME']] = damage if damage > 0 else 'No Damage'

    # Display progress
    progress = (idx + 1) / total_pokemon * 100
    print(f"Progress: {progress:.2f}%")

# Save to CSV
damage_matrix.to_csv('damage_matrix_full.csv')

print("Calculation complete and saved to 'damage_matrix_full.csv'")