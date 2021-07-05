from sqlalchemy import create_engine
from fractions import Fraction
import pandas as pd
import numpy as np
import urllib
import re
import os

os.chdir(r'C:\Users\Samuel\Google Drive\DnD\Data')

def die_mean(dmg_roll):
    if '-' in dmg_roll:
        modifier = -1*int(dmg_roll.split('-')[1])
        dmg_roll = dmg_roll.split('-')[0]
        count, die = int(dmg_roll.split('d')[0]), int(dmg_roll.split('d')[1])
    elif '+' in dmg_roll:
        modifier = int(dmg_roll.split('+')[1])
        dmg_roll = dmg_roll.split('+')[0]
        count, die = int(dmg_roll.split('d')[0]), int(dmg_roll.split('d')[1])
        
    else:
        count, die = int(dmg_roll.split('d')[0]), int(dmg_roll.split('d')[1])
        modifier = 0
    
    return ((die+1)/2)*count + modifier


files = os.listdir('Monsters')
damage_types = ['slashing', 'piercing', 'bludgeoning', 'poison', 'acid', 
                'fire', 'cold', 'radiant', 'necrotic', 'lightning', 
                'thunder', 'force', 'psychic']

condition_list = ['blinded', 'charmed', 'exhaustion', 'frightened',
                  'paralyzed', 'petrified', 'poisoned', 'prone', 
                  'deafened', 'grappled', 'restrained', 'stunned', 
                  'unconscious']

stat_cols = ['monster', 'challenge_rating', 'cr_numeric', 'size', 'race', 'subrace', 
             'armor', 'armor_type', 'hit_points', 'hit_die', 'str', 'dex', 'con', 'int', 
             'wis', 'cha', 'str_save', 'dex_save', 'con_save', 'int_save', 'wis_save', 
             'cha_save', 'multiattack']

stats = pd.DataFrame(index=range(len(files)), columns=stat_cols)

res = pd.DataFrame(index=range(0), columns=['monster', 'resistance'])
imm = pd.DataFrame(index=range(0), columns=['monster', 'immunity'])
cond = pd.DataFrame(index=range(0), columns=['monster', 'condition'])
atk = pd.DataFrame(index=range(0), columns=['monster', 'name', 'type', 'range', 'recharge', 'hit', 'save',
                                            'dmg_primary', 'roll_primary', 'type_primary', 'against_primary',
                                            'dmg_secondary', 'roll_secondary', 'type_secondary', 'against_secondary',
                                            'condition1', 'condition2', 'condition3', 'condition4', 'text'])
abilities = pd.DataFrame(index=range(0), columns=['monster', 'name', 'recharge', 'text'])

