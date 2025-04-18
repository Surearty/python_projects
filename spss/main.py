import pyreadstat
import pandas as pd

import pyreadstat

df, meta = pyreadstat.read_sav('лечение 01.25_1.sav')
df.to_csv('лечение_01.25_1.csv', index=False, encoding='utf-8-sig')