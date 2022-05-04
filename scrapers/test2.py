#!/usr/bin/env python3

import json
import re

regex1 = r"^--.*: form-data.*Content-Type: application\/json\\r\\n\\r\\n{"
regex2 = r"}\\r\\n--.*--\\r\\n"

test_str = ("--f763f87a54234577bd9e3542cafe522b\\r\\nContent-Disposition: form-data; name=\\\"Summary\\\"\\r\\nContent-Type: application/json\\r\\n\\r\\n{\\n    \\\"Device_serial\\\": \\\"CNN6KD564X\\\", \\n    \\\"Device_type\\\": \\\"IAP\\\", \\n    \\\"Group\\\": \\\"THD-13-IAP-20220222\\\", \\n    \\\"Configuration_error_status\\\": false, \\n    \\\"Override_status\\\": false, \\n    \\\"Template_name\\\": \\\"THD-13-IAP-20220222\\\", \\n    \\\"Template_hash\\\": \\\"9a641fff479b346d5c5bfb0696ba7eea\\\", \\n    \\\"Template_error_status\\\": false\\n}\\r\\n--f763f87a54234577bd9e3542cafe522b--\\r\\n\n\n")

subst = "{"

# You can manually specify the number of replacements by changing the 4th argument
result = re.sub(regex1, "{", test_str, 0, re.IGNORECASE)
result = re.sub(regex2, "}", result, 0, re.IGNORECASE)

if result:
    print (result)
    print(json.dumps(result))

