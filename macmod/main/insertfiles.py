# this module is used to upload files to the database

from pymongo import MongoClient
import pandas as pd
import subprocess
import docx2txt
import gridfs
import json
import os

db = MongoClient("mongodb+srv://<URI>?retryWrites=true&w=majority").macmod
fs = gridfs.GridFS(db)

# method to send all files in a directory to mongoDB GridFS
def send_file_to_mongodb(filename):
    with os.scandir(filename) as dirs:
        for entry in dirs:
            try:
                f = fs.new_file()
                f.filename = entry.name
                # application guides will contain brand :key: metadata, content for other items will have content :key: metadata
                f.metadata = {'filename': entry.name, 'content': 'Product Phase Table','belongsTo':'applications'}
                f.write(entry.name.encode("UTF-8"))
            finally: 
                f.close()


# sheet names will be sent from the frontend along with the file
sheetnames = {
    1 :  '1',
    2 :  '2',
    3 :  '3',
    4 :  '4',
    5 :  '5',
    6 :  '6',
    7 :  '7',
    8 :  '8',
    9 :  '9',
    10 : '10',
    12 : '12',
    13 : '13',
    14 : '14',
    15 : '15',
    16 : '16',
    17 : '17',
    18 : '18',
    19:  '19',
    20 : '20',
    21 : '21',
    22 : '22',
    23 : '23',
    24 : '24',
    25 : '25',
    26 : '26',
    27 : '27',
    28 : '28',
    29 : '29',
    30 : '30',
    31 : '31',
    32 : '32',
    33 : '33',
    34 : '34',
    35 : '35',
    36 : '36',
    37 : '37',
    38 : '38',
    39 : '39',
    40 : '40',
    41 : '41',
    42 : '42',
    43 : '43',
    44 : '44',
    45 : '45',
    46 : '46',
    47 : '47',
    48 : '48',
    49 : '49',
    50 : '50',
    51 : '51',
    52 : '52',
    53 : '53',
    54 : '54',
    55 : '55',
    56 : '56',
    57 : '57',
    58 : '58',
    59 : '59',
    60 : '60',
    61 : '61',
    62 : '62',
    63 : '63',
    64 : '64',
    65 : '65',
    66 : '66',
    67 : '67',
    68 : '68',
    69 : '69',
    70 : '70',
    71 : '71',
    72 : '72',
    73 : '73',
    74 : '74',
    75 : '75',
    76 : '76',
    77 : '77',
    78 : '78',
    79 : '79',
    80 : '80',
    81 : '81',
    82 : '82',
    83 : '83',
    84 : '84',
    85 : '85',
    86 : '86',
    87 : '87',
    88 : '88',
    89 : '89',
    90 : '90',
    91 : '91',
    92 : '92',
    93 : '93',
    94 : '94',
    95 : '95',
    96 : '96',
    97 : '97',
    98 : '98',
    99 : '99',
    100 : '100',
    101 : '101',
    102 : '102',
    103 : '103',
    104 : '104',
    105 : '105',
    106 : '106',
    107 : '107',
    108 : '108',
    109 : '109',
    110 : '110',
    111 : '111',
    112 : '112',
    113 : '113',
    114 : '114',
    115 : '115',
    116 : '116',
    117 : '117',
    118 : '118',
    119 : '119',
    120 : '120',
    121 : '121',
    122 : '122',
    123 : '123',
    124 : '124',
    125 : '125',
    126 : '126',
    127 : '127',
    128 : '128',
    129 : '129',
    130 : '130',
    131 : '131',
    132 : '132',
    133 : '133',
    134 : '134',
    135 : '135',
    136 : '136',
    137 : '137',
    138 : '138',
    139 : '139',
    140 : '140',
    141 : '141',
    142 : '142',
    143 : '143',
    144 : '144',
    145 : '145',
    146 : '146',
    147 : '147',
    148 : '148',
    149 : '149',
    150 : '150',
    151 : '151',
    152 : '152',
    153 : '153',
    154 : '154',
    155 : '155',
    156 : '156',
    157 : '157',
    158 : '158',
    159 : '159',
    160 : '160',
    161 : '161',
    162 : '162',
    163 : '163',
    164 : '164',
    165 : '165',
    166 : '166',
    167 : '167',
    168 : '168',
    169 : '169',
    170 : '170',
    171 : '171',
    172 : '172',
    173 : '173'
    }

# method to create json from xlsx
def create_json_from_xlsx(filename,sheetnames):
    # read the xlsx file once and store it so we only load the file once
    xls = pd.ExcelFile(filename)
    # loop over the sheetnames
    for i in sheetnames:
        # as we loop over sheetname we read items contained in each sheet by passing the sheetnames[i] iter val
        df = pd.read_excel(xls, sheet_name=sheetnames[i])
        # drop all null values 
        df = df.dropna(how='all',axis=1).dropna(how='all')
        df['bondedphase'] = sheetnames[i]
        # create a json file for each sheet in the dataframe record
        df.to_json(f'{i}.json',orient='records')
        cmds = ['mongoimport','--host','URI', '--ssl', '--username', '<USERNAME>', '--password', '<AUTH>', '--authenticationDatabase', 'admin', '--db', '<DATABASE>', '--collection', '<COLLECTION>', '--jsonArray' ,f'<FILE>']
        k = subprocess.Popen(cmds)
        try:
            k.wait(timeout=5)
        except subprocess.TimeoutExpired:
            kill(k.pid)

# create_json_from_xlsx('/Users/user/Desktop/my-projects/macmod/macmod-backend-prod/macmod/main/Allphasepages.xlsx',sheetnames)
