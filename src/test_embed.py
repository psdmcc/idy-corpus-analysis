from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
vec = model.encode("International Day of Yoga UN speech")

print(vec.shape)
