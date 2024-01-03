import requests
import pandas as pd

def team_look_up(player_id):
    api_url_template = "http://lookup-service-prod.mlb.com/json/named.player_teams.bam?&player_id=[player_id]&player_teams.col_in=team_id"

    api_url = api_url_template.replace("[player_id]", player_id.iloc[0])    
    response = requests.get(api_url)
    dict_list = response.json().get("player_teams").get("queryResults").get("row")
    
    return [d["team_id"] for d in dict_list if d["team_id"][0] == "1"]

def fetch_name(player_id):
    player_info_template = "http://lookup-service-prod.mlb.com/json/named.player_info.bam?sport_code='mlb'&player_id=[player_id]&player_info.col_in=name_display_first_last_html"
    api_url = player_info_template.replace("[player_id]", player_id.iloc[0])
    response = requests.get(api_url)
    dict_list = response.json().get("player_info").get("queryResults").get("row")

    return dict_list.get("name_display_first_last_html")


def main():
    team_id1 = input("Team ID 1: ")
    team_id2 = input("Team ID 2: ")

    api_url_template = "http://lookup-service-prod.mlb.com/json/named.roster_40.bam?team_id=[team_id1]&roster_40.col_in=player_id"

    api_url = api_url_template.replace("[team_id1]", team_id1)

    response = requests.get(api_url)
    df = pd.DataFrame
    if response.status_code == 200:
        if response.text:
            # print()
            massresponse = response.json().get("roster_40").get("queryResults").get("row")
            df = df.from_dict(massresponse, dtype=str)
            # df = df.from_dict()
            # print(df.to_string())
            df["Teams"] = df.apply(team_look_up, axis=1)
            # print(df.to_string())

            # print(df.to_string())
            # print(df['Teams'])
            filtered_df = df[df['Teams'].astype(str).str.contains(team_id2, na=False, case=False)]
            print(filtered_df.to_string())

            filtered_df['Name'] = filtered_df.apply(fetch_name, axis=1)
            print(filtered_df)

            

if __name__ == '__main__':
    main()
