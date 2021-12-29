from ..util.data import game_data
from src.config import pathConfig
from ..util.common import remove_xml_tag
import re
from typing import Tuple, Dict, Optional


def parse_template(blackboard, description):
    formatter = {
        '0%': lambda v: f'{round(v * 100)}%'
    }
    data_dict = {item['key']: item['value'] for index, item in enumerate(blackboard)}
    desc = remove_xml_tag(description.replace('>-{', '>{'))
    format_str = re.findall(r'({(\S+?)})', desc)
    if format_str:
        for desc_item in format_str:
            key = desc_item[1].split(':')
            fd = key[0].lower().strip('-')
            if fd in data_dict:
                value = round(data_dict[fd])

                if len(key) >= 2 and key[1] in formatter:
                    value = formatter[key[1]](value)

                desc = desc.replace(desc_item[0], f' [cl {value}@#174CC6 cle] ')

    return desc


async def char_detail(name: str) -> Optional[Tuple[Dict[str, str], Dict]]:
    char_id, char_data = await game_data.get_char_data(name)
    if char_data:
        items = game_data.load('item_table')['items']
        token_id = 'p_' + char_id
        token = None
        if token_id in items:
            token = items[token_id]
        max_phases = char_data['phases'][-1]
        max_attr = max_phases['attributesKeyFrames'][-1]['data']
        trait = remove_xml_tag(char_data['description'])
        if char_data['trait']:
            max_trait = char_data['trait']['candidates'][-1]
            trait = parse_template(max_trait['blackboard'], max_trait['overrideDescripton'] or trait)
            detail = {
                'operator_trait': trait.replace('\\n', '\n'),
                'operator_usage': char_data['itemUsage'] or '',
                'operator_quote': char_data['itemDesc'] or '',
                'operator_token': token['description'] if token else '',
                'max_level': '%s - %s' % (len(char_data['phases']) - 1, max_phases['maxLevel'])
            }
            detail.update(max_attr)
            return detail, char_data['favorKeyFrames'][-1]['data']
    return None
