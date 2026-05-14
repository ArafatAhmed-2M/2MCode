import random
import os

WORDS = [
    "apple", "crane", "dream", "earth", "flame", "grape", "heart", "image",
    "joker", "knife", "lemon", "mango", "noble", "ocean", "pearl", "queen",
    "radio", "sugar", "table", "ultra", "vital", "waste", "xenon", "yacht",
    "zebra", "about", "above", "abuse", "actor", "acute", "admit", "adopt",
    "adult", "after", "again", "agent", "agree", "ahead", "alarm", "album",
    "alert", "alien", "align", "alive", "allow", "alone", "along", "alter",
    "angel", "anger", "angle", "angry", "apart", "arena", "argue", "arise",
    "armor", "array", "aside", "asset", "avoid", "award", "aware", "awful",
    "bacon", "badge", "basic", "basin", "batch", "beach", "beard", "beast",
    "begin", "being", "below", "bench", "berry", "birth", "black", "blade",
    "blame", "blank", "blast", "blaze", "bleed", "blend", "bless", "blind",
    "block", "blood", "bloom", "blown", "board", "bonus", "booth", "bound",
    "brain", "brand", "brave", "bread", "break", "breed", "brick", "bride",
    "brief", "bring", "broad", "brook", "brown", "brush", "buddy", "build",
    "built", "bunch", "burst", "cabin", "cable", "candy", "cargo", "carry",
    "catch", "cause", "cedar", "chain", "chair", "chaos", "charm", "chart",
    "chase", "cheap", "check", "cheek", "cheer", "chess", "chest", "chief",
    "child", "chill", "china", "choir", "chord", "civil", "claim", "clash",
    "class", "clean", "clear", "clerk", "click", "cliff", "climb", "cling",
    "clock", "clone", "close", "cloth", "cloud", "coach", "coast", "color",
    "comet", "comic", "coral", "couch", "could", "count", "court", "cover",
    "crack", "craft", "crash", "crawl", "crazy", "cream", "crest", "crime",
    "crisp", "cross", "crowd", "crown", "crude", "curve", "cycle", "daily",
    "dance", "death", "debug", "decay", "decor", "decoy", "delay", "delta",
    "dense", "depot", "depth", "derby", "desert", "design", "desk", "devil",
    "diary", "dirty", "ditch", "dodge", "donor", "doubt", "dough", "draft",
    "drain", "drama", "drank", "drape", "drawn", "dread", "dress", "dried",
    "drift", "drill", "drink", "drive", "drone", "drove", "dying", "eager",
    "eagle", "early", "eight", "elder", "elect", "elite", "embed", "ember",
    "empty", "enemy", "enjoy", "enter", "entry", "equal", "equip", "error",
    "essay", "event", "every", "exact", "exile", "exist", "extra", "fable",
    "facet", "faith", "fancy", "fatal", "fault", "feast", "fence", "ferry",
    "fetch", "fever", "fiber", "field", "fifth", "fifty", "fight", "final",
    "first", "fixed", "flash", "fleet", "flesh", "float", "flock", "flood",
    "floor", "flora", "flour", "fluid", "flush", "flute", "focal", "focus",
    "force", "forge", "forth", "forum", "found", "frame", "frank", "fraud",
    "fresh", "front", "frost", "froze", "fruit", "fully", "gauge", "ghost",
    "giant", "given", "glass", "glide", "globe", "gloom", "glory", "gloss",
    "glove", "going", "grace", "grade", "grain", "grand", "grant", "grass",
    "grave", "great", "green", "greet", "grief", "grill", "grind", "groan",
    "groom", "gross", "group", "grove", "guard", "guess", "guest", "guide",
    "guild", "guilt", "gully", "happy", "harsh", "haste", "haunt", "haven",
    "heavy", "hedge", "hello", "hence", "hobby", "honey", "honor", "horse",
    "hotel", "house", "human", "humor", "hurry", "ideal", "imply", "index",
    "indie", "inner", "input", "irony", "ivory", "jelly", "jewel", "joint",
    "judge", "juice", "juicy", "jumbo", "kayak", "kebab", "knack", "kneel",
    "knock", "known", "label", "labor", "larch", "large", "laser", "later",
    "laugh", "layer", "learn", "lease", "least", "leave", "legal", "lemon",
    "level", "light", "limit", "linen", "liver", "local", "logic", "login",
    "loose", "lover", "lower", "lucky", "lunch", "lying", "magic", "major",
    "maker", "manor", "maple", "march", "marry", "match", "mayor", "media",
    "mercy", "merge", "merit", "merry", "metal", "meter", "might", "minor",
    "minus", "mixed", "model", "money", "month", "moral", "motor", "mount",
    "mouse", "mouth", "movie", "music", "naval", "nerve", "never", "newly",
    "night", "noise", "north", "noted", "novel", "nurse", "nylon", "occur",
    "ocean", "offer", "often", "olive", "onset", "opera", "orbit", "order",
    "organ", "other", "outer", "owned", "owner", "oxide", "ozone", "paint",
    "panel", "panic", "paper", "party", "pasta", "patch", "pause", "peace",
    "pearl", "penny", "phase", "phone", "photo", "piano", "piece", "pilot",
    "pinch", "pitch", "pixel", "place", "plain", "plane", "plant", "plate",
    "plaza", "plead", "pluck", "plumb", "plume", "plush", "point", "polar",
    "pound", "power", "press", "price", "pride", "prime", "prince", "print",
    "prior", "prize", "probe", "proof", "proud", "prove", "psalm", "pulse",
    "punch", "pupil", "purse", "queen", "quest", "queue", "quick", "quiet",
    "quote", "radar", "radio", "rally", "ranch", "range", "rapid", "ratio",
    "reach", "react", "realm", "rebel", "refer", "reign", "relax", "reply",
    "rider", "ridge", "rifle", "right", "rigid", "risky", "rival", "river",
    "robin", "robot", "rocky", "roost", "rough", "round", "route", "rover",
    "royal", "rugby", "ruler", "rural", "saint", "salad", "salon", "sauce",
    "scale", "scene", "scent", "scope", "score", "sense", "serve", "setup",
    "seven", "shade", "shaft", "shake", "shame", "shape", "share", "shark",
    "sharp", "sheep", "sheer", "sheet", "shelf", "shell", "shift", "shine",
    "shirt", "shock", "shore", "short", "shout", "shove", "sight", "sigma",
    "since", "sixth", "sixty", "sized", "skill", "skull", "slash", "sleep",
    "slice", "slide", "small", "smart", "smell", "smile", "smoke", "snack",
    "snake", "solid", "solve", "sorry", "sound", "south", "space", "spare",
    "spark", "speak", "speed", "spell", "spend", "spice", "spill", "spine",
    "spite", "split", "spoke", "sport", "spray", "squad", "stack", "staff",
    "stage", "stain", "stair", "stake", "stale", "stall", "stamp", "stand",
    "stark", "starr", "start", "state", "stays", "steal", "steam", "steel",
    "steep", "steer", "stern", "stick", "stiff", "still", "stock", "stone",
    "stood", "store", "storm", "story", "stove", "stuff", "style", "sugar",
    "suite", "sunny", "super", "surge", "swamp", "swarm", "swift", "swing",
    "sword", "swore", "syrup", "table", "taste", "teach", "teeth", "thank",
    "theme", "there", "thick", "thief", "thing", "think", "third", "thorn",
    "those", "three", "threw", "throw", "thumb", "tiger", "tight", "tired",
    "title", "today", "token", "total", "touch", "tough", "tower", "towns",
    "toxic", "trace", "track", "trade", "trail", "train", "trait", "trash",
    "treat", "trend", "trial", "tribe", "trick", "tried", "troop", "truck",
    "truly", "trump", "trunk", "trust", "truth", "tumor", "twice", "twist",
    "ultra", "uncle", "under", "unfair", "union", "unite", "unity", "until",
    "upper", "upset", "urban", "usage", "usual", "utter", "valid", "value",
    "valve", "vapor", "vault", "venue", "verse", "video", "vigor", "viral",
    "virus", "visit", "vista", "vital", "vivid", "vocal", "vodka", "voice",
    "volta", "voter", "wagon", "waist", "waste", "watch", "water", "weave",
    "weigh", "weird", "whale", "wheat", "wheel", "where", "which", "while",
    "white", "whole", "whose", "widen", "width", "witch", "woman", "world",
    "worry", "worse", "worst", "worth", "would", "wound", "wrath", "write",
    "wrong", "wrote", "yacht", "yield", "young", "youth", "zebra",
]

