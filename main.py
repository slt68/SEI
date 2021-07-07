import requests
import json

import pandas as pd


def execute_get_request(request):
    """
    Simple function to execute get requests
    :param request: url of the target endpoint, since these are gets no data is required
    :return: response obj
    """
    headers = {
        'Content-Type': 'application/json'
    }
    file = requests.get(request, headers=headers, auth=('admin', 'admin'))
    if file.status_code in [200, 201]:
        return json.loads(file.text)


def list_node_children(parent_id):
    """
    Given a parent_id list all of the children's ids
    :param parent_id:
    :return:
    """
    url = 'http://localhost:8080/alfresco/api/-default-/public/alfresco/versions/1/nodes/{}/children'.format(parent_id)
    resp = execute_get_request(url)

    if resp:
        return [x['entry']['id'] for x in resp['list']['entries']]
    else:
        print('Error finding folder with ID: {}'.format(parent_id))


def get_node_by_id(node_id):
    """
    Uses node_id to get folder or file with that id
    I couldn't get the token authorization working so I'm just going to use the auth field
    :param str node_id:
    :return dict containing name, title and description of file:
    """
    url = 'http://localhost:8080/alfresco/api/-default-/public/alfresco/versions/1/nodes/{}'.format(node_id)
    resp = execute_get_request(url)['entry']
    if resp:
        return {
            'name': resp['name'],
            'title': resp['properties']['cm:title'],
            'description': resp['properties']['cm:description']
        }
    else:
        print('Error finding file with ID: {}'.format(node_id))


def write_to_excel(metadata, path):
    """
    Build a pandas DataFrame from the metadata to easily write out to excel with path.
    :param metadata: list of metadata to be saved in excel
    :param path: path to save file at
    :return: None
    """
    metadata_df = pd.DataFrame.from_dict(metadata)
    metadata_df.to_excel(path)


if __name__ == '__main__':
    # get children of folder I created
    children_id = list_node_children('9bb42fa5-b72b-4547-adbd-6034d84e018b')
    data = []
    for child_id in children_id:
        data.append(get_node_by_id(child_id))
    write_to_excel(data, 'metadata.xlsx')
