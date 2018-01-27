#!/usr/bin/env python
"""Delete IAM user.  Remove from all groups, drop access keys, login profile, mfa, other"""
import sys
import boto3

if len(sys.argv) < 2:
    print('provide a user name')
    sys.exit()
user_name = sys.argv[1]
iam = boto3.resource('iam')
user = iam.User(user_name)
try:
    user.load()
except Exception as e:
    sys.exit(e)
for x in user.access_keys.all():
    print('deleting access key{}'.format(x.id))
    x.delete()
for x in user.attached_policies.all():
    print('detaching policy {}'.format(x.policy_name))
    x.detach_user()
for x in user.groups.all():
    print('removing user from group {}'.format(x.name))
    x.remove_user(UserName=user.name)
for x in user.mfa_devices.all():
    print('deleting mfa device {}'.format(x.serial_number))
    x.disassociate()
for x in user.policies.all():
    print('deleting policy {}'.format(x.name))
    x.delete()
for x in user.signing_certificates.all():
    print('deleting signing cert {}'.format(x.id))
    x.delete()


profile = user.LoginProfile()
try:
    profile.load()
    print('deleting login profile {}'.format(profile))
except Exception as e:
    pass
print('deleting user {}'.format(user.name))
user.delete()

"""
bug:

(python3.6) agould@horus:~/git-repos/code-commit/ashley-training/ashley-aws-hacks/bin> ./iam-userdel.py ashley
deleting user ashley
Traceback (most recent call last):
  File "./iam-userdel.py", line 43, in <module>
    user.delete()
  File "/home/agould/python-venv/python3.6/lib/python3.6/site-packages/boto3/resources/factory.py", line 520, in do_action
    response = action(self, *args, **kwargs)
  File "/home/agould/python-venv/python3.6/lib/python3.6/site-packages/boto3/resources/action.py", line 83, in __call__
    response = getattr(parent.meta.client, operation_name)(**params)
  File "/home/agould/python-venv/python3.6/lib/python3.6/site-packages/botocore/client.py", line 317, in _api_call
    return self._make_api_call(operation_name, kwargs)
  File "/home/agould/python-venv/python3.6/lib/python3.6/site-packages/botocore/client.py", line 615, in _make_api_call
    raise error_class(parsed_response, operation_name)
botocore.errorfactory.DeleteConflictException: An error occurred (DeleteConflict) when calling the DeleteUser operation: Cannot delete entity, must remove referenced objects first.
"""
