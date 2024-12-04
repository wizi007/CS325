from abc import ABC, abstractmethod
import openai
import os
import matplotlib.pyplot as plt 
import numpy as np
import re


PROMPT = "Please categorize this statement as either positive, neutral or negative: "

def remove_emojis(text):
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642" 
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
                           "]+", flags=re.UNICODE)
    return(emoji_pattern.sub(r'', text))

class Query:
    def __init__(self):
        self.client = openai.OpenAI(
            base_url="http://localhost:11434/v1",
            api_key="nokeyneeded",
            )

    def generate_output(self, text):
        response = self.client.chat.completions.create(
            model="tinyllama",
            temperature=0.7,
            n=1,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": PROMPT+text},
            ],
            stop=["\n"]
        )
        return remove_emojis(response.choices[0].message.content)
        

class TextGenerator:
    def __init__(self, function):
        self.function = function
        path = '../Project2/'
        try:
            self.files = [path + f for f in os.listdir(path) if f.endswith('_reviews.txt')]
        except FileNotFoundError:
            self.files = []
        self.file_limit = 10

    def generating_reader(self, input_file):
        with open(input_file) as file:
            yield from file

    def generating_output(self, input_file, output_file):
        texts = self.generating_reader(input_file)
        count = 0
        with open(output_file, "w") as f:
            # Empty the file
            pass
        for text in texts:
            if count == self.file_limit:
                break
            with open(output_file, "a", encoding="utf-8") as file:
                result = self.function(text)
                file.write(result+"\n")
                count += 1
    def run(self):
        for file in self.files:
            out_name = file.split('_')[0] + '_sentiment.txt'
            self.generating_output(file, out_name)

class Plotter:
    def __init__(self, products):
        self.barWidth = 0.25
        self.fig = plt.subplots(figsize =(12, 8))
        self.products = products
        self.get_data()

    def get_data(self):
        self.positives = []
        self.negatives = []
        self.neutrals = []
        for product in self.products:
            self.positives.append(0)
            self.negatives.append(0)
            self.neutrals.append(0)
            with open(product+'_sentiment.txt') as f:
                lines = f.readlines()
            for line in lines:
                count_p = sum(1 for _ in re.finditer(r'\b%s\b' % re.escape('positive'), line.lower()))
                count_n = sum(1 for _ in re.finditer(r'\b%s\b' % re.escape('negative'), line.lower()))
                if count_p > count_n:
                    self.positives[-1]+=1
                elif count_n > count_p:
                    self.negatives[-1]+=1
                else:
                    self.neutrals[-1]+=1

    def plot(self):
        br1 = np.arange(len(self.products)) 
        br2 = [x + self.barWidth for x in br1] 
        br3 = [x + self.barWidth for x in br2] 

        plt.bar(br1, self.positives, color ='r', width = self.barWidth, 
                edgecolor ='grey', label ='positive') 
        plt.bar(br2, self.neutrals, color ='g', width = self.barWidth, 
                edgecolor ='grey', label ='neutral') 
        plt.bar(br3, self.negatives, color ='b', width = self.barWidth, 
                edgecolor ='grey', label ='negative') 

        # Adding Xticks 
        plt.xlabel('Product', fontweight ='bold', fontsize = 15) 
        plt.ylabel('Number of Reviews', fontweight ='bold', fontsize = 15) 
        plt.xticks([r + self.barWidth for r in range(len(self.products))], 
                [product.split('/')[-1] for product in self.products])

        plt.legend()
        plt.show()

def main():
    query = Query()
    tg = TextGenerator(query.generate_output)
    tg.run()
    products = [file.split('_')[0] for file in tg.files]
    plotter = Plotter(products)
    plotter.plot()

if __name__ == "__main__":
    main()