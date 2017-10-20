#!/usr/bin/env python3
import pprint
import re
import requests
import requests_cache
import sys
import textwrap
import yaml


class lavaTriage(object):
    def __init__(self, lava_base_url, job_id):
        self.lava_base_url = lava_base_url
        self.job_id = job_id

        # Cache all lava requests for a week (they don't change)
        requests_cache.install_cache('lava-triage', expire_after=60*60*24*7)

        self._get_results()
        self._get_job_definition()
        self._get_job_log()
        self._set_attributes()

    def _get_results(self):
        url = "{}/results/{}/yaml".format(self.lava_base_url, self.job_id)
        r = requests.get(url)
        assert r.status_code == 200, (
                "Results are not available at {}, HTTP {}".format(
                    url, r.status_code))

        self.results = yaml.load(r.text.encode('utf-8', 'ignore'))

    def _get_job_definition(self):
        url = "{}/scheduler/job/{}/definition/plain".format(
            self.lava_base_url, self.job_id)
        r = requests.get(url)
        self.job_definition = yaml.load(r.text.encode('utf-8', 'ignore'))

    def _get_job_log(self):
        url = "{}/scheduler/job/{}/log_file/plain".format(
            self.lava_base_url, self.job_id)
        r = requests.get(url)
        self.job_log = yaml.load(r.text.encode('utf-8', 'ignore'))

    def _set_attributes(self):
        self.device_type = self.job_definition['device_type']
        self.error_msg = self.job_log[-1]['msg'].get('error_msg', "")
        self.job_name = self.job_definition['job_name']
        self.job_output = str(self.job_log)  # ok so this is kind of lazy..

    def re_match_check(self, re_match_dict):
        """ For each key/value regex in re_match_dict,
            determine if the regex matches self's attributes.
            Return True if all attributes match. Otherwise, False.
        """
        for rule_name, rule_value in re_match_dict.items():
            if not isinstance(rule_value, list):
                rule_value = [rule_value]
            for regex in rule_value:
                if re.search(regex, getattr(self, rule_name)):
                    continue
                else:
                    return False
        return True

    def find_matching_rules(self, rules):
        matching_rules = []
        for rule in rules:
            if self.re_match_check(rule.get('re_match', {})):
                matching_rules.append(rule)
        return matching_rules


def main(job_id):
    assert str(job_id).isdigit(), "job_id must be a number"
    with open("rules.yaml", 'r') as f:
        rule_file_content = yaml.load(f)

    lava_base_url = rule_file_content['lava_base_url']
    engine = lavaTriage(lava_base_url, job_id)
    # pprint.pprint(engine.job_definition)
    # pprint.pprint(engine.results)
    # pprint.pprint(engine.job_log)
    # print(engine.error_msg)
    # print(engine.job_output)

    matching_rules = engine.find_matching_rules(rule_file_content['rules'])
    return engine, matching_rules

if __name__ == '__main__':
    job_id = sys.argv[1]
    assert str(job_id).isdigit(), (
        "Usage: {} (lava job number)".format(sys.argv[0]))
    engine, matching_rules = main(job_id)

    if matching_rules:
        for rule in matching_rules:
            print(rule['description'])
    else:
        print("No known rule found. Here's a starting point:")
        new_rule = []
        new_rule.append({
            're_match': {
                'job_name': engine.job_name,
                'error_msg': engine.error_msg,
                'job_output': [],
                'device_type': '^'+engine.device_type+'$',
            },
            'known_jobs': [job_id],
            'description': "Job Description"
        })
        print(yaml.dump(new_rule))
        sys.exit(1)
