# Minecraft AI Command Builder

> **Part of MCmadeEasy** - A larger project to make Minecraft easier and more accessible

A beginner-friendly machine learning project that creates a natural language interface for Minecraft commands. This was my **first time learning and building a machine learning algorithm**, and I'm excited to share what I built!

## What This Project Does

This project converts plain English sentences into actual Minecraft game commands using machine learning and AI.

**Examples:**
| You Type | Converts To |
|----------|-------------|
| "give me 10 diamonds" | `/give @p diamond 10` |
| "teleport me to the village" | `/tp @p village` |
| "kick the griefer" | `/kick griefer` |
| "find nearest mansion" | `/locate woodland_mansion` |
| "kill all zombies" | `/kill @e[type=zombie]` |

---

## About This Project (My Learning Journey)

This was **my first time learning and creating a machine learning algorithm**! Before this, I had no experience with ML or AI. I learned:

- How machine learning models work (specifically Logistic Regression)
- Text vectorization with CountVectorizer
- Training and evaluating ML models
- Building an end-to-end NLP pipeline

This project is part of my bigger initiative called **MCmadeEasy** - a collection of tools to make Minecraft more accessible. The ML Command Builder is the intelligent core that understands what players want and converts it into game commands.

---

## How It Works (Detailed Explanation)

The system works in **4 main stages**:

```
User Input → Intent Classification → Parameter Extraction → Command Building → Output
```

### Stage 1: Intent Classification (ML Model)

When you type something, the system first needs to figure out: **Are they asking a question, having a chat, or wanting a command?**

This is done using a **Logistic Regression** model trained with scikit-learn:

1. **Text Vectorization** - The CountVectorizer converts text into numerical features (bag-of-words approach)
2. **ML Prediction** - The Logistic Regression model predicts "chat" or "command"
3. **Keyword Fallback** - For common keywords, simple rule-based detection is used as backup

**File:** `core/classifier.py` - Contains the trained ML model and prediction logic

### Stage 2: Parameter Extraction

If the intent is "command", the system extracts important information:

- **Items** - "diamond", "iron_sword", "enchanted_book"
- **Quantities** - "10", "2 stacks", "5 diamond blocks"
- **Coordinates** - Any numbers that look like X, Y, Z coordinates
- **Structure names** - "village", "mansion", "stronghold"
- **Player names** - Who to target

**Files:**
- `core/extractor.py` - Extracts quantities and coordinates
- `core/resolver.py` - Uses fuzzy matching (RapidFuzz) to find items/structures in text

### Stage 3: Command Building

The `CommandEngine` takes the command type and parameters, then fills in a template:

```python
# Template from commands.txt
"give": "/give {player} {item} {count}"

# After parameter filling
"/give @p diamond 10"
```

**File:** `core/command_engine.py` - Builds final Minecraft commands

### Stage 4: AI Chat (OpenRouter Integration)

For general questions or conversation (not Minecraft commands), the system uses **OpenRouter's DeepSeek AI**:

- **API**: OpenRouter (free tier available)
- **Model**: deepseek/deepseek-chat
- **Use case**: Answer Minecraft questions, help with crafting recipes, general chat

**File:** `core/ai_chat.py` - Handles AI conversation

---

## Project Structure & File Explanations

```
Command_builder/
├── main.py                        # Entry point - runs the chat interface
├── requirements.txt               # Python dependencies
│
├── core/                          # Core functionality modules
│   ├── classifier.py             # ML intent classifier (Logistic Regression)
│   ├── command_engine.py         # Builds Minecraft commands from templates
│   ├── extractor.py              # Extracts quantities, coordinates from text
│   ├── resolver.py               # Fuzzy matching for item/structure names
│   ├── router.py                 # Main routing logic - coordinates all components
│   ├── normalizer.py             # Text normalization (e.g., "teleport" → "tp")
│   ├── memory.py                 # Remembers context (recent locations, chat history)
│   ├── loader.py                 # Loads data files
│   └── ai_chat.py                # OpenRouter AI integration for chat
│
├── data/                          # Game data files
│   ├── commands.txt              # Command templates with {placeholders}
│   ├── items.txt                 # List of Minecraft items
│   ├── entities.txt              # List of Minecraft entities (mobs)
│   ├── structures.txt            # List of Minecraft structures
│   ├── blocks.txt                # List of Minecraft blocks
│   └── players.txt               # Saved player names
│
├── models/                        # Trained ML model files
│   ├── intent_model.pkl         # Trained Logistic Regression model
│   └── vectorizer.pkl           # Fitted CountVectorizer
│
└── training/                      # Model training code
    ├── train_intent_model.py    # Script to train the ML model
    └── dataset.txt              # Training data (text | label format)
```

---

## Detailed Component Breakdown

### core/router.py (The Brain)
The main coordinator that orchestrates everything:
- Receives user input
- Calls the classifier to determine intent
- Routes to appropriate handler (command builder or AI chat)
- Manages memory and context

### core/classifier.py (ML Classification)
My first ML model! Uses:
- Trained Logistic Regression (saved as `intent_model.pkl`)
- CountVectorizer (saved as `vectorizer.pkl`)
- Keyword-based fallback for common patterns

### core/resolver.py (Fuzzy Matching)
Uses **RapidFuzz** library for fuzzy string matching:
- "diamnd" → "diamond" (typo correction)
- "iron ingot" → "iron_ingot"
- Handles various text formats

### core/memory.py (Context)
Remembers:
- Last teleport location
- Recently used items
- Chat history (for AI conversation context)

### core/ai_chat.py (AI Integration)
Connects to OpenRouter API:
- Uses DeepSeek model
- Maintains conversation history
- System prompt: "You are a helpful Minecraft assistant"

---

## Requirements

```bash
pip install -r requirements.txt
```

Required packages:
- scikit-learn (ML)
- joblib (model serialization)
- rapidfuzz (fuzzy matching)
- requests (API calls)

---

## Training the Model

To retrain the ML model with new examples:

```bash
python training/train_intent_model.py
```

The training data is in `training/dataset.txt` in format:
```
give me diamonds|command
how are you|chat
what is creeper|chat
```

---

## Usage

```bash
python main.py
```

**Example session:**
```
Minecraft AI Assistant ready!
Type 'exit' to quit.

User: give me 10 diamonds
COMMAND: /give @p diamond 10

User: teleport me to the village
COMMAND: /locate village
Then run: /tp @s <x> <y> <z>

User: how do I make a pickaxe?
CHAT: To craft a pickaxe, you'll need 3 stone...

User: where am i?
CHAT: To find your coordinates in Minecraft:
1. Press F3 to open Debug Screen...
```

Type 'exit' to quit.

---

## What's Next for MCmadeEasy

This ML Command Builder is just one part of my MCmadeEasy project. Future plans include:
- Direct server integration (execute commands in-game)
- Web interface
- More ML models for advanced features
- Voice command support

---

## Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Main language |
| scikit-learn | ML (Logistic Regression) |
| joblib | Model serialization |
| RapidFuzz | Fuzzy string matching |
| OpenRouter API | AI chat (DeepSeek) |

---

## Learning Resources That Helped Me

- scikit-learn documentation
- Real Python tutorials
- OpenRouter API docs

---

## License

MIT License - Feel free to use and learn from this!

---

*Built with love as my first ML project. Happy crafting! ⛏️*
