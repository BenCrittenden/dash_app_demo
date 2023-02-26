import pandas as pd
import numpy as np
import json

mapbox_access_token = "enter-your-token-here"

party_abbreviations_dict = {
    "C": "Conservative",
    "Lab": "Labour",
    "LD": "Lib Dem",
    "Green": "Green",
    "Ind": "Independent",
    "DUP": "Democratic Unionist Party",
    "SF": "Sinn Fein",
    "SNP": "Scottish National Party",
    "PC": "Plaid Cymru",
}

party_renaming_dict = party_abbreviations_dict.copy()
del party_renaming_dict['Green']

with open('./data/parliamentary_boundaries.json') as f:
    geojson_data = json.load(f)
    
    
def clean_df(ge_df):
    
    ge_df = ge_df.loc[ge_df['Year']==2017]
    
    #remove the parties that didn't win a seat
    winning_parties = ge_df['Majority Party'].unique()
    ge_df = ge_df.loc[ge_df['Party Abbreviation'].isin(winning_parties)]
    
    #get the general information on each constituency and who won
    general_constituency_info = ge_df.drop_duplicates('Constituency', keep='first')
    general_constituency_info = general_constituency_info.drop(
        ['Party Abbreviation','Party','Candidate Votes','Share of Vote'],
        axis=1
    )
    
    df_votes = ge_df[['Code','Party Abbreviation','Candidate Votes']]
    df_votes = df_votes.pivot_table(
        index='Code', 
        columns='Party Abbreviation', 
        values='Candidate Votes', 
        aggfunc=max,
    ).fillna(0).reset_index()
    
    df_new = pd.merge(
        general_constituency_info,
        df_votes,
        how='outer',
        on='Code'
    )
    
    return df_new
    


def identify_the_winners(ge_df):
    ge_winners_df = ge_df['Majority Party'].value_counts().reset_index()
    ge_winners_df.columns = ['party','seats_won']
    ge_winners_df = ge_winners_df.replace({'party': party_renaming_dict})

    return ge_winners_df


def swing_to_new_party(ge_df, party_swings):

    new_votes = {}
    new_party = []
    for p in party_swings:
        
        new_votes[p] = ge_df[p] * (1-(party_swings[p]/100))
        new_party += [(ge_df[p] * (party_swings[p]/100)).values]
        
    
    new_votes_df = ge_df.copy()
    for p in new_votes:
        new_votes_df[p] = new_votes[p]
        
    new_votes_df["New"] = np.array(new_party).sum(axis=0)

    adjusted_winners_df = new_votes_df.iloc[:,8:].idxmax(axis=1).value_counts().reset_index()
    adjusted_winners_df.columns = ['party','seats_won']
    adjusted_winners_df = adjusted_winners_df.replace({'party': party_renaming_dict})

    return adjusted_winners_df
    
    
def recalculate_votes(ge_df, party_swings):

    new_votes = {}
    new_party = []
    for p in party_swings:
        
        new_votes[p] = ge_df[p] * (1-(party_swings[p]/100))
        new_party += [(ge_df[p] * (party_swings[p]/100)).values]
        
    
    new_votes_df = ge_df.copy()
    for p in new_votes:
        new_votes_df[p] = new_votes[p]
        
    new_votes_df["New"] = np.array(new_party).sum(axis=0)

    return new_votes_df



def make_party_json_list(ge_df,  party_swings):

    adjusted_winners_df = recalculate_votes(ge_df, party_swings)

    C_geojsons = {"type": "FeatureCollection", 
              "features": [],
              "class": 1}
    Lab_geojsons = {"type": "FeatureCollection", 
                "features": [],
                "class": 1}
    SNP_geojsons = {"type": "FeatureCollection", 
                "features": [],
                "class": 1}
    LD_geojsons = {"type": "FeatureCollection", 
                "features": [],
                "class": 1}
    Green_geojsons = {"type": "FeatureCollection", 
                "features": [],
                "class": 1}
    PC_geojsons = {"type": "FeatureCollection", 
                "features": [],
                "class": 1}
    New_geojsons = {"type": "FeatureCollection", 
                "features": [],
                "class": 1}
    other_geojsons = {"type": "FeatureCollection", 
                "features": [],
                "class": 1}

    for i in range(len(geojson_data['features'])):
        
        code = geojson_data['features'][i]['properties']['id']
        winning_party = adjusted_winners_df.loc[adjusted_winners_df['Code'] == code].iloc[:,8:].idxmax(axis=1).iloc[0]
        
        if winning_party == 'C':
            C_geojsons["features"] += [geojson_data['features'][i]]
        elif winning_party == 'Lab':
            Lab_geojsons["features"] += [geojson_data['features'][i]]
        elif winning_party == 'SNP':
            SNP_geojsons["features"] += [geojson_data['features'][i]]
        elif winning_party == 'LD':
            LD_geojsons["features"] += [geojson_data['features'][i]]
        elif winning_party == 'Green':
            Green_geojsons["features"] += [geojson_data['features'][i]]
        elif winning_party == 'PC':
            PC_geojsons["features"] += [geojson_data['features'][i]]
        elif winning_party == 'New':
            New_geojsons["features"] += [geojson_data['features'][i]]
        else:
            other_geojsons["features"] += [geojson_data['features'][i]]

    winners_geojson_list = [
        C_geojsons,
        Lab_geojsons,
        SNP_geojsons,
        LD_geojsons,
        Green_geojsons,
        PC_geojsons,
        New_geojsons,
        other_geojsons
    ]

    return winners_geojson_list

