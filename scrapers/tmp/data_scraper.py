from pycentral.base import ArubaCentralBase
from pycentral.configuration import Groups
from pycentral.configuration import Variables
from pycentral.configuration import Devices
from pycentral.configuration import Templates
import yaml,os,getpass
from pprint import pprint
from time import gmtime, strftime

def set_central_info (url_file_loc):
    """ Set Central Data return data """
    url_info = {}
    central_info_func = {}
    try:
        with open(url_file_loc, "r") as fileinfo:
            url_info = yaml.safe_load(fileinfo.read())
    except Exception as err:
        print("Error: ",str(err))
    access_token_raw = getpass.getpass("Please provide the auth token: ")
    access_token = {'access_token': access_token_raw }
    central_info_func = url_info['central_info']
    central_info_func['token'] = access_token
    central_customer = url_info['central_customer']
    return central_info_func, central_customer

def get_all_groups (central):
    """ Get all groups and return a flattened group list """
    # set initial vars
    print ("Getting groups")
    limit = 20
    g = Groups()
    full_group_list = []

    # loop through call to get groups appending groups to full group list
    # stop when response is empty
    counter = 0
    need_more = True

    while need_more:
        response = g.get_groups(central,offset=counter,limit=limit)
        if response['msg']['data'] != []:
            full_group_list = full_group_list + response['msg']['data']
        elif response['msg']['data'] == []:
            need_more = False
            break
        else:
            print("ERROR")
            need_more = False
            print(response)
            break
        counter = counter + limit
        print(counter)
    full_group_list_flat = [item for sublist in full_group_list for item in sublist]
    return full_group_list_flat

def get_all_variables (central):
    """ Return a full list of variables for all devices """
    print ("Getting Variables - Will Take Some time")
    # set initial vars
    limit = 20
    v = Variables()
    full_variable_dict = {}

    # loop through call to get groups appending groups to full group list
    # stop when response is empty
    counter = 0
    need_more = True

    while need_more:
        response = v.get_all_template_variables(central,offset=counter,limit=limit)
        if response['msg'] != {}:
            full_variable_dict.update(response['msg'])
        elif response['msg'] == {}:
            need_more = False
            break
        else:
            print("ERROR")
            need_more = False
            print(response)
            break
        counter = counter + limit
        print(counter)
    return full_variable_dict

def get_dev_to_template (central):
    """Return the device to template mapping."""
    # set initial vars
    limit = 20
    d = Devices()
    dev_to_template_dict = {}
    device_types = ["CX", "IAP"]

    for device in device_types:
        print ("Getting all "+device+" to Templates mapping")
        # stop when response is empty
        counter = 0
        need_more = True
        while need_more:
            response = d.get_devices_group_templates(central, device_type=device,
                                                    all_groups='true', offset=counter,
                                                    limit=limit)
            if response['msg']['data'] != {}:
                dev_to_template_dict.update(response['msg']['data'])
            elif response['msg']['data'] == {}:
                need_more = False
                break
            else:
                print("ERROR")
                need_more = False
                print(response)
                break
            counter = counter + limit
            print(counter)
    return dev_to_template_dict

def get_group_to_template (central, group_list):
    """Return group to template mapping."""
    print ("Getting Group to Template Mapping")
    # set initial vars
    t = Templates()
    group_to_template_dict = {}

    # loop over group list and get templates in each group - add to group_to_template_dict
    for gp in group_list:
        print (gp)
        response = t.get_template(central,group_name=gp)
        if response['code'] == 404:
            group_to_template_dict[gp]='none'
        elif response['code'] == 200:
            group_to_template_dict[gp]=response['msg']['data']
        else:
            group_to_template_dict[gp]='none'
    return group_to_template_dict 

def main():
    """ Main function to scrape data """
    # get auth info
    url_file_loc = "central_url_info.yml"
    file_info = set_central_info(url_file_loc)
    central_info = file_info[0]
    central_customer = file_info[1]
    ssl_verify=True

    # set Central data
    central = ArubaCentralBase(central_info=central_info, ssl_verify=ssl_verify)
    
    # Get dump directory to store data
    tstamp=strftime("%Y-%m-%d_%H_%M_%S", gmtime())
    directory= 'scraped_data/'+central_customer+'/'+tstamp
    os.makedirs(directory)    

    # get list of all groups
    group_list = get_all_groups (central)

    # Dump group list to file
    output_name = 'group_list.yml'
    with open(directory+'/'+output_name, 'w', encoding='utf8') as f:
        yaml.dump(group_list, f, sort_keys=False,
                    default_flow_style=False)    

    # get all device variables - this call takes some time
    variable_dict = get_all_variables (central)
    
    # Dump variable data to file
    output_name = 'variable_dict.yml'
    with open(directory+'/'+output_name, 'w', encoding='utf8') as f:
        yaml.dump(variable_dict, f, sort_keys=False,
                    default_flow_style=False)

    # get mapping of cx devices to group and template
    device_to_template_dict = get_dev_to_template(central)
    # Dump device_to_template_dict data to file
    output_name = 'device_to_template_dict.yml'
    with open(directory+'/'+output_name, 'w', encoding='utf8') as f:
        yaml.dump(device_to_template_dict, f, sort_keys=False,
                    default_flow_style=False)

    # get templates of each group
    group_to_template_dict = get_group_to_template(central,group_list)
    # Dump group_to_template_dict data to file
    output_name = 'group_to_template_dict.yml'
    with open(directory+'/'+output_name, 'w', encoding='utf8') as f:
        yaml.dump(group_to_template_dict, f, sort_keys=False,
                    default_flow_style=False)    

    # # merge data into one dictionary for data dump
    # dump_list = ['group_to_template_dict', 'device_to_template_dict','variable_dict','group_list']
    # all_data={}
    # all_data[central_customer]={}
    # all_data[central_customer]['group_to_template_dict'] = group_to_template_dict
    # all_data[central_customer]['device_to_template_dict'] = device_to_template_dict
    # all_data[central_customer]['variable_dict'] = variable_dict
    # all_data[central_customer]['group_list'] = group_list

    # # Create data dumps
    # os.makedirs(directory)
    # for item in dump_list:
    #     output_name = item+'.yml'
    #     with open(directory+'/'+output_name, 'w', encoding='utf8') as f:
    #         yaml.dump(all_data[central_customer][item], f, sort_keys=False,
    #                   default_flow_style=False)
    #         pprint (all_data[central_customer][item])

if __name__ == "__main__":
    main()
   
