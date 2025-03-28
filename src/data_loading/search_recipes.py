def create_culinary_dictionary():
    """
    Creates a dictionary containing various culinary categories and their associated lists of items,
    based on the categories defined in the search_recipes.py file.

    Returns:
        dict: A dictionary where keys are culinary categories (in French) and values are lists of items
              within those categories.
    """

    culinary_dictionary = {
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
        "Desserts": [
            "Gâteau au chocolat", "Tarte aux pommes", "Mousse au chocolat", "Crème brûlée", "Panna cotta", "Tiramisu",
            "Clafoutis", "Cheesecake", "Île flottante", "Crêpes", "Beignets", "Macarons", "Brownie", "Éclair au chocolat",
            "Charlotte aux fraises", "Flan pâtissier", "Millefeuille", "Galette des rois", "Baba au rhum", "Fondant au chocolat"
        ],
        "Accompagnements": [
            "Purée de pommes de terre", "Riz pilaf", "Frites", "Haricots verts", "Ratatouille", "Semoule",
            "Pommes dauphines", "Risotto", "Gratin de légumes", "Polenta", "Taboulé", "Salade verte",
            "Flan de courgettes", "Poêlée de champignons", "Tian de légumes", "Boulgour", "Épinards sautés",
            "Coleslaw", "Lentilles", "Pommes de terre sautées"
        ],
        "Ingrédients de base": [
            "Farine", "Sucre", "Sel", "Poivre", "Beurre", "Huile d'olive", "Lait", "Œufs", "Levure", "Crème fraîche",
            "Miel", "Vinaigre", "Tomates", "Oignons", "Ail", "Herbes de Provence", "Paprika", "Piment", "Moutarde", "Bouillon"
        ],
        "Boissons": [
            "Eau", "Café", "Thé", "Jus d’orange", "Jus de pomme", "Limonade", "Soda", "Vin rouge", "Vin blanc", "Bière",
            "Cocktail", "Smoothie", "Milkshake", "Chocolat chaud", "Infusion", "Cappuccino", "Mojito", "Spritz", "Sangria", "Cidre"
        ],
        "Épices et condiments": [
            "Curry", "Curcuma", "Cumin", "Cannelle", "Gingembre", "Piment d'Espelette", "Paprika", "Clous de girofle",
            "Noix de muscade", "Cardamome", "Anis étoilé", "Estragon", "Basilic", "Coriandre", "Thym", "Romarin",
            "Persil", "Origan", "Fenouil", "Laurier"
        ]
    }

    return culinary_dictionary

# Example usage:
culinary_dict = create_culinary_dictionary()
print(culinary_dict)
