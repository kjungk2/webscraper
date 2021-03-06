# Builds a hashtable of country code to country name
# Source: http://www.nationsonline.org/oneworld/country_code_list.htm

# set variables and open local files that were copied from source webpage
code_list = []
country_list = []
code_txt = open('C:\Users\jungkk\Desktop\webscrape\country_code_dict\code.txt')
country_txt = open('C:\Users\jungkk\Desktop\webscrape\country_code_dict\country.txt')


# Populate code_list
next = code_txt.readline()
while next != "":
	# append to list; [:2] chops off /n character
	code_list.append(next[:2])
	next = code_txt.readline()
code_txt.close()

# Populate country_list	
next = country_txt.readline()
while next != "":
	# append to list; was adding on an extra space so chop it off
	country_list.append(next[:len(next)-1])
	next = country_txt.readline()
country_txt.close()
	
# Populate my_dict using the lists
my_dict = {code_list[x].lower():country_list[x] for x in range(len(code_list))}



# Write to a text file so I can email to myself
final_dict = open('C:\Users\jungkk\Desktop\webscrape\country_code_dict\code_to_country.txt', 'w')
for element in my_dict:
	curr = "'" + element + "'" + ":" + "'" + my_dict[element] + "', "
	final_dict.write(curr)
final_dict.close()



