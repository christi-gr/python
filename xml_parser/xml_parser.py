import xml.etree.ElementTree as ET
import re, os, glob
import pandas as pd

def parse_file( parser_file ):
    print(parser_file)
    xml_p=open( parser_file,'r',  encoding="utf-8")
    text = xml_p.read()
    text = re.sub(r' xmlns="[^"]*"', '', text, count=1)
    tree = ET.fromstring( text )
    tags = ['PersonNm', 'TitleTxt', 'AverageHoursPerWeekRt', 'IndividualTrusteeOrDirectorInd', 'ReportableCompFromOrgAmt', 'ReportableCompFromRltdOrgAmt', 'OtherCompensationAmt']
    cols = ['PersonNm', 'TitleTxt', 'AverageHoursPerWeekRt', 'IndividualTrusteeOrDirectorInd', 'ReportableCompFromOrgAmt', 'ReportableCompFromRltdOrgAmt', 'OtherCompensationAmt']

    rows = []

    for item in tree.findall('.//ReturnData/IRS990/Form990PartVIISectionAGrp'):
        data = {}
        for tag in tags:
            data[ tag ] = ''
            try:
                data[ tag ] = item.find(tag).text
            except:
                pass
        rows.append( data )
    if ( len( rows ) ):
        df = pd.DataFrame(rows, columns=cols)
        output_file = os.path.basename( os.path.dirname(parser_file) ) + '_' + os.path.basename(parser_file).split('.')[0]
        df.to_csv( './CSV/' + output_file + '.csv')


files = glob.glob('**/*.xml', recursive=True)
for f in files:
    parse_file( f )
