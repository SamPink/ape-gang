def parse_ape_data(ape_dict):
    
    ape_id = ape_dict['token_id']
    
    try:
        creator_username = ape_dict['creator']['user']['username']
    except:
        creator_username = None
    try:
        creator_address = ape_dict['creator']['address']
    except:
        creator_address = None
    
    try:
        owner_username = ape_dict['owner']['user']['username']
    except:
        owner_username = None
    
    owner_address = ape_dict['owner']['address']
    
    traits = ape_dict['traits']
    num_sales = int(ape_dict['num_sales'])
        
    result = {'ape_id': ape_id,
              'creator_username': creator_username,
              'creator_address': creator_address,
              'owner_username': owner_username,
              'owner_address': owner_address,
              'traits': traits,
              'num_sales': num_sales}
    
    return result

