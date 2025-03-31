import json
import sys
import time
import os 
from dotenv import load_dotenv
from langchain.text_splitter import TokenTextSplitter
import tiktoken 
import google.generativeai as genai
import chromadb
from chromadb.api.types import EmbeddingFunction, Documents, Embeddings 

# --- Configuration ---
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


try:
    genai.configure(api_key=GOOGLE_API_KEY)
    result = genai.embed_content(model='models/text-embedding-004',
                                 content=["test"],
                                 task_type="retrieval_document")
    print("Test API réussi:", result['embedding'])
except Exception as e:
    print("Erreur lors du test API simple:", e)

# --- Embedding function---
class GeminiEmbeddingFunction(EmbeddingFunction):
  def __call__(self, input: Documents) -> Embeddings:
    model = 'models/text-embedding-004' # Ou 'models/embedding-001' 
    if not isinstance(input, list):
        input = [str(input)]
    try:
        result = genai.embed_content(model=model,
                                     content=input,
                                     task_type="retrieval_document" # Ou "semantic_similarity" 
                                     )
        return result["embedding"]

    except Exception as e:
        print(f"Erreur lors de l'appel à genai.embed_content: {e}")
        raise e 


# --- Fonction de Formatage ---
def format_recipe_for_embedding(recipe):
    """Met en forme un dictionnaire de recette en une chaîne de texte."""
    parts = []
    if title := recipe.get("title"): parts.append(f"Titre: {title}")
    if cuisine := recipe.get("cuisine"): parts.append(f"Type de plat: {cuisine}")
    if description := recipe.get("description"): parts.append(f"Description rapide: {description}")
    if keywords := recipe.get("keywords"):
        if isinstance(keywords, list) and keywords: parts.append(f"Mots-clés: {', '.join(keywords)}")
    if ingredients := recipe.get("ingredients"):
         if isinstance(ingredients, list) and ingredients:
            parts.append("\nIngrédients:")
            for ingredient in ingredients: parts.append(f"- {ingredient}")
    parts.append("\nInstructions:")
    if instructions_list := recipe.get("instructions_list"):
         if isinstance(instructions_list, list) and instructions_list:
            for i, step in enumerate(instructions_list, 1): parts.append(f"{i}. {step}")
    elif instructions := recipe.get("instructions"):
         if isinstance(instructions, str) and instructions: parts.append(instructions)
    if yields := recipe.get("yields"): parts.append(f"\nPortions: {yields}")
    if prep_time := recipe.get("prep_time"): parts.append(f"Temps de préparation: {prep_time} min")
    if cook_time := recipe.get("cook_time"):
         if cook_time is not None: parts.append(f"Temps de cuisson: {cook_time} min")
    if total_time := recipe.get("total_time"): parts.append(f"Temps total: {total_time} min")
    if ratings := recipe.get("ratings"):
         count = recipe.get('ratings_count', '')
         count_str = f" ({count} avis)" if count else ""
         parts.append(f"Note: {ratings}/5{count_str}")
    # Ajouter l'URL canonique dans le texte peut aussi aider le contexte
    if url := recipe.get("canonical_url"):
        parts.append(f"\nSource: {url}")
    return "\n".join(parts)


# --- Création DB  ---
def create_chroma_db(documents: list[str], ids: list[str], metadatas: list[dict], name: str, dir: str):
    """
    Crée ou charge une collection ChromaDB persistante et y ajoute les documents.

    Args:
        documents: Liste des textes des chunks.
        ids: Liste des IDs uniques pour chaque chunk.
        metadatas: Liste des dictionnaires de métadonnées pour chaque chunk.
        name: Nom de la collection ChromaDB.
        dir: Répertoire de persistance pour ChromaDB.
    """
    print(f"\nConfiguration de ChromaDB dans le répertoire : {dir}")
    persist_directory = dir
    os.makedirs(persist_directory, exist_ok=True)

    chroma_client = chromadb.PersistentClient(path=persist_directory)

    print(f"Obtention ou création de la collection ChromaDB : '{name}'")
    try:
        embedding_function_instance = GeminiEmbeddingFunction()
        db_collection = chroma_client.get_or_create_collection(
            name=name,
            embedding_function=embedding_function_instance 
        )
    except Exception as e:
        print(f"Erreur lors de la création/obtention de la collection ChromaDB: {e}")
        sys.exit(1)


    # L'ajout en batch plus efficace, mais limites de taux de l'API d'embedding.
    print(f"Ajout de {len(documents)} chunks à la collection '{name}'...")
    added_count = 0
    error_count = 0
    for i in range(len(documents)):
        try:
            db_collection.add(
                 documents=[documents[i]],
                 ids=[ids[i]],
                 metadatas=[metadatas[i]]
             )
            added_count += 1
            print(f"  Ajouté chunk {i+1}/{len(documents)} (ID: {ids[i]})")
            time.sleep(0.5) # rate limit de l'API Gemini 

        except Exception as e:
            error_count += 1
            print(f"  ERREUR lors de l'ajout du chunk {i+1} (ID: {ids[i]}): {e}")
            time.sleep(1)

    print(f"\nAjout terminé.")
    print(f"  Chunks ajoutés avec succès : {added_count}")
    print(f"  Erreurs lors de l'ajout    : {error_count}")
    return db_collection 


