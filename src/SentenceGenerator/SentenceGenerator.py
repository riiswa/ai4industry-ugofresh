import random, re

class SentenceGenerator:

    class Options:
        def __init__(self):
            self.optional_selection = {"general":0.5, "by_class":{}}
            self.prevent_duplicate = []

        def set_general_optional_selection(self, value):
            self.optional_selection["general"]=value
            return self

        def set_optional_selection_for_class(self, classname, value):
            self.optional_selection["by_class"][classname]=value
            return self

        def prevent_duplicated_value(self, classname):
            self.prevent_duplicate.append(classname)
            return self

        def as_dict(self):
            return {
                "optional_selection":self.optional_selection,
                "prevent_duplicate":self.prevent_duplicate
            }

    def default_options():
        return SentenceGenerator.Options()

    def __init__(self, options=None):
        if options == None:
            options = SentenceGenerator.Options()
        self.options = options.as_dict() if isinstance(options, SentenceGenerator.Options) else options
        self.patterns = []
        self.specifiers = {}
        self.filters = {}
        self.taggers = {}

    def add_pattern(self, pattern):
        self.patterns.append(pattern)
        return self
    
    def add_specifier(self, classname, cb):
        self.specifiers[classname] = cb
        return self

    def add_filter(self, classname, cb):
        self.filters[classname] = cb
        return self

    def add_tagger(self, classname, cb):
        self.taggers[classname] = cb
        return self

    def format_tag(start, end, name):
        return {"start":start, "end":end, "name":name}

    def select_instance(choices, rule):
        instance = random.choice(choices)
        if rule is not None:
            instance = rule(instance)
        return instance

    def buildSentences(self, instances_ref, count=50):
        sentences = []
        elements_by_classes={}
        for instance_name in instances_ref["instances"]:
            key = instances_ref["classes"][instances_ref["instances"][instance_name]]["type"]
            if key in elements_by_classes:
                elements_by_classes[key].append(instance_name)
            else:
                elements_by_classes[key] = [instance_name]
        for _ in range(count):
            pattern = str(random.choice(self.patterns))
            tags = []
            construct = {}
            ps = re.findall("{([\w|é|è|ê|\-|\?]*)}", pattern)
            while len(ps):
                p = ps[0]
                classname = p
                optional = classname.endswith("?")
                if optional:
                    classname = classname.split("?")[0]
                possible = elements_by_classes[classname]
                if classname in self.filters:
                    possible = self.filters[classname](construct, possible)
                if classname in construct and classname in self.options["prevent_duplicate"]:
                    for v in construct[classname]:
                        while v in possible:
                            possible.remove(v)
                selection_chance = self.options["optional_selection"]["by_class"][classname] if classname in self.options["optional_selection"]["by_class"] else self.options["optional_selection"]["general"] 
                if(len(possible)>0 and (not optional or random.random()<selection_chance)):
                    instance = SentenceGenerator.select_instance(possible, self.specifiers[classname] if classname in self.specifiers else None)
                    if classname in construct:
                        construct[classname].append(instance)
                    else:
                        construct[classname] = [instance]
                    start = pattern.find("{"+p+"}")
                    if classname in self.taggers:
                        for tag in self.taggers[classname](start, instance):
                            tags.append(tag)
                    else:
                        end = start+len(instance)
                        tags.append(SentenceGenerator.format_tag(start, end, classname))
                    pattern = pattern.replace("{"+p+"}", instance, 1)
                else:
                    pattern = pattern.replace("{"+p+"}", "", 1)
                ps = re.findall("{([\w|é|è|ê|\-|\?]*)}", pattern)
            if re.match("{.*}", pattern) is not None:
                print("WARNING: unfilled pattern detected")
            sentences.append({"sentence":" ".join(pattern.split()), "tags": tags})
        return sentences