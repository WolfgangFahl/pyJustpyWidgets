import justpy as jp
import sys
try:
    import spacy
    _has_spacy = True
except:
    _has_spacy = False


# Load English tokenizer, tagger, parser and NER
# python -m spacy download en_core_web_sm
from jpwidgets.widgets import TokenSequence


def parse(self, msg):
    # Find named entities, phrases and concepts
    doc = self.nlp(msg.value)
    tokens = []
    lastPos = 0
    entities = list(doc.ents)
    entities.sort(key=lambda ent: ent.start_char)
    for entity in doc.ents:
        rawStr = msg.value[lastPos:entity.start_char]
        if rawStr:
            tokens.append(rawStr)
        entityStr = msg.value[entity.start_char:entity.end_char]
        tokens.append((entity.label_, entity.text))
        lastPos = entity.end_char
    rawStr = msg.value[lastPos:-1]
    if rawStr:
        tokens.append(rawStr)
    self.output.delete_components()
    tokenSeq = TokenSequence(tokens, a=self.output)


def ner_demo():
    nlp = spacy.load("en_core_web_sm")
    wp = jp.QuasarPage()
    referenceInput = jp.QInputChange(a=wp,
                                     label="Spacy NER parser",
                                     key="input",
                                     placeholder="Please enter string for Named Entity Recognition")
    referenceInput.on("change", parse)
    referenceInput.nlp = nlp
    referenceInput.output = jp.QDiv(a=wp)
    return wp

if not _has_spacy:
    print("Please install spacy inorder to run this example and ensure that the model en_core_web_sm is downloaded ($python -m spacy download en_core_web_sm ) ")
    sys.exit(0)
    
from  jpdemo.examples.basedemo import Demo
Demo('Spacy NER token demo',ner_demo)