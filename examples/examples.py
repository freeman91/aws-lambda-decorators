from aws_lambda_decorators.decorators import extract, extract_from_event, extract_from_context, extract_from_ssm, \
    validate, log, handle_exceptions, response_body_as_json
from aws_lambda_decorators.classes import Parameter, SSMParameter, ValidatedParameter, ExceptionHandler
from aws_lambda_decorators.validators import Mandatory, RegexValidator

import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError


@extract(parameters=[
            Parameter(path='/parent/my_param', func_param_name='a_dictionary'),
            # extracts a non mandatory my_param from a_dictionary
            Parameter(path='/parent/missing_non_mandatory', func_param_name='a_dictionary', default='I am missing'),
            # extracts a non mandatory missing_non_mandatory from a_dictionary
            Parameter(path='/parent/missing_mandatory', func_param_name='a_dictionary'),
            # does not fail as the parameter is not validated as mandatory
            Parameter(path='/parent/child/id', validators=[Mandatory], var_name='user_id',
                      func_param_name='another_dictionary')
            # extracts a mandatory id as "user_id" from another_dictionary
        ])
def extract_example(a_dictionary, another_dictionary, my_param='aDefaultValue',
                   missing_non_mandatory='I am missing', missing_mandatory=None, user_id=None):
    #  you can now access the extracted parameters directly:
    return my_param, missing_non_mandatory, missing_mandatory, user_id


@extract(parameters=[
            Parameter(path='/parent/my_param', func_param_name='a_dictionary'),
            # extracts a non mandatory my_param from a_dictionary
        ])
def extract_to_kwargs_example(a_dictionary, **kwargs):
    return kwargs['my_param']


@extract(parameters=[
            Parameter(path='/parent/mandatory_param', func_param_name='a_dictionary', validators=[Mandatory]),
            # extracts a mandatory my_param from a_dictionary
        ])
def extract_missing_mandatory_param_example(a_dictionary, mandatory_param=None):
    print('Here!')  # this message will never be reached, if the mandatory_param is missing


@extract(parameters=[
    Parameter(path='/parent[json]/my_param', func_param_name='a_dictionary'),
    # extracts a non mandatory my_param from a_dictionary
])
def extract_from_json_example(a_dictionary, my_param=None):
    return my_param


@extract_from_event(parameters=[
            Parameter(path='/body[json]/my_param', validators=[Mandatory]),
            # extracts a mandatory my_param from the json body of the event
            Parameter(path='/headers/Authorization[jwt]/sub', validators=[Mandatory], var_name='user_id')
            # extract the mandatory sub value as user_id from the authorization JWT
        ])
def extract_from_event_example(event, context, my_param=None, user_id=None):
    return my_param, user_id  # returns ('Hello!', '1234567890')


@extract_from_context(parameters=[
    Parameter(path='/parent/my_param', validators=[Mandatory]),
    # extracts a mandatory my_param from the parent element in context
])
def extract_from_context_example(event, context, my_param=None):
    return my_param  # returns 'Hello!'


@extract_from_ssm(ssm_parameters=[
            SSMParameter(ssm_name='one_key'),  # extracts the value of one_key from SSM as a kwarg named "one_key"
            SSMParameter(ssm_name='another_key', var_name="another"),  # extracts another_key as a kwarg named "another"
        ])
def extract_from_ssm_example(your_func_params, one_key=None, another=None):
    return your_func_params, one_key, another


@validate(parameters=[
    ValidatedParameter(func_param_name='a_param', validators=[Mandatory]),  # validates a_param as mandatory
    ValidatedParameter(func_param_name='another_param', validators=[Mandatory, RegexValidator(r'\d+')])
    # validates another_param as mandatory and containing only digits
])
def validate_example(a_param, another_param):
    return a_param, another_param  # returns a_param, another_param


@log(parameters=True, response=True)
def log_example(parameters):
    return 'Done!'


@handle_exceptions(handlers=[
            ExceptionHandler(ClientError, "Your message when a client error happens.")
        ])
def handle_exceptions_example():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('non_existing_table')
    table.query(KeyConditionExpression=Key('user_id').eq('1234'))


@response_body_as_json
def response_body_as_json_example():
    return {'statusCode': 400, 'body': {'param': 'hello!'}}