i = -1
for file in [file for file in files if 'template' not in file.lower()]:
    i += 1
    stats.loc[stats.index==i, 'monster'] = file.replace('.txt', '').strip()
    
    monster = open(f'Monsters\{file}', 'r', encoding='utf8').read()
    monster = monster[monster.find('Attribute List]'):
                      monster.find('[View All Monsters')]
    
    search = file.replace(".txt", "").strip().replace('(', '\(')
    search = search.replace(')', '\)')
    
    cr = re.search('Challenge (.+?)\(', monster).group(1).strip()
    stats.loc[stats.index==i, 'challenge_rating'] = cr
    
    size = re.search(f'{search}\\n\\n(.+?),', monster).group(1)
    size = size.split()
    stats.loc[stats.index==i, 'size'] = size[0].lower()
    stats.loc[stats.index==i, 'race'] = size[1].lower()
    stats.loc[stats.index==i, 'subrace'] = (size[2].replace('(', '').replace(')', '').lower() if len(size) > 2 else np.nan)
    
    armor = re.search('Armor Class (.+?)\\n', monster).group(1)
    armor = armor.split('(') if '(' in armor else armor.split()
    stats.loc[stats.index==i, 'armor'] = int(armor[0])
    stats.loc[stats.index==i, 'armor_type'] = (armor[1].replace('(', '').replace(')', '').lower()
                                               if len(armor) > 1 else np.nan)
    
    hp = re.search('Hit Points (.+?)\n', monster).group(1)
    hp = hp.split('(')
    stats.loc[stats.index==i, 'hit_points'] = int(hp[0])
    stats.loc[stats.index==i, 'hit_die'] = (hp[1].replace(')', '') if len(hp) > 1 else np.nan)
    
    strength = monster[monster.find('Hit Points'):]
    strength = strength[strength.find('\n\nSTR'):strength.find('\n\nDEX')]
    strength = int(re.search('\((.+?)\)', strength).group(1))
    stats.loc[stats.index==i, ['str', 'str_save']] = strength
    
    dex = monster[monster.find('Hit Points'):]
    dex = dex[dex.find('\n\nDEX'):dex.find('\n\nCON')]
    dex = int(re.search('\((.+?)\)', dex).group(1))
    stats.loc[stats.index==i, ['dex', 'dex_save']] = dex
    
    con = monster[monster.find('Hit Points'):]
    con = con[con.find('\n\nCON'):con.find('\n\nINT')]
    con = int(re.search('\((.+?)\)', con).group(1))
    stats.loc[stats.index==i, ['con', 'con_save']] = con
    
    intel = monster[monster.find('Hit Points'):]
    intel = intel[intel.find('\n\nINT'):intel.find('\n\nWIS')]
    intel = int(re.search('\((.+?)\)', intel).group(1))
    stats.loc[stats.index==i, ['int', 'int_save']] = intel
    
    wis = monster[monster.find('Hit Points'):]
    wis = wis[wis.find('\n\nWIS'):wis.find('\n\nCHA')]
    wis = int(re.search('\((.+?)\)', wis).group(1))
    stats.loc[stats.index==i, ['wis', 'wis_save']] = wis
    
    cha = monster[monster.find('Hit Points'):]
    cha = cha[cha.find('\n\nCHA'):cha.find('\n\n  *')]
    cha = int(re.search('\((.+?)\)', cha).group(1))
    stats.loc[stats.index==i, ['cha', 'cha_save']] = cha
    
    try:
        saves = re.search('Saving Throws\\n\\n(.+?)\\n\\n', monster).group(1)
        saves = saves.split(',')
        saves = [save.lower() if 'Char' not in save else save.replace('Char', 'cha').lower() for save in saves]
    except AttributeError:
        saves = []
        
    for save in ['str', 'dex', 'con', 'int', 'wis', 'cha']:
        for throw in saves:
            if save in throw:
                stats.loc[stats.index==i, f'{save}_save'] = (-1 * int(''.join(x for x in throw if x.isdigit())) if '-' in throw
                                                             else int(''.join(x for x in throw if x.isdigit())))
            
    try:
        resistance = re.search('Damage Resistance (.+?)\\n', monster).group(1)
    except AttributeError:
        resistance = ''
    
    try:
        immunity = re.search('Damage Immunities (.+?)\\n', monster).group(1)
    except AttributeError:
        immunity = ''
        
    try:
        conditions = re.search('Condition Immunities (.+?)\\n', monster).group(1)
    except AttributeError:
        conditions = ''
        
        
    for damage_type in damage_types:
        if damage_type in resistance.lower():
            res = res.append({'monster': file.replace('.txt', '').strip(), 'resistance': damage_type}, ignore_index=True)
            
        if damage_type in immunity.lower():
            imm = imm.append({'monster': file.replace('.txt', '').strip(), 'immunity': damage_type}, ignore_index=True)
            
    for condition in condition_list:
        if condition in conditions:
            cond = cond.append({'monster': file.replace('.txt', '').strip(), 'condition': condition}, ignore_index=True)
        
    actions = monster[monster.find('## Actions')+10:]
    actions = actions[:actions.find('##')]
    actions = actions.split('*')
    actions = [action.strip().lower() for action in actions if len(action) > 10]
    
    if len(actions) > 0:
        for action in actions:
            if 'multiattack' in action:
                stats.loc[stats.index==i, 'multiattack'] = action.replace('multiattack.', '').strip()
                
            else:
                name = re.sub('\([^>]+\)', '', 
                              action.split('.')[0] if '\\' not in action 
                              else action.split('.')[0] if 'gaze. demogorgon' in action
                              else action.split('.')[0] if 'Iron Cobra' in file
                              else action.split('.')[1]).strip()
                
                kind = ('weapon' if any(x in action for x in ['weapon:_', 'weapon attack:_'])
                        else 'spell' if any(x in action for x in ['spell:_', 'spell attack:_'])
                        else 'ability')
                
                reach = re.search('reach(.+?),', action).group(1).strip() if re.search('reach(.+?),', action) else np.nan
                
                recharge = re.search('recharge(.+?)\)', action).group(1).strip() if re.search('recharge(.+?)\)', action) else np.nan
                
                try:
                    recharge = recharge.replace('s after a', '').strip()
                except AttributeError:
                    pass
                    
                
                if re.search(':_(.+?)to hit', action) and re.search(' dc(.+?) sav', action):
                    hit, save = re.search(':_(.+?)to hit', action).group(1), re.search(' dc(.+?) sav', action).group(1)
                    hit_loc, save_loc = action.find('to hit'), action.find(' sav')
                    
                    against_primary = 'ac' if hit_loc < save_loc else save.split()[1].strip()
                    against_secondary = 'ac' if hit_loc > save_loc else save.split()[1].strip()
                    
                    save = save.split()[0].replace('l', '1').replace(',', '').replace(')', '')
                    
                    dmg_roll = re.findall('\((.+?)\)', action)
                    dmg_roll = [attack for attack in dmg_roll 
                                if 'd' in attack and 'y' not in attack and 'dc' not in attack and len(attack) < 11
                                and any(x in attack for x in ['1', '2', '3', '4', '5', '6', '7', '8', '9'])]
                    
                    dmg = [die_mean(roll) for roll in dmg_roll]
                    
                    impact = [(condition, action.find(condition)) for condition in condition_list if condition in action]
                    impact.sort(key=lambda x: x[1])
                    impact = [condition[0] for condition in impact]
                    
                    style = [(damage_type, action.find(damage_type)) for damage_type in damage_types if damage_type in action]
                    style.sort(key=lambda x: x[1])
                    style = [damage_type[0] for damage_type in style]
                    
                    atk = atk.append({'monster': file.replace('.txt', '').strip(),
                                      'name': name, 'type': kind, 'range': reach, 'recharge': recharge,
                                      'save': int(save), 'hit': hit,
                                      'dmg_primary': dmg[0] if len(dmg) > 0 else np.nan, 
                                      'roll_primary': dmg_roll[0] if len(dmg_roll) > 0 else np.nan, 
                                      'type_primary': style[0] if len(style) > 0 else np.nan,
                                      'against_primary': against_primary,
                                      'dmg_secondary': dmg[1] if len(dmg) > 1 else np.nan,
                                      'roll_secondary': dmg_roll[1] if len(dmg_roll) > 1 else np.nan,
                                      'type_secondary': style[1] if len(style) > 1 else np.nan,
                                      'against_secondary': against_secondary,
                                      'condition1': impact[0] if len(impact) > 0 else np.nan,
                                      'condition2': impact[1] if len(impact) > 1 else np.nan,
                                      'condition3': impact[2] if len(impact) > 2 else np.nan,
                                      'condition4': impact[3] if len(impact) > 3 else np.nan,
                                      'text': ''.join(action.split('.')[1:]).strip()},
                                     ignore_index=True)
                    
                    
                
                elif re.search(':_(.+?)to hit', action):
                    hit = re.search(':_(.+?)to hit', action).group(1)
                    hit = int(hit.replace('+', '').strip())
                    against = 'ac'
                    
                    dmg_roll = re.findall('\((.+?)\)', action)
                    dmg_roll = [attack for attack in dmg_roll 
                                if 'd' in attack and 'y' not in attack and 'dc' not in attack and len(attack) < 11
                                and any(x in attack for x in ['1', '2', '3', '4', '5', '6', '7', '8', '9'])]
                    
                    dmg = [die_mean(roll) for roll in dmg_roll]
                    
                    impact = [(condition, action.find(condition)) for condition in condition_list if condition in action]
                    impact.sort(key=lambda x: x[1])
                    impact = [condition[0] for condition in impact]
                    
                    style = [(damage_type, action.find(damage_type)) for damage_type in damage_types if damage_type in action]
                    style.sort(key=lambda x: x[1])
                    style = [damage_type[0] for damage_type in style]
                    
                    atk = atk.append({'monster': file.replace('.txt', '').strip(),
                                      'name': name, 'type': kind, 'range': reach, 'recharge': recharge,
                                      'save': np.nan, 'hit': hit,
                                      'dmg_primary': dmg[0] if len(dmg) > 0 else np.nan, 
                                      'roll_primary': dmg_roll[0] if len(dmg_roll) > 0 else np.nan, 
                                      'type_primary': style[0] if len(style) > 0 else np.nan,
                                      'against_primary': against,
                                      'dmg_secondary': dmg[1] if len(dmg) > 1 else np.nan,
                                      'roll_secondary': dmg_roll[1] if len(dmg_roll) > 1 else np.nan,
                                      'type_secondary': style[1] if len(style) > 1 else np.nan,
                                      'against_secondary': against if len(dmg_roll) > 1 else np.nan,
                                      'condition1': impact[0] if len(impact) > 0 else 'No Condition',
                                      'condition2': impact[1] if len(impact) > 1 else 'No Condition',
                                      'condition3': impact[2] if len(impact) > 2 else 'No Condition',
                                      'condition4': impact[3] if len(impact) > 3 else 'No Condition',
                                      'text': ''.join(action.split('.')[1:]).strip()},
                                     ignore_index=True)
                    
                elif re.search(' dc(.+?) sav', action):
                    hit = re.search(' dc(.+?) sav', action).group(1)
                    against = hit.split()[1].strip()
                    hit = int(hit.split()[0].replace('l', '1'))
                    
                    dmg_roll = re.findall('\((.+?)\)', action)
                    dmg_roll = [attack for attack in dmg_roll 
                                if 'd' in attack and 'y' not in attack and 'dc' not in attack and len(attack) < 11
                                and any(x in attack for x in ['1', '2', '3', '4', '5', '6', '7', '8', '9'])]
                    
                    dmg = [die_mean(roll) for roll in dmg_roll]
                    
                    impact = [(condition, action.find(condition)) for condition in condition_list if condition in action]
                    impact.sort(key=lambda x: x[1])
                    impact = [condition[0] for condition in impact]
                    
                    style = [(damage_type, action.find(damage_type)) for damage_type in damage_types if damage_type in action]
                    style.sort(key=lambda x: x[1])
                    style = [damage_type[0] for damage_type in style]
                    
                    atk = atk.append({'monster': file.replace('.txt', '').strip(),
                                      'name': name, 'type': kind, 'range': reach, 'recharge': recharge,
                                      'save': hit, 'hit': np.nan,
                                      'dmg_primary': dmg[0] if len(dmg) > 0 else np.nan, 
                                      'roll_primary': dmg_roll[0] if len(dmg_roll) > 0 else np.nan, 
                                      'type_primary': style[0] if len(style) > 0 else np.nan,
                                      'against_primary': against,
                                      'dmg_secondary': dmg[1] if len(dmg) > 1 else np.nan,
                                      'roll_secondary': dmg_roll[1] if len(dmg_roll) > 1 else np.nan,
                                      'type_secondary': style[1] if len(style) > 1 else np.nan,
                                      'against_secondary': against if len(dmg_roll) > 1 else np.nan,
                                      'condition1': impact[0] if len(impact) > 0 else 'No Condition',
                                      'condition2': impact[1] if len(impact) > 1 else 'No Condition',
                                      'condition3': impact[2] if len(impact) > 2 else 'No Condition',
                                      'condition4': impact[3] if len(impact) > 3 else 'No Condition',
                                      'text': ''.join(action.split('.')[1:]).strip()},
                                     ignore_index=True)
                    
                else:
                    abilities = abilities.append({'monster': file.replace('.txt', '').strip(),
                                                  'name': name, 'recharge': recharge, 
                                                  'text': ''.join(action.split('.')[1:]).strip()}, 
                                                 ignore_index=True)
                
                