GREEN = "\033[92m"
YELLOW = "\033[93m"
GRAY = "\033[90m"
RESET = "\033[0m"
BOLD = "\033[1m"

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def colorize(char, status):
    colors = {"G": GREEN, "Y": YELLOW, "X": GRAY}
    return f"{colors[status]}{BOLD}{char}{RESET}"

def feedback(guess, target):
    result = ["X"] * 5
    target_list = list(target)
    for i in range(5):
        if guess[i] == target[i]:
            result[i] = "G"
            target_list[i] = None
    for i in range(5):
        if result[i] == "G":
            continue
        if guess[i] in target_list:
            result[i] = "Y"
            target_list[target_list.index(guess[i])] = None
    return result

def display_board(guesses, feedbacks):
    clear()
    print(f"{BOLD}  W O R D L E{RESET}\n")
    for g, f in zip(guesses, feedbacks):
        row = " ".join(colorize(g[i], f[i]) for i in range(5))
        print(f"  {row}")
    if len(guesses) < 6:
        print()
    print()

def play():
    target = random.choice(WORDS)
    guesses = []
    feedbacks = []
    for attempt in range(6):
        display_board(guesses, feedbacks)
        while True:
            guess = input(f"  Guess {attempt+1}/6: ").strip().lower()
            if len(guess) == 5 and guess.isalpha():
                break
            print(f"  {GRAY}Enter a 5-letter word.{RESET}")
        guesses.append(guess)
        fb = feedback(guess, target)
        feedbacks.append(fb)
        if guess == target:
            display_board(guesses, feedbacks)
            print(f"  {GREEN}{BOLD}You got it!{RESET}\n")
            return
    display_board(guesses, feedbacks)
    print(f"  The word was: {BOLD}{target.upper()}{RESET}\n")

if __name__ == "__main__":
    play()
