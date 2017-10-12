#!/usr/bin/env python3
import pprint
import re
import requests
import sys
import yaml

class lkftTriage(object):
    def __init__(self, lava_base_url, job_id):
        self.lava_base_url = lava_base_url
        self.job_id = job_id
        self._get_results()
        self._get_job_definition()
        self._get_job_log()
        self._set_attributes()

    def _get_results(self):
        url = "{}/results/{}/yaml".format(self.lava_base_url, self.job_id)
        r = requests.get(url)
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
        self.error_msg = self.job_log[-1]['msg'].get('error_msg', None)
        self.job_name = self.job_definition['job_name']
        self.job_output = str(self.job_log) # ok so this is kind of lazy..

with open("rules.yaml", 'r') as f:
    rule_file_content = yaml.load(f)

job_id = sys.argv[1]
lava_base_url = rule_file_content['lava_base_url']
engine = lkftTriage(lava_base_url, job_id)
#pprint.pprint(engine.job_definition)
#pprint.pprint(engine.results)
#pprint.pprint(engine.job_log)
#print(engine.error_msg)

def exact_match_check():
for rule in rule_file_content['rules']:
    for rule_name, rule_value in rule['exact_match'].items():
        # continue to process next rule; break to go to next set of rules
        if engine.device_type == rule_value:
            continue
        else:
            print("Not a match!")
            break
    for rule_name, rule_value in rule['re_match'].items():
        # continue to process next rule; break to go to next set of rules
        if not isinstance(rule_value, list):
            rule_value = [rule_value]
        for regex in rule_value:
            if re.search(regex, getattr(engine, rule_name)):
                continue
            else:
                print("Not a match!")
                break

    import textwrap
    print("Lava job {}/scheduler/job/{}".format(lava_base_url, job_id))
    print(textwrap.indent("Known issue:", '  '))
    print(textwrap.indent(rule['description'], '    '))