abilities.loc[abilities.name == '', 'name'] = 'summon yugoloth'
abilities = abilities.loc[abilities.monster != 'Cultist of Tharizdun']

stats.loc[stats.monster == 'Beholder', 'multiattack'] = abilities.loc[abilities.monster == 'Beholder', 'text'].item()
stats.loc[stats.monster == 'Death Tyrant', 'multiattack'] = abilities.loc[abilities.monster == 'Death Tyrant', 'text'].item()
stats.loc[stats.monster == 'Gauth', 'multiattack'] = abilities.loc[abilities.monster == 'Gauth', 'text'].item()
stats.loc[stats.monster == 'Gazer', 'multiattack'] = abilities.loc[abilities.monster == 'Gazer', 'text'].item()
stats.loc[stats.monster == 'Mindwitness', 'multiattack'] = abilities.loc[abilities.monster == 'Mindwitness', 'text'].item()
stats.loc[stats.monster == 'Spectator', 'multiattack'] = abilities.loc[(abilities.monster == 'Spectator') & (abilities.name.str.contains('eye')), 'text'].item()
stats = stats.loc[stats.monster.notnull()]
stats.cr_numeric = [float(Fraction(cr)) for cr in stats.challenge_rating if type(cr) != int]


abilities = abilities.loc[~abilities.name.str.contains('eye rays')]
abilities.name = abilities.name.str.replace('\(', '')
abilities.name = abilities.name.str.replace('variant: ', '')

