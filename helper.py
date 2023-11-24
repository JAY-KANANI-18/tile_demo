from sklearn.metrics.pairwise import cosine_similarity

class Search_Setup:

 def get_similar_images(self, image_path: str, number_of_images: int = 10):
  self.image_path = image_path
  self.number_of_images = number_of_images
  query_vector = self._get_query_vector(self.image_path)
  img_dict = self._search_by_vector(query_vector, self.number_of_images)
 # Calculate similarity percentages
  similarity_percentages = []
  for img_path in img_dict.values():
   img_vector = self._get_query_vector(img_path)
   similarity = cosine_similarity([query_vector], [img_vector])[0][0]
   similarity_percentages.append(similarity)
  return img_dict, similarity_percentages

