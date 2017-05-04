'''Helper functions for PCS webscraper'''

'''
params: takes in a string in format 'hh:mm:ss' or 'mm:ss'
return: a list of ints [HH, MM, SS] of length 3
'''
def hms_formatter(time):

    colon_count = 0
    hms_list = []

    # max of 2 colons so get the positions of each
    for ix in range(len(time)):
        if time[ix] == ':':
            if colon_count == 0:
                first_colon_ix = ix
            else:
                second_colon_ix = ix
            colon_count += 1

    # set the hours, minutes and seconds
    if colon_count == 2:
        hours = time[:first_colon_ix]
        minutes = time[first_colon_ix+1:second_colon_ix]
        seconds = time[second_colon_ix+1:]

    elif colon_count == 1:
        hours = 0
        minutes = time[:first_colon_ix]
        seconds = time[first_colon_ix+1:]

    else:
        return "Err: given parameter is in unexpected format. PARAM type: " + str(type(time))

    hms_list.append(hours)
    hms_list.append(minutes)
    hms_list.append(seconds)

    return hms_list

'''
params: winning_time and riders_time_diff, both in hms_format (lists)
return: a STRING of those two times added together, aka the riders total time ('HHMMSS')
'''
def hms_adder(winning_time, riders_time_diff):

    # get the integers from the hms_formatted times
    winning_hours = int(winning_time[0])
    winning_minutes = int(winning_time[1])
    winning_seconds = int(winning_time[2])
    rider_hours = int(riders_time_diff[0])
    rider_minutes = int(riders_time_diff[1])
    rider_seconds = int(riders_time_diff[2])

    # add them together to get rider's total time
    final_hours = winning_hours + rider_hours
    final_minutes = winning_minutes + rider_minutes
    final_seconds = winning_seconds + rider_seconds

    # if minutes or seconds exceeds 60, do some time-math; must do seconds first
    if final_seconds > 59:
        final_minutes += 1
        final_seconds -= 60

    if final_minutes > 59:
        final_hours += 1
        final_minutes -= 60

    # convert to string and use zfill to force leading zeros in case min or sec is < 10 (needed for SQL TIME field)
    final_hours = str(final_hours)
    final_minutes = str(final_minutes).zfill(2)
    final_seconds = str(final_seconds).zfill(2)


    return str(final_hours) + str(final_minutes) + str(final_seconds)

