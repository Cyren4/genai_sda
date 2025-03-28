def create_culinary_dictionary():
    """
    Creates a dictionary containing various culinary categories and their associated lists of items.

    Returns:
        dict: A dictionary where keys are culinary categories (e.g., "Entrees", "Main Courses")
              and values are lists of items within those categories.
    """

    culinary_dictionary = {
        "Entrees": [
            "Salad", "Soup", "Quiche", "Bruschetta", "Tapenade", "Velouté", "Carpaccio", "Terrine",
            "Gazpacho", "Tartare", "Omelette", "Hummus", "Eggplant Caviar", "Samosa", "Accras",
            "Rillettes", "Blinis", "Savory Mousse", "Gougères", "Tzatziki"
        ],
        "Main Courses": [
            "Roast Chicken", "Beef Bourguignon", "Lasagna", "Couscous", "Paella", "Ratatouille", "Veal Blanquette",
            "Coq au Vin", "Steak Frites", "Vegetable Curry", "Tajine", "Risotto", "Chili con Carne", "Quiche Lorraine",
            "Tartiflette", "Shepherd's Pie", "Meatballs", "Roast Pork", "Gratin Dauphinois", "Salmon Fillet"
        ],
        "Desserts": [
            "Chocolate Cake", "Apple Pie", "Chocolate Mousse", "Crème Brûlée", "Panna Cotta", "Tiramisu",
            "Clafoutis", "Cheesecake", "Floating Island", "Crepes", "Beignets", "Macarons", "Brownie", "Chocolate Éclair",
            "Strawberry Charlotte", "Custard Flan", "Millefeuille", "King Cake", "Rum Baba", "Chocolate Fondant"
        ],
        "Side Dishes": [
            "Mashed Potatoes", "Pilaf Rice", "French Fries", "Green Beans", "Ratatouille", "Semolina",
            "Dauphine Potatoes", "Risotto", "Vegetable Gratin", "Polenta", "Tabouleh", "Green Salad",
            "Zucchini Flan", "Sautéed Mushrooms", "Vegetable Tian", "Bulgur", "Sautéed Spinach",
            "Coleslaw", "Lentils", "Sautéed Potatoes"
        ],
        "Basic Ingredients": [
            "Flour", "Sugar", "Salt", "Pepper", "Butter", "Olive Oil", "Milk", "Eggs", "Yeast", "Fresh Cream",
            "Honey", "Vinegar", "Tomatoes", "Onions", "Garlic", "Herbs de Provence", "Paprika", "Chili", "Mustard", "Broth"
        ],
        "Beverages": [
            "Water", "Coffee", "Tea", "Orange Juice", "Apple Juice", "Lemonade", "Soda", "Red Wine", "White Wine", "Beer",
            "Cocktail", "Smoothie", "Milkshake", "Hot Chocolate", "Infusion", "Cappuccino", "Mojito", "Spritz", "Sangria", "Cider"
        ],
        "Spices and Condiments": [
            "Curry", "Turmeric", "Cumin", "Cinnamon", "Ginger", "Espelette Pepper", "Paprika", "Cloves",
            "Nutmeg", "Cardamom", "Star Anise", "Tarragon", "Basil", "Coriander", "Thyme", "Rosemary",
            "Parsley", "Oregano", "Fennel", "Bay Leaf"
        ]
    }

    return culinary_dictionary

# Example usage:
culinary_dict = create_culinary_dictionary()
print(culinary_dict)
