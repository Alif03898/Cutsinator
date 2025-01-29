import xml.etree.ElementTree as ET

class XMLHandler:
    def __init__(self, filepath):
        self.filepath = filepath

    def read_cutscene(self):
        tree = ET.parse(self.filepath)
        root = tree.getroot()

        cutscene_data = {
            'events': [],
            'event_args': [],
            'cutscene_objects': [],
            'load_events': [],
            'attributes': [],
            'camera_cut_list': [],
            'section_split_list': [],
            'concat_data_list': [],
            'discard_frame_list': [],
            'additional_attributes': {}  # New key for additional attributes
        }

        # Parse CutsceneEventList
        for event_item in root.findall('.//pCutsceneEventList/Item'):
            event = {
                'fTime': float(event_item.find('fTime').attrib['value']),
                'iEventId': int(event_item.find('iEventId').attrib['value']),
                'iEventArgsIndex': int(event_item.find('iEventArgsIndex').attrib['value']),
                'iObjectId': int(event_item.find('iObjectId').attrib['value']),
            }
            cutscene_data['events'].append(event)

        # Parse CutsceneEventArgsList
        for args_item in root.findall('.//pCutsceneEventArgsList/Item'):
            iObjectId_elem = args_item.find('iObjectId')
            cName_elem = args_item.find('cName')
            fSubtitleDuration_elem = args_item.find('fSubtitleDuration')

            args = {
                'iObjectId': int(iObjectId_elem.attrib['value']) if iObjectId_elem is not None else None,
                'cName': cName_elem.text if cName_elem is not None else None,
                'fSubtitleDuration': float(fSubtitleDuration_elem.attrib['value']) if fSubtitleDuration_elem is not None else None,
            }
            cutscene_data['event_args'].append(args)

        # Parse CutsceneObjects
        for object_item in root.findall('.//pCutsceneObjects/Item'):
            iObjectId_elem = object_item.find('iObjectId')
            cName_elem = object_item.find('cName')

            cutscene_object = {
                'object_id': int(iObjectId_elem.attrib['value']) if iObjectId_elem is not None else None,
                'name': cName_elem.text if cName_elem is not None else None,
            }
            cutscene_data['cutscene_objects'].append(cutscene_object)

        # Parse CutsceneLoadEventList
        for load_event_item in root.findall('.//pCutsceneLoadEventList/Item'):
            iEventId_elem = load_event_item.find('iEventId')
            fTime_elem = load_event_item.find('fTime')

            load_event = {
                'event_id': int(iEventId_elem.attrib['value']) if iEventId_elem is not None else None,
                'load_time': float(fTime_elem.attrib['value']) if fTime_elem is not None else None,
            }
            cutscene_data['load_events'].append(load_event)

        # Parse Attributes
        for attribute_item in root.findall('.//attributes/Item'):
            attribute = {
                'type': attribute_item.attrib.get('type'),
                'value': attribute_item.text.strip() if attribute_item.text is not None else None,
            }
            cutscene_data['attributes'].append(attribute)

        # Parse additional attributes
        additional_attributes = {
            'User    Data1': int(root.find('.//attributes/UserData1').attrib['value']) if root.find('.//attributes/UserData1') is not None else 0,
            'User    Data2': int(root.find('.//attributes/UserData2').attrib['value']) if root.find('.//attributes/UserData2') is not None else 0,
            'iRangeStart': int(root.find('.//iRangeStart').attrib['value']) if root.find('.//iRangeStart') is not None else 0,
            'iRangeEnd': int(root.find('.//iRangeEnd').attrib['value']) if root.find('.//iRangeEnd') is not None else 0,
            'iAltRangeEnd': int(root.find('.//iAltRangeEnd').attrib['value']) if root.find('.//iAltRangeEnd') is not None else 0,
            'fSectionByTimeSliceDuration': float(root.find('.//fSectionByTimeSliceDuration').attrib['value']) if root.find('.//fSectionByTimeSliceDuration') is not None else 0.0,
            'fFadeOutCutsceneDuration': float(root.find('.//fFadeOutCutsceneDuration').attrib['value']) if root.find('.//fFadeOutCutsceneDuration') is not None else 0.0,
            'fFadeInGameDuration': float(root.find('.//fFadeInGameDuration').attrib['value']) if root.find('.//fFadeInGameDuration') is not None else 0.0,
            'fadeInColor': root.find('.//fadeInColor').attrib['value'] if root.find('.//fadeInColor') is not None else '0xFFFFFFFF',
            'iBlendOutCutsceneDuration': int(root.find('.//iBlendOutCutsceneDuration').attrib['value']) if root.find('.//iBlendOutCutsceneDuration') is not None else 0,
            'iBlendOutCutsceneOffset': int(root.find('.//iBlendOutCutsceneOffset').attrib['value']) if root.find('.//iBlendOutCutsceneOffset') is not None else 0,
            'fFadeOutGameDuration': float(root.find('.//fFadeOutGameDuration').attrib['value']) if root.find('.//fFadeOutGameDuration') is not None else 0.0,
            'fFadeInCutsceneDuration': float(root.find('.//fFadeInCutsceneDuration').attrib['value']) if root.find('.//fFadeInCutsceneDuration') is not None else 0.0,
            'fadeOutColor': root.find('.//fadeOutColor').attrib['value'] if root.find('.//fadeOutColor') is not None else '0xFFFFFFFF',
            'DayCoCHours': int(root.find('.//DayCoCHours').attrib['value']) if root.find('.//DayCoCHours') is not None else 0,
        }
        cutscene_data['additional_attributes'] = additional_attributes

        # Parse CameraCutList
        for camera_cut_item in root.findall('.//cameraCutList/Item'):
            camera_cut = {
                'cut_id': int(camera_cut_item.find('cutId').attrib['value']),
                'cut_time': float(camera_cut_item.find('cutTime').attrib['value']),
            }
            cutscene_data['camera_cut_list'].append(camera_cut)

        # Parse SectionSplitList
        for section_split_item in root.findall('.//sectionSplitList/Item'):
            section_split = {
                'split_id': int(section_split_item.find('splitId').attrib['value']),
                'split_time': float(section_split_item.find('splitTime').attrib['value']),
            }
            cutscene_data['section_split_list'].append(section_split)

        # Parse ConcatDataList
        for concat_data_item in root.findall('.//concatDataList/Item'):
            concat_data = {
                'item_type': concat_data_item.attrib.get('itemType'),
                'data': concat_data_item.text.strip() if concat_data_item.text is not None else None,
            }
            cutscene_data['concat_data_list'].append(concat_data)

        # Parse DiscardFrameList
        for discard_frame_item in root.findall('.//discardFrameList/Item'):
            frame_number_elem = discard_frame_item.find('frameNumber')
            discard_frame = {
                'item_type': discard_frame_item.attrib.get('itemType'),
                'frame_number': int(frame_number_elem.attrib['value']) if frame_number_elem is not None else 0,
            }
            cutscene_data['discard_frame_list'].append(discard_frame)

        return cutscene_data

    def write_cutscene(self, cutscene_data):
        root = ET.Element('pCutscene')

        # Create pCutsceneEventList
        event_list = ET.SubElement(root, 'pCutsceneEventList')
        for event in cutscene_data['events']:
            event_item = ET.SubElement(event_list, 'Item')
            ET.SubElement(event_item, 'fTime', value=str(event['fTime']))
            ET.SubElement(event_item, 'iEventId', value=str(event['iEventId']))
            ET.SubElement(event_item, 'iEventArgsIndex', value=str(event['iEventArgsIndex']))
            ET.SubElement(event_item, 'iObjectId', value=str(event['iObjectId']))

        # Create pCutsceneEventArgsList
        event_args_list = ET.SubElement(root, 'pCutsceneEventArgsList')
        for args in cutscene_data['event_args']:
            args_item = ET.SubElement(event_args_list, 'Item')
            ET.SubElement(args_item, 'iObjectId', value=str(args['iObjectId']))
            if args['cName']:
                ET.SubElement(args_item, 'cName').text = args['cName']
            if args.get('fSubtitleDuration') is not None:
                ET.SubElement(args_item, 'fSubtitleDuration', value=str(args['fSubtitleDuration']))

        # Create pCutsceneObjects
        objects_list = ET.SubElement(root, 'pCutsceneObjects')
        for obj in cutscene_data['cutscene_objects']:
            object_item = ET.SubElement(objects_list, 'Item')
            ET.SubElement(object_item, 'iObjectId', value=str(obj['object_id']))
            if obj['name']:
                ET.SubElement(object_item, 'cName').text = obj['name']

        # Create pCutsceneLoadEventList
        load_event_list = ET.SubElement(root, 'pCutsceneLoadEventList')
        for load_event in cutscene_data['load_events']:
            load_event_item = ET.SubElement(load_event_list, 'Item')
            ET.SubElement(load_event_item, 'iEventId', value=str(load_event['event_id']))
            ET.SubElement(load_event_item, 'fTime', value=str(load_event['load_time']))

        # Create attributes
        attributes_list = ET.SubElement(root, 'attributes')
        for attribute in cutscene_data['attributes']:
            attribute_item = ET.SubElement(attributes_list, 'Item', type=attribute['type'])
            attribute_item.text = attribute['value']

        # Create additional attributes
        additional_attributes = cutscene_data['additional_attributes']
        attributes_element = ET.SubElement(root, 'attributes')
        ET.SubElement(attributes_element, 'User   Data1', value=str(additional_attributes['User    Data1']))
        ET.SubElement(attributes_element, 'User   Data2', value=str(additional_attributes['User    Data2']))
        ET.SubElement(root, 'iRangeStart', value=str(additional_attributes['iRangeStart']))
        ET.SubElement(root, 'iRangeEnd', value=str(additional_attributes['iRangeEnd']))
        ET.SubElement(root, 'iAltRangeEnd', value=str(additional_attributes['iAltRangeEnd']))
        ET.SubElement(root, 'fSectionByTimeSliceDuration', value=str(additional_attributes['fSectionByTimeSliceDuration']))
        ET.SubElement(root, 'fFadeOutCutsceneDuration', value=str(additional_attributes['fFadeOutCutsceneDuration']))
        ET.SubElement(root, 'fFadeInGameDuration', value=str(additional_attributes['fFadeInGameDuration']))
        ET.SubElement(root, 'fadeInColor', value=additional_attributes['fadeInColor'])
        ET.SubElement(root, 'iBlendOutCutsceneDuration', value=str(additional_attributes['iBlendOutCutsceneDuration']))
        ET.SubElement(root, 'iBlendOutCutsceneOffset', value=str(additional_attributes['iBlendOutCutsceneOffset']))
        ET.SubElement(root, 'fFadeOutGameDuration', value=str(additional_attributes['fFadeOutGameDuration']))
        ET.SubElement(root, 'fFadeInCutsceneDuration', value=str(additional_attributes['fFadeInCutsceneDuration']))
        ET.SubElement(root, 'fadeOutColor', value=additional_attributes['fadeOutColor'])
        ET.SubElement(root, 'DayCoCHours', value=str(additional_attributes['DayCoCHours']))

        # Create cameraCutList
        camera_cut_list = ET.SubElement(root, 'cameraCutList')
        for camera_cut in cutscene_data['camera_cut_list']:
            camera_cut_item = ET.SubElement(camera_cut_list, 'Item')
            ET.SubElement(camera_cut_item, 'cutId', value=str(camera_cut['cut_id']))
            ET.SubElement(camera_cut_item, 'cutTime', value=str(camera_cut['cut_time']))

        # Create sectionSplitList
        section_split_list = ET.SubElement(root, 'sectionSplitList')
        for section_split in cutscene_data['section_split_list']:
            section_split_item = ET.SubElement(section_split_list, 'Item')
            ET.SubElement(section_split_item, 'splitId', value=str(section_split['split_id']))
            ET.SubElement(section_split_item, 'splitTime', value=str(section_split['split_time']))

        # Create concatDataList
        concat_data_list = ET.SubElement(root, 'concatDataList')
        for concat_data in cutscene_data['concat_data_list']:
            concat_data_item = ET.SubElement(concat_data_list, 'Item', itemType=concat_data['item_type'])
            concat_data_item.text = concat_data['data']

        # Create discardFrameList
        discard_frame_list = ET.SubElement(root, 'discardFrameList')
        for discard_frame in cutscene_data['discard_frame_list']:
            discard_frame_item = ET.SubElement(discard_frame_list, 'Item', itemType=discard_frame['item_type'])
            ET.SubElement(discard_frame_item, 'frameNumber', value=str(discard_frame['frame_number']))

        # Write to XML file
        tree = ET.ElementTree(root)
        tree.write(self.filepath, encoding='utf-8', xml_declaration=True)