def get_country_name(country_code):
	country_code_dict = {'gw':'Guinea-Bissau',
	'gu':'Guam',
	'gt':'Guatemala',
	'gs':'South Georgia and the South Sandwich Islands',
	'gr':'Greece',
	'gq':'Equatorial Guinea',
	'gp':'Guadeloupe',
	'gy':'Guyana',
	'gg':'Guernsey',
	'gf':'French Guiana',
	'ge':'Georgia',
	'gd':'Grenada',
	'gb':'United Kingdom',
	'ga':'Gabon',
	'gn':'Guinea',
	'gm':'Gambia',
	'gl':'Greenland',
	'gi':'Gibraltar',
	'gh':'Ghana',
	'lb':'Lebanon',
	'lc':'Saint Lucia',
	'la':'Lao PDR',
	'tv':'Tuvalu',
	'tw':'Taiwan, Republic of China',
	'tt':'Trinidad and Tobago',
	'tr':'Turkey',
	'lk':'Sri Lanka',
	'li':'Liechtenstein',
	'lv':'Latvia',
	'to':'Tonga',
	'lt':'Lithuania',
	'lu':'Luxembourg',
	'lr':'Liberia',
	'ls':'Lesotho',
	'th':'Thailand',
	'tf':'French Southern Territories',
	'tg':'Togo',
	'td':'Chad',
	'tc':'Turks and Caicos Islands',
	'ly':'Libya',
	'do':'Dominican Republic',
	'dm':'Dominica',
	'dj':'Djibouti',
	'dk':'Denmark',
	'um':'US Minor Outlying Islands',
	'de':'Germany',
	'ye':'Yemen',
	'dz':'Algeria',
	'uy':'Uruguay',
	'yt':'Mayotte',
	'vu':'Vanuatu',
	'kn':'Saint Kitts and Nevis',
	'qa':'Qatar',
	'tm':'Turkmenistan',
	'eh':'Western Sahara',
	'wf':'Wallis and Futuna Islands',
	'ee':'Estonia',
	'eg':'Egypt',
	'za':'South Africa',
	'ec':'Ecuador',
	'sj':'Svalbard and Jan Mayen Islands',
	'us':'United States of America',
	'et':'Ethiopia',
	'zw':'Zimbabwe',
	'es':'Spain',
	'er':'Eritrea',
	'ru':'Russian Federation',
	'rw':'Rwanda',
	'rs':'Serbia',
	're':'Reunion',
	'it':'Italy',
	'ro':'Romania',
	'tk':'Tokelau',
	'tz':'United Republic of Tanzania',
	'bd':'Bangladesh',
	'be':'Belgium',
	'bf':'Burkina Faso',
	'bg':'Bulgaria',
	'ba':'Bosnia and Herzegovina',
	'bb':'Barbados',
	'bl':'Saint-Barthelemy',
	'bm':'Bermuda',
	'bn':'Brunei Darussalam',
	'bo':'Bolivia',
	'bh':'Bahrain',
	'bi':'Burundi',
	'bj':'Benin',
	'bt':'Bhutan',
	'jm':'Jamaica',
	'bv':'Bouvet Island',
	'bw':'Botswana',
	'ws':'Samoa',
	'sa':'Saudi Arabia',
	'br':'Brazil',
	'bs':'Bahamas',
	'je':'Jersey',
	'by':'Belarus',
	'bz':'Belize',
	'tn':'Tunisia',
	'om':'Oman',
	'zm':'Zambia',
	'ua':'Ukraine',
	'jo':'Jordan',
	'ch':'Switzerland',
	'mz':'Mozambique',
	'ck':'Cook Islands',
	'ci':'Cote dIvoire',
	'py':'Paraguay',
	'co':'Colombia',
	'cn':'China',
	'cm':'Cameroon',
	'cl':'Chile',
	'cc':'Cocos (Keeling) Islands',
	'ca':'Canada',
	'cg':'Congo (Brazzaville)',
	'cf':'Central African Republic',
	'cd':'Congo (Kinshasa)',
	'cz':'Czech Republic',
	'cy':'Cyprus',
	'cx':'Christmas Island',
	'cr':'Costa Rica',
	'cv':'Cape Verde',
	'cu':'Cuba',
	've':'Venezuela (Bolivarian Republic)',
	'pr':'Puerto Rico',
	'ps':'Palestinian Territory',
	'pw':'Palau',
	'pt':'Portugal',
	'vg':'British Virgin Islands',
	'tl':'Timor-Leste',
	'iq':'Iraq',
	'pa':'Panama',
	'pf':'French Polynesia',
	'pg':'Papua New Guinea',
	'pe':'Peru',
	'pk':'Pakistan',
	'ph':'Philippines',
	'pn':'Pitcairn',
	'pl':'Poland',
	'pm':'Saint Pierre and Miquelon',
	'hr':'Croatia',
	'ht':'Haiti',
	'hu':'Hungary',
	'hk':'Hong Kong (SAR China)',
	'hn':'Honduras',
	'vn':'Viet Nam',
	'hm':'Heard and Mcdonald Islands',
	'jp':'Japan',
	'me':'Montenegro',
	'md':'Moldova',
	'mg':'Madagascar',
	'mf':'Saint-Martin (French part)',
	'ma':'Morocco',
	'mc':'Monaco',
	'uz':'Uzbekistan',
	'mm':'Myanmar',
	'ml':'Mali',
	'mo':'Macao (SAR China)',
	'mn':'Mongolia',
	'mh':'Marshall Islands',
	'mk':'Republic of Macedonia',
	'mu':'Mauritius',
	'mt':'Malta',
	'mw':'Malawi',
	'mv':'Maldives',
	'mq':'Martinique',
	'mp':'Northern Mariana Islands',
	'ms':'Montserrat',
	'mr':'Mauritania',
	'im':'Isle of Man',
	'ug':'Uganda',
	'my':'Malaysia',
	'mx':'Mexico',
	'il':'Israel',
	'va':'Holy See (Vatican City State)',
	'vc':'Saint Vincent and Grenadines',
	'ae':'United Arab Emirates',
	'ad':'Andorra',
	'ag':'Antigua and Barbuda',
	'af':'Afghanistan',
	'ai':'Anguilla',
	'vi':'Virgin Islands (US)',
	'is':'Iceland',
	'ir':'Islamic Republic of Iran',
	'am':'Armenia',
	'al':'Albania',
	'ao':'Angola',
	'an':'Netherlands Antilles',
	'aq':'Antarctica',
	'as':'American Samoa',
	'ar':'Argentina',
	'au':'Australia',
	'at':'Austria',
	'aw':'Aruba',
	'in':'India',
	'ax':'Aland Islands',
	'az':'Azerbaijan',
	'ie':'Ireland',
	'id':'Indonesia',
	'ni':'Nicaragua',
	'nl':'Netherlands',
	'no':'Norway',
	'na':'Namibia',
	'nc':'New Caledonia',
	'ne':'Niger',
	'nf':'Norfolk Island',
	'ng':'Nigeria',
	'nz':'New Zealand',
	'sh':'Saint Helena',
	'np':'Nepal',
	'so':'Somalia',
	'nr':'Nauru',
	'nu':'Niue',
	'fr':'France',
	'io':'British Indian Ocean Territory',
	'sb':'Solomon Islands',
	'fi':'Finland',
	'fj':'Fiji',
	'fk':'Falkland Islands (Malvinas)',
	'fm':'Federated States of Micronesia',
	'fo':'Faroe Islands',
	'tj':'Tajikistan',
	'sz':'Swaziland',
	'sy':'Syrian Arab Republic (Syria)',
	'kg':'Kyrgyzstan',
	'ke':'Kenya',
	'ss':'South Sudan',
	'sr':'Suriname',
	'ki':'Kiribati',
	'kh':'Cambodia',
	'sv':'El Salvador',
	'km':'Comoros',
	'st':'Sao Tome and Principe',
	'sk':'Slovakia',
	'kr':'South Korea',
	'si':'Slovenia',
	'kp':'North Korea',
	'kw':'Kuwait',
	'sn':'Senegal',
	'sm':'San Marino',
	'sl':'Sierra Leone',
	'sc':'Seychelles',
	'kz':'Kazakhstan',
	'ky':'Cayman Islands',
	'sg':'Singapore',
	'se':'Sweden',
	'sd':'Sudan'}

	return country_code_dict[country_code]
