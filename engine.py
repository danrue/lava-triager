#!/usr/bin/env python3
import pprint
import re
import requests
import sys
import textwrap
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

def exact_match_check(engine, exact_match_dict):
    for rule_name, rule_value in exact_match_dict.items():
        if engine.device_type == rule_value:
            continue
        else:
            return False
    return True

def re_match_check(engine, re_match_dict):
    for rule_name, rule_value in re_match_dict.items():
        if not isinstance(rule_value, list):
            rule_value = [rule_value]
        for regex in rule_value:
            if re.search(regex, getattr(engine, rule_name)):
                continue
            else:
                return False
    return True

def main(job_id):
    with open("rules.yaml", 'r') as f:
        rule_file_content = yaml.load(f)

    lava_base_url = rule_file_content['lava_base_url']
    engine = lkftTriage(lava_base_url, job_id)
    #pprint.pprint(engine.job_definition)
    #pprint.pprint(engine.results)
    #pprint.pprint(engine.job_log)
    #print(engine.error_msg)
    #print(engine.job_output)

    buf = ""
    for rule in rule_file_content['rules']:
        if (exact_match_check(engine, rule.get('exact_match', {})) and
            re_match_check(engine, rule.get('re_match', {}))):
            buf += "Lava job {}/scheduler/job/{}\n".format(lava_base_url, job_id)
            buf += textwrap.indent("Known issue:\n", '  ')
            buf += textwrap.indent(rule['description'], '    ')
    return buf

if __name__ == '__main__':
    job_id = sys.argv[1]
    print(main(job_id))
