import os
import json
import requests
from flask import Flask, jsonify
from recipe_scrapers import scrape_me
from bs4 import BeautifulSoup

app = Flask(__name__)

# Fonction pour obtenir les liens de recettes via la recherche sur Marmiton en fonction d'un mot-clé
def search_recipes_by_keyword(keyword):
    search_url = f"https://www.marmiton.org/recettes/recherche.aspx?aqt={keyword}"
    try:
        response = requests.get(search_url)
        response.raise_for_status()  # Vérifie si la requête a réussi (code 200)
        soup = BeautifulSoup(response.text, 'html.parser')
    except requests.RequestException as e:
        print(f"Erreur lors de la récupération des résultats pour le mot-clé {keyword}: {e}")
        return []

    recipe_links = []
    # Recherche des liens des recettes sur la page de résultats
    for link in soup.find_all('a', {'class': 'recipe-card-link'}):
        recipe_url = link.get('href')
        if recipe_url:
            # Si l'URL est relative, la rendre complète
            if recipe_url.startswith('/'):
                recipe_links.append('https://www.marmiton.org' + recipe_url)
            else:
                recipe_links.append(recipe_url)  # Si l'URL est déjà complète

    return recipe_links

def get_recipe_data(recipe_url):
    try:
        scraper = scrape_me(recipe_url)
        # Utilisation de scraper.to_json() pour récupérer toutes les données sous forme de dictionnaire
        recipe_data = scraper.to_json()  # Cela récupère toutes les données de la recette dans un format JSON
        return recipe_data
    except Exception as e:
        print(f"Erreur lors du scraping de la recette {recipe_url}: {e}")
        return None

# Fonction pour sauvegarder toutes les recettes dans un fichier JSON
def save_recipes_to_json(categories_dict, output_filename):
    all_recipes = []

    for category, keywords in categories_dict.items():
        for keyword in keywords:
            print(f"Scraping recipes for category: {category}, keyword: {keyword}")
            recipe_links = search_recipes_by_keyword(keyword)
            
            for link in recipe_links:
                print(f"Scraping recipe: {link}")
                recipe_data = get_recipe_data(link)
                if recipe_data:  # Vérification que la recette a bien été récupérée
                    all_recipes.append(recipe_data)

    # Fonction pour sauvegarder toutes les recettes dans un fichier JSON
def save_recipes_to_json(categories_dict, output_filename):
    all_recipes = []
    scraped_recipes_count = 0  # Compteur de recettes scrappées

    for category, keywords in categories_dict.items():
        for keyword in keywords:
            print(f"Scraping recipes for category: {category}, keyword: {keyword}")
            recipe_links = search_recipes_by_keyword(keyword)
            
            for link in recipe_links:
                print(f"Scraping recipe: {link}")
                recipe_data = get_recipe_data(link)
                if recipe_data:  # Vérification que la recette a bien été récupérée
                    all_recipes.append(recipe_data)
                    scraped_recipes_count += 1  # Incrémenter le compteur de recettes

    # Sauvegarde des données dans un fichier JSON
    pwd = os.getcwd() 
    output_path = os.path.join(pwd + '/src/data_loading', output_filename)  # Change le chemin si nécessaire
    try:
        with open(output_path, 'w', encoding='utf-8') as json_file:
            json.dump(all_recipes, json_file, ensure_ascii=False, indent=4)
        print(f"Les recettes ont été sauvegardées dans {output_path}")
    except IOError as e:
        print(f"Erreur lors de la sauvegarde du fichier JSON: {e}")

    # Afficher le nombre de recettes scrappées
    print(f"Nombre total de recettes scrappées: {scraped_recipes_count}")


# Route Flask pour démarrer le scraping et sauvegarder dans un fichier JSON
@app.route('/scrape_recipes', methods=['GET'])
def scrape_recipes():
    # Dictionnaire des catégories et mots-clés pour le scraping
    culinary_dict = {
        "Entrées": [
            "Salade", "Soupe", "Quiche", "Bruschetta", "Tapenade", "Velouté", "Carpaccio", "Terrine",
            "Gazpacho", "Tartare", "Omelette", "Houmous", "Caviar d’aubergine", "Samossa", "Accras",
            "Rillettes", "Blinis", "Mousse salée", "Gougères", "Tzatziki"
        ],
        "Plats principaux": [
            "Poulet rôti", "Bœuf bourguignon", "Lasagnes", "Couscous", "Paella", "Ratatouille", "Blanquette de veau",
            "Coq au vin", "Steak frites", "Curry de légumes", "Tajine", "Risotto", "Chili con carne", "Quiche lorraine",
            "Tartiflette", "Hachis parmentier", "Boulettes de viande", "Rôti de porc", "Gratin dauphinois", "Filet de saumon"
        ],
        
    }

    # Sauvegarder les recettes dans un fichier JSON
    save_recipes_to_json(culinary_dict, "all_recipes.json")

    return jsonify({"message": "Toutes les recettes ont été sauvegardées avec succès dans le fichier JSON."})

if __name__ == '__main__':
    app.run(debug=True)


#http://127.0.0.1:5000/scrape_recipes