atk.hit = [int(h.replace('+', '').strip()) if '+' in str(h) else h for h in atk.hit]
atk.loc[atk.name.str.contains('flare'), 'name'] = 'lightning flare'
atk.loc[(atk.monster == 'Orthon') & (atk.text.str.contains('radiant')), 'name'] = 'blindness'
atk.loc[(atk.monster == 'Orthon') & (atk.text.str.contains('lightning')), 'name'] = 'paralysis'
atk.name = atk.name.str.replace('\(', '')


conn_str = (
    r'Driver={SQL Server};'
    r'Server=ZANGORTH\HOMEBASE;'
    r'Database=DND;'
    r'Trusted_Connection=yes;'
)
con = urllib.parse.quote_plus(conn_str)

engine = create_engine(f'mssql+pyodbc:///?odbc_connect={con}')

abilities.to_sql(name='abilities', con=engine, schema='monsters', if_exists='replace', index=False)
atk.to_sql(name='attack', con=engine, schema='monsters', if_exists='replace', index=False)
cond.to_sql(name='condition', con=engine, schema='monsters', if_exists='replace', index=False)
imm.to_sql(name='immunity', con=engine, schema='monsters', if_exists='replace', index=False)
res.to_sql(name='resistance', con=engine, schema='monsters', if_exists='replace', index=False)
stats.to_sql(name='stats', con=engine, schema='monsters', if_exists='replace', index=False)
            
        
=======
from sqlalchemy import create_engine
from fractions import Fraction
import pandas as pd
import numpy as np
import urllib
import re
import os

