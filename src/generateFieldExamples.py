import yaml
from string import Template

inputFile = './fieldDefinitions.yml'
outputFile = '../data/templates/https%3A%2F%2Fstatic.swissartresearch.net%2Fpartial%2FfieldExamples.html'

def loadSourceFromFile(file):
    try:
        with open (file, 'r') as f:
            source = yaml.safe_load(f.read())
            return source
    except:
        raise Exception("Could not read " + file)

fields = loadSourceFromFile(inputFile)['fields']

template = Template("""
<h3>$fieldName</h3>
<semantic-query
    query='$selectQuery LIMIT 10'
    template='<ul>{{#each bindings}}<li>{{#if (isIri value)}}<semantic-link iri="{{value.value}}"></semantic-link>{{else}}{{value.value}}{{/if}} <semantic-link iri="{{subject.value}}">&nbsp;<i class="fa fa-external-link" style="font-size:0.6rem"></i></semantic-link></li>{{/each}}</ul>'
    no-result-template='No results'
></semantic-query>
""")

output = ""

# Sort fields by label
fields = sorted(fields, key=lambda k: k['label'])

fieldsToOmit = ['mp_masse']

fields = [field for field in fields if field['id'] not in fieldsToOmit]

for field in fields:
    try:
        selectQuery = [d['select'] for d in field['queries'] if 'select' in d][0]
        selectQuery = selectQuery.replace("SELECT DISTINCT", "SELECT", 1)
        selectQuery = selectQuery.replace("SELECT", "SELECT DISTINCT ?subject", 1)
        output += template.substitute(fieldName=field['label'],selectQuery=selectQuery)
    except:
        pass

with open(outputFile, 'w') as f:
    f.write(output)
