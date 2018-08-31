#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '0.1',
    'status': ['preview'],
    'supported_by': 'BowenZhuang'
}

DOCUMENTATION = '''
---
module: MySQLQuery

short_description: This is MySQL Query module via mysql command on remote node

version_added: "2.4"

description:
    - "This is MySQL Query module via mysql command on remote node"

options:
    sql:
        description:
            - sql statment
        required: true

extends_documentation_fragment:
    - azure

author:
    - BowenZhuang (@yourhandle)
'''

EXAMPLES = '''
# Pass in a message
- name: Test with a message
  MySQLQuery:
    name: 'select @@hostname'
'''

RETURN = '''
original_message:
    description: The original name param that was passed in
    type: str
message:
    description: results
'''

from ansible.module_utils.basic import AnsibleModule
import commands

def run_module():
    # define the available arguments/parameters that a user can pass to
    # the module
    module_args = dict(
        sql=dict(type='str', required=True)
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # change is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        original_message='',
        message=''
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        return result

    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)
    result['original_message'] = module.params['sql']
    (status,output) = commands.getstatusoutput(module.params['sql'])
    result['message'] = output

    # use whatever logic you need to determine whether or not this module
    # made any modifications to your target
		
    if status != 0:
        module.fail_json(msg='You requested this to fail', **result)

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
