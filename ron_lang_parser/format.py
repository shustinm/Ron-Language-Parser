import re
from typing import List, Optional
from xml_dataclasses import rename, text, xml_dataclass

type_lut = {
    'uint8': 'u8',
    'uint16': 'u16',
    'uint32': 'u32',
    'uint': 'u32',
    'ushort': 'u16',
    'ulong': 'u64',
    'int': 'long'
}


@xml_dataclass
class IsArray:
    __ns__ = None
    is_arr: str = text(default='true')

@xml_dataclass
class IsPointer:
    __ns__ = None
    is_ptr: str = text(default='true')


@xml_dataclass
class ParameterDesciprion:
    __ns__ = None
    name: str
    param_type: str
    is_ptr: Optional[IsPointer] = rename(name='IsPointer')
    is_arr: Optional[IsArray] = rename( name='IsArray')

    @staticmethod
    def from_str_iter(s: str):
        for match in re.finditer(r'(?P<ptr>ref\s)?(?P<type>\w+)(?P<arr>\[\])?\s(?P<name>\w+)', s):
            match_data = match.groupdict()

            yield ParameterDesciprion(
                name=match_data['name'],
                param_type=type_lut[match_data['type']],
                is_ptr=IsPointer() if match_data['ptr'] else None,
                is_arr=IsArray() if match_data['arr'] else None)


@xml_dataclass
class MethodParameters:
    __ns__ = None
    params: List[ParameterDesciprion] = rename(name='Parameter')

    def __init__(self, s: str):
        self.params = list(ParameterDesciprion.from_str_iter(s))


@xml_dataclass
class MethodReturnType:
    __ns__ = None
    name: str = rename(name='Name')

@xml_dataclass
class MethodDescription:
    __ns__ = None
    name: str = rename(name='Name')
    params: MethodParameters = rename(name='Parameters')
    return_type: MethodReturnType = rename(name='ReturnType')

    def __init__(self, declaration: str):
        match = re.match(r'public\s(?P<ret_type>\w+)\s(?P<name>\w+)\((?P<params>.+)\)', declaration)
        match_Data = match.groupdict()
        self.name = match_Data['name']
        self.return_type = MethodReturnType(match_Data['ret_type'])
        self.params = MethodParameters(match_Data['params'])