os.chdir(r'C:\Users\Samuel\Google Drive\DnD\Data')

def die_mean(dmg_roll):
    if '-' in dmg_roll:
        modifier = -1*int(dmg_roll.split('-')[1])
        dmg_roll = dmg_roll.split('-')[0]
        count, die = int(dmg_roll.split('d')[0]), int(dmg_roll.split('d')[1])
    elif '+' in dmg_roll:
        modifier = int(dmg_roll.split('+')[1])
        dmg_roll = dmg_roll.split('+')[0]
        count, die = int(dmg_roll.split('d')[0]), int(dmg_roll.split('d')[1])
        
    else:
        count, die = int(dmg_roll.split('d')[0]), int(dmg_roll.split('d')[1])
        modifier = 0
    
    return ((die+1)/2)*count + modifier


files = os.listdir('Monsters')
damage_types = ['slashing', 'piercing', 'bludgeoning', 'poison', 'acid', 
                'fire', 'cold', 'radiant', 'necrotic', 'lightning', 
                'thunder', 'force', 'psychic']

condition_list = ['blinded', 'charmed', 'exhaustion', 'frightened',
                  'paralyzed', 'petrified', 'poisoned', 'prone', 
                  'deafened', 'grappled', 'restrained', 'stunned', 
                  'unconscious']

stat_cols = ['monster', 'challenge_rating', 'cr_numeric', 'size', 'race', 'subrace', 
             'armor', 'armor_type', 'hit_points', 'hit_die', 'str', 'dex', 'con', 'int', 
             'wis', 'cha', 'str_save', 'dex_save', 'con_save', 'int_save', 'wis_save', 
             'cha_save', 'multiattack']

stats = pd.DataFrame(index=range(len(files)), columns=stat_cols)

res = pd.DataFrame(index=range(0), columns=['monster', 'resistance'])
imm = pd.DataFrame(index=range(0), columns=['monster', 'immunity'])
cond = pd.DataFrame(index=range(0), columns=['monster', 'condition'])
atk = pd.DataFrame(index=range(0), columns=['monster', 'name', 'type', 'range', 'recharge', 'hit', 'save',
                                            'dmg_primary', 'roll_primary', 'type_primary', 'against_primary',
                                            'dmg_secondary', 'roll_secondary', 'type_secondary', 'against_secondary',
                                            'condition1', 'condition2', 'condition3', 'condition4', 'text'])
abilities = pd.DataFrame(index=range(0), columns=['monster', 'name', 'recharge', 'text'])

