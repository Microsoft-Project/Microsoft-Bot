import requests


def fetch_issue_data(repo_full_name):
    bug = requests.get(f'https://api.github.com/repos/{repo_full_name}/issues?labels=bug')
    doc = requests.get(f'https://api.github.com/repos/{repo_full_name}/issues?labels=documentation')
    wont_fix = requests.get(f'https://api.github.com/repos/{repo_full_name}/issues?labels=wontfix')
    duplicate = requests.get(f'https://api.github.com/repos/{repo_full_name}/issues?labels=duplicate')
    enhancement = requests.get(f'https://api.github.com/repos/{repo_full_name}/issues?labels=enhancement')
    good_first_issue = requests.get(f'https://api.github.com/repos/{repo_full_name}/issues?labels=good%20first%20issue')
    help_wanted = requests.get(f'https://api.github.com/repos/{repo_full_name}/issues?labels=help%20wanted')
    invalid = requests.get(f'https://api.github.com/repos/{repo_full_name}/issues?labels=invalid')
    question = requests.get(f'https://api.github.com/repos/{repo_full_name}/issues?labels=question')

    bug_list = get_data_from_json(bug)
    doc_list = get_data_from_json(doc)
    wont_fix_list = get_data_from_json(wont_fix)
    duplicate_list = get_data_from_json(duplicate)
    enhancement_list = get_data_from_json(enhancement)
    good_first_issue_list = get_data_from_json(good_first_issue)
    help_wanted_list = get_data_from_json(help_wanted)
    invalid_list = get_data_from_json(invalid)
    question_list = get_data_from_json(question)

    hash_map = dict({
        'bug': bug_list,
        'documentation': doc_list,
        'wont_fix': wont_fix_list,
        'duplicate': duplicate_list,
        'enhancement': enhancement_list,
        'good_first_issue': good_first_issue_list,
        'help_wanted': help_wanted_list,
        'invalid': invalid_list,
        'question': question_list
    })

    return hash_map


def get_data_from_json(json_data):
    """
    Returns list containing only 'body' from issue comments.

    :param json_data: json input from Github API
    :return: list
    """
    tmp_arr = []

    for i in json_data.json():
        tmp_arr.append(i['body'])

    return tmp_arr


# this is just for example
# print(fetch_issue_data('nanoninja/docker-nginx-php-mysql'))
