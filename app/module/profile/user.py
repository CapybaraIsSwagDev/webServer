from werkzeug.security import generate_password_hash, check_password_hash
import math


def calcLevel(xp):
    return math.floor(math.sqrt(xp / 50))


def calcXp(level):
    return level ** 2 * 50

# -----------------------------
# User class
# -----------------------------
class User:
    def __init__(self, row):
        if row is None:
            raise ValueError("Cannot create User without row")
        row = dict(row)
        self.id: int = row.get("id")
        self.username = row.get("username")
        self.hashed_password = row.get("password_hash")
        self.email = row.get("email")
        self.xp = row.get("xp")
        self.created = row.get("created")
        
    def getPublic(self,minimalist=False) -> dict:
        data = {
            "id":self.id,
            "username":self.username,
            "xp":self.xp,
        }
        if not minimalist:
            data.update({
                "created":str(self.created).split(" ")[0],
            })
        return data
    def __iter__(self):
        yield "id", self.id
        yield "username", self.username
        yield "email", self.email
        yield "xp", self.xp
        yield "created", str(self.created).split(" ")[0]

    def checkPassword(self, password) -> bool:
        return check_password_hash(self.hashed_password, password)

    def getLevel(self) -> int:
        return math.floor(math.sqrt(self.xp / 50))
    
    def getLevelProgress(self) -> int:
        currentLevelXP = calcLevel(self.xp)
        nextLevelXP = calcLevel(self.xp+1)+1

        xpIntoLevel = self.xp - currentLevelXP
        xpNeededForLevel = nextLevelXP - currentLevelXP
        
        return round(xpIntoLevel/xpNeededForLevel*100)
    

        
