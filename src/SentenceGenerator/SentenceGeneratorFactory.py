import abc, random, re
from SentenceGenerator import SentenceGenerator

class SentenceGeneratorFactory(abc.ABC):
    @abc.abstractclassmethod
    def generate(self)->SentenceGenerator:
        pass

class UgoFreshSentenceGeneratorFactory(SentenceGeneratorFactory):
    
    def generate(self):
        return SentenceGenerator()\
        .add_specifier("Quantité", lambda v: ("" if v.startswith("un ") else str(round(random.random()*50)+1))+v+(" {Conditionnement}" if v.startswith("un ") else ""))\
        .add_specifier("Conditionnement", lambda v: (str(round(random.random()*50)+1) if v.startswith("rang") else "")+v)\
        .add_specifier("Prix", lambda v:str(round(random.random()*200)+1)+v)\
        .add_specifier("Sous-famille", lambda v: ("d'" if v[0].lower() in ['a', 'e', 'i', 'o', 'u', 'y'] else "de ")+v)\
        .add_specifier("Pays", lambda v: ("d'" if v[0].lower() in ['a', 'e', 'i', 'o', 'u', 'y'] else "de ")+v.split("(")[0].strip())\
        \
        .add_filter("Variété", lambda o, v: [value.split(o["Sous-famille"][len(o["Sous-famille"])-1])[1] for value in v if value.startswith(o["Sous-famille"][len(o["Sous-famille"])-1])] if "Sous-famille" in o else v)\
        \
        .add_tagger("Quantité", lambda s, v: [SentenceGenerator.format_tag(s, s+len(re.findall(r'\d+', v)[0] if len(re.findall(r'\d+', v)) else ""), "Quantité_Value"), SentenceGenerator.format_tag(s+len(re.findall(r'\d+', v)[0] if len(re.findall(r'\d+', v)) else ""), s+len(v), "Quantité_Unite")])\
        .add_tagger("Prix", lambda s, v: [SentenceGenerator.format_tag(s, s+len(re.findall(r'\d+', v)[0] if len(re.findall(r'\d+', v)) else ""), "Prix_Value"), SentenceGenerator.format_tag(s+len(re.findall(r'\d+', v)[0] if len(re.findall(r'\d+', v)) else ""), s+len(v), "Prix_Unite")])\
        \
        .add_pattern("Je voudrais {Quantité} {Sous-famille} {Variété} {Variété?} {Labels} de calibre {Calibre} en {Conditionnement} originaire {Pays}")\
        .add_pattern("Je souhaiterai {Quantité} {Sous-famille} {Variété} de calibre {Calibre} en {Conditionnement} en provenance {Pays}")\
        .add_pattern("J'aimerais {Quantité} {Sous-famille} {Labels} de taille {Calibre} en {Conditionnement} originaire {Pays}")\
        .add_pattern("Je vous prendrai {Quantité} {Sous-famille} {Variété} de calibre {Calibre} en {Conditionnement} originaire {Pays}")\
        .add_pattern("Je payerai bien {Quantité} {Sous-famille} {Labels} de calibre {Calibre} en {Conditionnement} venant {Pays}")\
        .add_pattern("Je vends des examplaires {Sous-famille} {Variété} {Variété} de taille {Calibre}, elles sont en {Conditionnement}, j'en ai {Quantité} qui me viennent {Pays}, je les vends à {Prix}")\
        .add_pattern("Je vends mes marchandises {Sous-famille} {Labels} de calibre {Calibre}, j'en ai {Quantité} en {Conditionnement} qui me viennent {Pays}, vendues à {Prix} l'unité")\
        .add_pattern("Je vends {Quantité} {Sous-famille} {Variété} {Variété?} à {Prix}, labélisées {Labels} de calibre {Calibre}, elles sont en {Conditionnement} en provenance {Pays}")
