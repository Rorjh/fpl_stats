import pandas as pd

def data_prep():
    # load datasets
    df_matchlogs = pd.read_csv('data/fbref_matchlogs.csv')
    df = pd.read_csv('data/gameweeks_fpl.csv')

    # fix columns
    df_matchlogs['code'].iloc[0] = 'code'
    df_matchlogs.iloc[0,30] += '_passes'
    df_matchlogs.iloc[0,35] += '_takeons'
    df_matchlogs.iloc[0,-8] += '_GK'
    df_matchlogs.iloc[0,-14] += '_Lounched'
    df_matchlogs.iloc[0,-15] += '_Lounched'
    df_matchlogs.iloc[0,-19] += '_GK'
    df_matchlogs.columns = df_matchlogs.iloc[0]
    df_matchlogs = df_matchlogs.drop(0)

    #change kickoff time to datetime format
    df['kickoff_time'] = pd.to_datetime(df['kickoff_time'])
    df['Date'] = df['kickoff_time'].dt.date
    df['Date'] = pd.to_datetime(df["Date"])
    df_matchlogs['Date'] = pd.to_datetime(df_matchlogs['Date'])

    # Drop first columns (index)
    df = df.drop("Unnamed: 0", axis=1)
    df_matchlogs = df_matchlogs.iloc[: , 1:]

    # merge datasets
    df = df.merge(df_matchlogs, on=['code', 'Date'], how='left')

    # drop rows with 0 minutes played
    df = df[df['minutes'] != 0]

    # drop incomplete records
    df.dropna(subset=['Start'], inplace=True)

    # drop irrelevant or duplicating features
    df.drop(['team', 'xP', 'element', 'fixture', 'Date', 'kickoff_time', 'opponent_team', 'round', 'selected', 'team_a_score', 'team_h_score','transfers_balance', 
            'transfers_in', 'transfers_out', 'code', 'expected_assists', 'expected_goal_involvements', 'expected_goals', 'expected_goals_conceded',
            'starts', 'Comp', 'Round', 'Venue', 'Result', 'Min', 'Gls', 'Ast', 'Match Report', 'Pos', 'Day'], axis=1, inplace=True)

    # fill NANs with 0s:
    df.fillna(0, inplace=True)

    # create rolling features:
    df['gw_points'] = df['total_points']
    rolling_features_sum = [
        'assists',
        'bonus',
        'bps',
        'clean_sheets',
        'goals_conceded',
        'goals_scored',
        'minutes',
        'own_goals',
        'penalties_missed',
        'penalties_saved',
        'red_cards',
        'saves',
        'total_points',
        'yellow_cards',
        'PK',
        'PKatt',
        'Sh',
        'SoT',
        'CrdY',
        'CrdR',
        'Touches',
        'Tkl',
        'Int',
        'Blocks',
        'xG',
        'npxG',
        'xAG',
        'SCA',
        'GCA',
        'Cmp',
        'PrgP',
        'Carries',
        'PrgC',
        'Succ',
        'SoTA',
        'GA',
        'Saves',
        'CS',
        'PSxG',
        'PKA',
        'PKsv',
        'PKm',
        'Att (GK)',
        'Thr',
        'Opp',
        'Stp',
        '#OPA',
        'Att_passes',
        'Att_takeons',
        'PKatt_GK',
        'Cmp_Lounched',
        'Att_Lounched',
        'Att_GK']

    rolling_features_mean = [
        'Cmp%',
        'Save%',
        'Launch%',
        'AvgLen',
        'Stp%',
        'AvgDist']

    for feature in rolling_features_sum:
        # print(feature, type(df[feature]))
        df.replace('On matchday squad, but did not play', 0, inplace=True)
        df[feature] = df[feature].astype(float)
        df[feature] = df.groupby('name')[feature].rolling(window=5, min_periods=1, closed='left').sum().reset_index(level=0, drop=True)

    for feature in rolling_features_mean:
    #     print(df[feature].dtype)
        df[feature] = df[feature].astype(float)
        df[feature] = df.groupby('name')[feature].rolling(window=5, min_periods=1, closed='left').mean().reset_index(level=0, drop=True)

    df.dropna(inplace=True)

    df['was_home'] = df['was_home'].astype(int)

    def categorical_to_dummies(df, feature):
        # get the dummies and store it in a variable
        dummies = pd.get_dummies(df[feature], prefix=feature)
        dummies = dummies.astype(int)
        
        # Concatenate the dummies to original dataframe
        merged = pd.concat([df, dummies], axis='columns')
        
        # drop the values
        merged.drop(feature, axis='columns', inplace=True)

        return merged

    # df = categorical_to_dummies(df, 'name')
    df = categorical_to_dummies(df, 'position')
    df = categorical_to_dummies(df, 'Squad')
    df = categorical_to_dummies(df, 'Opponent')

    df.drop('name', axis=1, inplace=True)
    df.Start = df.Start.replace({"Y":1, "Y*":1, "N":0})

    return df