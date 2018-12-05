def main_templates():
    '''Dict definition for all current templates.
    '''
    templates_list = [ \
        {'sheet_name': 'Artifact', 'title': 'Artifact', 'file_name': 'Artifact.xml', 'columns': 5}, \
        {'sheet_name': 'Helper', 'title': 'RO Helper', 'file_name': 'Zstructures.xml', 'columns': 3}, \
        {'sheet_name': 'Control', 'title': 'Control', 'file_name': 'Control Template.xml', 'columns': 3}, \
        {'sheet_name': 'GTV', 'title': 'GTV', 'file_name': 'GTV Template.xml', 'columns': 3}, \
        {'sheet_name': 'GTV 1-5', 'title': 'GTV 1-5', 'file_name': 'GTV 1-5 Template.xml', 'columns': 3}, \
        {'sheet_name': 'CTV', 'title': 'CTV', 'file_name': 'CTV Template.xml', 'columns': 3}, \
        {'sheet_name': 'PTV', 'title': 'PTV', 'file_name': 'PTV Template.xml', 'columns': 3}, \
        {'sheet_name': 'PTV 1-5', 'title': 'PTV 1-5', 'file_name': 'PTV 1-5 Template.xml', 'columns': 3}, \
        {'sheet_name': 'CT', 'title': 'CT', 'file_name': 'CT Template.xml', 'columns': 3}, \
        {'sheet_name': 'Basic', 'title': 'Basic', 'file_name': 'Basic Template.xml', 'columns': 3}, \
        {'sheet_name': 'Palliative', 'title': 'Palliative', 'file_name': 'Palliative Template.xml', 'columns': 3}, \
        {'sheet_name': 'Palliative Brain', 'title': 'Palliative Brain', 'file_name': 'Palliative Brain Template.xml', 'columns': 3}, \
        {'sheet_name': 'PET', 'title': 'PET', 'file_name': 'Pet Template.xml', 'columns': 3}, \
        {'sheet_name': 'Pelvis Anatomy General', 'title': 'Pelvis Anatomy General', 'file_name': 'Pelvis Template.xml', 'columns': 3}, \
        {'sheet_name': 'Pelvis Anatomy Male', 'title': 'Pelvis Anatomy Male', 'file_name': 'Pelvis Male Template.xml', 'columns': 3}, \
        {'sheet_name': 'Pelvis Anatomy Female', 'title': 'Pelvis Anatomy Female', 'file_name': 'Pelvis Female Template.xml', 'columns': 3}, \
        {'sheet_name': 'Pelvis Nodes', 'title': 'Pelvis Nodes', 'file_name': 'Pelvis Nodes Template.xml', 'columns': 3}, \
        {'sheet_name': 'VMAT ANUS', 'title': 'VMAT ANUS', 'file_name': 'VMAT ANUS Template.xml', 'columns': 5}, \
        {'sheet_name': 'Rectum', 'title': 'Rectum', 'file_name': 'Rectum Template.xml', 'columns': 5}, \
        {'sheet_name': 'Bladder Single Phase', 'title': 'Bladder Single Phase', 'file_name': 'Bladder 1Ph Template.xml', 'columns': 5}, \
        {'sheet_name': 'Bladder Two Phase', 'title': 'Bladder Two Phase', 'file_name': 'Bladder 2Ph Template.xml', 'columns': 5}, \
        {'sheet_name': 'Gyne', 'title': 'Gyne', 'file_name': 'Gyne Template.xml', 'columns': 5}, \
        {'sheet_name': 'Prostate', 'title': 'Prostate', 'file_name': 'Prostate Template.xml', 'columns': 5}, \
        {'sheet_name': 'Abdomen Anatomy', 'title': 'Abdomen Anatomy', 'file_name': 'Abdomen.xml', 'columns': 3}, \
        {'sheet_name': 'Abdomen Nodes', 'title': 'Abdomen Nodes', 'file_name': 'Abdomen Nodes.xml', 'columns': 3}, \
        {'sheet_name': 'Esophagus', 'title': 'Esophagus', 'file_name': 'Esophagus Template.xml', 'columns': 5}, \
        {'sheet_name': 'Chest Anatomy', 'title': 'Chest Anatomy', 'file_name': 'Chest.xml', 'columns': 3}, \
        {'sheet_name': 'Lung VMAT', 'title': 'Lung VMAT', 'file_name': 'Lung VMAT.xml', 'columns': 5}, \
        {'sheet_name': 'Lung SBRT', 'title': 'Lung (SBRT)', 'file_name': 'Lung SBRT.xml', 'columns': 5}, \
        {'sheet_name': 'SBRT Control', 'title': 'SBRT Control', 'file_name': 'SBRT Control.xml', 'columns': 3}, \
        {'sheet_name': '4D GTV', 'title': '4D GTV', 'file_name': '4D GTV Template.xml', 'columns': 3}, \
        {'sheet_name': 'Breast', 'title': 'Breast', 'file_name': 'Breast Template.xml', 'columns': 5}, \
        {'sheet_name': 'H&N Anatomy', 'title': 'H&N Anatomy', 'file_name': 'H and N Anatomy.xml', 'columns': 3}, \
        {'sheet_name': 'H&N Lymph Nodes', 'title': 'H&N Lymph Nodes', 'file_name': 'H and N Lymph Nodes.xml', 'columns': 3}, \
        {'sheet_name': 'H&N 70 in 35', 'title': r'H&N 70/35', 'file_name': 'H and N 70 in 35.xml', 'columns': 5}, \
        {'sheet_name': 'H&N 66 in 33', 'title': r'H&N 66/33', 'file_name': 'H and N 66 in 33.xml', 'columns': 5}, \
        {'sheet_name': 'H&N 60 in 30', 'title': r'H&N 60/30', 'file_name': 'H and N 60 in 30.xml', 'columns': 5}, \
        {'sheet_name': 'Brain Anatomy', 'title': 'Brain Anatomy', 'file_name': 'Brain Anatomy.xml', 'columns': 3}, \
        {'sheet_name': 'CNS', 'title': 'CNS', 'file_name': 'CNS Template.xml', 'columns': 5}, \
        {'sheet_name': 'FSRT', 'title': 'FSRT', 'file_name': 'FSRT Template.xml', 'columns': 5}]
    return templates_list