# Some testing, dict1 is code_to_country.txt copied and pasted
dict1 = {'gw':'Guinea-Bissau', 'gu':'Guam', 'gt':'Guatemala', 'gs':'South Georgia and the South Sandwich Islands', 'gr':'Greece', 'gq':'Equatorial Guinea', 'gp':'Guadeloupe', 'gy':'Guyana', 'gg':'Guernsey', 'gf':'French Guiana', 'ge':'Georgia', 'gd':'Grenada', 'gb':'United Kingdom', 'ga':'Gabon', 'gn':'Guinea', 'gm':'Gambia', 'gl':'Greenland', 'gi':'Gibraltar', 'gh':'Ghana', 'lb':'Lebanon', 'lc':'Saint Lucia', 'la':'Lao PDR', 'tv':'Tuvalu', 'tw':'Taiwan, Republic of China', 'tt':'Trinidad and Tobago', 'tr':'Turkey', 'lk':'Sri Lanka', 'li':'Liechtenstein', 'lv':'Latvia', 'to':'Tonga', 'lt':'Lithuania', 'lu':'Luxembourg', 'lr':'Liberia', 'ls':'Lesotho', 'th':'Thailand', 'tf':'French Southern Territories', 'tg':'Togo', 'td':'Chad', 'tc':'Turks and Caicos Islands', 'ly':'Libya', 'do':'Dominican Republic', 'dm':'Dominica', 'dj':'Djibouti', 'dk':'Denmark', 'um':'US Minor Outlying Islands', 'de':'Germany', 'ye':'Yemen', 'dz':'Algeria', 'uy':'Uruguay', 'yt':'Mayotte', 'vu':'Vanuatu', 'kn':'Saint Kitts and Nevis', 'qa':'Qatar', 'tm':'Turkmenistan', 'eh':'Western Sahara', 'wf':'Wallis and Futuna Islands', 'ee':'Estonia', 'eg':'Egypt', 'za':'South Africa', 'ec':'Ecuador', 'sj':'Svalbard and Jan Mayen Islands', 'us':'United States of America', 'et':'Ethiopia', 'zw':'Zimbabwe', 'es':'Spain', 'er':'Eritrea', 'ru':'Russian Federation', 'rw':'Rwanda', 'rs':'Serbia', 're':'Reunion', 'it':'Italy', 'ro':'Romania', 'tk':'Tokelau', 'tz':'United Republic of Tanzania', 'bd':'Bangladesh', 'be':'Belgium', 'bf':'Burkina Faso', 'bg':'Bulgaria', 'ba':'Bosnia and Herzegovina', 'bb':'Barbados', 'bl':'Saint-Barthelemy', 'bm':'Bermuda', 'bn':'Brunei Darussalam', 'bo':'Bolivia', 'bh':'Bahrain', 'bi':'Burundi', 'bj':'Benin', 'bt':'Bhutan', 'jm':'Jamaica', 'bv':'Bouvet Island', 'bw':'Botswana', 'ws':'Samoa', 'sa':'Saudi Arabia', 'br':'Brazil', 'bs':'Bahamas', 'je':'Jersey', 'by':'Belarus', 'bz':'Belize', 'tn':'Tunisia', 'om':'Oman', 'zm':'Zambia', 'ua':'Ukraine', 'jo':'Jordan', 'ch':'Switzerland', 'mz':'Mozambique', 'ck':'Cook Islands', 'ci':'Cote dIvoire', 'py':'Paraguay', 'co':'Colombia', 'cn':'China', 'cm':'Cameroon', 'cl':'Chile', 'cc':'Cocos (Keeling) Islands', 'ca':'Canada', 'cg':'Congo (Brazzaville)', 'cf':'Central African Republic', 'cd':'Congo (Kinshasa)', 'cz':'Czech Republic', 'cy':'Cyprus', 'cx':'Christmas Island', 'cr':'Costa Rica', 'cv':'Cape Verde', 'cu':'Cuba', 've':'Venezuela (Bolivarian Republic)', 'pr':'Puerto Rico', 'ps':'Palestinian Territory', 'pw':'Palau', 'pt':'Portugal', 'vg':'British Virgin Islands', 'tl':'Timor-Leste', 'iq':'Iraq', 'pa':'Panama', 'pf':'French Polynesia', 'pg':'Papua New Guinea', 'pe':'Peru', 'pk':'Pakistan', 'ph':'Philippines', 'pn':'Pitcairn', 'pl':'Poland', 'pm':'Saint Pierre and Miquelon', 'hr':'Croatia', 'ht':'Haiti', 'hu':'Hungary', 'hk':'Hong Kong (SAR China)', 'hn':'Honduras', 'vn':'Viet Nam', 'hm':'Heard and Mcdonald Islands', 'jp':'Japan', 'me':'Montenegro', 'md':'Moldova', 'mg':'Madagascar', 'mf':'Saint-Martin (French part)', 'ma':'Morocco', 'mc':'Monaco', 'uz':'Uzbekistan', 'mm':'Myanmar', 'ml':'Mali', 'mo':'Macao (SAR China)', 'mn':'Mongolia', 'mh':'Marshall Islands', 'mk':'Republic of Macedonia', 'mu':'Mauritius', 'mt':'Malta', 'mw':'Malawi', 'mv':'Maldives', 'mq':'Martinique', 'mp':'Northern Mariana Islands', 'ms':'Montserrat', 'mr':'Mauritania', 'im':'Isle of Man', 'ug':'Uganda', 'my':'Malaysia', 'mx':'Mexico', 'il':'Israel', 'va':'Holy See (Vatican City State)', 'vc':'Saint Vincent and Grenadines', 'ae':'United Arab Emirates', 'ad':'Andorra', 'ag':'Antigua and Barbuda', 'af':'Afghanistan', 'ai':'Anguilla', 'vi':'Virgin Islands (US)', 'is':'Iceland', 'ir':'Islamic Republic of Iran', 'am':'Armenia', 'al':'Albania', 'ao':'Angola', 'an':'Netherlands Antilles', 'aq':'Antarctica', 'as':'American Samoa', 'ar':'Argentina', 'au':'Australia', 'at':'Austria', 'aw':'Aruba', 'in':'India', 'ax':'Aland Islands', 'az':'Azerbaijan', 'ie':'Ireland', 'id':'Indonesia', 'ni':'Nicaragua', 'nl':'Netherlands', 'no':'Norway', 'na':'Namibia', 'nc':'New Caledonia', 'ne':'Niger', 'nf':'Norfolk Island', 'ng':'Nigeria', 'nz':'New Zealand', 'sh':'Saint Helena', 'np':'Nepal', 'so':'Somalia', 'nr':'Nauru', 'nu':'Niue', 'fr':'France', 'io':'British Indian Ocean Territory', 'sb':'Solomon Islands', 'fi':'Finland', 'fj':'Fiji', 'fk':'Falkland Islands (Malvinas)', 'fm':'Federated States of Micronesia', 'fo':'Faroe Islands', 'tj':'Tajikistan', 'sz':'Swaziland', 'sy':'Syrian Arab Republic (Syria)', 'kg':'Kyrgyzstan', 'ke':'Kenya', 'ss':'South Sudan', 'sr':'Suriname', 'ki':'Kiribati', 'kh':'Cambodia', 'sv':'El Salvador', 'km':'Comoros', 'st':'Sao Tome and Principe', 'sk':'Slovakia', 'kr':'South Korea', 'si':'Slovenia', 'kp':'North Korea', 'kw':'Kuwait', 'sn':'Senegal', 'sm':'San Marino', 'sl':'Sierra Leone', 'sc':'Seychelles', 'kz':'Kazakhstan', 'ky':'Cayman Islands', 'sg':'Singapore', 'se':'Sweden', 'sd':'Sudan'}
print dict1['gw']
print dict1['ci']
print dict1['sy']
print dict1['kp']
print dict1['us']