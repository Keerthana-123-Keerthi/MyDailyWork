import pandas as pd
import numpy as np
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

def collaborative_filtering_recommendations(user_item_matrix, user_id, num_recommendations=3):
    # Perform SVD
    svd = TruncatedSVD(n_components=2)
    matrix = user_item_matrix.values
    matrix_reduced = svd.fit_transform(matrix)
    matrix_reconstructed = np.dot(matrix_reduced, svd.components_)

    # Make predictions
    predictions = pd.DataFrame(matrix_reconstructed, index=user_item_matrix.index, columns=user_item_matrix.columns)
    
    # Recommend items for the given user
    user_ratings = user_item_matrix.loc[user_id]
    predicted_ratings = predictions.loc[user_id]
    recommendations = predicted_ratings[~user_ratings.index.isin(user_ratings[user_ratings > 0].index)]
    top_recommendations = recommendations.sort_values(ascending=False).head(num_recommendations)
    
    return top_recommendations

def content_based_filtering_recommendations(items_df, liked_items, num_recommendations=3):
    # Vectorize item descriptions
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(items_df['description'])
    
    # User's liked items descriptions
    liked_items_descriptions = items_df[items_df['item_id'].isin(liked_items)]['description']
    liked_items_matrix = vectorizer.transform(liked_items_descriptions)
    
    # Compute similarity between liked items and all items
    cosine_sim = cosine_similarity(liked_items_matrix, tfidf_matrix)
    similarities = cosine_sim.mean(axis=0)
    
    # Recommend items based on similarity
    items_df['similarity'] = similarities
    recommendations = items_df.sort_values(by='similarity', ascending=False)
    top_recommendations = recommendations[~recommendations['item_id'].isin(liked_items)]
    
    return top_recommendations.head(num_recommendations)

# Sample Data for Collaborative Filtering
data = {
    'user_id': [1, 1, 2, 2, 3, 3, 4, 4],
    'item_id': [1, 2, 1, 3, 2, 3, 1, 4],
    'rating': [5, 3, 4, 2, 4, 5, 2, 4]
}
df = pd.DataFrame(data)

# Create a user-item matrix
user_item_matrix = df.pivot(index='user_id', columns='item_id', values='rating').fillna(0)

# Collaborative Filtering
user_id = 1
collab_recommendations = collaborative_filtering_recommendations(user_item_matrix, user_id)
print("Collaborative Filtering Recommendations:")
print(collab_recommendations)

# Sample Data for Content-Based Filtering
item_features = {
    'item_id': [1, 2, 3, 4],
    'description': [
        "Action adventure movie",
        "Romantic comedy film",
        "Sci-fi thriller",
        "Documentary about nature"
    ]
}
items_df = pd.DataFrame(item_features)

# Content-Based Filtering
liked_items = [1, 2]
content_recommendations = content_based_filtering_recommendations(items_df, liked_items)
print("\nContent-Based Filtering Recommendations:")
print(content_recommendations)
