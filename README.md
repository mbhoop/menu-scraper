# menu-scraper

A command-line tool that reads a restaurant menu (PDF or photo) and tells you which dishes are safe to eat based on your allergies and dietary restrictions — powered by Claude's multimodal API.

## Why I built this

I'm severely allergic to quinoa and I'm vegan, and finding restaurants I can safely eat at is genuinely hard. Menus rarely list full ingredients, and cross-checking every dish against an allergy *and* a diet is tedious and error-prone. So I built this to do it for me: hand it a menu, tell it what I can't eat, and get back a clear breakdown of what's safe, what's not, and what's uncertain.

Because the stakes are real for someone with a severe allergy, the tool is deliberately cautious — it flags ambiguous dishes as **uncertain** rather than giving a false all-clear.

## What it does

- Accepts a menu as a **PDF or image** (JPG, JPEG, PNG, or WebP)
- Asks you for your **allergies** and **dietary restrictions**
- Uses the **Claude API** to read the menu and analyze every dish
- Returns a readable report that sorts dishes into **safe**, **contains-allergen**, and **uncertain**

## How it works

1. The menu file is base64-encoded and sent to the Claude API as a document or image content block (so it works on both PDFs and photos).
2. A structured prompt asks the model to parse the menu and return **JSON** — per-dish ingredients, allergens present, diet flags, and any uncertain items.
3. The JSON response is parsed and formatted into a plain-text safety report in the terminal.

## Getting started

### Prerequisites

- Python 3.10+
- An [Anthropic API key](https://console.anthropic.com/)

### Installation

```bash
git clone https://github.com/mbhoop/menu-scraper.git
cd menu-scraper
pip install -r requirements.txt
```

### Setup

Create a `.env` file in the project root and add your API key:

```
ANTHROPIC_API_KEY=your_key_here
```

> The `.env` file is gitignored so your key is never committed.

### Usage

Pass the path to a menu file as an argument, then answer the prompts:

```bash
python parser.py path/to/menu.pdf
```

```
Any food allergies? (If none, enter 'no') quinoa
Any dietary restrictions? (If none, enter 'no') vegan
```

## Example output

```
This restaurant poses a moderate risk for quinoa-allergic diners; quinoa
appears in two dishes. Several vegan options are available.

This restaurant contains quinoa!
Harvest Bowl
Quinoa Tabbouleh

The following dishes are vegan and quinoa free:
Hummus Plate
Garden Salad
Roasted Veggie Wrap

The following dishes may possibly contain quinoa:
Chef's Grain Bowl
```
