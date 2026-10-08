import re
import spacy
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer


# Download required NLTK tokenizer data
nltk.download("punkt_tab", quiet=True)


# Load spaCy English NLP model
nlp = spacy.load("en_core_web_sm")


# ---------------------------------------------------------
# 1. TEXT PREPROCESSING
# ---------------------------------------------------------

def preprocess_text(text):
    """
    Cleans and normalizes the meeting notes.
    """

    text = text.strip()
    text = re.sub(r"\s+", " ", text)

    return text


# ---------------------------------------------------------
# 2. ENTITY EXTRACTION
# ---------------------------------------------------------

def extract_entities(text):
    """
    Extracts persons, organizations, locations,
    dates and technologies using spaCy NER.
    """

    doc = nlp(text)

    entities = {
        "Persons": [],
        "Organizations": [],
        "Locations": [],
        "Dates": [],
        "Technologies": []
    }

    for ent in doc.ents:

        if ent.label_ == "PERSON":
            entities["Persons"].append(ent.text)

        elif ent.label_ == "ORG":
            entities["Organizations"].append(ent.text)

        elif ent.label_ in ["GPE", "LOC"]:
            entities["Locations"].append(ent.text)

        elif ent.label_ in ["DATE", "TIME"]:
            entities["Dates"].append(ent.text)

    # Simple technology detection
    technology_keywords = [
        "Python",
        "Java",
        "JavaScript",
        "React",
        "Node.js",
        "SQL",
        "MongoDB",
        "AWS",
        "Docker",
        "Kubernetes",
        "NLP",
        "Machine Learning",
        "Cybersecurity"
    ]

    text_lower = text.lower()

    for technology in technology_keywords:
        if technology.lower() in text_lower:
            entities["Technologies"].append(technology)

    # Remove duplicates
    for key in entities:
        entities[key] = list(dict.fromkeys(entities[key]))

    return entities


# ---------------------------------------------------------
# 3. KEYWORD EXTRACTION
# ---------------------------------------------------------

def extract_keywords(text, number_of_keywords=8):
    """
    Extracts important keywords using TF-IDF.
    """

    vectorizer = TfidfVectorizer(
        stop_words="english",
        max_features=number_of_keywords
    )

    matrix = vectorizer.fit_transform([text])

    scores = matrix.toarray()[0]
    words = vectorizer.get_feature_names_out()

    keyword_scores = list(zip(words, scores))

    keyword_scores.sort(
        key=lambda item: item[1],
        reverse=True
    )

    return [word for word, score in keyword_scores]


# ---------------------------------------------------------
# 4. ACTION ITEM DETECTION
# ---------------------------------------------------------

def extract_action_items(text):
    """
    Identifies sentences containing action/task words.
    """

    sentences = re.split(r"(?<=[.!?])\s+", text)

    action_words = [
        "will",
        "must",
        "should",
        "need to",
        "needs to",
        "assigned",
        "complete",
        "prepare",
        "submit",
        "review",
        "finish",
        "create",
        "develop",
        "make"
    ]

    action_items = []

    for sentence in sentences:

        sentence_lower = sentence.lower()

        if any(word in sentence_lower for word in action_words):

            person = None
            deadline = None

            # Try to identify person using spaCy
            doc = nlp(sentence)

            for ent in doc.ents:
                if ent.label_ == "PERSON":
                    person = ent.text
                    break

            # Try to identify date/deadline
            for ent in doc.ents:
                if ent.label_ in ["DATE", "TIME"]:
                    deadline = ent.text
                    break

            action_items.append({
                "Task": sentence.strip(),
                "Responsible Person": person,
                "Deadline": deadline
            })

    return action_items


# ---------------------------------------------------------
# 5. METADATA EXTRACTION
# ---------------------------------------------------------

def extract_metadata(text):
    """
    Extracts available meeting metadata.
    """

    doc = nlp(text)

    metadata = {
        "Dates": [],
        "People Mentioned": [],
        "Organizations Mentioned": []
    }

    for ent in doc.ents:

        if ent.label_ in ["DATE", "TIME"]:
            metadata["Dates"].append(ent.text)

        elif ent.label_ == "PERSON":
            metadata["People Mentioned"].append(ent.text)

        elif ent.label_ == "ORG":
            metadata["Organizations Mentioned"].append(ent.text)

    for key in metadata:
        metadata[key] = list(dict.fromkeys(metadata[key]))

    return metadata


# ---------------------------------------------------------
# 6. COMPLETE EXTRACTION PIPELINE
# ---------------------------------------------------------

def process_meeting_notes(text):

    cleaned_text = preprocess_text(text)

    entities = extract_entities(cleaned_text)

    keywords = extract_keywords(cleaned_text)

    action_items = extract_action_items(cleaned_text)

    metadata = extract_metadata(cleaned_text)

    return {
        "Entities": entities,
        "Keywords": keywords,
        "Action Items": action_items,
        "Metadata": metadata
    }


# ---------------------------------------------------------
# 7. MAIN PROGRAM
# ---------------------------------------------------------

if __name__ == "__main__":

    print("=" * 60)
    print("ENTITY & KEYWORD EXTRACTOR")
    print("=" * 60)

    meeting_notes = input(
        "\nEnter meeting notes:\n> "
    )

    if not meeting_notes.strip():

        print("\nError: Meeting notes cannot be empty.")

    else:

        result = process_meeting_notes(meeting_notes)

        print("\n" + "=" * 60)
        print("STRUCTURED OUTPUT")
        print("=" * 60)

        print("\nENTITIES:")
        for category, values in result["Entities"].items():
            print(f"{category}: {values}")

        print("\nKEYWORDS:")
        print(result["Keywords"])

        print("\nACTION ITEMS:")

        if result["Action Items"]:

            for item in result["Action Items"]:
                print(f"\nTask: {item['Task']}")
                print(
                    f"Responsible Person: "
                    f"{item['Responsible Person']}"
                )
                print(
                    f"Deadline: "
                    f"{item['Deadline']}"
                )

        else:
            print("No action items detected.")

        print("\nMETADATA:")

        for category, values in result["Metadata"].items():
            print(f"{category}: {values}")

        print("\n" + "=" * 60)