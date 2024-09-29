import heapq

# Function to tokenize documents into sentences using a basic split method
def segment_document(document):
    return document.split('\n')

# Heuristic function: estimates how many sentences are yet to be matched
def heuristic_cost(doc1_segments, doc2_segments, current_index):
    return abs(len(doc1_segments) - current_index)

# Cost function: computes the dissimilarity between two sentences using simple word overlap
def compute_cost(segment1, segment2):
    # Convert segments to sets of words and calculate overlap ratio
    set1 = set(segment1.split())
    set2 = set(segment2.split())
    if not set1 or not set2:
        return 1.0  # Max dissimilarity if either segment is empty
    return 1 - len(set1.intersection(set2)) / max(len(set1), len(set2))

# A* search algorithm implementation for plagiarism detection
def a_star_plagiarism_detection(doc1, doc2):
    # Segment the documents
    doc1_segments = segment_document(doc1)
    doc2_segments = segment_document(doc2)
    
    # Priority queue to store the states (segment index, path cost, and total estimated cost)
    priority_queue = []
    heapq.heappush(priority_queue, (0, 0, 0, []))  # (total_cost, g_value, index_in_doc1, path)

    # Keep track of visited states
    visited = set()

    # While there are states to explore
    while priority_queue:
        total_cost, g_value, index_in_doc1, path = heapq.heappop(priority_queue)

        # Goal state: all sentences in doc1 have been aligned
        if index_in_doc1 == len(doc1_segments):
            return path, total_cost

        if (index_in_doc1, g_value) in visited:
            continue

        visited.add((index_in_doc1, g_value))

        # Explore matching each segment of doc1 with every segment in doc2
        for index_in_doc2, segment2 in enumerate(doc2_segments):
            # Compute the cost to match doc1's current segment with doc2's current segment
            current_segment_cost = compute_cost(doc1_segments[index_in_doc1], segment2)
            new_g_value = g_value + current_segment_cost  # Accumulated cost so far

            # Calculate heuristic cost (estimated future cost)
            h_value = heuristic_cost(doc1_segments, doc2_segments, index_in_doc1 + 1)
            total_estimated_cost = new_g_value + h_value

            # Add new state to the priority queue
            new_path = path + [(doc1_segments[index_in_doc1], segment2)]
            heapq.heappush(priority_queue, (total_estimated_cost, new_g_value, index_in_doc1 + 1, new_path))

    return None, float('inf')  # No solution found

# Function to calculate similarity percentage based on total cost
def calculate_similarity(total_cost, total_segments):
    max_cost = total_segments  # Maximum possible cost is the number of segments
    similarity_score = (1 - (total_cost / max_cost)) * 100  # Convert to percentage
    return max(0, min(100, similarity_score))  # Ensure it's within 0 to 100

# Input from user
doc1_input = input("Enter the first statement: ")
doc2_input = input("Enter the second statement: ")

# Call the plagiarism detection function
path, total_cost = a_star_plagiarism_detection(doc1_input.strip(), doc2_input.strip())

# Output the result
total_segments = len(segment_document(doc1_input.strip()))
similarity_score = calculate_similarity(total_cost, total_segments)

if similarity_score > 60:
    print("Plagiarism detected!")
print(f"Similarity score: {similarity_score:.2f}")