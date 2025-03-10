# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

import jwt
from unittest import mock
import os
import azure.cli.command_modules.role.custom
from azure.cli.testsdk import ScenarioTest
from azure.cli.testsdk import ResourceGroupPreparer
from .example_steps import step_terms_list
from .example_steps import step_organization_show
from .example_steps import step_organization_list
from .example_steps import step_organization_list2
from .example_steps import step_organization_update
from .example_steps import step_organization_delete
from azure_devtools.scenario_tests import AllowLargeResponse
from .. import (
    try_manual,
    raise_if,
    calc_coverage
)


TEST_DIR = os.path.abspath(os.path.join(os.path.abspath(__file__), '..'))


def step_offer_detail_show(test, rg, checks=None):
    if checks is None:
        checks = []
    result = test.cmd('az confluent offer-detail show '
             '--publisher-id confluentinc '
             '--offer-id confluent-cloud-azure-stag',
             checks=checks).get_output_in_json()

    # check
    for plan in result:
        assert plan.get('offerId', None) is not None
        assert plan.get('publisherId', None) is not None
        for term_unit in plan['termUnits']:
            if term_unit.get('termUnits', None): 
                assert term_unit['termUnits'] in ['P1M', 'P1Y']
            assert term_unit.get('price', None) is not None
            assert term_unit['price'].get('isPIRequired', None) is None
            assert term_unit['price'].get('msrp', None) is None
            assert term_unit.get('termDescription', None) is not None


orig_decode = jwt.decode


def mock_jwt_decode(jwt_str, **kwargs):
    if jwt_str == 'top-secret-token-for-you':
        return {
            'given_name': 'contoso',
            'family_name': 'zhou',
            'email': 'contoso@microsoft.com',
            'oid': '00000000-0000-0000-0000-000000000000'
        }
    else:
        return orig_decode(jwt_str, **kwargs)


orig_list_role = azure.cli.command_modules.role.custom.list_role_assignments


def mock_list_role_assignments(cmd, **kwargs):
    if kwargs['assignee'] == '00000000-0000-0000-0000-000000000000':
        return [{}]  # mock it to pass non-empty check
    else:
        return orig_list_role(cmd, **kwargs)


def step_organization_create(test, rg, checks=None):
    if checks is None:
        checks = []
    with mock.patch('jwt.decode', mock_jwt_decode):
        with mock.patch('azure.cli.command_modules.role.custom.list_role_assignments', mock_list_role_assignments):
            test.cmd('az confluent organization create '
                     '--location "eastus2euap" '
                     '--offer-id "confluent-cloud-azure-stag" '
                     '--plan-id "confluent-cloud-azure-payg-stag" '
                     '--plan-name "Confluent Cloud - Pay as you Go" '
                     '--publisher-id "confluentinc" '
                     '--term-unit "P1M" '
                     '--tags environment="Dev" '
                     '--name "{myOrganization}" '
                     '--resource-group "{rg}"',
                     checks=checks)
    test.cmd('az confluent organization wait --created '
             '--name "{myOrganization}" '
             '--resource-group "{rg}"',
             checks=[])


# Env setup_scenario
@try_manual
def setup_scenario(test, rg):
    pass


# Env cleanup_scenario
@try_manual
def cleanup_scenario(test, rg):
    pass


# Testcase: Scenario
@try_manual
def call_scenario(test, rg):
    setup_scenario(test, rg)
    step_terms_list(test, rg, checks=[
        test.greater_than('length(@)', 1)
    ])
    step_offer_detail_show(test, rg, checks=[
        test.greater_than('length(@)', 0)
    ])
    step_organization_create(test, rg, checks=[
        test.check("location", "eastus2euap", case_sensitive=False),
        # change to real values for userDetail in live tests
        test.check("userDetail.emailAddress", "contoso@microsoft.com", case_sensitive=False),
        test.check("userDetail.firstName", "contoso", case_sensitive=False),
        test.check("userDetail.lastName", "zhou", case_sensitive=False),
        test.check("tags.environment", "Dev", case_sensitive=False),
        test.check("name", "{myOrganization}", case_sensitive=False),
    ])
    step_organization_show(test, rg, checks=[
        test.check("location", "eastus2euap", case_sensitive=False),
        # change to real values for userDetail in live tests
        test.check("userDetail.emailAddress", "contoso@microsoft.com", case_sensitive=False),
        test.check("userDetail.firstName", "contoso", case_sensitive=False),
        test.check("userDetail.lastName", "zhou", case_sensitive=False),
        test.check("tags.environment", "Dev", case_sensitive=False),
        test.check("name", "{myOrganization}", case_sensitive=False),
    ])
    step_organization_list(test, rg, checks=[
        test.greater_than('length(@)', 0),
    ])
    step_organization_list2(test, "", checks=[
        test.greater_than('length(@)', 0),
    ])
    step_organization_update(test, rg, checks=[
        test.check("location", "eastus2euap", case_sensitive=False),
        test.check("userDetail.emailAddress", "contoso@microsoft.com", case_sensitive=False),
        test.check("userDetail.firstName", "contoso", case_sensitive=False),
        test.check("userDetail.lastName", "zhou", case_sensitive=False),
        test.check("name", "{myOrganization}", case_sensitive=False),
        test.check("tags.client", "dev-client", case_sensitive=False),
    ])
    step_organization_delete(test, rg, checks=[])
    cleanup_scenario(test, rg)


# Test class for Scenario
@try_manual
class ConfluentScenarioTest(ScenarioTest):

    def __init__(self, *args, **kwargs):
        super(ConfluentScenarioTest, self).__init__(*args, **kwargs)
        self.kwargs.update({
            'myOrganization': 'cliTestOrg',
        })

    @ResourceGroupPreparer(name_prefix='clitestconfluent_myResourceGroup'[:7], key='rg', parameter_name='rg')
    @AllowLargeResponse()
    def test_confluent_Scenario(self, rg):
        call_scenario(self, rg)
        calc_coverage(__file__)
        raise_if()
