import main

class TestRemoveEmoji:
    def test_remove_emoji(self):
        test_word = "This is a string with an emoji 🙂 between"
        new_word = main.remove_emojis(test_word)
        expected_word = "This is a string with an emoji  between"
        assert new_word == expected_word

class TestQuery:
    def test_generate_output(self):
        test_query = main.Query()
        output = test_query.generate_output("test words")
        assert output != None

class TestTextGenerator:
    def test_generating_reader(self):
        test_tg = main.TextGenerator(None)
        output = test_tg.generating_reader('test_product_sentiment.txt')
        assert next(output) == 'positive, positive\n'


class TestPlotter:
    def test_get_data(self):
        test_plot = main.Plotter(['test_product'])
        assert test_plot.positives[0] == 2
        assert test_plot.negatives[0] == 1
        assert test_plot.neutrals[0] == 2
