import json

dict = {'device_type': 'CX', 'group': 'THD-01-IDF-20211208', 'model': 'ALL', 'name': 'THD-01-IDF-20211208', 'template_hash': '2bc16a9c82ba612dc7c6a16bfe8e3e24', 'version': 'ALL'}

dict2 = {'default': 'none', 'Staging-test-6-stack-3only': [{'device_type': 'CX', 'group': 'Staging-test-6-stack-3only', 'model': 'ALL', 'name': 'Staging-test-6-stack-3only', 'template_hash': '6a71338093411b98c20f32b6a1eb3fe7', 'version': 'ALL'}], 'STRATIX': 'none', 'THD-01-IAP-20220222': [{'device_type': 'IAP', 'group': 'THD-01-IAP-20220222', 'model': 'ALL', 'name': 'THD-01-IAP-20220222', 'template_hash': '9a641fff479b346d5c5bfb0696ba7eea', 'version': 'ALL'}], 'THD-01-IDF-20211208': [{'device_type': 'CX', 'group': 'THD-01-IDF-20211208', 'model': 'ALL', 'name': 'THD-01-IDF-20211208', 'template_hash': '2bc16a9c82ba612dc7c6a16bfe8e3e24', 'version': 'ALL'}]} 


for i in dict2:
  print(i)
  if (dict2[i] != 'none'):
    print(dict2[i][0]['template_hash'])
    print(dict2[i][0]['device_type'])
