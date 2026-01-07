from database import init_db, SessionLocal
from models import Question
import questions as q_data

def seed_data():
    init_db()
    db = SessionLocal()
    
    # Check if empty
    if db.query(Question).count() > 0:
        print("Database already seeded.")
        db.close()
        return

    print("Seeding database...")
    
    count = 0
    
    # 1. Process Vocab and Grammar data from questions.py
    # We will map "Beginner" -> Grades 1-3, "Intermediate" -> 4-6, "Advanced" -> 7-10
    
    grade_bands = {
        "Beginner": [1, 2, 3],
        "Intermediate": [4, 5, 6],
        "Advanced": [7, 8, 9, 10]
    }
    
    # Helper to insert MC
    def insert_mc(band, item, type_label):
        nonlocal count
        # For each grade in the band, we insert a copy (or we could just have one entry and filter by band, 
        # but to keep schema simple "grade" column, let's duplicate or pick one. 
        # The prompt asked for separate question bank for DB. Let's just insert for ALL grades in the band to be robust.)
        
        for grade in grade_bands[band]:
            if type_label == "vocab":
                # Create Synonym Question
                q_text_syn = f"What is a synonym for '{item['word']}'?"
                # Create clean options
                opts_syn = [item['syn']] + [o for o in item['opts'] if o != item['syn']][:3]
                if len(opts_syn) < 4: opts_syn += ["random"] * (4 - len(opts_syn)) # safety
                
                db.add(Question(
                    grade=grade, category=band, type="Multiple Choice", subtype="vocab_syn",
                    question_text=q_text_syn, answer=item['syn'], options=opts_syn
                ))
                count += 1
                
                # Create Antonym Question
                q_text_ant = f"What is a synonym for '{item['word']}'?" # Typo in my generic logic? No, antonym.
                q_text_ant = f"What is an antonym for '{item['word']}'?"
                opts_ant = [item['ant']] + [o for o in item['opts'] if o != item['ant']][:3]
                if len(opts_ant) < 4: opts_ant += ["random"] * (4 - len(opts_ant))

                db.add(Question(
                    grade=grade, category=band, type="Multiple Choice", subtype="vocab_ant",
                    question_text=q_text_ant, answer=item['ant'], options=opts_ant
                ))
                count += 1
                
            elif type_label == "grammar":
                # Item has q, a, o
                db.add(Question(
                    grade=grade, category=band, type="Multiple Choice", subtype="grammar",
                    question_text=item['q'], answer=item['a'], options=item['o']
                ))
                count += 1

    # Beginner
    for item in q_data.BEGINNER_VOCAB: insert_mc("Beginner", item, "vocab")
    for item in q_data.BEGINNER_GRAMMAR: insert_mc("Beginner", item, "grammar")
    
    # Intermediate
    for item in q_data.INTERMEDIATE_VOCAB: insert_mc("Intermediate", item, "vocab")
    for item in q_data.INTERMEDIATE_GRAMMAR: insert_mc("Intermediate", item, "grammar")
    
    # Advanced
    for item in q_data.ADVANCED_VOCAB: insert_mc("Advanced", item, "vocab")
    for item in q_data.ADVANCED_GRAMMAR: insert_mc("Advanced", item, "grammar")
    
    # Essay Topics
    for band, topics in q_data.ESSAY_TOPICS.items():
        for grade in grade_bands[band]:
            for topic in topics:
                db.add(Question(
                    grade=grade, category=band, type="Essay", subtype="essay",
                    question_text=f"Write a short essay on: '{topic}'", answer=None, options=None
                ))
                count += 1
                
    db.commit()
    print(f"Seeded {count} questions.")
    db.close()

if __name__ == "__main__":
    seed_data()
