import config
from tqdm import tqdm
import pandas as pd
from recipe_scrapers import scrape_me
from langdetect import detect, DetectorFactory

DetectorFactory.seed = 0
df = pd.read_csv(config.input_csv_path)
tqdm.pandas()


def extractor_func(link):
    global count
    title = ''
    instructions = ''
    ingredients = ''
    language = ''
    try:
        current_scraper = scrape_me(link, wild_mode=True)
    except:
        return title, instructions, ingredients, language
    try:
        title = current_scraper.title()
    except Exception:
        title = ''
    try:
        instructions = current_scraper.instructions()
        if len(instructions):
            language = detect(instructions)
        else:
            language = 'none'
    except Exception:
        instructions = ''
    try:
        ingredients = current_scraper.ingredients()
        ingredients = str(ingredients)
    except Exception:
        ingredients = ''

    return title, instructions, ingredients, language


data = df['url'].progress_apply(extractor_func)

titles = []
instructions = []
ingredients = []
languages = []

for row in data:
    titles.append(row[0])
    instructions.append(row[1])
    ingredients.append(row[2])
    languages.append(row[3])
    # print(row)
df['title'] = titles
df['instructions'] = instructions
df['ingredients'] = ingredients
df['language'] = languages
df.to_csv(config.output_csv_path)