def trial_templates():
    '''Dict definition for all clinical trial templates.
    '''
    template_list = [ \
        {'sheet_name': 'CC003_PCI Brain', 'title': 'CC003_PCI Brain', 'file_name': 'CC003_PCI Brain Template.xml', 'columns': 5}, \
        {'sheet_name': 'GA1_TOPGEAR_TROG', 'title': 'GA1_TOPGEAR_TROG', 'file_name': 'GA1_TOPGEAR_TROG Template.xml', 'columns': 5}, \
        {'sheet_name': 'GU001 BLADDER', 'title': 'GU001 BLADDER', 'file_name': 'GU001 BLADDER Template.xml', 'columns': 5}, \
        {'sheet_name': 'HDR BREAST', 'title': 'HDR BREAST', 'file_name': 'HDR BREAST Template.xml', 'columns': 5}, \
        {'sheet_name': 'HDR CERVIX', 'title': 'HDR CERVIX', 'file_name': 'HDR CERVIX Template.xml', 'columns': 5}, \
        {'sheet_name': 'HN002_H+N', 'title': 'HN002_H+N', 'file_name': 'HN002_H and N Template.xml', 'columns': 5}, \
        {'sheet_name': 'LIVR_HE1 Protocol', 'title': 'LIVR_HE1 Protocol', 'file_name': 'LIVR_HE1 Protocol Template.xml', 'columns': 5}, \
        {'sheet_name': 'LUNG - LUSTRE', 'title': 'LUNG - LUSTRE', 'file_name': 'LUNG - LUSTRE Template.xml', 'columns': 5}]
    return template_list


