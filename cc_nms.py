#-*- coding:utf-8 -*-
from bs4 import BeautifulSoup as bs

#导入模板文件
south_path=r'C:\Users\cchen\Desktop\migration_PtMP_service.xml'
#生成的python模板文件
output_path=r'C:\Users\cchen\Desktop\new_out_put_service.py'
file=open(south_path,'r+')
outfile=open(output_path,'w+')

#.format()所用到的字符串
format_s=''
#for循环中用到的字符串
for_s=''

#读取文件，获取头尾以及要迭代的文档
#目前默认头为前三行，尾为最后一行
str1=file.readlines()
head=''.join(str1[:3])
tail=str1[-1]
article=''.join(str1[3:-1])

#Python文件的头
outfile.write("# -*- coding: utf-8 -*-'\n")
outfile.write(r"file_object = open(r'C:\Users\cchen\Desktop\wy_test_MPtMP_service_wy.xml', 'w+')"+'\n')
outfile.write('file_object.write('+"'''"+head+"'''"+')'+'\n')
outfile.write('for Repeat_Time in xrange(1,2):\n')

#处理XML文件
soup=bs(article,'xml')

#ID值，默认都有，而且唯一，利用create 关键字判断。
soup.find_all(OPERATION="CREATE")[0]['ID']="{ID}"
format_s+='ID=ID'
for_s+='    ID=ID+Repeat_Time\n'

#NAME属性，默认都有，且唯一，利用<NAME>进行查找
soup.find_all('NAME')[0].string.replace_with('{NAME}')
format_s+=',NAME=NAME'
for_s+='    NAME=NAME+Repeat_Time\n'

#VPN ID 属性，不一定有，有则认为唯一
vpn_id_flag=False
if soup.find_all('VPN_ID'):
    soup.find_all('VPN_ID')[0].string.replace_with('{VPN_ID}')
    vpn_id_flag=True
    format_s+=',VPN_ID=VPN_ID'
    for_s+='    VPN_ID=VPN_ID+Repeat_Time\n'
    
#C_VLAN 属性，不一定有，有也不一定唯一，进行二重判断。
c_vlan_id_flag=False
if soup.find_all('C_VLAN_ID'):
    c_vlan_id_times=len(set(soup.find_all('C_VLAN_ID')))
    c_vlan_id_flag=True
    d1=dict()
    num=1
    for i in soup.find_all('C_VLAN_ID'):
        if i.string in d1:
            i.string.replace_with(d1[i.string])
        else:
            d1[i.string]='{C_VlAN_ID_'+str(num)+'}'
            i.string.replace_with(d1[i.string])
            format_s+=',C_VlAN_ID_'+str(num)+'='+'C_VlAN_ID_'+str(num)
            for_s+='    C_VlAN_ID_'+str(num)+'=C_VlAN_ID_'+str(num)+'+'+str(c_vlan_id_times)+'*Repeat_Time\n'
            num+=1
			
#VLAN_IDS 属性，不一定有，有也不一定唯一，进行二重判断。
VLAN_IDS_flag=False
if soup.find_all('VLAN_IDS'):
    VLAN_IDS_times=len(set(soup.find_all('VLAN_IDS')))
    VLAN_IDS_flag=True
    d1=dict()
    num=1
    for i in soup.find_all('VLAN_IDS'):
        if i.string in d1:
            i.string.replace_with(d1[i.string])
        else:
            d1[i.string]='{VLAN_IDS_'+str(num)+'}'
            i.string.replace_with(d1[i.string])
            format_s+=',VLAN_IDS_'+str(num)+'='+'VLAN_IDS_'+str(num)
            for_s+='    VLAN_IDS_'+str(num)+'=VLAN_IDS_'+str(num)+'+'+str(VLAN_IDS_times)+'*Repeat_Time\n'
            num+=1
            
#Tunnel NAME 属性处理，不一定有，有也不一定唯一，采用多重判断
tunnel_name_flag=False
if soup.find_all('TUNNEL_NAME'):
    tunnel_name_times=len(set(soup.find_all('TUNNEL_NAME')))
    tunnel_name_flag=True
    d1=dict()
    num=1
    for i in soup.find_all('TUNNEL_NAME'):
        if i.string in d1:
            i.string.replace_with(d1[i.string])
        else:
            d1[i.string]='{TUNNEL_NAME_'+str(num)+'}'
            i.string.replace_with(d1[i.string])
            format_s+=',TUNNEL_NAME_'+str(num)+'='+'TUNNEL_NAME_'+str(num)
            for_s+="    TUNNEL_NAME_"+str(num)+"='TUNNEL_NAME_'"+'+str('+str(num)+'+'+str(tunnel_name_times)+'*Repeat_Time)\n'
            num+=1

#VC_LABEL 属性处理，不一定有，有也不一定唯一，采用多重判断
vc_lable_flag=False
if soup.find_all('VC_LABEL'):
    vc_lable_times=len(set(soup.find_all('VC_LABEL')))
    vc_lable_flag=True
    d1=dict()
    num=1
    for i in soup.find_all('VC_LABEL'):
        if i.string in d1:
            i.string.replace_with(d1[i.string])
        else:
            d1[i.string]='{VC_LABEL_'+str(num)+'}'
            i.string.replace_with(d1[i.string])
            format_s+=',VC_LABEL_'+str(num)+'='+'VC_LABEL_'+str(num)
            for_s+='    VC_LABEL_'+str(num)+'=VC_LABEL_'+str(num)+'+'+str(vc_lable_times)+'*Repeat_Time\n'
            num+=1
            
#PE_TUNNEL_NAME属性，不一定有，有则唯一
pe_tunnel_name_flag=False
if soup.find_all('PE_TUNNEL_NAME'):
    soup.find_all('PE_TUNNEL_NAME')[0].string.replace_with('{PE_TUNNEL_NAME}')
    pe_tunnel_name_flag=True
    format_s+=',PE_TUNNEL_NAME=PE_TUNNEL_NAME'
    for_s+='    PE_TUNNEL_NAME=PE_TUNNEL_NAME+Repeat_Time\n'
    
    
#写入python文件中的循环    
outfile.write(for_s)
outfile.write('    file_object.write(')
outfile.write("'''")
outfile.write(str(soup).strip('<?xml version="1.0" encoding="utf-8"?>'))
outfile.write('>')
outfile.write("'''")
outfile.write('.format('+format_s+'))'+'\n')

#写入python文件中的末尾
outfile.write('file_object.write("\\n</XML_TRAFFIC>")\n')
outfile.write('file_object.close()')
file.close() 
outfile.close()