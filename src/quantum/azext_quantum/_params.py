# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
# pylint: disable=line-too-long,protected-access

import argparse
from knack.arguments import CLIArgumentType
from azure.cli.core.azclierror import InvalidArgumentValueError


class JobParamsAction(argparse._AppendAction):
    def __call__(self, parser, namespace, values, option_string=None):
        action = self.get_action(values, option_string)
        namespace.job_params = action

    def get_action(self, values, option_string):
        params = {}
        for item in values:
            try:
                key, value = item.split('=', 1)
                params[key] = value
            except ValueError as e:
                raise InvalidArgumentValueError('Usage error: {} KEY=VALUE [KEY=VALUE ...]'.format(option_string)) from e
        return params


def load_arguments(self, _):
    workspace_name_type = CLIArgumentType(options_list=['--workspace-name', '-w'], help='Name of the Quantum Workspace. You can configure the default workspace using `az quantum workspace set`.', id_part=None, required=False)
    storage_account_name_type = CLIArgumentType(options_list=['--storage-account', '-a'], help='Name of the storage account to be used by a quantum workspace.')
    program_args_type = CLIArgumentType(nargs='*', help='List of arguments expected by the Q# operation specified as --name=value after `--`.')
    target_id_type = CLIArgumentType(options_list=['--target-id', '-t'], help='Execution engine for quantum computing jobs. When a workspace is configured with a set of provider, they each enable one or more targets. You can configure the default target using `az quantum target set`.')
    project_type = CLIArgumentType(help='The location of the Q# project to submit. Defaults to current folder.')
    job_name_type = CLIArgumentType(help='A friendly name to give to this run of the program.')
    job_id_type = CLIArgumentType(options_list=['--job-id', '-j'], help='Job unique identifier in GUID format.')
    job_params_type = CLIArgumentType(options_list=['--job-params'], help='Job parameters passed to the target as a list of key=value pairs.', action=JobParamsAction, nargs='+')
    shots_type = CLIArgumentType(help='The number of times to run the Q# program on the given target.')
    no_build_type = CLIArgumentType(help='If specified, the Q# program is not built before submitting.')
    storage_type = CLIArgumentType(help='If specified, the ConnectionString of an Azure Storage is used to store job data and results.')
    max_poll_wait_secs_type = CLIArgumentType(help='Poll time in seconds to query Azure Quantum for results of the corresponding job.')
    tag_type = CLIArgumentType(help='Show only quantum workspaces that have associated the specified tag.')
    skip_role_assignment_type = CLIArgumentType(help='Skip the role assignment step for the quantum workspace in the storage account.')
    provider_id_type = CLIArgumentType(options_list=['--provider-id', '-p'], help='Identifier of an Azure Quantum provider.')
    sku_type = CLIArgumentType(options_list=['--sku', '-k'], help='Identify a plan or SKU offered by an Azure Quantum provider.')
    provider_sku_list_type = CLIArgumentType(options_list=['--provider-sku-list', '-r'], help='Comma separated list of Provider/SKU pairs.')

    with self.argument_context('quantum workspace') as c:
        c.argument('workspace_name', workspace_name_type)
        c.argument('storage_account', storage_account_name_type)
        c.argument('tag', tag_type)
        c.argument('skip_role_assignment', skip_role_assignment_type)
        c.argument('provider_sku_list', provider_sku_list_type)

    with self.argument_context('quantum target') as c:
        c.argument('workspace_name', workspace_name_type)
        c.argument('target_id', target_id_type)

    with self.argument_context('quantum job') as c:
        c.argument('workspace_name', workspace_name_type)
        c.argument('job_id', job_id_type)
        c.argument('target_id', target_id_type)
        c.argument('project', project_type)
        c.argument('job_name', job_name_type)
        c.argument('shots', shots_type)
        c.argument('storage', storage_type)
        c.argument('no_build', no_build_type)
        c.argument('max_poll_wait_secs', max_poll_wait_secs_type)

    with self.argument_context('quantum job submit') as c:
        c.argument('job_params', job_params_type)
        c.positional('program_args', program_args_type)

    with self.argument_context('quantum execute') as c:
        c.argument('workspace_name', workspace_name_type)
        c.argument('target_id', target_id_type)
        c.argument('project', project_type)
        c.argument('job_name', job_name_type)
        c.argument('shots', shots_type)
        c.argument('storage', storage_type)
        c.argument('no_build', no_build_type)
        c.argument('job_params', job_params_type)
        c.positional('program_args', program_args_type)

    with self.argument_context('quantum run') as c:
        c.argument('workspace_name', workspace_name_type)
        c.argument('target_id', target_id_type)
        c.argument('project', project_type)
        c.argument('job_name', job_name_type)
        c.argument('shots', shots_type)
        c.argument('storage', storage_type)
        c.argument('no_build', no_build_type)
        c.argument('job_params', job_params_type)
        c.positional('program_args', program_args_type)

    with self.argument_context('quantum offerings') as c:
        c.argument('provider_id', provider_id_type)
        c.argument('sku', sku_type)
