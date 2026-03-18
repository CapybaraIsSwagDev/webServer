import os, json, random
from pathlib import Path
tasks_dir = Path(__file__).parent.parent / "site" / "tasks"
from .database import get_db



#  {id:"",title:""}
def getTasks():
    # Resolve **here**, at request time
    dir_path = tasks_dir.resolve()
    print("Using input dir:", dir_path)

    result = []

    for file in dir_path.glob("*.json"):
        print("Reading file:", file)
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)

        result.append({
            "id": file.stem,
            "title": data.get("title", "No title")
        })

    return result # <-- wrap list in jsonify for proper HTTP response

def getTask(id):
    with get_db() as db:
        pass
        row = db.execute(
            "SELECT * FROM lessons WHERE id = ?;",
            (ID,)
        ).fetchone()


def getFeatured():
    dir_path = tasks_dir.resolve()
    print("Using input dir:", dir_path)

    # Collect only filenames, not contents
    files = list(dir_path.glob("*.json"))

    needed = 3
    count = min(len(files), needed)

    # Randomly choose which files to read
    chosen_files = random.sample(files, count)

    tasks = []
    for file in chosen_files:
        print("Reading file:", file)
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)

        #difficulty mapping
        
        
        tasks.append({
            "id": file.stem,
            "summary": data.get("description", ""),
            "difficulty": data.get("difficulty", -1),
            "xp":"Not yet implemented",
            "title": data.get("title", "No title")
        })

    # Pad with dummies if needed
    missing = needed - len(tasks)
    dummies = [{
        "id": "dummy",
        "summary":"None its a dummy",
        "title": "Dummy Task"
    }] * missing

    return tasks + dummies

    