i = -1
for file in [file for file in files if 'template' not in file.lower()]:
    i += 1
    stats.loc[stats.index==i, 'monster'] = file.replace('.txt', '').strip()
    
    monster = open(f'Monsters\{file}', 'r', encoding='utf8').read()
    monster = monster[monster.find('Attribute List]'):
                      monster.find('[View All Monsters')]
    
    search = file.replace(".txt", "").strip().replace('(', '\(')
    search = search.replace(')', '\)')
    
    cr = re.search('Challenge (.+?)\(', monster).group(1).strip()
    stats.loc[stats.index==i, 'challenge_rating'] = cr
    
    size = re.search(f'{search}\\n\\n(.+?),', monster).group(1)
    size = size.split()
    stats.loc[stats.index==i, 'size'] = size[0].lower()
    stats.loc[stats.index==i, 'race'] = size[1].lower()
    stats.loc[stats.index==i, 'subrace'] = (size[2].replace('(', '').replace(')', '').lower() if len(size) > 2 else np.nan)
    
    armor = re.search('Armor Class (.+?)\\n', monster).group(1)
    armor = armor.split('(') if '(' in armor else armor.split()
    stats.loc[stats.index==i, 'armor'] = int(armor[0])
    stats.loc[stats.index==i, 'armor_type'] = (armor[1].replace('(', '').replace(')', '').lower()
                                               if len(armor) > 1 else np.nan)
    
    hp = re.search('Hit Points (.+?)\n', monster).group(1)
    hp = hp.split('(')
    stats.loc[stats.index==i, 'hit_points'] = int(hp[0])
    stats.loc[stats.index==i, 'hit_die'] = (hp[1].replace(')', '') if len(hp) > 1 else np.nan)
    
    strength = monster[monster.find('Hit Points'):]
    strength = strength[strength.find('\n\nSTR'):strength.find('\n\nDEX')]
    strength = int(re.search('\((.+?)\)', strength).group(1))
    stats.loc[stats.index==i, ['str', 'str_save']] = strength
    
    dex = monster[monster.find('Hit Points'):]
    dex = dex[dex.find('\n\nDEX'):dex.find('\n\nCON')]
    dex = int(re.search('\((.+?)\)', dex).group(1))
    stats.loc[stats.index==i, ['dex', 'dex_save']] = dex
    
    con = monster[monster.find('Hit Points'):]
    con = con[con.find('\n\nCON'):con.find('\n\nINT')]
    con = int(re.search('\((.+?)\)', con).group(1))
    stats.loc[stats.index==i, ['con', 'con_save']] = con
    
    intel = monster[monster.find('Hit Points'):]
    intel = intel[intel.find('\n\nINT'):intel.find('\n\nWIS')]
    intel = int(re.search('\((.+?)\)', intel).group(1))
    stats.loc[stats.index==i, ['int', 'int_save']] = intel
    
    wis = monster[monster.find('Hit Points'):]
    wis = wis[wis.find('\n\nWIS'):wis.find('\n\nCHA')]
    wis = int(re.search('\((.+?)\)', wis).group(1))
    stats.loc[stats.index==i, ['wis', 'wis_save']] = wis
    
    cha = monster[monster.find('Hit Points'):]
    cha = cha[cha.find('\n\nCHA'):cha.find('\n\n  *')]
    cha = int(re.search('\((.+?)\)', cha).group(1))
    stats.loc[stats.index==i, ['cha', 'cha_save']] = cha
    
    try:
        saves = re.search('Saving Throws\\n\\n(.+?)\\n\\n', monster).group(1)
        saves = saves.split(',')
        saves = [save.lower() if 'Char' not in save else save.replace('Char', 'cha').lower() for save in saves]
    except AttributeError:
        saves = []
        
    for save in ['str', 'dex', 'con', 'int', 'wis', 'cha']:
        for throw in saves:
            if save in throw:
                stats.loc[stats.index==i, f'{save}_save'] = (-1 * int(''.join(x for x in throw if x.isdigit())) if '-' in throw
                                                             else int(''.join(x for x in throw if x.isdigit())))
            
    try:
        resistance = re.search('Damage Resistance (.+?)\\n', monster).group(1)
    except AttributeError:
        resistance = ''
    
    try:
        immunity = re.search('Damage Immunities (.+?)\\n', monster).group(1)
    except AttributeError:
        immunity = ''
        
    try:
        conditions = re.search('Condition Immunities (.+?)\\n', monster).group(1)
    except AttributeError:
        conditions = ''
        
        
    for damage_type in damage_types:
        if damage_type in resistance.lower():
            res = res.append({'monster': file.replace('.txt', '').strip(), 'resistance': damage_type}, ignore_index=True)
            
        if damage_type in immunity.lower():
            imm = imm.append({'monster': file.replace('.txt', '').strip(), 'immunity': damage_type}, ignore_index=True)
            
    for condition in condition_list:
        if condition in conditions:
            cond = cond.append({'monster': file.replace('.txt', '').strip(), 'condition': condition}, ignore_index=True)
        
    actions = monster[monster.find('## Actions')+10:]
    actions = actions[:actions.find('##')]
    actions = actions.split('*')
    actions = [action.strip().lower() for action in actions if len(action) > 10]
    
    if len(actions) > 0:
        for action in actions:
            if 'multiattack' in action:
                stats.loc[stats.index==i, 'multiattack'] = action.replace('multiattack.', '').strip()
                
            else:
                name = re.sub('\([^>]+\)', '', 
                              action.split('.')[0] if '\\' not in action 
                              else action.split('.')[0] if 'gaze. demogorgon' in action
                              else action.split('.')[0] if 'Iron Cobra' in file
                              else action.split('.')[1]).strip()
                
                kind = ('weapon' if any(x in action for x in ['weapon:_', 'weapon attack:_'])
                        else 'spell' if any(x in action for x in ['spell:_', 'spell attack:_'])
                        else 'ability')
                
                reach = re.search('reach(.+?),', action).group(1).strip() if re.search('reach(.+?),', action) else np.nan
                
                recharge = re.search('recharge(.+?)\)', action).group(1).strip() if re.search('recharge(.+?)\)', action) else np.nan
                
                try:
                    recharge = recharge.replace('s after a', '').strip()
                except AttributeError:
                    pass
                    
                
                if re.search(':_(.+?)to hit', action) and re.search(' dc(.+?) sav', action):
                    hit, save = re.search(':_(.+?)to hit', action).group(1), re.search(' dc(.+?) sav', action).group(1)
                    hit_loc, save_loc = action.find('to hit'), action.find(' sav')
                    
                    against_primary = 'ac' if hit_loc < save_loc else save.split()[1].strip()
                    against_secondary = 'ac' if hit_loc > save_loc else save.split()[1].strip()
                    
                    save = save.split()[0].replace('l', '1').replace(',', '').replace(')', '')
                    
                    dmg_roll = re.findall('\((.+?)\)', action)
                    dmg_roll = [attack for attack in dmg_roll 
                                if 'd' in attack and 'y' not in attack and 'dc' not in attack and len(attack) < 11
                                and any(x in attack for x in ['1', '2', '3', '4', '5', '6', '7', '8', '9'])]
                    
                    dmg = [die_mean(roll) for roll in dmg_roll]
                    
                    impact = [(condition, action.find(condition)) for condition in condition_list if condition in action]
                    impact.sort(key=lambda x: x[1])
                    impact = [condition[0] for condition in impact]
                    
                    style = [(damage_type, action.find(damage_type)) for damage_type in damage_types if damage_type in action]
                    style.sort(key=lambda x: x[1])
                    style = [damage_type[0] for damage_type in style]
                    
                    atk = atk.append({'monster': file.replace('.txt', '').strip(),
                                      'name': name, 'type': kind, 'range': reach, 'recharge': recharge,
                                      'save': int(save), 'hit': hit,
                                      'dmg_primary': dmg[0] if len(dmg) > 0 else np.nan, 
                                      'roll_primary': dmg_roll[0] if len(dmg_roll) > 0 else np.nan, 
                                      'type_primary': style[0] if len(style) > 0 else np.nan,
                                      'against_primary': against_primary,
                                      'dmg_secondary': dmg[1] if len(dmg) > 1 else np.nan,
                                      'roll_secondary': dmg_roll[1] if len(dmg_roll) > 1 else np.nan,
                                      'type_secondary': style[1] if len(style) > 1 else np.nan,
                                      'against_secondary': against_secondary,
                                      'condition1': impact[0] if len(impact) > 0 else np.nan,
                                      'condition2': impact[1] if len(impact) > 1 else np.nan,
                                      'condition3': impact[2] if len(impact) > 2 else np.nan,
                                      'condition4': impact[3] if len(impact) > 3 else np.nan,
                                      'text': ''.join(action.split('.')[1:]).strip()},
                                     ignore_index=True)
                    
                    
                
                elif re.search(':_(.+?)to hit', action):
                    hit = re.search(':_(.+?)to hit', action).group(1)
                    hit = int(hit.replace('+', '').strip())
                    against = 'ac'
                    
                    dmg_roll = re.findall('\((.+?)\)', action)
                    dmg_roll = [attack for attack in dmg_roll 
                                if 'd' in attack and 'y' not in attack and 'dc' not in attack and len(attack) < 11
                                and any(x in attack for x in ['1', '2', '3', '4', '5', '6', '7', '8', '9'])]
                    
                    dmg = [die_mean(roll) for roll in dmg_roll]
                    
                    impact = [(condition, action.find(condition)) for condition in condition_list if condition in action]
                    impact.sort(key=lambda x: x[1])
                    impact = [condition[0] for condition in impact]
                    
                    style = [(damage_type, action.find(damage_type)) for damage_type in damage_types if damage_type in action]
                    style.sort(key=lambda x: x[1])
                    style = [damage_type[0] for damage_type in style]
                    
                    atk = atk.append({'monster': file.replace('.txt', '').strip(),
                                      'name': name, 'type': kind, 'range': reach, 'recharge': recharge,
                                      'save': np.nan, 'hit': hit,
                                      'dmg_primary': dmg[0] if len(dmg) > 0 else np.nan, 
                                      'roll_primary': dmg_roll[0] if len(dmg_roll) > 0 else np.nan, 
                                      'type_primary': style[0] if len(style) > 0 else np.nan,
                                      'against_primary': against,
                                      'dmg_secondary': dmg[1] if len(dmg) > 1 else np.nan,
                                      'roll_secondary': dmg_roll[1] if len(dmg_roll) > 1 else np.nan,
                                      'type_secondary': style[1] if len(style) > 1 else np.nan,
                                      'against_secondary': against if len(dmg_roll) > 1 else np.nan,
                                      'condition1': impact[0] if len(impact) > 0 else 'No Condition',
                                      'condition2': impact[1] if len(impact) > 1 else 'No Condition',
                                      'condition3': impact[2] if len(impact) > 2 else 'No Condition',
                                      'condition4': impact[3] if len(impact) > 3 else 'No Condition',
                                      'text': ''.join(action.split('.')[1:]).strip()},
                                     ignore_index=True)
                    
                elif re.search(' dc(.+?) sav', action):
                    hit = re.search(' dc(.+?) sav', action).group(1)
                    against = hit.split()[1].strip()
                    hit = int(hit.split()[0].replace('l', '1'))
                    
                    dmg_roll = re.findall('\((.+?)\)', action)
                    dmg_roll = [attack for attack in dmg_roll 
                                if 'd' in attack and 'y' not in attack and 'dc' not in attack and len(attack) < 11
                                and any(x in attack for x in ['1', '2', '3', '4', '5', '6', '7', '8', '9'])]
                    
                    dmg = [die_mean(roll) for roll in dmg_roll]
                    
                    impact = [(condition, action.find(condition)) for condition in condition_list if condition in action]
                    impact.sort(key=lambda x: x[1])
                    impact = [condition[0] for condition in impact]
                    
                    style = [(damage_type, action.find(damage_type)) for damage_type in damage_types if damage_type in action]
                    style.sort(key=lambda x: x[1])
                    style = [damage_type[0] for damage_type in style]
                    
                    atk = atk.append({'monster': file.replace('.txt', '').strip(),
                                      'name': name, 'type': kind, 'range': reach, 'recharge': recharge,
                                      'save': hit, 'hit': np.nan,
                                      'dmg_primary': dmg[0] if len(dmg) > 0 else np.nan, 
                                      'roll_primary': dmg_roll[0] if len(dmg_roll) > 0 else np.nan, 
                                      'type_primary': style[0] if len(style) > 0 else np.nan,
                                      'against_primary': against,
                                      'dmg_secondary': dmg[1] if len(dmg) > 1 else np.nan,
                                      'roll_secondary': dmg_roll[1] if len(dmg_roll) > 1 else np.nan,
                                      'type_secondary': style[1] if len(style) > 1 else np.nan,
                                      'against_secondary': against if len(dmg_roll) > 1 else np.nan,
                                      'condition1': impact[0] if len(impact) > 0 else 'No Condition',
                                      'condition2': impact[1] if len(impact) > 1 else 'No Condition',
                                      'condition3': impact[2] if len(impact) > 2 else 'No Condition',
                                      'condition4': impact[3] if len(impact) > 3 else 'No Condition',
                                      'text': ''.join(action.split('.')[1:]).strip()},
                                     ignore_index=True)
                    
                else:
                    abilities = abilities.append({'monster': file.replace('.txt', '').strip(),
                                                  'name': name, 'recharge': recharge, 
                                                  'text': ''.join(action.split('.')[1:]).strip()}, 
                                                 ignore_index=True)
                
                
