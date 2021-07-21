from googletrans import Translator

class GoogleTranslator:
    
    translator = Translator()

    @classmethod
    def translate_one(cls, text_to_translate):
        translated_text = cls.translator.translate(text_to_translate, dest='ru', src='en').text
        return translated_text

    @classmethod
    def translate_many(cls, texts_to_translate):
        str_to_translate = '\n'.join(texts_to_translate)
        translated_str = cls.translator.translate(str_to_translate, dest='ru', src='en').text
        translated_array = translated_str.split('\n')
        return translated_array
