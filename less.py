import urllib.request
from bs4 import SoupStrainer
from bs4 import BeautifulSoup

print('LESS Effort: Standings Scraper')

conf_selector = ''
conf_mappings = {
    'ah': 'Atlantic Hockey',
    'b1g': 'Big Ten',
    'ecac': 'ECAC',
    'he': 'Hockey East',
    'nchc': 'NCHC',
    'wcha': 'WCHA',
    'ind': 'Independents'
}
while len(conf_mappings.get(conf_selector, '')) == 0:
    conf_selector = input('Enter a conference (ah|b1g|ecac|he|nchc|wcha|ind): ')

stats_table = SoupStrainer('table', { 'class': 'data' })
url = 'http://www.collegehockeynews.com/reports/standings.php'

print('Selected conference: ' + conf_mappings[conf_selector])
print('Scraping \'' + url + '\'...')

with urllib.request.urlopen(url) as f:
    soup = BeautifulSoup(f.read().decode('latin-1'), 'html.parser', parse_only=stats_table)

data = []

logo_mappings = {
    'Brown': '{o.brown.logo}',
    'Clarkson': '{o.clark.logo}',
    'Colgate': '{o.colgate.logo}',
    'Cornell': '{o.cornell.logo}',
    'Dartmouth': '{o.dartmouth.logo}',
    'Harvard': '{o.harvard.logo}',
    'Princeton': '{o.princeton.logo}',
    'Quinnipiac': '{o.quinnipiac.logo}',
    'Rensselaer': '{o.rpi.logo}',
    'St. Lawrence': '{o.slu.logo}',
    'Union': '{o.union.logo}',
    'Yale': '{o.yale.logo}'
}

stats_col_mappings = {      # these are the columns we want to display
    'rank': 0,              # conference rank (by pts)
    'school': 1,            # school name
    'conf_record': 3,       # conference record (W-L-T)
    'pts': 5,               # conference points
    'overall_record': 10    # overall record (W-L-T)
}

for i in range(0, 12):
    data.append([])

for a_tag in soup.find_all('a'):
    a_tag.unwrap()
row = soup.find(string=conf_mappings[conf_selector])
if row == None:
    # above condition may occur if a conference is disbanded, or if there are no longer any independents
    print ("Conference " + conf_mappings[conf_selector] + " not found")
    raise SystemExit
row = row.parent.parent.next_sibling # go to the row after the one containing the conference name
while row != None and row['class'][0] == 'stats-section' or row['class'][0] == 'stats-header':
    row = row.next_sibling.next_sibling # every other sibling is a newline
while row != None and row['class'][0] != 'stats-section':
    col_ind = 0
    col = row.td
    while col != None:
        new_cell = col.text.strip()
        data[col_ind].append(new_cell)
        col_ind += 1
        col = col.next_sibling.next_sibling
    row = row.next_sibling.next_sibling

print('===!RANK!===')
print('\\n', end="")
# RPITS ignores leading newlines unless a newline character is used
# There can only be one leading newline in the output, for formatting reasons
for data_row in data[stats_col_mappings['rank']]:
    print(data_row)

print('===!SCHOOL!===')
print('School')
for data_row in data[stats_col_mappings['school']]:
    print(data_row)

print('===!PTS!===')
print('Pts')
for data_row in data[stats_col_mappings['pts']]:
    print(data_row)

print('===!CONF!===')
print('Conf')
for data_row in data[stats_col_mappings['conf_record']]:
    print(data_row)

print('===!OVERALL!===')
print('Overall')
for data_row in data[stats_col_mappings['overall_record']]:
    print(data_row)

print('===!LOGOS!===')
if conf_selector == 'ecac':
    for data_row in data[stats_col_mappings['school']]:
        print(logo_mappings[data_row])
else:
    print('logo order is currently available for the ECAC only')
