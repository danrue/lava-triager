import engine
import pytest
import yaml

with open("rules.yaml", 'r') as f:
    rules = yaml.load(f)

@pytest.mark.parametrize("rule", rules['rules'])
def test_rule(rule):
    '''
        For every rule defined in rules.yaml, run engine against each known_job
        defined and ensure that the rule returned matches the rule defined.
        Note that such an implementation might cause high load on the lava
        server, and is rather slow.
    '''
    for known_job in rule['known_jobs']:
        _, engine_results = engine.main(known_job)
        assert rule in engine_results
