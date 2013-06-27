from xivo_dao.mapping_alchemy_sdm.user_mapping import UserMapping
from xivo_dao.service_data_model.sdm_exception import MissingParametersException, IncorrectParametersException


def validate_params(parameters):
    unknown = []
    for param_name in parameters.keys():
        if param_name not in UserMapping.mapping.values():
            unknown.append(param_name)

    if len(unknown) > 0:
        raise IncorrectParametersException(*unknown)


def validate_user(user):
    if not hasattr(user, 'firstname') or user.firstname.strip() == '':
        print "user data", user.todict()
        raise MissingParametersException('firstname')
