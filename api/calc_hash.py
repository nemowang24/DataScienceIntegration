import hashlib
import json


def get_doc_hash(doc):
    # Method 1: Using SHA-256 (recommended for uniqueness)
    # Convert the document to a canonical string representation
    if isinstance(doc, dict):
        # Sort the dictionary to ensure consistent ordering
        doc_str = json.dumps(doc, sort_keys=True)
    else:
        doc_str = str(doc)

    # Create SHA-256 hash
    return hashlib.sha256(doc_str.encode('utf-8')).hexdigest()


def get_doc_hash_md5(doc):
    # Method 2: Using MD5 (shorter hash, but less collision resistant)
    if isinstance(doc, dict):
        doc_str = json.dumps(doc, sort_keys=True)
    else:
        doc_str = str(doc)

    return hashlib.md5(doc_str.encode('utf-8')).hexdigest()

if __name__ == "__main__":

    # Example usage:
    doc1 = {
        "name": "John",
        "age": 30,
        "city": "New York"
    }

    doc2 = {
        "age": 30,
        "city": "New York",
        "name": "John"  # Same content as doc1, different order
    }

    doc3 = {
        "name": "John",
        "age": 31,  # Different content
        "city": "New York"
    }

    doc3 = """Create a realistic, flat-design style icon based on the following word:
    
                    Word: '{word}'
    
                    The icon should:
                    - Be suitable for a vocabulary flashcard.
                    - Depict a single, clearly identifiable visual hint or association to the definition, rather than a literal depiction.
                    - Use a realistic, natural-looking style (NOT cartoonish), avoiding exaggerated features.
                    - Ensure the image looks friendly and natural, avoiding any Uncanny Valley effects (such as distorted faces, unnatural hands, or unsettling expressions).
                    - Be visually engaging and encourage active recall and deeper thinking for language learners.
                    - Center the subject on a clean white background.
                    - Absolutely no text, letters, or alphabet characters should appear in the image.
    
                    Focus on visual clarity, conceptual simplicity, realism, and memorability."""
    doc4 = """Create a realistic, flat-design style icon based on the following word:
    
                    Word: {word}
    
                    The icon should:
                    - Be suitable for a vocabulary flashcard.
                    - Depict a single, clearly identifiable visual hint or association to the definition, rather than a literal depiction.
                    - Use a realistic, natural-looking style (NOT cartoonish), avoiding exaggerated features.
                    - Ensure the image looks friendly and natural, avoiding any Uncanny Valley effects (such as distorted faces, unnatural hands, or unsettling expressions).
                    - Be visually engaging and encourage active recall and deeper thinking for language learners.
                    - Center the subject on a clean white background.
                    - Absolutely no text, letters, or alphabet characters should appear in the image.
    
                    Focus on visual clarity, conceptual simplicity, realism, and memorability."""


    # Test the hashing
    print(f"Doc1 SHA-256: {get_doc_hash(doc1)}")
    print(f"Doc2 SHA-256: {get_doc_hash(doc2)}")  # Will be same as doc1
    print(f"Doc3 SHA-256: {get_doc_hash(doc3)}")  # Will be different
    print(f"Doc3 SHA-256: {get_doc_hash(doc4)}")  # Will be different

    print(f"\nDoc1 MD5: {get_doc_hash_md5(doc1)}")
    print(f"Doc2 MD5: {get_doc_hash_md5(doc2)}")  # Will be same as doc1
    print(f"Doc3 MD5: {get_doc_hash_md5(doc3)}")  # Will be different