abilities.loc[abilities.name == '', 'name'] = 'summon yugoloth'
abilities = abilities.loc[abilities.monster != 'Cultist of Tharizdun']

stats.loc[stats.monster == 'Beholder', 'multiattack'] = abilities.loc[abilities.monster == 'Beholder', 'text'].item()
stats.loc[stats.monster == 'Death Tyrant', 'multiattack'] = abilities.loc[abilities.monster == 'Death Tyrant', 'text'].item()
stats.loc[stats.monster == 'Gauth', 'multiattack'] = abilities.loc[abilities.monster == 'Gauth', 'text'].item()
stats.loc[stats.monster == 'Gazer', 'multiattack'] = abilities.loc[abilities.monster == 'Gazer', 'text'].item()
stats.loc[stats.monster == 'Mindwitness', 'multiattack'] = abilities.loc[abilities.monster == 'Mindwitness', 'text'].item()
stats.loc[stats.monster == 'Spectator', 'multiattack'] = abilities.loc[(abilities.monster == 'Spectator') & (abilities.name.str.contains('eye')), 'text'].item()
stats = stats.loc[stats.monster.notnull()]
stats.cr_numeric = [float(Fraction(cr)) for cr in stats.challenge_rating if type(cr) != int]


abilities = abilities.loc[~abilities.name.str.contains('eye rays')]
abilities.name = abilities.name.str.replace('\(', '')
abilities.name = abilities.name.str.replace('variant: ', '')