if __name__ == "__main__":
    # --- Paramètres ---
    pwd = os.getcwd()
    file_path = f'{pwd}/data/all_recipes.json'  # Répertoire  data source 
    chroma_db_dir = f'{pwd}/data/chroma_db_recipes'  # Répertoire pour stocker la DB Chroma
    collection_name = "marmiton_recipes"   #Nom de la collection dans ChromaDB

    # Paramètres pour le TokenTextSplitter chunk_size doit être inférieur à la limite du modèle (2048 pour text-embedding-004)
    chunk_size = 2000 
    chunk_overlap = 200 # Chevauchement pour garder le contexte entre les chunks

    # --- Chargement des données ---
    loaded_data = None
    print(f"--- Étape 1: Chargement des recettes depuis '{file_path}' ---")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            loaded_data = json.load(f)
        print(f"Chargement réussi. Nombre de recettes : {len(loaded_data)}")
    except FileNotFoundError:
        print(f"ERREUR : Fichier '{file_path}' introuvable.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"ERREUR : JSON invalide dans '{file_path}'. Détails : {e}")
        sys.exit(1)
    except Exception as e:
        print(f"ERREUR inattendue lors du chargement : {e}")
        sys.exit(1)

    if not isinstance(loaded_data, list):
         print(f"ERREUR : Le contenu JSON dans '{file_path}' n'est pas une liste.")
         sys.exit(1)

    # --- Initialisation du Splitter ---
    print(f"\n--- Étape 2: Initialisation du TokenTextSplitter (chunk: {chunk_size}, overlap: {chunk_overlap}) ---")
    try:
        token_splitter = TokenTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        print("TokenTextSplitter initialisé.")
    except Exception as e:
        print(f"Erreur lors de l'initialisation de TokenTextSplitter (vérifiez l'installation de tiktoken) : {e}")
        sys.exit(1)


    # --- Préparation des Chunks ---
    print("\n--- Étape 3: Formatage et découpage des recettes en chunks ---")
    all_chunks_text = []
    all_chunk_ids = []
    all_chunk_metadata = []
    total_recipes_processed = 0
    total_chunks_generated = 0

    for index, recipe in enumerate(loaded_data):
        if not isinstance(recipe, dict):
            print(f" Avertissement: Élément ignoré à l'index {index}, ce n'est pas un dictionnaire.")
            continue

        # Générer l'ID principal de la recette
        recipe_id = recipe.get("canonical_url", recipe.get("title", f"recette_inconnue_{index}"))
        recipe_title = recipe.get("title", "Titre inconnu")

        # 1. Formater la recette en texte
        recipe_text = format_recipe_for_embedding(recipe)

        # 2. Découper le texte formaté avec le TokenTextSplitter
        try:
            sub_chunks = token_splitter.split_text(recipe_text)
        except Exception as e:
            print(f"  Erreur lors du découpage de la recette ID {recipe_id}: {e}")
            sub_chunks = [recipe_text] # En cas d'erreur de split, on garde le texte entier (peut échouer à l'embedding)

        # 3. Stocker chaque sub-chunk avec un ID unique et des métadonnées
        num_sub_chunks = len(sub_chunks)
        total_chunks_generated += num_sub_chunks
        print(f"  Recette {index+1}/{len(loaded_data)} (ID: {recipe_id}) -> {num_sub_chunks} chunk(s)")

        for chunk_index, chunk_text in enumerate(sub_chunks):
            # Créer un ID unique pour ce chunk spécifique
            # Format: {ID_Recette}_part_{Index_Chunk}
            chunk_id = f"{recipe_id}_part_{chunk_index}"

            # Préparer les métadonnées pour ce chunk
            chunk_metadata = {
                "original_recipe_id": recipe_id,
                "recipe_title": recipe_title,
                "chunk_index": chunk_index, # Pour savoir quelle partie de la recette c'est
                "total_chunks_for_recipe": num_sub_chunks, # Pour savoir combien il y avait de parties
                "author": recipe.get("author"),
                "cuisine": recipe.get("cuisine"),
                "source_host": recipe.get("host")
            }

            all_chunks_text.append(chunk_text)
            all_chunk_ids.append(chunk_id)
            all_chunk_metadata.append(chunk_metadata)

        total_recipes_processed += 1

    print(f"\nPréparation terminée.")
    print(f"  Nombre total de recettes traitées : {total_recipes_processed}")
    print(f"  Nombre total de chunks générés   : {total_chunks_generated}")

    # --- Création/Peuplement de la base ChromaDB ---
    if all_chunks_text:
        print(f"\n--- Étape 4: Création/Peuplement de la base ChromaDB ('{collection_name}') ---")
        try:
            db_collection = create_chroma_db(
                documents=all_chunks_text,
                ids=all_chunk_ids,
                metadatas=all_chunk_metadata,
                name=collection_name,
                dir=chroma_db_dir
            )
            print(f"\nBase de données ChromaDB '{collection_name}' prête dans '{chroma_db_dir}'.")

            # Optionnel : Vérifier le nombre d'éléments dans la collection
            count = db_collection.count()
            print(f"Vérification : La collection '{collection_name}' contient {count} éléments.")

        except Exception as e:
            print(f"ERREUR majeure lors de la création ou du peuplement de la base ChromaDB : {e}")
            sys.exit(1)
    else:
        print("\nAucun chunk n'a été généré, la base ChromaDB n'a pas été créée/peuplée.")

    print("\n--- Embedding done successfully ---")