atk.hit = [int(h.replace('+', '').strip()) if '+' in str(h) else h for h in atk.hit]
atk.loc[atk.name.str.contains('flare'), 'name'] = 'lightning flare'
atk.loc[(atk.monster == 'Orthon') & (atk.text.str.contains('radiant')), 'name'] = 'blindness'
atk.loc[(atk.monster == 'Orthon') & (atk.text.str.contains('lightning')), 'name'] = 'paralysis'
atk.name = atk.name.str.replace('\(', '')


conn_str = (
    r'Driver={SQL Server};'
    r'Server=ZANGORTH\HOMEBASE;'
    r'Database=DND;'
    r'Trusted_Connection=yes;'
)
con = urllib.parse.quote_plus(conn_str)

engine = create_engine(f'mssql+pyodbc:///?odbc_connect={con}')

abilities.to_sql(name='abilities', con=engine, schema='monsters', if_exists='replace', index=False)
atk.to_sql(name='attack', con=engine, schema='monsters', if_exists='replace', index=False)
cond.to_sql(name='condition', con=engine, schema='monsters', if_exists='replace', index=False)
imm.to_sql(name='immunity', con=engine, schema='monsters', if_exists='replace', index=False)
res.to_sql(name='resistance', con=engine, schema='monsters', if_exists='replace', index=False)
stats.to_sql(name='stats', con=engine, schema='monsters', if_exists='replace', index=False)
    